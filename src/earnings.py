"""Calendario de earnings — Finnhub API con fallback yfinance."""
from __future__ import annotations

import os
from datetime import date, datetime, timedelta

import streamlit as st


# ── Cliente Finnhub ───────────────────────────────────────────────────────────

def get_finnhub_client():
    """Retorna finnhub.Client o None si no hay API key o librería."""
    try:
        api_key = st.secrets["FINNHUB_API_KEY"]
    except Exception:
        api_key = os.getenv("FINNHUB_API_KEY", "")

    if not api_key:
        return None

    try:
        import finnhub
        return finnhub.Client(api_key=api_key)
    except ImportError:
        return None


def finnhub_disponible() -> bool:
    return get_finnhub_client() is not None


# ── Funciones principales (Finnhub) ──────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_calendario(tickers: tuple) -> list:
    """Próximos earnings (90 días) de los tickers. Cache 1 hora.

    Retorna lista ordenada por fecha con campos:
    ticker, fecha, dias, urgencia, eps_estimado, hour, revenue_estimado
    """
    client = get_finnhub_client()
    if client is None:
        return []

    hoy      = date.today()
    hasta    = hoy + timedelta(days=90)
    from_str = hoy.strftime("%Y-%m-%d")
    to_str   = hasta.strftime("%Y-%m-%d")

    resultado: list = []
    for ticker in tickers:
        try:
            data = client.earnings_calendar(_from=from_str, to=to_str, symbol=ticker)
            cal  = (data or {}).get("earningsCalendar", [])
            for item in cal:
                fecha_str = item.get("date")
                if not fecha_str:
                    continue
                try:
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except ValueError:
                    continue
                resultado.append({
                    "ticker":            ticker,
                    "fecha":             fecha,
                    "dias":              (fecha - hoy).days,
                    "urgencia":          clasificar_earnings(fecha),
                    "eps_estimado":      item.get("epsEstimate"),
                    "eps_actual":        item.get("epsActual"),
                    "hour":              item.get("hour", ""),   # "bmo" / "amc"
                    "revenue_estimado":  item.get("revenueEstimate"),
                })
        except Exception:
            continue

    resultado.sort(key=lambda x: x["fecha"])
    return resultado


@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_historico(ticker: str, trimestres: int = 4) -> list:
    """Historial EPS real vs estimado (últimos N trimestres). Cache 1 hora."""
    client = get_finnhub_client()
    if client is None:
        return []

    try:
        data = client.company_earnings(ticker, limit=trimestres)
    except Exception:
        return []

    resultado: list = []
    for item in (data or []):
        eps_est  = item.get("estimate")
        eps_real = item.get("actual")
        period   = item.get("period", "")

        sorpresa = None
        beat     = None
        if eps_est is not None and eps_real is not None and eps_est != 0:
            sorpresa = (eps_real - eps_est) / abs(eps_est) * 100
            beat     = "BEAT" if eps_real >= eps_est else "MISS"

        resultado.append({
            "ticker":   ticker,
            "period":   period,
            "eps_est":  round(float(eps_est),  2) if eps_est  is not None else None,
            "eps_real": round(float(eps_real), 2) if eps_real is not None else None,
            "sorpresa": round(sorpresa, 1)         if sorpresa is not None else None,
            "beat":     beat,
        })

    return resultado


# ── Helpers ───────────────────────────────────────────────────────────────────

def clasificar_earnings(fecha: date | None) -> str:
    if fecha is None:
        return "SIN FECHA"
    hoy   = date.today()
    delta = (fecha - hoy).days
    if delta == 0:
        return "HOY"
    if delta <= 7:
        return "ESTA SEMANA"
    if delta <= 30:
        return "ESTE MES"
    if delta <= 90:
        return "PRÓXIMO TRIMESTRE"
    return "MÁS ADELANTE"


def _to_date(val):
    if val is None:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    try:
        import pandas as pd
        ts = pd.Timestamp(val)
        if pd.isna(ts):
            return None
        return ts.date()
    except Exception:
        return None


# ── Fallback yfinance ─────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_portfolio_yf(tickers: tuple) -> tuple[list, list]:
    """Fallback yfinance: historial últimos 90 días (no garantiza fechas futuras)."""
    import yfinance as yf
    from src.datos import get_ticker_adr
    import pandas as pd

    hoy   = date.today()
    corte = hoy - timedelta(days=90)
    proximos:  list = []
    historico: list = []

    for raw_ticker in tickers:
        adr = get_ticker_adr(raw_ticker)
        try:
            t      = yf.Ticker(adr)
            nombre = (t.info or {}).get("shortName") or adr
            ed     = t.earnings_dates
            if ed is None or ed.empty:
                continue
            for idx, row in ed.iterrows():
                f = _to_date(idx)
                if f is None:
                    continue
                if f >= hoy:
                    eps_est = row.get("EPS Estimate")
                    proximos.append({
                        "ticker":           adr,
                        "nombre":           nombre,
                        "fecha":            f,
                        "dias":             (f - hoy).days,
                        "urgencia":         clasificar_earnings(f),
                        "eps_estimado":     None if (eps_est is None or pd.isna(eps_est)) else float(eps_est),
                        "hour":             "",
                        "revenue_estimado": None,
                    })
                elif corte <= f < hoy:
                    eps_est  = row.get("EPS Estimate")
                    eps_real = row.get("Reported EPS")
                    sorpresa = row.get("Surprise(%)")
                    if pd.isna(eps_real):
                        continue
                    beat = None
                    if not pd.isna(eps_est) and not pd.isna(eps_real):
                        beat = "BEAT" if float(eps_real) >= float(eps_est) else "MISS"
                    historico.append({
                        "ticker":   adr,
                        "nombre":   nombre,
                        "fecha":    f,
                        "eps_est":  None if pd.isna(eps_est)  else round(float(eps_est),  2),
                        "eps_real": None if pd.isna(eps_real) else round(float(eps_real), 2),
                        "sorpresa": None if pd.isna(sorpresa) else round(float(sorpresa), 1),
                        "beat":     beat,
                    })
        except Exception:
            continue

    proximos.sort(key=lambda x:  x["fecha"])
    historico.sort(key=lambda x: x["fecha"], reverse=True)
    return proximos, historico


# Alias para compatibilidad con imports existentes
def get_earnings_portfolio(tickers: tuple) -> tuple[list, list]:
    """Compatibilidad: usa Finnhub si hay key, sino yfinance."""
    if finnhub_disponible():
        cal = get_earnings_calendario(tickers)
        # Para historial, necesitamos datos por ticker
        hist: list = []
        for tk in tickers:
            hist.extend(get_earnings_historico(tk))
        return cal, hist
    return get_earnings_portfolio_yf(tickers)
