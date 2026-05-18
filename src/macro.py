"""Datos macro Argentina: riesgo pais, dolar historico, tasas BCRA."""
import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600)
def get_riesgo_pais():
    """Riesgo pais historico completo desde argentinadatos.com. Cache 1 hora."""
    try:
        r = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais",
            timeout=10,
        )
        r.raise_for_status()
        df = pd.DataFrame(r.json())
        df = df.dropna(subset=["valor"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        return df.sort_values("fecha").reset_index(drop=True)
    except Exception:
        return None


def get_tasas_bcra():
    """Tasas BCRA. API actualmente deprecada — retorna None."""
    return None


@st.cache_data(ttl=3600)
def get_dolar_historico(casa="blue"):
    """Dolar historico completo para una casa desde argentinadatos.com. Cache 1 hora."""
    try:
        r = requests.get(
            f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{casa}",
            timeout=10,
        )
        r.raise_for_status()
        df = pd.DataFrame(r.json())
        df["fecha"] = pd.to_datetime(df["fecha"])
        return df.sort_values("fecha").reset_index(drop=True)
    except Exception:
        return None
