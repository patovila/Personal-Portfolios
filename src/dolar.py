"""Cotizaciones del dolar argentino en tiempo real via dolarapi.com."""
import requests
import streamlit as st

NOMBRES_DISPLAY = {
    "oficial": "Oficial",
    "blue": "Blue",
    "bolsa": "MEP",
    "contadoconliqui": "CCL",
    "cripto": "Cripto",
    "tarjeta": "Tarjeta",
}

CASAS_ORDEN = ["oficial", "blue", "bolsa", "contadoconliqui", "cripto", "tarjeta"]


@st.cache_data(ttl=300)
def get_cotizaciones():
    """Obtiene todas las cotizaciones desde dolarapi.com. Cache de 5 minutos."""
    try:
        resp = requests.get("https://dolarapi.com/v1/dolares", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def get_cotizacion_by_casa(casa: str):
    """Retorna la cotizacion de una casa especifica o None si no existe."""
    datos = get_cotizaciones()
    if not datos:
        return None
    for item in datos:
        if item.get("casa", "").lower() == casa.lower():
            return item
    return None


def format_cotizacion(valor: float) -> str:
    """Formatea como '$1.090' con separador de miles estilo argentino."""
    if valor is None or valor == 0:
        return "—"
    return f"${valor:,.0f}".replace(",", ".")
