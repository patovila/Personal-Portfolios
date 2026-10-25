"""Capa única de acceso a yfinance.

REGLA: Solo este módulo hace llamadas directas a ``yf.*``.
Todos los demás módulos de ``src/`` importan desde aquí.

Garantías:
- Nunca propaga excepción a los consumidores.
- Ante fallo de red: devuelve último valor válido (``_LAST_VALID``) o vacío.
- Cache: precios 5 min · info/fundamentals/noticias 24 h / 30 min.
"""
from __future__ import annotations

import time as _time
import pandas as pd
import yfinance as yf
import streamlit as st

# Sobrevive reruns de Streamlit; actúa como fallback cuando yfinance falla.
_LAST_VALID: dict[str, object] = {}


# ─────────────────────────────────────────────────────────────────────────────
# Precios históricos — batch download
# ─────────────────────────────────────────────────────────────────────────────

def get_precios(
    tickers: list[str] | tuple[str, ...],
    period: str = "1y",
    interval: str = "1d",
) -> dict[str, pd.DataFrame]:
    """Descarga precios históricos en una sola request HTTP. Cache 5 min.

    Args:
        tickers:  lista/tuple de símbolos yfinance.
        period:   "1d" | "5d" | "1mo" | "3mo" | "6mo" | "1y" | "2y" |
                  "5y" | "10y" | "ytd" | "max"
        interval: "1d" | "1wk" | "1mo"

    Returns:
        ``{ticker: DataFrame(Open/High/Low/Close/Volume)}``
        DataFrame vacío para tickers que fallaron.
    """
    t_tuple = tuple(tickers) if isinstance(tickers, list) else tickers
    return _cached_precios(t_tuple, period, interval)


@st.cache_data(ttl=300, show_spinner=False)
def _cached_precios(
    tickers: tuple[str, ...],
    period: str,
    interval: str,
) -> dict[str, pd.DataFrame]:
    if not tickers:
        return {}
    unique = list(dict.fromkeys(tickers))
    cache_key = f"precios:{','.join(unique)}:{period}:{interval}"

    try:
        raw = yf.download(
            " ".join(unique),
            period=period,
            interval=interval,
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return _fallback_dict(cache_key, unique)

    if raw is None or raw.empty:
        return _fallback_dict(cache_key, unique)

    result: dict[str, pd.DataFrame] = {}
    if len(unique) == 1:
        df = raw.copy()
        result[unique[0]] = df if "Close" in df.columns and not df["Close"].dropna().empty else pd.DataFrame()
    else:
        for tk in unique:
            try:
                sub = raw[tk].dropna(subset=["Close"])
                result[tk] = sub if not sub.empty else pd.DataFrame()
            except (KeyError, TypeError):
                result[tk] = pd.DataFrame()

    _LAST_VALID[cache_key] = result
    return result


def get_precios_rango(
    tickers: list[str] | tuple[str, ...],
    start: str,
    end: str,
) -> dict[str, pd.DataFrame]:
    """Descarga precios para un rango de fechas. Cache 1 hora.

    Args:
        tickers: lista/tuple de símbolos.
        start:   fecha inicio "YYYY-MM-DD".
        end:     fecha fin "YYYY-MM-DD" (inclusive).
    """
    t_tuple = tuple(tickers) if isinstance(tickers, list) else tickers
    return _cached_precios_rango(t_tuple, start, end)


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_precios_rango(
    tickers: tuple[str, ...],
    start: str,
    end: str,
) -> dict[str, pd.DataFrame]:
    if not tickers:
        return {}
    unique = list(dict.fromkeys(tickers))
    cache_key = f"precios_rango:{','.join(unique)}:{start}:{end}"

    try:
        raw = yf.download(
            " ".join(unique),
            start=start,
            end=end,
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return _fallback_dict(cache_key, unique)

    if raw is None or raw.empty:
        return _fallback_dict(cache_key, unique)

    result: dict[str, pd.DataFrame] = {}
    if len(unique) == 1:
        df = raw.copy()
        result[unique[0]] = df if "Close" in df.columns else pd.DataFrame()
    else:
        for tk in unique:
            try:
                sub = raw[tk].dropna(subset=["Close"])
                result[tk] = sub if not sub.empty else pd.DataFrame()
            except (KeyError, TypeError):
                result[tk] = pd.DataFrame()

    _LAST_VALID[cache_key] = result
    return result


def _fallback_dict(cache_key: str, unique: list[str]) -> dict[str, pd.DataFrame]:
    """Devuelve último resultado cacheado o dict de DataFrames vacíos."""
    cached = _LAST_VALID.get(cache_key)
    if isinstance(cached, dict):
        return cached
    return {tk: pd.DataFrame() for tk in unique}


# ─────────────────────────────────────────────────────────────────────────────
# Info / metadata del ticker
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=86400, show_spinner=False)
def get_info(ticker: str) -> dict:
    """``yf.Ticker.info`` con cache 24 h, 3 reintentos y fallback.

    Nunca propaga excepción. Retorna ``{}`` si todos los intentos fallan
    y no hay valor previo en ``_LAST_VALID``.
    """
    cache_key = f"info:{ticker}"
    for intento in range(3):
        try:
            info = yf.Ticker(ticker).info
            if info and len(info) >= 5:
                _LAST_VALID[cache_key] = info
                return info
            break
        except Exception as exc:
            msg = str(exc).lower()
            if intento < 2 and ("too many requests" in msg or "429" in msg or "rate" in msg):
                _time.sleep(2 ** intento)
            else:
                break

    return _LAST_VALID.get(cache_key, {})


# ─────────────────────────────────────────────────────────────────────────────
# Fundamentals (estados financieros)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=86400, show_spinner=False)
def get_fundamentals(ticker: str) -> dict[str, pd.DataFrame]:
    """``financials``, ``balance_sheet``, ``cashflow`` con fallbacks. Cache 24 h.

    Returns::

        {
            "pl":       DataFrame,   # income statement
            "balance":  DataFrame,   # balance sheet
            "cashflow": DataFrame,   # cash flow statement
        }

    DataFrames vacíos si no hay datos disponibles.
    """
    cache_key = f"fundamentals:{ticker}"
    _empty = {
        "pl":      pd.DataFrame(),
        "balance": pd.DataFrame(),
        "cashflow": pd.DataFrame(),
    }
    try:
        t = yf.Ticker(ticker)
        result = {
            "pl":      t.financials    if not _df_empty(t.financials)    else pd.DataFrame(),
            "balance": t.balance_sheet if not _df_empty(t.balance_sheet) else pd.DataFrame(),
            "cashflow": t.cashflow     if not _df_empty(t.cashflow)      else pd.DataFrame(),
        }
        _LAST_VALID[cache_key] = result
        return result
    except Exception:
        return _LAST_VALID.get(cache_key, _empty)


def _df_empty(df) -> bool:
    return df is None or (hasattr(df, "empty") and df.empty)


# ─────────────────────────────────────────────────────────────────────────────
# Noticias
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=1800, show_spinner=False)
def get_news(ticker: str) -> list[dict]:
    """Noticias recientes vía ``yf.Ticker.news``. Cache 30 min.

    Retorna lista vacía si falla; nunca propaga excepción.
    """
    try:
        raw = yf.Ticker(ticker).news or []
        return list(raw)
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de validación y formato
# ─────────────────────────────────────────────────────────────────────────────

def safe_val(v, decimals: int = 2, suffix: str = "") -> str:
    """Formatea número para display; retorna ``"N/D"`` si None/NaN/inf.

    Ejemplos::

        safe_val(None)          → "N/D"
        safe_val(float('nan'))  → "N/D"
        safe_val(1234.5)        → "1,234.50"
        safe_val(0.153, suffix="%") → "0.15%"
    """
    if v is None:
        return "N/D"
    try:
        f = float(v)
        if not pd.isfinite(f):
            return "N/D"
        return f"{f:,.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return "N/D"


def safe_ratio(numerator, denominator, decimals: int = 2, suffix: str = "") -> str:
    """División segura con formato. Retorna ``"N/D"`` ante div/0 o None."""
    if numerator is None or denominator is None:
        return "N/D"
    try:
        n, d = float(numerator), float(denominator)
        if not (pd.isfinite(n) and pd.isfinite(d)) or d == 0:
            return "N/D"
        return safe_val(n / d, decimals, suffix)
    except (TypeError, ValueError):
        return "N/D"


@st.cache_data(ttl=60, show_spinner=False)
def get_precio_actual(ticker: str) -> float | None:
    """Último precio de mercado vía fast_info. Cache 60 seg.

    Más ligero que get_info(); ideal para calculadoras y precios spot.
    Nunca propaga excepción.
    """
    cache_key = f"precio_actual:{ticker}"
    try:
        precio = yf.Ticker(ticker).fast_info["lastPrice"]
        if precio and float(precio) > 0:
            _LAST_VALID[cache_key] = float(precio)
            return float(precio)
    except Exception:
        pass
    # Fallback: currentPrice de info (puede ser del mismo día)
    info = get_info(ticker)
    precio = info.get("currentPrice") or info.get("regularMarketPrice")
    return float(precio) if precio else _LAST_VALID.get(cache_key)


def normalize_debt_equity(raw_value) -> float | None:
    """Normaliza ``debtToEquity`` de yfinance al ratio real (divide por 100).

    yfinance reporta debtToEquity como porcentaje (ej. ``170`` = 1.70×).
    Esta función lo convierte a ratio (``1.70``) para display correcto.

    Returns:
        float normalizado, o ``None`` si el valor es inválido.
    """
    if raw_value is None:
        return None
    try:
        v = float(raw_value)
        return v / 100.0 if pd.isfinite(v) else None
    except (TypeError, ValueError):
        return None
