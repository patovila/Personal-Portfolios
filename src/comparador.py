"""Comparador side-by-side de 2 a 4 tickers."""
from __future__ import annotations

import pandas as pd
import yfinance as yf
import streamlit as st

from src.datos import get_ticker_info_safe, get_ticker_adr


# Métricas donde un valor MENOR es mejor
_MENOR_ES_MEJOR: set[str] = {"PE Trailing", "P/B", "EV/EBITDA", "Deuda/Equity", "Beta"}

# Métricas sin best/worst (no se colorean)
_NEUTRAL: set[str] = {"Precio actual", "Market Cap (B USD)"}

METRICAS: list[str] = [
    "Precio actual",
    "Market Cap (B USD)",
    "PE Trailing",
    "P/B",
    "EV/EBITDA",
    "Margen Bruto %",
    "Margen Operativo %",
    "Margen Neto %",
    "Revenue CAGR 3a %",
    "ROE %",
    "Deuda/Equity",
    "Dividend Yield %",
    "Beta",
    "Var 1 día %",
    "Var 1 año %",
]


@st.cache_data(ttl=86400, show_spinner=False)
def _revenue_cagr(ticker_adr: str) -> float | None:
    """Revenue CAGR ~3 años desde financials. Cache 24h."""
    try:
        fin = yf.Ticker(ticker_adr).financials
        if fin.empty or "Total Revenue" not in fin.index:
            return None
        serie = fin.loc["Total Revenue"].dropna()
        if len(serie) < 2:
            return None
        v_f   = float(serie.iloc[0])
        v_i   = float(serie.iloc[-1])
        años  = abs(serie.index[0].year - serie.index[-1].year)
        if v_i <= 0 or v_f <= 0 or años <= 0:
            return None
        return round(((v_f / v_i) ** (1 / años) - 1) * 100, 2)
    except Exception:
        return None


def _var_hist(df: pd.DataFrame | None) -> float | None:
    """Variación % del primer al último close de un DataFrame."""
    if df is None or df.empty or "Close" not in df.columns:
        return None
    c = df["Close"].dropna()
    if len(c) < 2:
        return None
    return float((c.iloc[-1] - c.iloc[0]) / c.iloc[0] * 100)


@st.cache_data(ttl=300, show_spinner=False)
def _batch_hist(tickers: tuple, period: str) -> dict[str, pd.DataFrame]:
    """Batch download de historial. Cache 5 min."""
    if not tickers:
        return {}
    unique = list(tickers)
    try:
        raw = yf.download(
            " ".join(unique),
            period=period,
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return {tk: pd.DataFrame() for tk in unique}
    if raw is None or raw.empty:
        return {tk: pd.DataFrame() for tk in unique}
    result: dict[str, pd.DataFrame] = {}
    if len(unique) == 1:
        result[unique[0]] = raw if "Close" in raw.columns else pd.DataFrame()
    else:
        for tk in unique:
            try:
                result[tk] = raw[tk]
            except (KeyError, TypeError):
                result[tk] = pd.DataFrame()
    return result


@st.cache_data(ttl=3600)
def get_datos_comparador(tickers: tuple) -> pd.DataFrame:
    """DataFrame comparativo. Filas = métricas, Columnas = tickers. Cache 1h.

    Usa get_ticker_info_safe() para fundamentals (cache 24h) y
    batch download para variaciones de precio (cache 5 min).
    """
    if not tickers:
        return pd.DataFrame()

    hist_2d = _batch_hist(tickers, "2d")
    hist_1y = _batch_hist(tickers, "1y")

    columnas: dict[str, list] = {}
    for tk in tickers:
        tk_fund = get_ticker_adr(tk)
        info    = get_ticker_info_safe(tk_fund)

        def _safe(k: str, decs: int = 2):
            v = info.get(k)
            try:
                f = float(v)
                return round(f, decs) if not pd.isna(f) else None
            except Exception:
                return None

        def _pct(k: str):
            v = info.get(k)
            try:
                f = float(v)
                return round(f * 100, 2) if not pd.isna(f) else None
            except Exception:
                return None

        mcap  = info.get("marketCap")
        mcap_b = round(float(mcap) / 1e9, 2) if mcap else None
        precio = info.get("currentPrice") or info.get("regularMarketPrice")
        v1d    = _var_hist(hist_2d.get(tk))
        v1y    = _var_hist(hist_1y.get(tk))

        columnas[tk] = [
            round(float(precio), 2) if precio else None,  # Precio actual
            mcap_b,                                        # Market Cap (B USD)
            _safe("trailingPE"),                           # PE Trailing
            _safe("priceToBook"),                          # P/B
            _safe("enterpriseToEbitda"),                   # EV/EBITDA
            _pct("grossMargins"),                          # Margen Bruto %
            _pct("operatingMargins"),                      # Margen Operativo %
            _pct("profitMargins"),                         # Margen Neto %
            _revenue_cagr(tk_fund),                        # Revenue CAGR 3a %
            _pct("returnOnEquity"),                        # ROE %
            _safe("debtToEquity"),                         # Deuda/Equity
            _pct("dividendYield"),                         # Dividend Yield %
            _safe("beta"),                                 # Beta
            round(v1d, 2) if v1d is not None else None,   # Var 1 día %
            round(v1y, 2) if v1y is not None else None,   # Var 1 año %
        ]

    return pd.DataFrame(columnas, index=METRICAS)


@st.cache_data(ttl=300)
def performance_relativa(tickers: tuple, periodo: str = "1y") -> pd.DataFrame:
    """Precios históricos normalizados base 100 desde inicio del período. Cache 5 min.

    Retorna DataFrame con fecha como índice, un ticker por columna.
    """
    if not tickers:
        return pd.DataFrame()
    try:
        raw = yf.download(
            tickers=" ".join(tickers),
            period=periodo,
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return pd.DataFrame()
    if raw is None or raw.empty:
        return pd.DataFrame()

    closes = pd.DataFrame()
    for tk in tickers:
        try:
            serie = raw["Close"] if len(tickers) == 1 else raw[tk]["Close"]
            closes[tk] = serie.dropna()
        except Exception:
            continue

    if closes.empty or closes.shape[0] < 2:
        return pd.DataFrame()
    closes = closes.dropna(how="all")
    return closes.div(closes.iloc[0]).mul(100).round(4)
