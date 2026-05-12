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
.stMarkdown, p, span, div, label, button, input, select, textarea {
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
    st.header("🔍 Buscador")
    
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
    st.subheader("📂 Atajos")
    
    if universo and "portfolios" in universo:
        for nombre, tickers in universo["portfolios"].items():
            with st.expander(f"📁 {nombre.capitalize()}"):
                st.write(f"{len(tickers)} tickers")
                st.write(", ".join(tickers))

# CONTENIDO PRINCIPAL
if not ticker:
    st.info("👈 Escribe un ticker en el buscador")
    st.stop()

try:
    with st.spinner(f"Cargando datos de {ticker}..."):
        datos = cargar_ticker(ticker)
except Exception as e:
    st.error(f"❌ Error al cargar {ticker}: {e}")
    st.stop()

st.header(f"{datos['nombre']} ({datos['ticker']})")
st.caption(f"{datos['sector']} | {datos['industria']} | {datos['pais']}")

tab1, tab2, tab3 = st.tabs(["🏢 Ficha", "📊 Fundamental", "📈 Tecnico"])

# TAB 1: FICHA
with tab1:
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