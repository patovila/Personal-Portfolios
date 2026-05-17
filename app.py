"""Mi Bloomberg Personal - FASE 2 completa"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.datos import cargar_ticker, cargar_universo

st.set_page_config(
    page_title="Mi Bloomberg Personal",
    page_icon="📊",
    layout="wide"
)

# ============== ESTILO INVESTING / TRADINGVIEW ==============
st.markdown("""
<style>
/* === IMPORT INTER === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* === TIPOGRAFIA GLOBAL === */
html, body, [class*="css"], .stApp, .main, [data-testid="stSidebar"],
.stMarkdown, p, label, button, input, select, textarea {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    font-feature-settings: "tnum", "cv02", "cv11";
}
[data-testid="stMetricValue"],
[data-testid="stDataFrame"] td {
    font-variant-numeric: tabular-nums;
}

/* === FONDO === */
.stApp { background: #FAFBFC; }
.main .block-container {
    background: #FAFBFC;
    padding-top: 1.5rem;
    max-width: 1400px;
}

/* === HEADER === */
.bloomberg-header {
    background: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    padding: 24px 28px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}
.bloomberg-header .title-block h1 {
    color: #1E40AF;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.15;
}
.bloomberg-header .subtitle {
    color: #6B7280;
    font-size: 14px;
    margin-top: 4px;
    letter-spacing: 0;
}
.live-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #16A34A;
    font-weight: 600;
    font-size: 13px;
    background: #DCFCE7;
    padding: 6px 12px;
    border-radius: 20px;
}
.live-dot {
    width: 8px;
    height: 8px;
    background: #16A34A;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.5; transform: scale(0.85); }
}

/* === METRIC CARDS === */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.15s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-color: #CBD5E1;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #6B7280 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0;
    text-transform: none;
}
[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-bottom: 1px solid #E1E4E8;
    border-radius: 8px 8px 0 0;
    gap: 4px;
    padding: 0 8px;
}
.stTabs [data-baseweb="tab"] {
    color: #6B7280;
    font-weight: 500;
    font-size: 15px;
    padding: 14px 22px;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    text-transform: none !important;
    letter-spacing: 0;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #2563EB !important;
}
.stTabs [aria-selected="true"] {
    color: #2563EB !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #2563EB !important;
    background: transparent !important;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: #F0F2F5;
    border-right: 1px solid #E1E4E8;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #1E40AF !important;
    font-weight: 600;
    font-size: 18px !important;
    letter-spacing: -0.01em;
    margin-bottom: 0.8rem;
    text-transform: none;
    border: none;
}
[data-testid="stSidebar"] h3 {
    color: #374151 !important;
    font-weight: 600;
    font-size: 14px !important;
    margin-top: 1.2rem;
    text-transform: none;
    letter-spacing: 0;
}
[data-testid="stSidebar"] label {
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-transform: none;
    letter-spacing: 0;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E1E4E8 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 6px;
}
[data-testid="stSidebar"] [data-testid="stExpander"]:hover {
    background: #F9FAFB;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #1F2937 !important;
    font-weight: 500;
    text-transform: none;
    letter-spacing: 0;
    font-size: 14px;
}
[data-testid="stSidebar"] hr {
    border-color: #E1E4E8 !important;
}

/* === ENCABEZADOS MAIN === */
.main h1 {
    color: #1E40AF !important;
    font-weight: 700;
    font-size: 28px !important;
    letter-spacing: -0.02em;
    text-transform: none;
}
.main h2 {
    color: #111827 !important;
    font-weight: 600;
    font-size: 22px !important;
    letter-spacing: -0.02em;
    text-transform: none;
}
.main h3, [data-testid="stMarkdownContainer"] h3 {
    color: #374151 !important;
    font-weight: 600;
    font-size: 16px !important;
    margin-top: 1.6rem;
    margin-bottom: 0.8rem;
    text-transform: none;
    border: none;
    letter-spacing: 0;
    padding-bottom: 0;
}

/* === CAPTION === */
[data-testid="stCaptionContainer"],
.main [data-testid="stCaptionContainer"] p {
    color: #6B7280 !important;
    font-size: 13px !important;
    text-transform: none;
    letter-spacing: 0;
}

/* === ALERTAS === */
[data-testid="stAlert"] {
    border-radius: 6px !important;
    padding: 12px 16px !important;
    border-left: 4px solid !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
    box-shadow: none !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    letter-spacing: 0;
}
div[data-baseweb="notification"][kind="positive"],
[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] {
    background: #DCFCE7 !important;
    border-left-color: #16A34A !important;
    color: #166534 !important;
}
div[data-baseweb="notification"][kind="warning"],
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background: #FEF3C7 !important;
    border-left-color: #F59E0B !important;
    color: #92400E !important;
}
div[data-baseweb="notification"][kind="negative"],
[data-testid="stAlert"][data-baseweb="notification"][kind="negative"] {
    background: #FEE2E2 !important;
    border-left-color: #DC2626 !important;
    color: #991B1B !important;
}
div[data-baseweb="notification"][kind="info"],
[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background: #DBEAFE !important;
    border-left-color: #2563EB !important;
    color: #1E40AF !important;
}

/* === DIVIDERS === */
hr {
    border-color: #E1E4E8 !important;
    margin: 1.8rem 0 !important;
}

/* === PROGRESS BAR === */
[data-testid="stProgress"] > div > div {
    background: #E5E7EB !important;
    border-radius: 4px;
    height: 8px;
}
[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #4ADE80 0%, #16A34A 100%) !important;
    border-radius: 4px;
}

/* === DATAFRAMES === */
[data-testid="stDataFrame"] thead th,
[data-testid="stTable"] thead th {
    background: #F3F4F6 !important;
    color: #374151 !important;
    font-weight: 600 !important;
    text-transform: none;
    letter-spacing: 0;
    border-color: #E5E7EB !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even),
[data-testid="stTable"] tbody tr:nth-child(even) {
    background: #FAFBFC !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(odd),
[data-testid="stTable"] tbody tr:nth-child(odd) {
    background: #FFFFFF !important;
}
[data-testid="stDataFrame"] td,
[data-testid="stTable"] td {
    border-color: #E5E7EB !important;
    color: #1F2937 !important;
    padding: 10px 12px;
}

/* === LINKS === */
a, a:visited {
    color: #2563EB !important;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: #F0F2F5;
}
::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}
</style>
""", unsafe_allow_html=True)
# =================================================

universo = cargar_universo()

st.markdown("""
<div class="bloomberg-header">
    <div class="title-block">
        <h1>Mi Bloomberg Personal</h1>
        <div class="subtitle">Sistema de analisis financiero &middot; Educacion Financiera AR</div>
    </div>
    <div class="live-indicator">
        <span class="live-dot"></span>
        <span>LIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("Buscador")
    
    ticker = st.text_input(
        "Escribe un ticker:",
        value="YPF",
        placeholder="Ej: YPF, MELI, AAPL"
    ).upper()
    
    periodo = st.selectbox(
        "Periodo para graficos:",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )
    
    st.divider()
    st.subheader("Atajos")
    
    if universo and "portfolios" in universo:
        for nombre, tickers in universo["portfolios"].items():
            with st.expander(nombre.capitalize()):
                st.write(f"{len(tickers)} tickers")
                st.write(", ".join(tickers))

    st.divider()
    st.subheader("💵 Dólar en vivo")
    try:
        from src.dolar import get_cotizaciones, format_cotizacion
        _cots = get_cotizaciones()
        if _cots is None:
            st.caption("Sin conexión")
        else:
            _por_casa = {item["casa"]: item for item in _cots}
            _casas_sb = [
                ("oficial",        "Oficial", True),
                ("blue",           "Blue",    True),
                ("bolsa",          "MEP",     False),
                ("contadoconliqui","CCL",     False),
                ("tarjeta",        "Tarjeta", False),
            ]
            for _casa, _nombre, _mostrar_compra in _casas_sb:
                _item = _por_casa.get(_casa)
                if not _item:
                    continue
                _compra = _item.get("compra")
                _venta  = _item.get("venta")
                _sb1, _sb2 = st.columns([2, 3])
                with _sb1:
                    st.markdown(
                        f"<span style='color:#6B7280;font-size:12px;'>{_nombre}</span>",
                        unsafe_allow_html=True,
                    )
                with _sb2:
                    if _mostrar_compra and _compra:
                        _precio_txt = f"{format_cotizacion(_compra)} / {format_cotizacion(_venta)}"
                    else:
                        _precio_txt = format_cotizacion(_venta)
                    st.markdown(
                        f"<span style='font-weight:700;font-size:12px;'>{_precio_txt}</span>",
                        unsafe_allow_html=True,
                    )
            # Timestamp
            _ts = next(
                (i["fechaActualizacion"] for i in _cots if i.get("fechaActualizacion")),
                None,
            )
            if _ts:
                try:
                    from datetime import datetime
                    _dt = datetime.fromisoformat(_ts.replace("Z", "+00:00"))
                    st.caption(f"Act: {_dt.strftime('%H:%M')} UTC")
                except Exception:
                    st.caption(f"Act: {_ts[:16]}")
    except Exception:
        st.caption("Sin conexión")

# CONTENIDO PRINCIPAL
# Cargamos el ticker del sidebar pero NO abortamos si falla:
# el tab Mi Portfolio funciona aunque el ticker sea invalido.
datos = None
ticker_error = None
if not ticker:
    ticker_error = "Escribe un ticker en el buscador para ver Ficha/Fundamental/Tecnico"
else:
    try:
        with st.spinner(f"Cargando datos de {ticker}..."):
            datos = cargar_ticker(ticker)
    except Exception as e:
        ticker_error = f"Error al cargar {ticker}: {e}"

if datos:
    st.header(f"{datos['nombre']} ({datos['ticker']})")
    st.caption(f"{datos['sector']} | {datos['industria']} | {datos['pais']}")
else:
    st.header("Mi Bloomberg Personal")
    st.caption(ticker_error or "")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏢 Ficha",
    "📊 Fundamental",
    "📈 Tecnico",
    "🗂️ Mi Portfolio",
    "🧮 Calculadoras",
])

# TAB 1: FICHA
with tab1:
    if not datos:
        st.info(f"👈 {ticker_error}")
    else:
        col1, col2, col3, col4 = st.columns(4)

        precio = datos.get('precio_actual')
        col1.metric("Precio", f"${precio:.2f}" if precio else "N/A")

        mcap = datos.get('market_cap_b', 0)
        col2.metric("Mkt Cap", f"${mcap:.1f}B" if mcap else "N/A")

        pe = datos.get('pe')
        col3.metric("PE", f"{pe:.1f}" if pe else "N/A")

        roe = datos.get('roe')
        col4.metric("ROE", f"{roe*100:.1f}%" if roe else "N/A")

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("📋 Detalles")
            st.write(f"**Moneda:** {datos.get('moneda', 'N/A')}")

            empleados = datos.get('empleados')
            if empleados:
                st.write(f"**Empleados:** {empleados:,}")

            min52 = datos.get('min_52w')
            max52 = datos.get('max_52w')
            if min52 and max52:
                st.write(f"**Rango 52w:** ${min52:.2f} - ${max52:.2f}")

            pb = datos.get('pb')
            if pb:
                st.write(f"**P/B Ratio:** {pb:.2f}")

        with col_b:
            st.subheader("📊 Margen operativo")
            margen = datos.get('margen_op')
            if margen:
                st.metric("Margen", f"{margen*100:.1f}%")
                st.progress(min(max(margen, 0), 1))

                if margen > 0.25:
                    st.success("🟢 Excelente (>25%)")
                elif margen > 0.15:
                    st.info("🟡 Bueno (15-25%)")
                elif margen > 0:
                    st.warning("🟠 Ajustado (<15%)")
                else:
                    st.error("🔴 Negativo")
            else:
                st.write("Sin datos")

# TAB 2: FUNDAMENTAL
with tab2:
    if not datos:
        st.info(f"👈 {ticker_error}")
    else:
        st.subheader(f"📊 Analisis Fundamental - {ticker}")

        try:
            from src.fundamentals import ratios_avanzados
            ratios = ratios_avanzados(ticker)

            st.markdown("### 💰 Valuacion")
            c1, c2, c3, c4 = st.columns(4)

            pe_t = ratios.get('PE_trailing')
            c1.metric("PE Trailing", f"{pe_t:.2f}" if pe_t else "N/A")

            pe_f = ratios.get('PE_forward')
            c2.metric("PE Forward", f"{pe_f:.2f}" if pe_f else "N/A")

            pb = ratios.get('PB')
            c3.metric("P/B", f"{pb:.2f}" if pb else "N/A")

            ev = ratios.get('EV_EBITDA')
            c4.metric("EV/EBITDA", f"{ev:.2f}" if ev else "N/A")

            c5, c6, c7, c8 = st.columns(4)

            ps = ratios.get('PS')
            c5.metric("P/S", f"{ps:.2f}" if ps else "N/A")

            peg = ratios.get('PEG')
            c6.metric("PEG", f"{peg:.2f}" if peg else "N/A")

            evr = ratios.get('EV_Revenue')
            c7.metric("EV/Revenue", f"{evr:.2f}" if evr else "N/A")

            dy = ratios.get('Dividend_Yield_%')
            c8.metric("Div Yield", f"{dy:.2f}%" if dy else "N/A")

            st.divider()

            st.markdown("### 📈 Rentabilidad")
            r1, r2, r3, r4, r5 = st.columns(5)

            roe_val = ratios.get('ROE_%')
            r1.metric("ROE", f"{roe_val:.1f}%" if roe_val else "N/A")

            roa_val = ratios.get('ROA_%')
            r2.metric("ROA", f"{roa_val:.1f}%" if roa_val else "N/A")

            mb = ratios.get('Margen_Bruto_%')
            r3.metric("Mg Bruto", f"{mb:.1f}%" if mb else "N/A")

            mo = ratios.get('Margen_Operativo_%')
            r4.metric("Mg Operativo", f"{mo:.1f}%" if mo else "N/A")

            mn = ratios.get('Margen_Neto_%')
            r5.metric("Mg Neto", f"{mn:.1f}%" if mn else "N/A")

            st.divider()

            st.markdown("### 🏛️ Solvencia")
            s1, s2, s3, s4 = st.columns(4)

            de = ratios.get('Debt_Equity')
            s1.metric("Debt/Equity", f"{de:.2f}" if de else "N/A")

            cr = ratios.get('Current_Ratio')
            s2.metric("Current Ratio", f"{cr:.2f}" if cr else "N/A")

            qr = ratios.get('Quick_Ratio')
            s3.metric("Quick Ratio", f"{qr:.2f}" if qr else "N/A")

            beta = ratios.get('Beta')
            s4.metric("Beta", f"{beta:.2f}" if beta else "N/A")

        except Exception as e:
            st.error(f"❌ Error cargando fundamentals: {e}")

# TAB 3: TECNICO
with tab3:
    if not datos:
        st.info(f"👈 {ticker_error}")
    else:
        st.subheader(f"📈 Analisis Tecnico - {ticker}")

        try:
            import yfinance as yf
            import plotly.graph_objects as go
            from src.tecnico import rsi, macd, bollinger

            with st.spinner(f"Cargando precios de {ticker}..."):
                hist = yf.Ticker(ticker).history(period=periodo)

            if hist.empty:
                st.error("Sin datos de precio")
            else:
                close = hist['Close']

                st.markdown("### 📊 Señales actuales")

                rsi_serie = rsi(close)
                rsi_actual = rsi_serie.iloc[-1]

                macd_df = macd(close)
                macd_actual = macd_df['MACD'].iloc[-1]
                senal_actual = macd_df['Senal'].iloc[-1]

                boll_df = bollinger(close)
                precio = close.iloc[-1]
                banda_sup = boll_df['Banda_Superior'].iloc[-1]
                banda_inf = boll_df['Banda_Inferior'].iloc[-1]

                posicion_banda = ((precio - banda_inf) / (banda_sup - banda_inf)) * 100

                t1, t2, t3, t4 = st.columns(4)
                t1.metric("Precio", f"${precio:.2f}")
                t2.metric("RSI(14)", f"{rsi_actual:.1f}")
                t3.metric("MACD", f"{macd_actual:.3f}")
                t4.metric("Pos. banda", f"{posicion_banda:.1f}%")

                col_i1, col_i2 = st.columns(2)

                with col_i1:
                    st.markdown("**RSI:**")
                    if rsi_actual > 70:
                        st.warning(f"🟠 Sobrecompra ({rsi_actual:.1f})")
                    elif rsi_actual < 30:
                        st.success(f"🟢 Sobreventa ({rsi_actual:.1f})")
                    else:
                        st.info(f"🟡 Zona neutral ({rsi_actual:.1f})")

                with col_i2:
                    st.markdown("**MACD:**")
                    if macd_actual > senal_actual:
                        st.success(f"🟢 Alcista (MACD>Senal)")
                    else:
                        st.warning(f"🟠 Bajista (MACD<Senal)")

                st.divider()

                st.markdown("### 📈 Precio con Bandas de Bollinger")

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=hist.index, y=boll_df['Banda_Superior'],
                    line=dict(color='rgba(239, 85, 59, 0.5)', dash='dash'),
                    name='Banda Sup'
                ))

                fig.add_trace(go.Scatter(
                    x=hist.index, y=boll_df['Banda_Inferior'],
                    line=dict(color='rgba(0, 204, 150, 0.5)', dash='dash'),
                    name='Banda Inf',
                    fill='tonexty',
                    fillcolor='rgba(100, 100, 100, 0.1)'
                ))

                fig.add_trace(go.Scatter(
                    x=hist.index, y=boll_df['Media'],
                    line=dict(color='orange', width=1),
                    name='Media 20'
                ))

                fig.add_trace(go.Scatter(
                    x=hist.index, y=close,
                    line=dict(color='#00CC96', width=2),
                    name='Precio'
                ))

                fig.update_layout(
                    template='plotly_dark',
                    height=500,
                    hovermode='x unified',
                    xaxis_title='Fecha',
                    yaxis_title='Precio'
                )

                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📊 RSI (14)")

                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=hist.index, y=rsi_serie,
                    line=dict(color='#FFA15A', width=2),
                    name='RSI'
                ))
                fig_rsi.add_hline(y=70, line_dash='dash', line_color='red')
                fig_rsi.add_hline(y=30, line_dash='dash', line_color='green')
                fig_rsi.update_layout(
                    template='plotly_dark',
                    height=300,
                    yaxis_range=[0, 100]
                )
                st.plotly_chart(fig_rsi, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error en analisis tecnico: {e}")

# TAB 4: MI PORTFOLIO
with tab4:
    import pandas as pd
    import plotly.graph_objects as go
    from src.portfolio import (
        cargar_portfolio,
        actualizar_precios_actuales,
        calcular_metricas_posicion,
        calcular_metricas_portfolio,
        calcular_composicion_por_sector,
        calcular_composicion_por_tipo,
        comparar_vs_benchmark,
        guardar_portfolio,
        agregar_posicion,
        agregar_cantidad_a_posicion,
        eliminar_posicion,
        editar_posicion,
    )

    PALETA_INVESTING = [
        "#16A34A", "#2563EB", "#F59E0B", "#8B5CF6",
        "#EC4899", "#06B6D4", "#84CC16", "#F97316",
    ]

    # --- Carga del portfolio ---
    try:
        portfolio = cargar_portfolio("pato")
    except FileNotFoundError:
        st.warning(
            "📁 No se encontro un portfolio en `data/portfolio/pato.json`. "
            "Cargá primero un portfolio para usar esta seccion."
        )
        portfolio = None
    except Exception as e:
        st.error(f"❌ Error cargando el portfolio: {e}")
        portfolio = None

    if portfolio:
        config = portfolio.get("configuracion", {})
        tipo_cambio = config.get("tipo_cambio_ars_usd", 1)

        # --- Header: toggle moneda + boton actualizar ---
        header_l, header_r = st.columns([3, 1])
        with header_l:
            moneda = st.radio(
                "Moneda de visualizacion",
                ["ARS", "USD"],
                horizontal=True,
                key="portfolio_moneda",
            )
        with header_r:
            st.write("")  # espaciador
            if st.button("🔄 Actualizar precios", use_container_width=True):
                actualizar_precios_actuales.clear()
                st.rerun()

        # --- Actualizar precios desde yfinance (con cache) ---
        with st.spinner("Refrescando precios..."):
            try:
                portfolio_live = actualizar_precios_actuales(portfolio)
            except Exception as e:
                st.warning(f"No se pudo refrescar precios desde yfinance: {e}")
                portfolio_live = portfolio

        def _fmt_money(valor_ars: float, moneda_ui: str) -> str:
            """Formatea un monto en ARS o USD segun el toggle."""
            if moneda_ui == "USD":
                return f"US$ {valor_ars / tipo_cambio:,.2f}"
            return f"$ {valor_ars:,.0f}"

        from datetime import datetime
        ahora = datetime.now()
        st.caption(f"🕐 Ultima actualizacion: {ahora.strftime('%H:%M:%S')} - {ahora.strftime('%d/%m/%Y')}")

        psub1, psub2 = st.tabs(["📊 Resumen", "✏️ Gestionar Portfolio"])

        # ── SUB-TAB 1: RESUMEN (contenido existente sin cambios) ──────────────
        with psub1:
            # ========== C1: RESUMEN EJECUTIVO ==========
            st.markdown("### 📊 Resumen ejecutivo")
            try:
                m = calcular_metricas_portfolio(portfolio_live)

                k1, k2, k3, k4 = st.columns(4)
                k1.metric(
                    f"Valor total ({moneda})",
                    _fmt_money(m["valor_total_ars"], moneda),
                )
                pnl_str = _fmt_money(m["pnl_total_ars"], moneda)
                k2.metric(
                    "P&L total",
                    pnl_str,
                    delta=f"{m['pnl_total_pct']*100:+.2f}%",
                )
                k3.metric(
                    "Retorno",
                    f"{m['pnl_total_pct']*100:+.2f}%",
                    delta=f"{m['pnl_total_pct']*100:+.2f}%",
                    delta_color="normal",
                )
                k4.metric("# Posiciones", f"{m['num_posiciones']}")

                k5, k6, k7, k8 = st.columns(4)
                k5.metric("Beta ponderada", f"{m['beta_ponderada']:.2f}")

                top = m["top_performer"] or {}
                k6.metric(
                    "Top performer",
                    top.get("ticker", "—"),
                    delta=f"{top.get('pnl_pct',0)*100:+.2f}%" if top else None,
                )

                worst = m["worst_performer"] or {}
                k7.metric(
                    "Worst performer",
                    worst.get("ticker", "—"),
                    delta=f"{worst.get('pnl_pct',0)*100:+.2f}%" if worst else None,
                )

                mayor = m["mayor_posicion"] or {}
                peso_mayor = (
                    mayor.get("valor_ars", 0) / m["valor_total_ars"] * 100
                    if m["valor_total_ars"] else 0
                )
                k8.metric(
                    "Mayor posicion",
                    mayor.get("ticker", "—"),
                    delta=f"{peso_mayor:.1f}% del total" if mayor else None,
                    delta_color="off",
                )
            except Exception as e:
                st.error(f"Error calculando metricas globales: {e}")

            st.divider()

            # ========== C2: POSICIONES DETALLE ==========
            st.markdown("### 📋 Posiciones")
            try:
                filas = []
                for pos in portfolio_live.get("posiciones", []):
                    mp = calcular_metricas_posicion(pos, tipo_cambio)
                    valor_total = m["valor_total_ars"] if m["valor_total_ars"] else 1
                    peso = mp["valor_actual_ars"] / valor_total * 100

                    if moneda == "USD":
                        costo = mp["costo_total_usd"]
                        valor = mp["valor_actual_usd"]
                        pnl = mp["pnl_usd"]
                    else:
                        costo = mp["costo_total_ars"]
                        valor = mp["valor_actual_ars"]
                        pnl = mp["pnl_ars"]

                    filas.append({
                        "Activo": pos.get("activo", ""),
                        "Ticker": pos.get("ticker", ""),
                        "Tipo": pos.get("tipo", ""),
                        "Cantidad": pos.get("cantidad", 0),
                        f"Costo ({moneda})": costo,
                        f"Valor ({moneda})": valor,
                        f"P&L ({moneda})": pnl,
                        "P&L %": mp["pnl_pct"] * 100,
                        "Peso %": peso,
                        "Senal": pos.get("senal", ""),
                    })

                df = pd.DataFrame(filas)

                def _color_pnl(val):
                    if isinstance(val, (int, float)):
                        if val > 0:
                            return "background-color: #DCFCE7; color: #166534;"
                        if val < 0:
                            return "background-color: #FEE2E2; color: #991B1B;"
                    return ""

                styled = (
                    df.style
                    .map(_color_pnl, subset=["P&L %", f"P&L ({moneda})"])
                    .format({
                        f"Costo ({moneda})": "{:,.2f}",
                        f"Valor ({moneda})": "{:,.2f}",
                        f"P&L ({moneda})": "{:,.2f}",
                        "P&L %": "{:+.2f}%",
                        "Peso %": "{:.1f}%",
                        "Cantidad": "{:,.0f}",
                    })
                )
                st.dataframe(styled, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Error armando la tabla de posiciones: {e}")

            st.divider()

            # ========== C3: COMPOSICION ==========
            st.markdown("### 📈 Composicion")
            comp_l, comp_r = st.columns(2)

            def _donut(titulo, datos_comp):
                labels = list(datos_comp.keys())
                valores = [v["valor_ars"] for v in datos_comp.values()]
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=valores,
                    hole=0.55,
                    marker=dict(colors=PALETA_INVESTING[:len(labels)]),
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
                )])
                fig.update_layout(
                    title=titulo,
                    template="plotly_white",
                    height=380,
                    showlegend=True,
                    legend=dict(orientation="v", x=1.05, y=0.5),
                    margin=dict(l=20, r=20, t=50, b=20),
                )
                return fig

            with comp_l:
                try:
                    sectores = calcular_composicion_por_sector(portfolio_live)
                    st.plotly_chart(_donut("Por sector", sectores), use_container_width=True)
                except Exception as e:
                    st.error(f"Error composicion por sector: {e}")

            with comp_r:
                try:
                    tipos = calcular_composicion_por_tipo(portfolio_live)
                    st.plotly_chart(_donut("Por tipo de activo", tipos), use_container_width=True)
                except Exception as e:
                    st.error(f"Error composicion por tipo: {e}")

            st.divider()

            # ========== C4: PERFORMANCE vs BENCHMARK ==========
            st.markdown("### 📉 Performance vs Benchmark")
            bench_l, bench_r = st.columns(2)
            with bench_l:
                periodo_bench = st.selectbox(
                    "Periodo",
                    ["1mo", "3mo", "6mo", "1y"],
                    index=2,
                    key="portfolio_periodo_bench",
                )
            with bench_r:
                benchmark_sel = st.selectbox(
                    "Benchmark",
                    ["SPY", "QQQ", "^MERV"],
                    index=0,
                    key="portfolio_benchmark",
                )

            try:
                with st.spinner("Descargando series historicas..."):
                    comp = comparar_vs_benchmark(portfolio_live, benchmark_sel, periodo_bench)

                if "error" in comp:
                    st.warning(f"⚠ {comp['error']}")
                else:
                    fig_b = go.Figure()
                    fig_b.add_trace(go.Scatter(
                        x=comp["fechas"], y=comp["portfolio"],
                        line=dict(color="#16A34A", width=2.5),
                        name="Mi Portfolio",
                    ))
                    fig_b.add_trace(go.Scatter(
                        x=comp["fechas"], y=comp["benchmark"],
                        line=dict(color="#6B7280", width=2, dash="dash"),
                        name=comp["ticker_benchmark"],
                    ))
                    fig_b.update_layout(
                        template="plotly_white",
                        height=420,
                        hovermode="x unified",
                        xaxis_title="Fecha",
                        yaxis_title="Indice (base 100)",
                        margin=dict(l=20, r=20, t=30, b=20),
                    )
                    st.plotly_chart(fig_b, use_container_width=True)

                    rb1, rb2, rb3 = st.columns(3)
                    rb1.metric("Retorno portfolio", f"{comp['retorno_portfolio_pct']:+.2f}%")
                    rb2.metric(
                        f"Retorno {benchmark_sel}",
                        f"{comp['retorno_benchmark_pct']:+.2f}%",
                    )
                    rb3.metric(
                        "Alpha",
                        f"{comp['alpha_pct']:+.2f}%",
                        delta=f"{comp['alpha_pct']:+.2f}%",
                    )
            except Exception as e:
                st.error(f"Error comparando vs benchmark: {e}")

            st.divider()

            # ========== C5: ANALISIS DETALLADO ==========
            st.markdown("### 🎯 Analisis detallado por posicion")
            try:
                for pos in portfolio_live.get("posiciones", []):
                    senal = pos.get("senal", "")
                    # Color del badge segun emoji presente en la senal
                    if "🟢" in senal or "✅" in senal:
                        bg, fg = "#DCFCE7", "#166534"
                    elif "⚠" in senal or "🟠" in senal or "🟡" in senal:
                        bg, fg = "#FEF3C7", "#92400E"
                    elif "🔴" in senal:
                        bg, fg = "#FEE2E2", "#991B1B"
                    else:
                        bg, fg = "#DBEAFE", "#1E40AF"

                    tesis = pos.get("tesis", "—")
                    activo = pos.get("activo", "")
                    ticker_pos = pos.get("ticker", "")

                    st.markdown(
                        f"""
<div style="background:#FFFFFF; border:1px solid #E1E4E8; border-radius:8px;
            padding:14px 18px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
        <div style="font-weight:600; color:#111827; font-size:15px;">
            {activo} <span style="color:#6B7280; font-weight:500;">({ticker_pos})</span>
        </div>
        <div style="background:{bg}; color:{fg}; padding:4px 12px; border-radius:14px;
                    font-size:12px; font-weight:600;">
            {senal or "—"}
        </div>
    </div>
    <div style="color:#374151; font-size:14px; margin-top:6px; line-height:1.45;">
        {tesis}
    </div>
</div>
""",
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"Error en analisis detallado: {e}")

            st.divider()

            # ========== C6: TIPOS DE CAMBIO ==========
            st.markdown("### 💵 Tipos de Cambio")
            try:
                import pandas as pd
                from src.dolar import (
                    get_cotizaciones, format_cotizacion,
                    NOMBRES_DISPLAY, CASAS_ORDEN,
                )

                _dolar_data = get_cotizaciones()

                if _dolar_data is None:
                    st.warning("⚠️ No se pudo conectar con dolarapi.com. Verificá tu conexión a internet.")
                else:
                    _d_por_casa = {item["casa"]: item for item in _dolar_data}

                    # Construir tabla
                    _filas = []
                    for _casa in CASAS_ORDEN:
                        _it = _d_por_casa.get(_casa)
                        if not _it:
                            continue
                        _compra = _it.get("compra") or 0
                        _venta  = _it.get("venta") or 0
                        _spread = _venta - _compra if _compra and _venta else 0
                        _spread_pct = (_spread / _compra * 100) if _compra else 0
                        _filas.append({
                            "Tipo":     NOMBRES_DISPLAY.get(_casa, _casa.capitalize()),
                            "Compra":   _compra,
                            "Venta":    _venta,
                            "Spread":   _spread,
                            "Spread %": _spread_pct,
                            "_casa":    _casa,
                        })

                    _df_d = pd.DataFrame(_filas)
                    _blue_idx = next(
                        (i for i, f in enumerate(_filas) if f["_casa"] == "blue"), None
                    )

                    def _hl_blue(row):
                        if row.name == _blue_idx and _filas[row.name]["Spread %"] > 2:
                            return ["background-color: #FEF3C7;"] * len(row)
                        return [""] * len(row)

                    _df_display = _df_d.drop(columns=["_casa"])
                    _styled_d = (
                        _df_display.style
                        .apply(_hl_blue, axis=1)
                        .format({
                            "Compra":   lambda v: format_cotizacion(v) if v else "—",
                            "Venta":    lambda v: format_cotizacion(v) if v else "—",
                            "Spread":   lambda v: format_cotizacion(v) if v else "—",
                            "Spread %": "{:.2f}%",
                        })
                    )
                    st.dataframe(_styled_d, use_container_width=True, hide_index=True)

                    # Métricas comparativas
                    _oficial = _d_por_casa.get("oficial", {})
                    _blue    = _d_por_casa.get("blue", {})
                    _mep     = _d_por_casa.get("bolsa", {})
                    _ccl     = _d_por_casa.get("contadoconliqui", {})

                    _dm1, _dm2 = st.columns(2)

                    _ofic_v = _oficial.get("venta")
                    _blue_v = _blue.get("venta")
                    if _ofic_v and _blue_v:
                        _diff_bo = (_blue_v / _ofic_v - 1) * 100
                        _dm1.metric(
                            "Blue vs Oficial",
                            f"{_diff_bo:+.1f}%",
                            delta=f"Blue {format_cotizacion(_blue_v)} | Ofic {format_cotizacion(_ofic_v)}",
                            delta_color="off",
                            help="Brecha entre el dolar blue y el oficial. Refleja la restriccion cambiaria.",
                        )

                    _mep_v = _mep.get("venta")
                    _ccl_v = _ccl.get("venta")
                    if _mep_v and _ccl_v:
                        _diff_cm = (_ccl_v / _mep_v - 1) * 100
                        _dm2.metric(
                            "CCL vs MEP",
                            f"{_diff_cm:+.1f}%",
                            delta=f"CCL {format_cotizacion(_ccl_v)} | MEP {format_cotizacion(_mep_v)}",
                            delta_color="off",
                            help="Diferencia entre CCL y MEP. Cuando divergen puede haber oportunidad de arbitraje.",
                        )

                    # Timestamp API
                    _ts_d = next(
                        (i["fechaActualizacion"] for i in _dolar_data if i.get("fechaActualizacion")),
                        None,
                    )
                    if _ts_d:
                        try:
                            from datetime import datetime
                            _dt_d = datetime.fromisoformat(_ts_d.replace("Z", "+00:00"))
                            st.caption(f"Fuente: dolarapi.com · Ultima actualizacion: {_dt_d.strftime('%d/%m/%Y %H:%M')} UTC · Cache: 5 min")
                        except Exception:
                            st.caption(f"Fuente: dolarapi.com · Actualizacion: {_ts_d[:16]}")

            except Exception as _e_dolar:
                st.warning(f"No se pudo cargar tipos de cambio: {_e_dolar}")

        # ── SUB-TAB 2: GESTIONAR PORTFOLIO ───────────────────────────────────
        with psub2:
            import json as _json
            from datetime import date as _date

            _pos_list = portfolio.get("posiciones", [])

            # ── SECCIÓN 1: TABLA + ELIMINAR ──────────────────────────────────
            st.markdown("#### 📋 Posiciones actuales")

            if not _pos_list:
                st.info("No hay posiciones en el portfolio.")
            else:
                _hc1, _hc2, _hc3, _hc4, _hc5 = st.columns([2, 1, 2, 2, 1])
                _hc1.markdown("**Ticker**")
                _hc2.markdown("**Cantidad**")
                _hc3.markdown("**Precio compra (ARS)**")
                _hc4.markdown("**Fecha compra**")
                _hc5.markdown("**Accion**")

                for _gi, _gpos in enumerate(_pos_list):
                    _gc1, _gc2, _gc3, _gc4, _gc5 = st.columns([2, 1, 2, 2, 1])
                    _gc1.write(f"**{_gpos.get('ticker', '')}**")
                    _gc2.write(f"{_gpos.get('cantidad', 0):,}")
                    _gc3.write(f"$ {_gpos.get('precio_promedio_compra_ars', 0):,.0f}")
                    _gc4.write(_gpos.get("fecha_primera_compra", "—"))
                    if _gc5.button(
                        "🗑️", key=f"del_btn_{_gi}",
                        help=f"Eliminar {_gpos.get('ticker', '')}",
                    ):
                        st.session_state["pending_delete"] = _gpos.get("ticker", "")

            # Confirmacion de eliminacion (fuera del loop para evitar re-renders)
            if "pending_delete" in st.session_state:
                _del_tk = st.session_state["pending_delete"]
                st.warning(
                    f"⚠️ ¿Confirmas eliminar **{_del_tk}** del portfolio? "
                    "Esta accion no se puede deshacer."
                )
                _dc1, _dc2 = st.columns(2)
                if _dc1.button("✅ Sí, eliminar", key="confirm_del"):
                    _mut = _json.loads(_json.dumps(portfolio))
                    eliminar_posicion(_mut, _del_tk)
                    guardar_portfolio("pato", _mut)
                    del st.session_state["pending_delete"]
                    st.success(f"✅ {_del_tk} eliminado del portfolio.")
                    st.rerun()
                if _dc2.button("❌ Cancelar", key="cancel_del"):
                    del st.session_state["pending_delete"]
                    st.rerun()

            st.divider()

            # ── SECCIÓN 2: AGREGAR NUEVA POSICIÓN ────────────────────────────
            st.markdown("#### ➕ Agregar nueva posición")
            _ag_c1, _ag_c2 = st.columns(2)
            with _ag_c1:
                _ag_ticker = st.text_input(
                    "Ticker", value="", placeholder="Ej: AAPL, MELI, TGNO4.BA",
                    key="ag_ticker",
                ).upper().strip()
                _ag_cantidad = st.number_input(
                    "Cantidad", min_value=1, value=1, step=1, key="ag_cantidad",
                )
            with _ag_c2:
                _ag_precio = st.number_input(
                    "Precio de compra (ARS)", min_value=0.0, value=0.0,
                    step=100.0, format="%.0f", key="ag_precio",
                )
                _ag_fecha = st.date_input(
                    "Fecha de compra", value=_date.today(), key="ag_fecha",
                )

            if st.button("➕ Agregar posición", key="btn_agregar", use_container_width=True):
                if not _ag_ticker:
                    st.error("❌ El ticker no puede estar vacío.")
                elif _ag_cantidad <= 0:
                    st.error("❌ La cantidad debe ser mayor a 0.")
                elif _ag_precio <= 0:
                    st.error("❌ El precio de compra debe ser mayor a 0.")
                else:
                    _mut = _json.loads(_json.dumps(portfolio))
                    _res = agregar_posicion(
                        _mut, _ag_ticker, _ag_cantidad,
                        _ag_precio, _ag_fecha.isoformat(),
                    )
                    if _res["accion"] == "existente":
                        _pe = _res["posicion_existente"]
                        st.session_state["agregar_duplicado"] = {
                            "ticker": _ag_ticker,
                            "cantidad_nueva": _ag_cantidad,
                            "cantidad_existente": _pe.get("cantidad", 0),
                        }
                    else:
                        guardar_portfolio("pato", _mut)
                        st.success(
                            f"✅ {_ag_ticker} agregado con {int(_ag_cantidad):,} unidades "
                            f"a $ {_ag_precio:,.0f}."
                        )
                        st.rerun()

            # Manejo de ticker duplicado
            if "agregar_duplicado" in st.session_state:
                _dup = st.session_state["agregar_duplicado"]
                st.warning(
                    f"⚠️ Ya tenés **{_dup['cantidad_existente']:,} acciones** de "
                    f"**{_dup['ticker']}**. "
                    f"¿Querés agregar {int(_dup['cantidad_nueva']):,} más?"
                )
                _dup_c1, _dup_c2 = st.columns(2)
                if _dup_c1.button("✅ Sí, agregar más", key="dup_confirmar"):
                    _mut = _json.loads(_json.dumps(portfolio))
                    agregar_cantidad_a_posicion(_mut, _dup["ticker"], _dup["cantidad_nueva"])
                    guardar_portfolio("pato", _mut)
                    _total = int(_dup["cantidad_existente"] + _dup["cantidad_nueva"])
                    del st.session_state["agregar_duplicado"]
                    st.success(
                        f"✅ {int(_dup['cantidad_nueva']):,} unidades sumadas a "
                        f"{_dup['ticker']}. Total ahora: {_total:,}."
                    )
                    st.rerun()
                if _dup_c2.button("❌ Cancelar", key="dup_cancelar"):
                    del st.session_state["agregar_duplicado"]
                    st.rerun()

            st.divider()

            # ── SECCIÓN 3: EDITAR POSICIÓN EXISTENTE ─────────────────────────
            st.markdown("#### ✏️ Editar posición existente")
            _tickers_ed = [p.get("ticker", "") for p in _pos_list if p.get("ticker")]

            if not _tickers_ed:
                st.info("No hay posiciones para editar.")
            else:
                _ed_ticker = st.selectbox(
                    "Seleccioná la posición a editar", _tickers_ed, key="ed_ticker",
                )
                _pos_sel = next(
                    (p for p in _pos_list if p.get("ticker") == _ed_ticker), None,
                )
                if _pos_sel:
                    _ed_c1, _ed_c2 = st.columns(2)
                    with _ed_c1:
                        _ed_cantidad = st.number_input(
                            "Cantidad",
                            min_value=1,
                            value=max(1, int(_pos_sel.get("cantidad", 1))),
                            step=1,
                            key="ed_cantidad",
                        )
                        _ed_precio = st.number_input(
                            "Precio promedio compra (ARS)",
                            min_value=0.0,
                            value=float(_pos_sel.get("precio_promedio_compra_ars", 0)),
                            step=100.0,
                            format="%.0f",
                            key="ed_precio",
                        )
                    with _ed_c2:
                        _fecha_str = _pos_sel.get(
                            "fecha_primera_compra", _date.today().isoformat()
                        )
                        try:
                            _fecha_dt = _date.fromisoformat(_fecha_str)
                        except Exception:
                            _fecha_dt = _date.today()
                        _ed_fecha = st.date_input(
                            "Fecha de compra", value=_fecha_dt, key="ed_fecha",
                        )
                        st.caption(
                            f"Activo: {_pos_sel.get('activo', '—')} · "
                            f"Tipo: {_pos_sel.get('tipo', '—')} · "
                            f"Sector: {_pos_sel.get('sector', '—')}"
                        )

                    if st.button(
                        "💾 Guardar cambios", key="btn_editar", use_container_width=True,
                    ):
                        _mut = _json.loads(_json.dumps(portfolio))
                        editar_posicion(_mut, _ed_ticker, {
                            "cantidad": _ed_cantidad,
                            "precio_promedio_compra_ars": _ed_precio,
                            "fecha_primera_compra": _ed_fecha.isoformat(),
                        })
                        guardar_portfolio("pato", _mut)
                        st.success(
                            f"✅ {_ed_ticker} actualizado: "
                            f"{int(_ed_cantidad):,} unidades a $ {_ed_precio:,.0f}."
                        )
                        st.rerun()

# TAB 5: CALCULADORAS
with tab5:
    import plotly.graph_objects as go
    from src.calculadoras import (
        calc_billetera, calc_plazo_fijo, calc_fci, calc_bono,
        comparar_todas, evolucion_diaria,
    )

    csub1, csub2, csub3, csub4 = st.tabs([
        "💵 Billetera Virtual",
        "📅 Plazo Fijo / FCI",
        "📊 Bono / TIR",
        "⚖️ Comparador",
    ])

    # ── SUB-TAB 1: BILLETERA VIRTUAL ──────────────────────────────────────────
    with csub1:
        st.info(
            "💡 Las billeteras virtuales pagan intereses **todos los dias** sobre tu saldo "
            "(capitalizacion diaria). Esto significa que cada dia ganas intereses sobre los "
            "intereses del dia anterior — el efecto del interes compuesto."
        )

        bv_c1, bv_c2 = st.columns(2)
        with bv_c1:
            bv_monto = st.number_input(
                "Monto inicial (ARS)", min_value=1_000.0, value=100_000.0,
                step=1_000.0, format="%.0f", key="bv_monto",
            )
            bv_tna = st.number_input(
                "TNA %", min_value=0.0, max_value=200.0, value=32.0,
                step=0.5, key="bv_tna",
            )
        with bv_c2:
            bv_dias = st.number_input(
                "Dias a invertir", min_value=1, max_value=365, value=30,
                step=1, key="bv_dias",
            )
            bv_inflacion = st.number_input(
                "Inflacion mensual esperada %", min_value=0.0, max_value=20.0,
                value=2.5, step=0.1, key="bv_inflacion",
            )

        res_bv = calc_billetera(bv_monto, bv_tna, int(bv_dias), bv_inflacion)

        st.divider()
        bv_m1, bv_m2, bv_m3, bv_m4 = st.columns(4)
        bv_m1.metric("Monto final", f"$ {res_bv['monto_final']:,.0f}")
        bv_m2.metric("Intereses ganados", f"$ {res_bv['intereses']:,.0f}")
        bv_m3.metric(
            "TEA",
            f"{res_bv['tea_pct']:.2f}%",
            help="Tasa Efectiva Anual: lo que ganas en un año completo con capitalizacion diaria. "
                 "Siempre es MAYOR que la TNA porque incluye el efecto del interes compuesto.",
        )
        bv_rr = res_bv["rendimiento_real_pct"]
        bv_m4.metric(
            "Rendimiento real",
            f"{bv_rr:+.2f}%",
            delta=f"{bv_rr:+.2f}%",
            delta_color="normal" if bv_rr >= 0 else "inverse",
            help="Tu ganancia despues de descontar la inflacion estimada del periodo. "
                 "Si es negativo, perdiste poder adquisitivo aunque el saldo en ARS aumento.",
        )

        st.caption(
            f"TNA {bv_tna}% → TEA equivalente: **{res_bv['tea_pct']:.2f}%** | "
            f"Inflacion estimada del periodo: {res_bv['inflacion_periodo_pct']:.2f}%"
        )

        st.markdown("#### Evolucion dia a dia del saldo")
        ev_bv = evolucion_diaria(bv_monto, bv_tna, int(bv_dias), tipo="diaria")
        fig_bv = go.Figure()
        fig_bv.add_trace(go.Scatter(
            x=ev_bv["dia"], y=ev_bv["monto"],
            line=dict(color="#16A34A", width=2.5),
            fill="tozeroy", fillcolor="rgba(22,163,74,0.08)",
            name="Saldo",
            hovertemplate="Dia %{x}: $ %{y:,.0f}<extra></extra>",
        ))
        fig_bv.add_hline(
            y=bv_monto, line_dash="dash", line_color="#6B7280",
            annotation_text="Monto inicial", annotation_position="bottom right",
        )
        fig_bv.update_layout(
            template="plotly_white", height=320,
            xaxis_title="Dias", yaxis_title="Saldo (ARS)",
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_bv, use_container_width=True)

    # ── SUB-TAB 2: PLAZO FIJO / FCI ───────────────────────────────────────────
    with csub2:
        pf_tipo = st.radio(
            "Tipo de instrumento",
            ["Plazo Fijo", "FCI Money Market"],
            horizontal=True,
            key="pf_tipo",
        )

        if pf_tipo == "Plazo Fijo":
            st.info(
                "📅 El plazo fijo paga **al vencimiento**. No podes retirar antes sin penalidad. "
                "La tasa es fija y garantizada por el banco. Capitalizacion simple (no diaria)."
            )
        else:
            st.info(
                "📊 **Fondos Money Market**: capitalizan diario como una billetera virtual pero con "
                "tasas tipicamente mas altas. Podes retirar cuando quieras (liquidez inmediata o 24hs). "
                "Ideal para capital de trabajo."
            )

        pf_c1, pf_c2 = st.columns(2)
        with pf_c1:
            pf_monto = st.number_input(
                "Monto inicial (ARS)", min_value=1_000.0, value=100_000.0,
                step=1_000.0, format="%.0f", key="pf_monto",
            )
            pf_tna = st.number_input(
                "TNA %", min_value=0.0, max_value=200.0, value=38.0,
                step=0.5, key="pf_tna",
            )
        with pf_c2:
            pf_dias = st.selectbox(
                "Plazo (dias)", [30, 60, 90, 180, 365], index=0, key="pf_dias",
            )
            pf_inflacion = st.number_input(
                "Inflacion mensual esperada %", min_value=0.0, max_value=20.0,
                value=2.5, step=0.1, key="pf_inflacion",
            )

        if pf_tipo == "Plazo Fijo":
            res_sel = calc_plazo_fijo(pf_monto, pf_tna, pf_dias, pf_inflacion)
            res_alt = calc_fci(pf_monto, pf_tna, pf_dias, pf_inflacion)
            nombre_sel, nombre_alt = "Plazo Fijo", "FCI (misma TNA)"
            tipo_ev_sel, tipo_ev_alt = "vencimiento", "diaria"
        else:
            res_sel = calc_fci(pf_monto, pf_tna, pf_dias, pf_inflacion)
            res_alt = calc_plazo_fijo(pf_monto, pf_tna, pf_dias, pf_inflacion)
            nombre_sel, nombre_alt = "FCI Money Market", "Plazo Fijo (misma TNA)"
            tipo_ev_sel, tipo_ev_alt = "diaria", "vencimiento"

        diferencia = res_sel["monto_final"] - res_alt["monto_final"]

        st.divider()
        pf_m1, pf_m2, pf_m3, pf_m4 = st.columns(4)
        pf_m1.metric("Monto final", f"$ {res_sel['monto_final']:,.0f}")
        pf_m2.metric("Intereses", f"$ {res_sel['intereses']:,.0f}")
        pf_m3.metric("TEA", f"{res_sel['tea_pct']:.2f}%")
        pf_rr = res_sel["rendimiento_real_pct"]
        pf_m4.metric(
            "Rend. real", f"{pf_rr:+.2f}%",
            delta=f"{pf_rr:+.2f}%",
            delta_color="normal" if pf_rr >= 0 else "inverse",
        )

        if diferencia > 0:
            st.success(
                f"✅ **{nombre_sel}** rinde **$ {diferencia:,.0f} mas** que {nombre_alt} "
                f"en {pf_dias} dias (con la misma TNA). La diferencia es el efecto del interes compuesto."
            )
        elif diferencia < 0:
            st.warning(
                f"⚠️ **{nombre_sel}** rinde **$ {abs(diferencia):,.0f} menos** que {nombre_alt} "
                f"en {pf_dias} dias (con la misma TNA)."
            )

        st.markdown("#### Comparativo: tu eleccion vs la alternativa (misma TNA)")
        ev_sel = evolucion_diaria(pf_monto, pf_tna, pf_dias, tipo=tipo_ev_sel)
        ev_alt = evolucion_diaria(pf_monto, pf_tna, pf_dias, tipo=tipo_ev_alt)

        fig_pf = go.Figure()
        fig_pf.add_trace(go.Scatter(
            x=ev_sel["dia"], y=ev_sel["monto"],
            line=dict(color="#2563EB", width=2.5),
            name=nombre_sel,
            hovertemplate="Dia %{x}: $ %{y:,.0f}<extra></extra>",
        ))
        fig_pf.add_trace(go.Scatter(
            x=ev_alt["dia"], y=ev_alt["monto"],
            line=dict(color="#6B7280", width=2, dash="dash"),
            name=nombre_alt,
            hovertemplate="Dia %{x}: $ %{y:,.0f}<extra></extra>",
        ))
        fig_pf.update_layout(
            template="plotly_white", height=320,
            xaxis_title="Dias", yaxis_title="Saldo (ARS)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_pf, use_container_width=True)

    # ── SUB-TAB 3: BONO / TIR ─────────────────────────────────────────────────
    with csub3:
        st.info(
            "📈 Comprar un bono es **prestarle plata** al Estado o a una empresa. "
            "La **TIR** (Tasa Interna de Retorno) es tu rendimiento anualizado considerando "
            "el precio que pagas hoy y lo que cobras al vencimiento."
        )

        bono_moneda = st.radio("Moneda del bono", ["ARS", "USD"], horizontal=True, key="bono_moneda")

        bono_c1, bono_c2 = st.columns(2)
        with bono_c1:
            bono_precio = st.number_input(
                f"Precio de compra ({bono_moneda})",
                min_value=0.01, value=100.0, step=1.0, format="%.2f",
                key="bono_precio",
            )
            bono_valor = st.number_input(
                f"Valor de cobro al vencimiento ({bono_moneda})",
                min_value=0.01, value=115.0, step=1.0, format="%.2f",
                key="bono_valor",
            )
        with bono_c2:
            bono_dias = st.number_input(
                "Dias hasta vencimiento",
                min_value=1, max_value=3_650, value=365, step=1,
                key="bono_dias",
            )
            st.markdown("")
            st.caption(
                "Pista para bonos argentinos: el precio suele cotizarse cada 100 de VN. "
                "Ejemplo: AL30 a 65 significa que pagas $65 por cada $100 de valor nominal."
            )

        res_bono = calc_bono(bono_precio, bono_valor, int(bono_dias))

        st.divider()
        bn_m1, bn_m2, bn_m3 = st.columns(3)
        bn_m1.metric("Rendimiento total", f"{res_bono['rendimiento_total_pct']:.2f}%")
        bn_m2.metric(
            "TIR anualizada",
            f"{res_bono['tir_anualizada_pct']:.2f}%",
            help="Lo que ganas por año si mantenes el bono hasta el vencimiento. "
                 "Equivalente a la TEA de un plazo fijo.",
        )
        simbolo = "US$" if bono_moneda == "USD" else "$"
        bn_m3.metric("Ganancia absoluta", f"{simbolo} {res_bono['ganancia']:,.2f}")

        st.markdown("#### Diagrama de flujo del bono")
        fig_bono = go.Figure()
        fig_bono.add_trace(go.Scatter(
            x=[0, int(bono_dias)], y=[0, 0],
            mode="lines",
            line=dict(color="#E1E4E8", width=4),
            showlegend=False,
        ))
        fig_bono.add_trace(go.Scatter(
            x=[0], y=[0],
            mode="markers+text",
            marker=dict(color="#DC2626", size=20),
            text=[f"HOY\n-{simbolo} {bono_precio:,.2f}"],
            textposition="top center",
            name="Compra",
            textfont=dict(color="#DC2626", size=13),
        ))
        fig_bono.add_trace(go.Scatter(
            x=[int(bono_dias)], y=[0],
            mode="markers+text",
            marker=dict(color="#16A34A", size=20),
            text=[f"DIA {int(bono_dias)}\n+{simbolo} {bono_valor:,.2f}"],
            textposition="top center",
            name="Cobro",
            textfont=dict(color="#16A34A", size=13),
        ))
        fig_bono.update_layout(
            template="plotly_white", height=220,
            xaxis_title="Dias",
            yaxis=dict(visible=False, range=[-0.5, 1]),
            margin=dict(l=20, r=20, t=30, b=20),
        )
        st.plotly_chart(fig_bono, use_container_width=True)
        st.caption(
            f"Precio de compra: {simbolo} {bono_precio:,.2f} → "
            f"Cobro al vencimiento: {simbolo} {bono_valor:,.2f} en {int(bono_dias)} dias. "
            f"Rendimiento diario implicito: {res_bono['rendimiento_diario_pct']:.4f}%"
        )

    # ── SUB-TAB 4: COMPARADOR ─────────────────────────────────────────────────
    with csub4:
        st.info(
            "⚖️ Compara cuanto rinde tu plata en **cada opcion disponible** con el mismo monto y plazo. "
            "Considera el rendimiento **real** (ajustado por inflacion) para tomar la mejor decision."
        )

        cmp_c1, cmp_c2 = st.columns(2)
        with cmp_c1:
            cmp_monto = st.number_input(
                "Monto inicial (ARS)", min_value=1_000.0, value=100_000.0,
                step=1_000.0, format="%.0f", key="cmp_monto",
            )
            cmp_dias = st.number_input(
                "Plazo (dias)", min_value=1, max_value=365, value=30,
                step=1, key="cmp_dias",
            )
            cmp_inflacion = st.number_input(
                "Inflacion mensual esperada %", min_value=0.0, max_value=20.0,
                value=2.5, step=0.1, key="cmp_inflacion",
            )
        with cmp_c2:
            st.markdown("**Tasas asumidas (editables)**")
            cmp_billet = st.number_input(
                "Billetera virtual TNA %", min_value=0.0, max_value=200.0,
                value=32.0, step=0.5, key="cmp_billet",
            )
            cmp_pf = st.number_input(
                "Plazo fijo TNA %", min_value=0.0, max_value=200.0,
                value=38.0, step=0.5, key="cmp_pf",
            )
            cmp_fci = st.number_input(
                "FCI Money Market TNA %", min_value=0.0, max_value=200.0,
                value=40.0, step=0.5, key="cmp_fci",
            )
            cmp_bono = st.number_input(
                "Bono (rendimiento total del periodo %)", min_value=0.0, max_value=200.0,
                value=8.0, step=0.5, key="cmp_bono",
            )

        tasas = {
            "billetera": cmp_billet,
            "plazo_fijo": cmp_pf,
            "fci": cmp_fci,
            "bono": cmp_bono,
        }

        df_cmp = comparar_todas(cmp_monto, int(cmp_dias), tasas, cmp_inflacion)
        mejor_opcion = df_cmp.iloc[0]["Instrumento"]

        st.divider()
        st.markdown("#### Tabla comparativa")

        def _color_instrumento(val):
            if val == mejor_opcion:
                return "background-color: #DCFCE7; color: #166534; font-weight: 600;"
            return ""

        def _color_real(val):
            if isinstance(val, (int, float)):
                if val > 0:
                    return "color: #166534; font-weight: 600;"
                if val < 0:
                    return "color: #991B1B; font-weight: 600;"
            return ""

        styled_cmp = (
            df_cmp.style
            .map(_color_instrumento, subset=["Instrumento"])
            .map(_color_real, subset=["Rend. real %"])
            .format({
                "Monto final": "$ {:,.0f}",
                "Intereses": "$ {:,.0f}",
                "TEA %": "{:.2f}%",
                "Rend. real %": "{:+.2f}%",
            })
        )
        st.dataframe(styled_cmp, use_container_width=True, hide_index=True)

        st.success(f"🏆 **Mejor opcion con estas tasas:** {mejor_opcion}")

        st.markdown("#### Rendimiento nominal por instrumento")

        instrumentos = df_cmp["Instrumento"].tolist()
        rendimientos = [(row["Monto final"] / cmp_monto - 1) * 100 for _, row in df_cmp.iterrows()]
        colores = ["#16A34A"] + ["#2563EB"] * (len(instrumentos) - 1)

        fig_cmp = go.Figure(go.Bar(
            x=rendimientos,
            y=instrumentos,
            orientation="h",
            marker=dict(color=colores),
            text=[f"{r:.2f}%" for r in rendimientos],
            textposition="outside",
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
        ))
        fig_cmp.update_layout(
            template="plotly_white",
            height=280,
            xaxis_title="Rendimiento nominal %",
            margin=dict(l=20, r=80, t=10, b=20),
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        st.caption(
            "Rendimiento real negativo = perdiste poder adquisitivo aunque el monto en ARS aumento. "
            "Siempre compara contra la inflacion esperada del periodo."
        )