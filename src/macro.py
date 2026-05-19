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


@st.cache_data(ttl=3600)
def get_tasas_bcra():
    """Tasas de referencia argentinas desde argentinadatos.com. Cache 1 hora.

    Retorna dict con:
      tasa_politica      float  — TNA % (depósitos 30d BCRA, proxy tasa PM)
      tasa_politica_fecha str   — fecha del dato o None si es fallback
      tasa_plazo_fijo    float  — TNA % promedio entidades privadas
      fallback           bool   — True si algún dato es hardcodeado
    """
    resultado = {
        "tasa_politica": None,
        "tasa_politica_fecha": None,
        "tasa_plazo_fijo": None,
        "fallback": False,
    }

    # Tasa de referencia: depósitos a 30 días (serie histórica BCRA via argentinadatos)
    try:
        r = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/tasas/depositos30Dias",
            timeout=10,
        )
        r.raise_for_status()
        con_valor = [d for d in r.json() if d.get("valor") is not None]
        if con_valor:
            ultimo = con_valor[-1]
            resultado["tasa_politica"] = float(ultimo["valor"])
            resultado["tasa_politica_fecha"] = ultimo.get("fecha")
    except Exception:
        pass

    # Tasa plazo fijo: promedio de tnaClientes entre entidades (snapshot actual)
    try:
        r = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/tasas/plazoFijo",
            timeout=10,
        )
        r.raise_for_status()
        tnas = [d["tnaClientes"] for d in r.json() if d.get("tnaClientes")]
        if tnas:
            resultado["tasa_plazo_fijo"] = round(sum(tnas) / len(tnas) * 100, 2)
    except Exception:
        pass

    # Fallback hardcodeado si alguna falló
    if resultado["tasa_politica"] is None:
        resultado["tasa_politica"] = 29.0
        resultado["fallback"] = True
    if resultado["tasa_plazo_fijo"] is None:
        resultado["tasa_plazo_fijo"] = 32.0
        resultado["fallback"] = True

    return resultado


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
