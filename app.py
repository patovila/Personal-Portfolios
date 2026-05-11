"""
Mi Bloomberg Personal - App Web con Streamlit
Version Fase 1.5 - Tema oscuro + Buscador basico
"""
import sys
sys.path.append(".")

import streamlit as st
from src.datos import cargar_ticker, cargar_universo

# Configuracion de la pagina
st.set_page_config(
    page_title="Mi Bloomberg Personal",
    page_icon="📊",
    layout="wide"
)

# Cargar el universo de tickers
universo = cargar_universo()

# Titulo principal
st.title("📊 Mi Bloomberg Personal")
st.caption("Sistema de analisis financiero | Construido con Python + Streamlit")

# Sidebar con buscador
with st.sidebar:
    st.header("🔍 Buscador")
    
    # Listas predefinidas
    todos_tickers = []
    if universo:
        for cat in universo.get("categorias", {}).values():
            todos_tickers.extend(cat)
        todos_tickers = sorted(list(set(todos_tickers)))
    
    # Input del usuario
    ticker = st.text_input(
        "Escribe un ticker:",
        value="YPF",
        placeholder="Ej: YPF, MELI, AAPL"
    ).upper()
    
    # Selector rapido de portfolios
    st.divider()
    st.subheader("📂 Atajos")
    
    if universo and "portfolios" in universo:
        for nombre, tickers in universo["portfolios"].items():
            with st.expander(f"📁 {nombre.capitalize()}"):
                st.write(f"{len(tickers)} tickers")
                st.write(", ".join(tickers))
    
    st.divider()
    st.caption(f"Total tickers en universo: {len(todos_tickers)}")

# CONTENIDO PRINCIPAL
if ticker:
    try:
        # Cargar datos del ticker
        with st.spinner(f"Cargando datos de {ticker}..."):
            datos = cargar_ticker(ticker)
        
        # Mostrar datos
        st.header(f"{datos['nombre']} ({datos['ticker']})")
        st.caption(f"{datos['sector']} | {datos['industria']} | {datos['pais']}")
        
        # Metricas en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            precio = datos.get('precio_actual')
            st.metric(
                "Precio actual",
                f"${precio:.2f}" if precio else "N/A"
            )
        
        with col2:
            mcap = datos.get('market_cap_b', 0)
            st.metric(
                "Market Cap",
                f"${mcap:.2f}B" if mcap else "N/A"
            )
        
        with col3:
            pe = datos.get('pe')
            st.metric(
                "PE Ratio",
                f"{pe:.2f}" if pe else "N/A"
            )
        
        with col4:
            roe = datos.get('roe')
            st.metric(
                "ROE",
                f"{roe*100:.1f}%" if roe else "N/A"
            )
        
        st.divider()
        
        # Detalles adicionales
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("📋 Detalles")
            st.write(f"**Moneda:** {datos.get('moneda', 'N/A')}")
            st.write(f"**Empleados:** {datos.get('empleados', 'N/A'):,}" if datos.get('empleados') else "**Empleados:** N/A")
            min52 = datos.get('min_52w')
            max52 = datos.get('max_52w')
            if min52 and max52:
                st.write(f"**Rango 52 semanas:** ${min52:.2f} - ${max52:.2f}")
            
            pb = datos.get('pb')
            if pb:
                st.write(f"**P/B Ratio:** {pb:.2f}")
        
        with col_b:
            st.subheader("📊 Margen operativo")
            margen = datos.get('margen_op')
            if margen:
                st.metric("Margen operativo", f"{margen*100:.1f}%")
                # Barra de progreso visual del margen
                progress_value = min(max(margen, 0), 1)
                st.progress(progress_value)
                
                if margen > 0.25:
                    st.success("🟢 Margen excelente (>25%)")
                elif margen > 0.15:
                    st.info("🟡 Margen bueno (15-25%)")
                elif margen > 0:
                    st.warning("🟠 Margen ajustado (<15%)")
                else:
                    st.error("🔴 Margen negativo")
            else:
                st.write("Sin datos de margen operativo")
        
        st.divider()
        st.success("✅ Datos cargados correctamente")
        
    except Exception as e:
        st.error(f"❌ Error al cargar {ticker}")
        st.write(f"Detalle: {str(e)}")
        st.info("Verifica que el ticker sea valido. Ejemplos: YPF, MELI, AAPL, PAM, TGS")

else:
    st.info("👈 Escribe un ticker en el buscador de la izquierda")