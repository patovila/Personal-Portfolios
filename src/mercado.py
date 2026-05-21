"""Datos de mercado en tiempo real para la home screen."""
import yfinance as yf
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

_TAPE_INDICES = ["^GSPC", "^IXIC", "^MERV"]


def _var_pct(hist) -> float | None:
    """Calcula variacion dia% desde un DataFrame de history(period='2d')."""
    if hist is None or hist.empty:
        return None
    close = hist["Close"].dropna()
    if len(close) >= 2:
        return float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
    return None


@st.cache_data(ttl=120)
def get_indices_globales() -> list:
    result = []
    for idx in INDICES:
        try:
            hist = yf.Ticker(idx["ticker"]).history(period="2d")
            precio = float(hist["Close"].iloc[-1]) if not hist.empty else None
            var = _var_pct(hist)
            result.append({**idx, "precio": precio, "variacion_pct": var})
        except Exception:
            result.append({**idx, "precio": None, "variacion_pct": None})
    return result


@st.cache_data(ttl=120)
def get_movers_portfolio(tickers: tuple) -> dict:
    items = []
    for tk in tickers:
        try:
            hist = yf.Ticker(tk).history(period="2d")
            if hist.empty:
                continue
            precio = float(hist["Close"].iloc[-1])
            var = _var_pct(hist) or 0.0
            vol = int(hist["Volume"].iloc[-1]) if "Volume" in hist.columns else 0
            items.append({"ticker": tk, "precio": precio, "variacion_pct": var, "volumen": vol})
        except Exception:
            pass
    gainers = sorted([i for i in items if i["variacion_pct"] >= 0],
                     key=lambda x: x["variacion_pct"], reverse=True)[:5]
    losers  = sorted([i for i in items if i["variacion_pct"] < 0],
                     key=lambda x: x["variacion_pct"])[:5]
    return {"gainers": gainers, "losers": losers}


@st.cache_data(ttl=60)
def get_ticker_tape(portfolio_tickers: tuple) -> list:
    all_tks = list(portfolio_tickers) + [t for t in _TAPE_INDICES if t not in portfolio_tickers]
    result = []
    for tk in all_tks:
        try:
            hist = yf.Ticker(tk).history(period="2d")
            if hist.empty:
                continue
            precio = float(hist["Close"].iloc[-1])
            var = _var_pct(hist) or 0.0
            nombre = tk.replace("^", "").replace("-USD", "").replace("=F", "")
            result.append({"ticker": nombre, "precio": precio, "variacion_pct": var})
        except Exception:
            pass
    return result
