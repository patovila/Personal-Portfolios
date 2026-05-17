"""Portfolio tracker: carga, valuacion, metricas y comparacion vs benchmark.

Convenciones de tipos de activo (campo posicion["tipo"]):
- LOCAL .BA  : cotiza en BYMA en ARS (ej TGNO4.BA). yfinance devuelve ARS.
- LOCAL ADR  : cotiza en NYSE en USD pero el campo precio_actual_ars
               del JSON esta convertido (ej YPF, PAM, TGS). Multiplicamos
               el precio USD por tipo de cambio.
- CEDEAR     : precio_cedear_ars = precio_subyacente_usd * tc / ratio_cedear
- ETF        : se trata igual que CEDEAR si tiene ratio.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import yfinance as yf


# ---------- carga ----------

@st.cache_data(ttl=3600, show_spinner=False)
def cargar_portfolio(user_id: str = "pato") -> dict:
    """Carga el portfolio desde data/portfolio/{user_id}.json."""
    ruta = Path("data/portfolio") / f"{user_id}.json"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro {ruta}")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- valuacion ----------

def _precio_actual_ars(posicion: dict, tipo_cambio: float) -> float | None:
    """Calcula precio actual en ARS usando yfinance. None si no se pudo."""
    ticker = posicion.get("ticker")
    tipo = posicion.get("tipo", "").upper()
    ratio = posicion.get("ratio_cedear")

    if not ticker:
        return None

    try:
        hist = yf.Ticker(ticker).history(period="5d")
        if hist.empty:
            return None
        precio = float(hist["Close"].iloc[-1])
    except Exception:
        return None

    if tipo == "LOCAL":
        if ticker.upper().endswith(".BA"):
            return precio
        # ADR en NYSE: solo convertir si el JSON confirma precio USD.
        # Si precio_actual_usd es null (PAMPA, TGN, TGS local), el precio
        # yfinance del ADR no es comparable con precio_promedio_compra_ars
        # que viene de BYMA → devolver None para usar el fallback del JSON.
        if posicion.get("precio_actual_usd") is None:
            return None
        return precio * tipo_cambio

    if tipo in ("CEDEAR", "ETF"):
        if ratio and ratio > 0:
            return precio * tipo_cambio / ratio
        # ETF sin ratio: lo tratamos como ADR USD.
        return precio * tipo_cambio

    return precio * tipo_cambio


@st.cache_data(ttl=600, show_spinner=False)
def actualizar_precios_actuales(portfolio: dict) -> dict:
    """Devuelve una copia del portfolio con precio_actual_ars refrescado.

    Si yfinance falla para un ticker, mantiene el precio del JSON como
    fallback. Nunca lanza excepcion por un ticker individual.
    """
    tc = portfolio.get("configuracion", {}).get("tipo_cambio_ars_usd", 1)
    nuevo = json.loads(json.dumps(portfolio))  # deep copy serializable

    for pos in nuevo.get("posiciones", []):
        nuevo_precio = _precio_actual_ars(pos, tc)
        if nuevo_precio is not None:
            pos["precio_actual_ars"] = nuevo_precio
    return nuevo


# ---------- metricas por posicion ----------

def calcular_metricas_posicion(posicion: dict, tipo_cambio: float) -> dict:
    """Calcula costo, valor actual y P&L para una posicion."""
    cant = posicion.get("cantidad", 0) or 0
    precio_compra = posicion.get("precio_promedio_compra_ars", 0) or 0
    precio_actual = posicion.get("precio_actual_ars", 0) or 0

    costo_total_ars = cant * precio_compra
    valor_actual_ars = cant * precio_actual
    pnl_ars = valor_actual_ars - costo_total_ars
    pnl_pct = (pnl_ars / costo_total_ars) if costo_total_ars else 0.0
    costo_total_usd = (costo_total_ars / tipo_cambio) if tipo_cambio else 0.0
    valor_actual_usd = (valor_actual_ars / tipo_cambio) if tipo_cambio else 0.0
    pnl_usd = valor_actual_usd - costo_total_usd

    return {
        "costo_total_ars": costo_total_ars,
        "valor_actual_ars": valor_actual_ars,
        "pnl_ars": pnl_ars,
        "pnl_pct": pnl_pct,
        "costo_total_usd": costo_total_usd,
        "valor_actual_usd": valor_actual_usd,
        "pnl_usd": pnl_usd,
    }


# ---------- metricas del portfolio ----------

def calcular_metricas_portfolio(portfolio: dict) -> dict:
    """Agrega metricas globales del portfolio."""
    tc = portfolio.get("configuracion", {}).get("tipo_cambio_ars_usd", 1)
    posiciones = portfolio.get("posiciones", [])

    valor_total_ars = 0.0
    costo_total_ars = 0.0
    suma_beta_ponderada = 0.0
    detalle: list[dict[str, Any]] = []

    for pos in posiciones:
        m = calcular_metricas_posicion(pos, tc)
        valor_total_ars += m["valor_actual_ars"]
        costo_total_ars += m["costo_total_ars"]
        detalle.append({
            "ticker": pos.get("ticker"),
            "activo": pos.get("activo"),
            "valor_ars": m["valor_actual_ars"],
            "pnl_pct": m["pnl_pct"],
            "beta": pos.get("beta") or 0,
        })

    # Beta ponderada por peso
    if valor_total_ars > 0:
        for d in detalle:
            peso = d["valor_ars"] / valor_total_ars
            suma_beta_ponderada += peso * d["beta"]

    pnl_total_ars = valor_total_ars - costo_total_ars
    pnl_total_pct = (pnl_total_ars / costo_total_ars) if costo_total_ars else 0.0

    top = max(detalle, key=lambda x: x["pnl_pct"], default=None)
    worst = min(detalle, key=lambda x: x["pnl_pct"], default=None)
    mayor = max(detalle, key=lambda x: x["valor_ars"], default=None)

    return {
        "valor_total_ars": valor_total_ars,
        "valor_total_usd": valor_total_ars / tc if tc else 0.0,
        "costo_total_ars": costo_total_ars,
        "pnl_total_ars": pnl_total_ars,
        "pnl_total_pct": pnl_total_pct,
        "num_posiciones": len(posiciones),
        "beta_ponderada": suma_beta_ponderada,
        "top_performer": top,
        "worst_performer": worst,
        "mayor_posicion": mayor,
    }


# ---------- composicion ----------

def _composicion_por_campo(portfolio: dict, campo: str) -> dict:
    """Agrupa valor por un campo de la posicion."""
    tc = portfolio.get("configuracion", {}).get("tipo_cambio_ars_usd", 1)
    agrupado: dict[str, float] = {}
    for pos in portfolio.get("posiciones", []):
        m = calcular_metricas_posicion(pos, tc)
        clave = pos.get(campo) or "Sin clasificar"
        agrupado[clave] = agrupado.get(clave, 0.0) + m["valor_actual_ars"]

    total = sum(agrupado.values())
    return {
        k: {
            "valor_ars": v,
            "peso_pct": (v / total * 100) if total else 0.0,
        }
        for k, v in agrupado.items()
    }


def calcular_composicion_por_sector(portfolio: dict) -> dict:
    """Composicion del portfolio por sector. {sector: {valor_ars, peso_pct}}."""
    return _composicion_por_campo(portfolio, "sector")


def calcular_composicion_por_tipo(portfolio: dict) -> dict:
    """Composicion por tipo de activo (LOCAL/CEDEAR/ETF)."""
    return _composicion_por_campo(portfolio, "tipo")


# ---------- benchmark ----------

def _ticker_para_historico(pos: dict) -> str:
    """Para series historicas usamos el ticker subyacente (NYSE o .BA)."""
    return pos.get("ticker", "")


def comparar_vs_benchmark(
    portfolio: dict,
    benchmark: str = "SPY",
    periodo: str = "6mo",
) -> dict:
    """Compara valor diario del portfolio (en ARS) vs un benchmark.

    Calcula valor historico del portfolio asumiendo las cantidades actuales
    y convierte cada precio diario a ARS con la misma logica que
    _precio_actual_ars.

    Retorna serie temporal normalizada base 100. En caso de error, retorna
    {"error": "..."}.
    """
    tc = portfolio.get("configuracion", {}).get("tipo_cambio_ars_usd", 1)
    posiciones = portfolio.get("posiciones", [])
    if not posiciones:
        return {"error": "Portfolio vacio"}

    tickers = list({_ticker_para_historico(p) for p in posiciones if p.get("ticker")})
    todos = tickers + [benchmark]

    try:
        data = yf.download(
            todos,
            period=periodo,
            progress=False,
            auto_adjust=True,
            group_by="ticker",
        )
    except Exception as e:
        return {"error": f"No se pudieron descargar precios: {e}"}

    if data is None or data.empty:
        return {"error": "Sin datos historicos"}

    # Armar DataFrame de Close por ticker (yfinance varia el shape segun n)
    closes = pd.DataFrame()
    for tk in todos:
        try:
            if len(todos) == 1:
                serie = data["Close"]
            else:
                serie = data[tk]["Close"]
            closes[tk] = serie
        except Exception:
            continue

    closes = closes.dropna(how="all")
    if closes.empty:
        return {"error": "Series historicas vacias"}

    # Valor diario del portfolio en ARS
    valor_portfolio = pd.Series(0.0, index=closes.index)
    for pos in posiciones:
        tk = pos.get("ticker")
        cant = pos.get("cantidad", 0) or 0
        if tk not in closes.columns or cant <= 0:
            continue
        precio_serie = closes[tk].ffill()
        tipo = pos.get("tipo", "").upper()
        ratio = pos.get("ratio_cedear")

        if tipo == "LOCAL" and tk.upper().endswith(".BA"):
            precio_ars = precio_serie
        elif tipo in ("CEDEAR", "ETF") and ratio and ratio > 0:
            precio_ars = precio_serie * tc / ratio
        else:
            precio_ars = precio_serie * tc

        valor_portfolio = valor_portfolio.add(precio_ars * cant, fill_value=0)

    valor_portfolio = valor_portfolio.dropna()
    if benchmark not in closes.columns or valor_portfolio.empty:
        return {"error": "No se pudo construir la serie del portfolio"}

    bench_serie = closes[benchmark].dropna()

    # Alinear ambos indices
    idx_comun = valor_portfolio.index.intersection(bench_serie.index)
    if len(idx_comun) < 2:
        return {"error": "Series sin suficiente solapamiento"}

    vp = valor_portfolio.loc[idx_comun]
    vb = bench_serie.loc[idx_comun]

    # Normalizar base 100
    vp_norm = vp / vp.iloc[0] * 100
    vb_norm = vb / vb.iloc[0] * 100

    retorno_p = float(vp_norm.iloc[-1] - 100)
    retorno_b = float(vb_norm.iloc[-1] - 100)

    return {
        "fechas": [d.strftime("%Y-%m-%d") for d in idx_comun],
        "portfolio": vp_norm.tolist(),
        "benchmark": vb_norm.tolist(),
        "retorno_portfolio_pct": retorno_p,
        "retorno_benchmark_pct": retorno_b,
        "alpha_pct": retorno_p - retorno_b,
        "ticker_benchmark": benchmark,
    }
