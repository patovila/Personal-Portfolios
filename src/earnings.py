"""Calendario de earnings para el portfolio."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import streamlit as st
import yfinance as yf


# ── helpers ───────────────────────────────────────────────────────────────────

def _to_date(val) -> date | None:
    """Convierte Timestamp, datetime, date o string a date. None si falla."""
    if val is None:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, (datetime,)):
        return val.date()
    try:
        import pandas as pd
        ts = pd.Timestamp(val)
        if pd.isna(ts):
            return None
        return ts.date()
    except Exception:
        return None


def _parse_calendar(cal) -> dict:
    """Extrae campos clave del objeto calendar de yfinance (dict o DataFrame)."""
    out: dict = {
        "fecha_earnings":    None,
        "eps_estimado":      None,
        "eps_actual":        None,
        "revenue_estimado":  None,
        "revenue_actual":    None,
    }
    if cal is None:
        return out

    # yfinance puede devolver dict o DataFrame según versión
    try:
        import pandas as pd
        if isinstance(cal, pd.DataFrame):
            # DataFrame transpuesto: filas = campos, columna 0 = valor
            cal_dict: dict = cal.squeeze().to_dict() if not cal.empty else {}
        else:
            cal_dict = dict(cal)
    except Exception:
        return out

    # Fecha (puede ser lista con una o dos fechas — próxima primera)
    for key in ("Earnings Date", "earningsDate"):
        raw = cal_dict.get(key)
        if raw is not None:
            if isinstance(raw, (list, tuple)) and len(raw) > 0:
                out["fecha_earnings"] = _to_date(raw[0])
            else:
                out["fecha_earnings"] = _to_date(raw)
            break

    # EPS estimado
    for key in ("Earnings Average", "epsAverage", "EPS Estimate"):
        v = cal_dict.get(key)
        if v is not None:
            try:
                out["eps_estimado"] = float(v)
            except (TypeError, ValueError):
                pass
            break

    # Revenue estimado
    for key in ("Revenue Average", "revenueAverage", "Revenue Estimate"):
        v = cal_dict.get(key)
        if v is not None:
            try:
                out["revenue_estimado"] = float(v)
            except (TypeError, ValueError):
                pass
            break

    return out


# ── funciones públicas ────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_ticker(ticker: str) -> dict | None:
    """Próximo earnings de un ticker. Cache 1 hora. None si falla o sin datos."""
    try:
        t   = yf.Ticker(ticker)
        cal = t.calendar
        data = _parse_calendar(cal)
        data["ticker"] = ticker

        # Nombre de la empresa
        try:
            data["nombre"] = (t.info or {}).get("shortName") or ticker
        except Exception:
            data["nombre"] = ticker

        # Historial reciente: earnings_dates da fecha + EPS est + EPS real
        try:
            import pandas as pd
            ed = t.earnings_dates
            if ed is not None and not ed.empty:
                data["earnings_dates_df"] = ed
            else:
                data["earnings_dates_df"] = None
        except Exception:
            data["earnings_dates_df"] = None

        return data
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_portfolio(tickers: tuple) -> tuple[list, list]:
    """Retorna (proximos, historico) para los tickers del portfolio.

    proximos: earnings futuros ordenados por fecha asc.
    historico: earnings de los últimos 90 días con Beat/Miss.
    """
    from src.datos import get_ticker_adr  # import local para no circular

    hoy    = date.today()
    corte  = hoy - timedelta(days=90)

    proximos: list  = []
    historico: list = []

    for raw_ticker in tickers:
        adr = get_ticker_adr(raw_ticker)  # usa ADR si es ticker AR
        data = get_earnings_ticker(adr)
        if data is None:
            continue

        nombre = data.get("nombre", adr)

        # ── Próximo earnings ──────────────────────────────────────────────
        fecha = data.get("fecha_earnings")
        if fecha and fecha >= hoy:
            proximos.append({
                "ticker":           adr,
                "nombre":           nombre,
                "fecha":            fecha,
                "dias":             (fecha - hoy).days,
                "urgencia":         clasificar_earnings(fecha),
                "eps_estimado":     data.get("eps_estimado"),
                "revenue_estimado": data.get("revenue_estimado"),
            })

        # ── Historial reciente ────────────────────────────────────────────
        df_ed = data.get("earnings_dates_df")
        if df_ed is not None:
            try:
                import pandas as pd
                for idx, row in df_ed.iterrows():
                    f = _to_date(idx)
                    if f is None or not (corte <= f < hoy):
                        continue
                    eps_est  = row.get("EPS Estimate")
                    eps_real = row.get("Reported EPS")
                    sorpresa = row.get("Surprise(%)")
                    if pd.isna(eps_real):  # aún no reportado
                        continue
                    beat: str | None = None
                    if not pd.isna(eps_est) and not pd.isna(eps_real):
                        beat = "BEAT" if eps_real >= eps_est else "MISS"
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
                pass

    proximos.sort(key=lambda x: x["fecha"])
    historico.sort(key=lambda x: x["fecha"], reverse=True)
    return proximos, historico


def clasificar_earnings(fecha: date | None) -> str:
    if fecha is None:
        return "SIN FECHA"
    hoy = date.today()
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
