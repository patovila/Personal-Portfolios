"""Watchlist compartible — gestión, precios y links públicos."""
import pandas as pd
import streamlit as st

from src.data_layer import get_precios
from src import storage

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
    data = storage.load("watchlist", nombre, default=[])
    return data if isinstance(data, list) else []


def guardar_watchlist(nombre: str, tickers: list) -> bool:
    """Guarda watchlist: session_state primero, luego JSON como backup."""
    return storage.save("watchlist", nombre, tickers)


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
