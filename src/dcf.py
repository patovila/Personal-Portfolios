"""DCF y valuación: descuento de flujos de caja para valor intrínseco."""
import yfinance as yf
import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600)
def get_datos_base_dcf(ticker):
    """Obtiene datos base para el DCF desde yfinance. Cache 1 hora.

    FCF: del cashflow statement (más confiable que info['freeCashflow']).
    Deuda/cash: del balance sheet.
    Retorna dict o None si falla por completo.
    """
    try:
        t = yf.Ticker(ticker)
        info = t.info

        # FCF desde cashflow statement
        fcf_base = None
        fcf_anio = None
        fcf_serie = {}
        try:
            cf = t.cashflow
            if not cf.empty and "Free Cash Flow" in cf.index:
                serie = cf.loc["Free Cash Flow"].dropna()
                if not serie.empty:
                    fcf_serie = {col.year: float(val) for col, val in serie.items()}
                    fcf_base = float(serie.iloc[0])
                    fcf_anio = serie.index[0].year
        except Exception:
            pass

        # Deuda y cash del balance sheet
        deuda = None
        cash = None
        try:
            bs = t.balance_sheet
            if not bs.empty:
                if "Total Debt" in bs.index:
                    deuda = float(bs.loc["Total Debt"].iloc[0])
                if "Cash And Cash Equivalents" in bs.index:
                    cash = float(bs.loc["Cash And Cash Equivalents"].iloc[0])
        except Exception:
            pass

        # Fallback a info si el balance sheet falla
        if deuda is None:
            deuda = info.get("totalDebt")
        if cash is None:
            cash = info.get("totalCash")

        return {
            "fcf_base": fcf_base,
            "fcf_anio": fcf_anio,
            "fcf_serie": fcf_serie,       # {año: valor} para mostrar historial
            "fcf_negativo": fcf_base is not None and fcf_base <= 0,
            "shares": info.get("sharesOutstanding"),
            "precio_actual": info.get("currentPrice") or info.get("regularMarketPrice"),
            "beta": info.get("beta"),
            "deuda": deuda,
            "cash": cash,
            "currency": info.get("currency", "USD"),
            "nombre": info.get("longName", ticker),
        }
    except Exception:
        return None


def calcular_dcf(fcf_base, g1, g2, wacc, tg, años, shares, deuda, cash):
    """Descuento de flujos en dos fases de crecimiento.

    Args:
        fcf_base: FCF del año 0 (en USD, valor absoluto)
        g1: tasa de crecimiento años 1-5 (fracción, ej 0.15)
        g2: tasa de crecimiento años 6-10 (fracción) — ignorado si años=5
        wacc: tasa de descuento (fracción)
        tg: tasa terminal/perpetuidad (fracción)
        años: 5 o 10
        shares: acciones outstanding
        deuda: deuda total (USD)
        cash: caja (USD)

    Returns dict con valor_intrinseco (USD/acción), flujos y métricas intermedias.
    Raises ValueError si wacc <= tg.
    """
    if wacc <= tg:
        raise ValueError(f"WACC ({wacc:.2%}) debe ser mayor que la tasa terminal ({tg:.2%})")

    flujos = []
    fcf = fcf_base
    for año in range(1, años + 1):
        g = g1 if año <= 5 else g2
        fcf = fcf * (1 + g)
        vp = fcf / (1 + wacc) ** año
        flujos.append({"año": año, "fcf_proyectado": fcf, "valor_presente": vp})

    # Valor terminal Gordon Growth
    fcf_terminal = flujos[-1]["fcf_proyectado"] * (1 + tg)
    valor_terminal_bruto = fcf_terminal / (wacc - tg)
    vp_terminal = valor_terminal_bruto / (1 + wacc) ** años

    suma_vp = sum(f["valor_presente"] for f in flujos)
    valor_empresa = suma_vp + vp_terminal
    deuda_neta = (deuda or 0) - (cash or 0)
    valor_equity = valor_empresa - deuda_neta
    valor_intrinseco = valor_equity / shares if shares else None

    return {
        "valor_intrinseco": valor_intrinseco,
        "valor_empresa": valor_empresa,
        "valor_terminal": valor_terminal_bruto,
        "vp_terminal": vp_terminal,
        "suma_vp_flujos": suma_vp,
        "deuda_neta": deuda_neta,
        "flujos": flujos,
    }


def tabla_sensibilidad(fcf_base, g1_base, g2, wacc_base, tg, años, shares, deuda, cash):
    """Matriz 5×5: filas = WACC ± 2 pp, columnas = g1 ± 2 pp.

    Retorna DataFrame con valor intrínseco (USD/acción) en cada celda.
    Celdas donde WACC ≤ tg quedan en None.
    """
    waccs = [round(wacc_base + d / 100, 4) for d in range(-2, 3)]
    gs    = [round(g1_base   + d / 100, 4) for d in range(-2, 3)]

    data = {}
    for g in gs:
        label = f"{g*100:.0f}%"
        data[label] = []
        for w in waccs:
            if w <= tg or g < 0:
                data[label].append(None)
            else:
                try:
                    res = calcular_dcf(fcf_base, g, g2, w, tg, años, shares, deuda, cash)
                    data[label].append(res["valor_intrinseco"])
                except Exception:
                    data[label].append(None)

    df = pd.DataFrame(data, index=[f"{w*100:.0f}%" for w in waccs])
    df.index.name = "WACC"
    return df


def calcular_escenarios(fcf_base, g1, g2, wacc, tg, años, shares, deuda, cash):
    """DCF para 3 escenarios. Retorna dict con claves 'bull', 'base', 'bear'."""
    _tg_safe = tg + 0.001  # mínimo margen wacc > tg

    configs = {
        "bull": (g1 * 1.5, g2 * 1.5, max(wacc - 0.01, _tg_safe)),
        "base": (g1,       g2,        wacc),
        "bear": (g1 * 0.5, g2 * 0.5, wacc + 0.02),
    }

    resultados = {}
    for nombre, (eg1, eg2, ew) in configs.items():
        try:
            res = calcular_dcf(fcf_base, eg1, eg2, ew, tg, años, shares, deuda, cash)
        except Exception as e:
            res = {"valor_intrinseco": None, "error": str(e)}
        res["g1_usado"] = eg1
        res["wacc_usado"] = ew
        resultados[nombre] = res

    return resultados
