"""Comparación de rendimiento del portfolio vs benchmarks."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import streamlit as st
import yfinance as yf
import pandas as pd


_BENCHMARKS = {
    "S&P 500":  "^GSPC",
    "Nasdaq":   "^IXIC",
    "Merval":   "^MERV",
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_benchmark_data(fecha_inicio: date, fecha_fin: date) -> dict:
    """Descarga rendimiento total de S&P500, Nasdaq y Merval en el período.

    Retorna {nombre: {"ticker": str, "rendimiento_pct": float | None}}
    """
    tickers = list(_BENCHMARKS.values())
    result: dict = {}

    try:
        data = yf.download(
            tickers=" ".join(tickers),
            start=fecha_inicio.strftime("%Y-%m-%d"),
            end=(fecha_fin + timedelta(days=1)).strftime("%Y-%m-%d"),
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        for nombre, tk in _BENCHMARKS.items():
            result[nombre] = {"ticker": tk, "rendimiento_pct": None}
        return result

    for nombre, tk in _BENCHMARKS.items():
        rend = None
        try:
            if len(tickers) == 1:
                serie = data["Close"].dropna()
            else:
                serie = data[tk]["Close"].dropna()
            if len(serie) >= 2:
                rend = float((serie.iloc[-1] - serie.iloc[0]) / serie.iloc[0] * 100)
        except Exception:
            pass
        result[nombre] = {"ticker": tk, "rendimiento_pct": rend}

    return result


def calcular_rendimiento_portfolio(posiciones: list) -> dict:
    """Calcula rendimiento del portfolio usando precios almacenados.

    No hace llamadas a yfinance — usa precio_actual_ars y
    precio_promedio_compra_ars de cada posición (ya cargados).

    Retorna:
        rendimiento_pct        : retorno total %
        rendimiento_anualizado : CAGR % (None si < 30 días)
        fecha_inicio           : date más antigua de fecha_primera_compra
        valor_costo            : costo total ARS
        valor_actual           : valor actual ARS
    """
    if not posiciones:
        return {"rendimiento_pct": None, "rendimiento_anualizado": None,
                "fecha_inicio": None, "valor_costo": 0, "valor_actual": 0}

    costo  = 0.0
    actual = 0.0
    fechas = []

    for pos in posiciones:
        cant  = pos.get("cantidad") or 0
        pc    = pos.get("precio_promedio_compra_ars") or 0
        pa    = pos.get("precio_actual_ars") or 0
        costo  += cant * pc
        actual += cant * pa
        raw_f = pos.get("fecha_primera_compra")
        if raw_f:
            try:
                if isinstance(raw_f, str):
                    fechas.append(datetime.strptime(raw_f[:10], "%Y-%m-%d").date())
                elif isinstance(raw_f, (date, datetime)):
                    fechas.append(raw_f if isinstance(raw_f, date) else raw_f.date())
            except Exception:
                pass

    if costo == 0:
        return {"rendimiento_pct": None, "rendimiento_anualizado": None,
                "fecha_inicio": None, "valor_costo": 0, "valor_actual": 0}

    rend_pct = (actual - costo) / costo * 100
    fecha_inicio = min(fechas) if fechas else None

    rend_anual = None
    if fecha_inicio:
        dias = (date.today() - fecha_inicio).days
        if dias >= 30:
            años = dias / 365.25
            rend_anual = ((actual / costo) ** (1 / años) - 1) * 100

    return {
        "rendimiento_pct":        round(rend_pct, 2),
        "rendimiento_anualizado": round(rend_anual, 2) if rend_anual is not None else None,
        "fecha_inicio":           fecha_inicio,
        "valor_costo":            round(costo, 0),
        "valor_actual":           round(actual, 0),
    }


def comparar_benchmarks(rend_portfolio_pct: float | None,
                        rend_benchmarks: dict) -> dict:
    """Calcula alpha del portfolio vs cada benchmark y genera veredictos.

    rend_benchmarks: {nombre: {"ticker": str, "rendimiento_pct": float|None}}

    Retorna:
        alphas    : {nombre: float | None}   — portfolio - benchmark
        veredictos: {nombre: str}            — texto ✅/⚠️
    """
    alphas: dict    = {}
    veredictos: dict = {}

    if rend_portfolio_pct is None:
        return {"alphas": {}, "veredictos": {}}

    for nombre, info in rend_benchmarks.items():
        rb = info.get("rendimiento_pct")
        if rb is None:
            alphas[nombre]     = None
            veredictos[nombre] = "Sin datos"
            continue
        alpha = rend_portfolio_pct - rb
        alphas[nombre] = round(alpha, 2)
        if alpha >= 0:
            veredictos[nombre] = f"✅ Superás al {nombre} por {alpha:+.1f}pp"
        else:
            veredictos[nombre] = f"⚠️ El {nombre} te ganó por {abs(alpha):.1f}pp"

    return {"alphas": alphas, "veredictos": veredictos}
