"""Datos de mercado en tiempo real para la home screen."""
import yfinance as yf
import pandas as pd
import streamlit as st

INDICES = [
    {"ticker": "^GSPC",   "nombre": "S&P 500"},
    {"ticker": "^DJI",    "nombre": "Dow Jones"},
    {"ticker": "^IXIC",   "nombre": "Nasdaq"},
    {"ticker": "^RUT",    "nombre": "Russell 2000"},
    {"ticker": "^MERV",   "nombre": "Merval"},
    {"ticker": "GC=F",    "nombre": "Oro"},
    {"ticker": "CL=F",    "nombre": "Petróleo WTI"},
    {"ticker": "BTC-USD", "nombre": "Bitcoin"},
]

_TAPE_INDICES    = ["^GSPC", "^IXIC", "^MERV"]
_INDICES_TICKERS = [i["ticker"] for i in INDICES]


def _batch_download(tickers: list) -> dict:
    """Una sola request HTTP para N tickers. Retorna {ticker: DataFrame}."""
    if not tickers:
        return {}
    unique = list(dict.fromkeys(tickers))  # deduplica preservando orden
    try:
        data = yf.download(
            tickers=" ".join(unique),
            period="2d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return {tk: pd.DataFrame() for tk in unique}

    if data is None or data.empty:
        return {tk: pd.DataFrame() for tk in unique}

    result = {}
    if len(unique) == 1:
        # Un solo ticker: yf.download devuelve DataFrame plano (sin MultiIndex)
        df = data.dropna(subset=["Close"]) if "Close" in data.columns else pd.DataFrame()
        result[unique[0]] = df
    else:
        for tk in unique:
            try:
                sub = data[tk].dropna(subset=["Close"])
                result[tk] = sub
            except (KeyError, TypeError):
                result[tk] = pd.DataFrame()
    return result


def _var_pct(df) -> float | None:
    """Variación % del día desde un DataFrame con columna Close (period='2d')."""
    if df is None or df.empty or "Close" not in df.columns:
        return None
    close = df["Close"].dropna()
    if len(close) >= 2:
        return float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
    return None


@st.cache_data(ttl=300)
def get_indices_globales() -> list:
    """8 índices globales en una sola request. Cache 5 min."""
    data = _batch_download(_INDICES_TICKERS)
    result = []
    for idx in INDICES:
        df = data.get(idx["ticker"], pd.DataFrame())
        precio = float(df["Close"].iloc[-1]) if not df.empty else None
        result.append({**idx, "precio": precio, "variacion_pct": _var_pct(df)})
    return result


@st.cache_data(ttl=300)
def get_movers_portfolio(tickers: tuple) -> dict:
    """Gainers y losers del portfolio en una sola request. Cache 5 min."""
    data = _batch_download(list(tickers))
    items = []
    for tk in tickers:
        df = data.get(tk, pd.DataFrame())
        if df.empty:
            continue
        precio = float(df["Close"].iloc[-1])
        var    = _var_pct(df) or 0.0
        vol    = int(df["Volume"].iloc[-1]) if "Volume" in df.columns else 0
        items.append({"ticker": tk, "precio": precio, "variacion_pct": var, "volumen": vol})
    gainers = sorted([i for i in items if i["variacion_pct"] >= 0],
                     key=lambda x: x["variacion_pct"], reverse=True)[:5]
    losers  = sorted([i for i in items if i["variacion_pct"] < 0],
                     key=lambda x: x["variacion_pct"])[:5]
    return {"gainers": gainers, "losers": losers}


@st.cache_data(ttl=180)
def get_ticker_tape(portfolio_tickers: tuple) -> list:
    """Banda de precios: portfolio + índices principales. Cache 3 min."""
    all_tks = list(portfolio_tickers) + [t for t in _TAPE_INDICES if t not in portfolio_tickers]
    data = _batch_download(all_tks)
    result = []
    for tk in all_tks:
        df = data.get(tk, pd.DataFrame())
        if df.empty:
            continue
        precio = float(df["Close"].iloc[-1])
        var    = _var_pct(df) or 0.0
        nombre = tk.replace("^", "").replace("-USD", "").replace("=F", "")
        result.append({"ticker": nombre, "precio": precio, "variacion_pct": var})
    return result
