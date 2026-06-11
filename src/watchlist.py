"""Watchlist compartible — gestión, precios y links públicos."""
import json
import os

import pandas as pd
import streamlit as st

from src.data_layer import get_precios

_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "watchlists",
)

_BASE_URL = "https://personalfinances.streamlit.app"

WATCHLISTS_PREDEFINIDAS = {
    "🇦🇷 Merval Top 10": [
        "GGAL.BA", "YPF.BA", "PAMP.BA", "TGS.BA", "BMA.BA",
        "ALUA.BA", "TXAR.BA", "SUPV.BA", "CEPU.BA", "LOMA.BA",
    ],
    "🚀 Tech Giants": [
        "AAPL", "GOOGL", "NVDA", "META", "MSFT", "AMZN", "TSLA", "NFLX",
    ],
    "💰 Dividendos": [
        "KO", "JNJ", "PEP", "V", "MA", "T", "VZ", "IBM",
    ],
}


def cargar_watchlist(nombre: str) -> list:
    """Carga watchlist: session_state → JSON → [].

    session_state es la fuente de verdad durante la sesión.
    """
    ss_key = f"watchlist_{nombre}"
    if ss_key in st.session_state:
        return st.session_state[ss_key]
    os.makedirs(_DIR, exist_ok=True)
    path = os.path.join(_DIR, f"{nombre}.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            data = data if isinstance(data, list) else []
        except Exception:
            data = []
    else:
        data = []
    st.session_state[ss_key] = data
    return data


def guardar_watchlist(nombre: str, tickers: list) -> bool:
    """Guarda watchlist: session_state primero, luego JSON como backup."""
    st.session_state[f"watchlist_{nombre}"] = tickers
    os.makedirs(_DIR, exist_ok=True)
    path = os.path.join(_DIR, f"{nombre}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tickers, f)
        return True
    except Exception:
        return False


def generar_link_compartir(nombre: str) -> str:
    """URL pública para compartir la watchlist en modo lectura."""
    return f"{_BASE_URL}/?watchlist={nombre}"


def get_precios_watchlist(tickers: tuple) -> list:
    """Precio actual y variación % del día para cada ticker.

    Delega a data_layer.get_precios (cache 5 min).
    """
    if not tickers:
        return []

    data = get_precios(list(tickers), "2d")
    result = []
    for tk in tickers:
        df = data.get(tk, pd.DataFrame())
        try:
            close = df["Close"].dropna() if not df.empty and "Close" in df.columns else pd.Series(dtype=float)
            precio = float(close.iloc[-1]) if len(close) >= 1 else None
            var    = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) >= 2 else None
            result.append({"ticker": tk, "precio": precio, "variacion_pct": var})
        except Exception:
            result.append({"ticker": tk, "precio": None, "variacion_pct": None})
    return result
