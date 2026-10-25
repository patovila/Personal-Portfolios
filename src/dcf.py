"""DCF y valuación: descuento de flujos de caja para valor intrínseco."""
import pandas as pd
import streamlit as st

from src.datos import get_ticker_adr, get_ticker_local, is_ticker_argentino
from src.data_layer import get_info, get_fundamentals, get_precios


# ─────────────────────────────────────────────────────────────────────────────
# WACC automático (CAPM)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def calcular_wacc_automatico(ticker: str, erp: float = 0.045) -> dict:
    """Calcula WACC usando CAPM. Cache 1 hora.

    WACC = (E/V) × Re + (D/V) × Rd × (1 − T)
      Re = Rf + beta × ERP   (CAPM)
      Rf = yield del bono del Tesoro a 10 años (^TNX)
      ERP = prima de riesgo de mercado (editable, default 4.5%)
      Rd = gasto_intereses / deuda_total
      T  = tasa impositiva efectiva
      E  = market cap  |  D = deuda total  |  V = E + D

    Retorna dict con todos los componentes y lista de advertencias
    para los datos que no se pudieron obtener.
    """
    advertencias = []
    resultado = {
        "wacc": None,
        "rf": None,
        "beta": None,
        "erp": erp,
        "re": None,
        "rd": None,
        "tax_rate": None,
        "e_weight": None,
        "d_weight": None,
        "mkt_cap": None,
        "total_debt": None,
        "advertencias": advertencias,
    }

    try:
        tk_fund = get_ticker_adr(ticker)
        info = get_info(tk_fund)
        fund = get_fundamentals(tk_fund)

        # ── Tasa libre de riesgo: yield ^TNX (10Y Treasury) ──────────────────
        rf = None
        try:
            df_tnx = get_precios(("^TNX",), "5d")
            df_tnx = df_tnx.get("^TNX")
            if df_tnx is not None and not df_tnx.empty and "Close" in df_tnx.columns:
                rf_raw = float(df_tnx["Close"].dropna().iloc[-1])
                rf = rf_raw / 100  # ^TNX cotiza en %, convertir a fracción
        except Exception:
            pass
        if rf is None:
            rf = 0.045  # fallback razonable si yfinance no responde
            advertencias.append("Tasa libre de riesgo (^TNX) no disponible — usando 4.5% como fallback.")
        resultado["rf"] = rf

        # ── Beta ─────────────────────────────────────────────────────────────
        beta = info.get("beta")
        if beta is None or beta <= 0:
            beta = 1.0
            advertencias.append("Beta no disponible — usando 1.0 (mercado promedio).")
        resultado["beta"] = beta

        # ── Costo de equity (CAPM) ────────────────────────────────────────────
        re = rf + beta * erp
        resultado["re"] = re

        # ── Market cap ───────────────────────────────────────────────────────
        mkt_cap = info.get("marketCap")
        if not mkt_cap:
            px = info.get("currentPrice") or info.get("regularMarketPrice")
            shares = info.get("sharesOutstanding")
            if px and shares:
                mkt_cap = px * shares
        if not mkt_cap:
            advertencias.append("Market cap no disponible — no se puede calcular pesos E/D.")
            return resultado
        resultado["mkt_cap"] = mkt_cap

        # ── Deuda total ───────────────────────────────────────────────────────
        total_debt = None
        try:
            bs = fund.get("balance", pd.DataFrame())
            if not bs.empty and "Total Debt" in bs.index:
                total_debt = float(bs.loc["Total Debt"].iloc[0])
        except Exception:
            pass
        if total_debt is None:
            total_debt = info.get("totalDebt") or 0
        resultado["total_debt"] = total_debt

        # ── Costo de deuda ────────────────────────────────────────────────────
        rd = None
        try:
            inc = fund.get("income", pd.DataFrame())
            if not inc.empty and "Interest Expense" in inc.index:
                interest = abs(float(inc.loc["Interest Expense"].iloc[0]))
                if total_debt and total_debt > 0:
                    rd = interest / total_debt
        except Exception:
            pass
        if rd is None or rd <= 0 or rd > 0.25:
            rd = 0.05  # fallback: 5% costo de deuda
            advertencias.append("Gasto de intereses no disponible — usando Rd = 5.0%.")
        resultado["rd"] = rd

        # ── Tasa impositiva efectiva ──────────────────────────────────────────
        tax_rate = None
        try:
            inc = fund.get("income", pd.DataFrame())
            if not inc.empty:
                ebt_row = next(
                    (r for r in ["Pretax Income", "Income Before Tax"] if r in inc.index),
                    None,
                )
                tax_row = next(
                    (r for r in ["Tax Provision", "Income Tax Expense"] if r in inc.index),
                    None,
                )
                if ebt_row and tax_row:
                    ebt = float(inc.loc[ebt_row].iloc[0])
                    tax = abs(float(inc.loc[tax_row].iloc[0]))
                    if ebt and ebt > 0:
                        tax_rate = min(tax / ebt, 0.40)  # cap a 40%
        except Exception:
            pass
        if tax_rate is None or tax_rate <= 0:
            tax_rate = 0.25
            advertencias.append("Tasa impositiva no disponible — usando T = 25%.")
        resultado["tax_rate"] = tax_rate

        # ── Pesos E y D ───────────────────────────────────────────────────────
        v = mkt_cap + (total_debt or 0)
        e_weight = mkt_cap / v
        d_weight = (total_debt or 0) / v
        resultado["e_weight"] = e_weight
        resultado["d_weight"] = d_weight

        # ── WACC final ────────────────────────────────────────────────────────
        wacc = e_weight * re + d_weight * rd * (1 - tax_rate)
        resultado["wacc"] = round(wacc, 4)

    except Exception as exc:
        advertencias.append(f"Error inesperado calculando WACC: {exc}")

    return resultado


@st.cache_data(ttl=3600)
def get_datos_base_dcf(ticker):
    """Obtiene datos base para el DCF desde yfinance. Cache 1 hora.

    Para tickers argentinos:
    - FCF, deuda, cash, shares → ADR en NYSE (USD)
    - Precio actual → .BA (ARS) con fallback al ADR (USD)
    Retorna dict o None si falla por completo.
    """
    try:
        es_ar   = is_ticker_argentino(ticker)
        tk_fund = get_ticker_adr(ticker)     # ADR para fundamentals
        tk_px   = get_ticker_local(ticker)   # .BA para precio local

        info = get_info(tk_fund)
        fund = get_fundamentals(tk_fund)

        # FCF desde cashflow statement
        fcf_base = None
        fcf_anio = None
        fcf_serie = {}
        try:
            cf = fund["cashflow"]
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
            bs = fund["balance"]
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

        # Precio: .BA en ARS (si existe) o ADR en USD
        precio_actual  = None
        precio_moneda  = None
        if es_ar:
            try:
                df_local = get_precios([tk_px], "2d").get(tk_px)
                if df_local is not None and not df_local.empty and "Close" in df_local.columns:
                    precio_actual = float(df_local["Close"].dropna().iloc[-1])
                    precio_moneda = "ARS"
            except Exception:
                pass
        if precio_actual is None:
            precio_actual = info.get("currentPrice") or info.get("regularMarketPrice")
            precio_moneda = info.get("currency", "USD")

        return {
            "fcf_base":     fcf_base,
            "fcf_anio":     fcf_anio,
            "fcf_serie":    fcf_serie,
            "fcf_negativo": fcf_base is not None and fcf_base <= 0,
            "shares":       info.get("sharesOutstanding"),
            "precio_actual":  precio_actual,
            "precio_moneda":  precio_moneda,
            "es_argentino":   es_ar,
            "ticker_adr":     tk_fund,
            "beta":   info.get("beta"),
            "deuda":  deuda,
            "cash":   cash,
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


def tabla_sensibilidad(fcf_base, g1, g2, wacc_base, tg_base, años, shares, deuda, cash):
    """Matriz 5×5: filas = WACC ± 2 pp, columnas = tasa terminal (tg) ± 2 pp.

    Retorna DataFrame con valor intrínseco (USD/acción) en cada celda.
    Celdas donde WACC ≤ tg quedan en None.
    """
    waccs = [round(wacc_base + d / 100, 4) for d in range(-2, 3)]
    tgs   = [round(tg_base   + d / 100, 4) for d in range(-2, 3)]

    data = {}
    for tg in tgs:
        label = f"{tg*100:.0f}%"
        data[label] = []
        for w in waccs:
            if w <= tg or tg < 0:
                data[label].append(None)
            else:
                try:
                    res = calcular_dcf(fcf_base, g1, g2, w, tg, años, shares, deuda, cash)
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
