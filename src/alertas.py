"""Sistema de alertas de precio: take profit, stop loss, variación diaria."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st
import yfinance as yf


# ──────────────────────────────────────────────────────────────────
# PERSISTENCIA
# ──────────────────────────────────────────────────────────────────

def cargar_alertas(portfolio_name: str) -> list:
    """Carga alertas: session_state → JSON → [].

    session_state es la fuente de verdad durante la sesión.
    """
    ss_key = f"alertas_{portfolio_name}"
    if ss_key in st.session_state:
        return st.session_state[ss_key]
    ruta = Path("data/alertas") / f"{portfolio_name}.json"
    if ruta.exists():
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    else:
        data = []
    st.session_state[ss_key] = data
    return data


def guardar_alertas(portfolio_name: str, alertas: list) -> None:
    """Guarda alertas: session_state primero, luego JSON como backup."""
    st.session_state[f"alertas_{portfolio_name}"] = alertas
    try:
        ruta = Path("data/alertas") / f"{portfolio_name}.json"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(alertas, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # Filesystem puede ser read-only en Streamlit Cloud


def nueva_alerta(ticker: str, tipo: str, valor: float) -> dict:
    """Crea dict de nueva alerta con defaults."""
    return {
        "id": str(uuid4())[:8],
        "ticker": ticker,
        "tipo": tipo,          # "take_profit" | "stop_loss" | "variacion_dia"
        "valor": valor,
        "activa": True,
        "creada": datetime.now().isoformat(),
        "disparada": False,
        "fecha_disparo": None,
    }


# ──────────────────────────────────────────────────────────────────
# PRECIOS
# ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def get_precios_para_alertas(tickers: tuple) -> dict:
    """Precio actual y variación diaria para cada ticker. Cache 60 s.

    Recibe tuple (hashable) para compatibilidad con st.cache_data.
    Retorna {ticker: {"precio": float, "variacion_dia": float}}.
    """
    resultado = {}
    for ticker in tickers:
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if hist.empty:
                continue
            precio = float(hist["Close"].iloc[-1])
            variacion = 0.0
            if len(hist) >= 2:
                prev = float(hist["Close"].iloc[-2])
                if prev:
                    variacion = (precio - prev) / prev * 100
            resultado[ticker] = {"precio": precio, "variacion_dia": variacion}
        except Exception:
            pass  # No crashear si yfinance falla
    return resultado


# ──────────────────────────────────────────────────────────────────
# LÓGICA DE ALERTAS
# ──────────────────────────────────────────────────────────────────

def verificar_alertas(alertas: list, precios_actuales: dict) -> list:
    """Retorna las alertas que deben dispararse. NO modifica las originales.

    Solo evalúa alertas con activa=True y disparada=False.
    """
    disparadas = []
    for alerta in alertas:
        if not alerta.get("activa") or alerta.get("disparada"):
            continue
        datos = precios_actuales.get(alerta["ticker"])
        if not datos:
            continue
        precio = datos["precio"]
        variacion = datos["variacion_dia"]
        tipo = alerta["tipo"]
        valor = alerta["valor"]

        if tipo == "take_profit" and precio >= valor:
            disparadas.append(alerta)
        elif tipo == "stop_loss" and precio <= valor:
            disparadas.append(alerta)
        elif tipo == "variacion_dia" and abs(variacion) >= valor:
            disparadas.append(alerta)

    return disparadas


def formatear_alerta_disparada(alerta: dict, precio_actual: float) -> str:
    """Mensaje legible de una alerta disparada.

    Para variacion_dia, pasar datos["variacion_dia"] como precio_actual.
    """
    ticker = alerta["ticker"]
    valor = alerta["valor"]
    tipo = alerta["tipo"]
    if tipo == "take_profit":
        return f"🚨 {ticker} superó ${valor:,.2f} (precio actual: ${precio_actual:,.2f})"
    elif tipo == "stop_loss":
        return f"🛑 {ticker} bajó de ${valor:,.2f} (precio actual: ${precio_actual:,.2f})"
    elif tipo == "variacion_dia":
        return f"⚡ {ticker} varió {precio_actual:.1f}% en el día (umbral: {valor:.0f}%)"
    return f"🔔 Alerta {ticker}"
