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

st.markdown("""
<meta name="description" content="Análisis financiero para inversores argentinos. Precios en tiempo real, fundamentals, DCF, macro Argentina, CEDEARs y más. Gratis.">
<meta name="keywords" content="inversiones argentina, cedears, dolar blue, merval, analisis fundamental">
<meta property="og:title" content="Mi Bloomberg Personal">
<meta property="og:description" content="Tu herramienta de análisis financiero para el mercado argentino">
""", unsafe_allow_html=True)

# ============== TRADINGVIEW DARK THEME ==============
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

/* ===== BASE ===== */
.stApp {
    background-color: #131722 !important;
    color: #d1d4dc !important;
}
.main .block-container {
    background: #131722;
    padding-top: 1.5rem;
    max-width: 1400px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #1e222d !important;
    border-right: 1px solid #2a2e39 !important;
}
section[data-testid="stSidebar"] * {
    color: #d1d4dc !important;
}
section[data-testid="stSidebar"] .stTextInput input {
    background-color: #2a2e39 !important;
    border-color: #363a45 !important;
    color: #d1d4dc !important;
    border-radius: 6px !important;
}

/* ===== HEADER ===== */
.bloomberg-header {
    background: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-radius: 10px;
    padding: 16px 24px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}
.bloomberg-header .title-block h1 {
    color: #d1d4dc;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.15;
}
.bloomberg-header .subtitle {
    color: #787b86;
    font-size: 13px;
    margin-top: 4px;
}
.live-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #26a69a;
    font-weight: 600;
    font-size: 13px;
    background: rgba(38,166,154,0.15);
    padding: 6px 12px;
    border-radius: 20px;
}
.live-dot {
    width: 8px;
    height: 8px;
    background: #26a69a;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.5; transform: scale(0.85); }
}

/* ===== MÉTRICAS / CARDS ===== */
[data-testid="stMetric"] {
    background-color: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-radius: 8px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    color: #787b86 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricValue"] {
    color: #d1d4dc !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1e222d !important;
    border-bottom: 1px solid #2a2e39 !important;
    gap: 0 !important;
    overflow-x: auto !important;
    scrollbar-width: thin !important;
    scrollbar-color: #2962ff #1e222d !important;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
    height: 3px !important;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
    background: #2962ff !important;
    border-radius: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #787b86 !important;
    border-radius: 0 !important;
    padding: 10px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #d1d4dc !important;
    border-bottom: 2px solid #2962ff !important;
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #d1d4dc !important;
    background-color: #2a2e39 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #131722 !important;
    padding-top: 16px !important;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox > div > div {
    background-color: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-radius: 6px !important;
    color: #d1d4dc !important;
}
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #2962ff !important;
    box-shadow: 0 0 0 2px rgba(41,98,255,0.2) !important;
}

/* ===== BOTONES ===== */
.stButton > button {
    background-color: #2a2e39 !important;
    color: #d1d4dc !important;
    border: 1px solid #363a45 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background-color: #2962ff !important;
    border-color: #2962ff !important;
    color: #fff !important;
}

/* ===== DATAFRAMES / TABLAS ===== */
[data-testid="stDataFrame"] {
    background-color: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-radius: 8px !important;
}
.stDataFrame th {
    background-color: #2a2e39 !important;
    color: #787b86 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
}
.stDataFrame td {
    color: #d1d4dc !important;
    border-color: #2a2e39 !important;
}

/* ===== SLIDERS ===== */
.stSlider [data-baseweb="slider"] div {
    background-color: #2962ff !important;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background-color: #2962ff !important;
    border-color: #2962ff !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background-color: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-radius: 8px !important;
    color: #d1d4dc !important;
}
.streamlit-expanderContent {
    background-color: #1e222d !important;
    border: 1px solid #2a2e39 !important;
    border-top: none !important;
}

/* ===== ALERTS / INFO BOXES ===== */
[data-testid="stAlert"] {
    background-color: #1e222d !important;
    border-radius: 8px !important;
    border-left: 4px solid !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
}
.stAlert [data-testid="stMarkdownContainer"] {
    color: #d1d4dc !important;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #2a2e39 !important;
    margin: 1.8rem 0 !important;
}

/* ===== TEXTO ===== */
h1, h2, h3, h4, h5, h6 {
    color: #d1d4dc !important;
}
p, li, span {
    color: #d1d4dc !important;
}
.stMarkdown {
    color: #d1d4dc !important;
}

/* ===== CAPTION ===== */
[data-testid="stCaptionContainer"],
.main [data-testid="stCaptionContainer"] p {
    color: #787b86 !important;
    font-size: 13px !important;
}

/* ===== SELECTBOX ===== */
.stSelectbox [data-baseweb="select"] div {
    background-color: #1e222d !important;
    border-color: #2a2e39 !important;
    color: #d1d4dc !important;
}

/* ===== RADIO BUTTONS ===== */
.stRadio label {
    color: #d1d4dc !important;
}
.stRadio [data-baseweb="radio"] div {
    border-color: #2962ff !important;
}

/* ===== CHECKBOXES ===== */
.stCheckbox label {
    color: #d1d4dc !important;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div {
    background-color: #2962ff !important;
}

/* ===== TICKER TAPE ===== */
.ticker-wrapper {
    background: #1e222d !important;
    border-bottom: 1px solid #2a2e39 !important;
}

/* ===== COLORES POSITIVO/NEGATIVO ===== */
.positive { color: #26a69a !important; }
.negative { color: #ef5350 !important; }
.neutral { color: #787b86 !important; }

/* ===== LINKS ===== */
a, a:visited { color: #2962ff !important; text-decoration: none; }
a:hover { text-decoration: underline; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #1e222d; }
::-webkit-scrollbar-thumb { background: #363a45; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #4a4f5e; }

/* ===== MOBILE ===== */
@media (max-width: 768px) {
    [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
    .stTabs [data-baseweb="tab"] { padding: 8px 12px !important; font-size: 12px !important; }
}

/* ===== SIDEBAR BUTTON ESTILO MENU ===== */
[data-testid="collapsedControl"] {
    background-color: #2a2e39 !important;
    border: 1px solid #363a45 !important;
    border-radius: 6px !important;
    width: auto !important;
    padding: 6px 12px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}
[data-testid="collapsedControl"]:hover {
    background-color: #2962ff !important;
    border-color: #2962ff !important;
}
[data-testid="collapsedControl"] svg {
    fill: #d1d4dc !important;
    width: 16px !important;
    height: 16px !important;
}
[data-testid="collapsedControl"]::after {
    content: "MENU" !important;
    color: #d1d4dc !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}
</style>
""", unsafe_allow_html=True)
# =================================================


universo = cargar_universo()

import datetime as _hdr_dt
import pytz as _hdr_pytz

def get_market_status():
    ny_tz = _hdr_pytz.timezone('America/New_York')
    now_ny = _hdr_dt.datetime.now(ny_tz)
    hora, minuto, dia = now_ny.hour, now_ny.minute, now_ny.weekday()
    if dia >= 5:
        return "cerrado", "⚫"
    h = hora + minuto / 60
    if 4 <= h < 9.5:
        return "pre-market", "🟡"
    elif 9.5 <= h < 16:
        return "abierto", "🟢"
    elif 16 <= h < 20:
        return "after-hours", "🟠"
    return "cerrado", "⚫"

_mkt_estado, _mkt_emoji = get_market_status()
_mkt_color = {"abierto": "#26a69a", "pre-market": "#ff9800", "after-hours": "#ff9800"}.get(_mkt_estado, "#ef5350")

st.markdown(f"""
<div class="bloomberg-header">
    <div class="title-block">
        <h1>Mi Bloomberg Personal</h1>
        <div class="subtitle">Sistema de analisis financiero &middot; Educacion Financiera AR</div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:13px;font-weight:600;color:{_mkt_color};">
            {_mkt_emoji} NYSE: {_mkt_estado.upper()}
        </div>
        <div class="live-indicator">
            <span class="live-dot"></span>
            <span>LIVE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if "sidebar_hint_shown" not in st.session_state:
    st.session_state["sidebar_hint_shown"] = True
    st.caption("☰ Usá las flechas arriba a la izquierda para abrir el menú")

# ── ONBOARDING (primera visita por sesión) ────────────────────────────────────
if "onboarding_completado" not in st.session_state:
    st.session_state["onboarding_completado"] = False

if not st.session_state["onboarding_completado"]:
    with st.container():
        st.markdown("""
## 👋 Bienvenido a Mi Bloomberg Personal

Tu herramienta de análisis financiero para el inversor argentino.

**¿Qué podés hacer?**

🔍 **Buscar cualquier acción** — escribí el ticker o el nombre de la empresa

📊 **Analizar fundamentals** — PE, ROE, DCF, Fair Value en un click

💼 **Gestionar tu portfolio** — cargá tus posiciones y seguí tu P&L en tiempo real

🇦🇷 **Datos argentinos** — dólar, riesgo país, CEDEARs con CCL implícito
""")
        _ob_c1, _ob_c2 = st.columns(2)
        with _ob_c1:
            if st.button("🚀 Empezar", use_container_width=True, type="primary"):
                st.session_state["onboarding_completado"] = True
                st.rerun()
        with _ob_c2:
            if st.button("⏭️ Saltar", use_container_width=True):
                st.session_state["onboarding_completado"] = True
                st.rerun()
    st.stop()

# SIDEBAR
with st.sidebar:
    st.header("Buscador")
    
    ticker = st.text_input(
        "Escribe un ticker:",
        value="",
        placeholder="Buscar empresa o ticker...",
        key="ticker_input",
    ).upper()
    if ticker:
        st.session_state["seccion_activa"] = ""
    
    periodo = st.selectbox(
        "Periodo para graficos:",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )
    
    st.divider()
    st.subheader("💼 Portfolio")

    if universo and "portfolios" in universo:
        for nombre, tickers in universo["portfolios"].items():
            with st.expander(nombre.capitalize()):
                st.write(f"{len(tickers)} tickers")
                st.write(", ".join(tickers))

    st.divider()
    st.markdown("### 🧭 Herramientas")

    _nav_secciones = [
        ("🧮 Calculadoras",    "calculadoras"),
        ("🇦🇷 Macro Argentina", "macro"),
        ("🎯 Perfil Inversor",  "perfil"),
        ("🔎 Screener",         "screener"),
        ("📅 Earnings",         "earnings"),
    ]
    for _nav_label, _nav_key in _nav_secciones:
        if st.button(_nav_label, key=f"nav_{_nav_key}", use_container_width=True):
            st.session_state["seccion_activa"] = _nav_key
            st.session_state["ticker_input"] = ""
            st.rerun()

    # Botón ← Inicio en sidebar: visible siempre sin necesidad de hacer scroll
    if st.session_state.get("seccion_activa", "") and not ticker:
        if st.button("← Inicio", key="btn_sb_home", use_container_width=True):
            st.session_state["seccion_activa"] = ""
            st.session_state["ticker_input"] = ""
            st.rerun()

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

    st.divider()
    st.toggle(
        "🌙 Modo oscuro",
        value=st.session_state.get("modo_oscuro", False),
        key="modo_oscuro",
    )
    st.toggle(
        "🔄 Auto-refresh (5 min)",
        value=False,
        key="auto_refresh",
    )
    if st.session_state.get("auto_refresh"):
        st.caption("⏱️ Actualizando cada 5 minutos")
    _ar_countdown_slot = st.empty()

    st.markdown("---")
    st.markdown(
        "<div style='background:#2a1a1a;border:1px solid #7f1d1d;border-radius:6px;"
        "padding:8px 10px;font-size:11px;color:#fca5a5;line-height:1.5;'>"
        "<b>⚠️ DISCLAIMER</b><br>"
        "Herramienta educativa. No constituye asesoramiento financiero. "
        "Toda decisión de inversión es responsabilidad exclusiva del usuario."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("")
    with st.expander("ℹ️ Acerca de la app"):
        st.markdown("""
**Mi Bloomberg Personal v2.0**
Sistema de análisis financiero para inversores argentinos.

**Datos:**
- 📊 Yahoo Finance
- 💵 DolarAPI
- 🌎 ArgentinaDatos

**GitHub:** [Ver código fuente](https://github.com/tu-usuario/mi-bloomberg-personal)
""")

# ── MODO OSCURO CSS ───────────────────────────────────────────────────────────
if st.session_state.get("modo_oscuro"):
    st.markdown("""
<style>
.stApp { background-color: #0d1117 !important; color: #e6edf3 !important; }
section[data-testid="stSidebar"] { background-color: #161b22 !important; }
[data-testid="stMetric"] { background-color: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 8px !important; padding: 16px !important; }
.stTabs [data-baseweb="tab"] { color: #8b949e !important; }
.stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }
.stTextInput input, .stNumberInput input { background-color: #1c2128 !important; color: #e6edf3 !important; border-color: #30363d !important; }
h1, h2, h3 { color: #e6edf3 !important; }
hr { border-color: #30363d !important; }
[data-testid="stDataFrame"] { background-color: #1c2128 !important; }
.stSelectbox > div { background-color: #1c2128 !important; color: #e6edf3 !important; }
</style>""", unsafe_allow_html=True)

def show_skeleton(rows=3):
    st.markdown(f"""
    <style>
    .skeleton {{
        background: linear-gradient(
            90deg,
            #f0f0f0 25%,
            #e8e8e8 50%,
            #f0f0f0 75%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
        margin: 8px 0;
    }}
    .skeleton-title {{
        height: 24px;
        width: 40%;
    }}
    .skeleton-card {{
        height: 80px;
        width: 100%;
    }}
    .skeleton-text {{
        height: 16px;
        width: 70%;
    }}
    .skeleton-text-short {{
        height: 16px;
        width: 40%;
    }}
    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}
    </style>
    {"".join([f'''
    <div class="skeleton skeleton-title"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin:12px 0">
        <div class="skeleton skeleton-card"></div>
        <div class="skeleton skeleton-card"></div>
        <div class="skeleton skeleton-card"></div>
        <div class="skeleton skeleton-card"></div>
    </div>
    <div class="skeleton skeleton-text"></div>
    <div class="skeleton skeleton-text-short"></div>
    ''' for _ in range(rows)])}
    """, unsafe_allow_html=True)


# CONTENIDO PRINCIPAL
# Cargamos el ticker del sidebar pero NO abortamos si falla:
# el tab Mi Portfolio funciona aunque el ticker sea invalido.
datos = None
ticker_error = None
if not ticker:
    ticker_error = "Escribe un ticker en el buscador para ver Ficha/Fundamental/Tecnico"
else:
    _sk_slot = st.empty()
    with _sk_slot:
        show_skeleton()
    try:
        datos = cargar_ticker(ticker)
    except Exception as e:
        ticker_error = f"Error al cargar {ticker}: {e}"
    finally:
        _sk_slot.empty()

if datos:
    _precio_actual = datos.get('precio_actual')
    _title_precio = f" ${_precio_actual:.2f}" if _precio_actual else ""
    st.markdown(
        f"<title>{ticker}{_title_precio} — Mi Bloomberg Personal</title>",
        unsafe_allow_html=True,
    )
    st.header(f"{datos['nombre']} ({datos['ticker']})")
    st.caption(f"{datos['sector']} | {datos['industria']} | {datos['pais']}")
else:
    if ticker:
        st.caption(ticker_error or "")

# Saltear contenido del home cuando hay una sección activa (calculadoras, macro, etc.)
# Sin esto los tabs de sección quedan enterrados debajo del heatmap y no se ven.
_seccion_activa = st.session_state.get("seccion_activa", "")
_skip_home = bool(_seccion_activa) and not ticker

# ── TICKER TAPE ANIMADO ───────────────────────────────────────────────────────
try:
    if _skip_home: raise Exception("__skip__")
    from src.mercado import get_ticker_tape as _get_tape
    # Tickers del tape: portfolio guardado en sesión, o fallback a watchlist del universo
    try:
        from src.portfolio import cargar_portfolio as _cp_tape
        _port_tape = _cp_tape("pato")
        _tks_tape = tuple(p["ticker"] for p in _port_tape.get("posiciones", []))
        if not _tks_tape and universo:
            _tks_tape = tuple(
                (universo.get("portfolios", {}).get("watchlist", []) or
                 universo.get("categorias", {}).get("acciones_ar_adr", []))[:12]
            )
    except Exception:
        _tks_tape = tuple(
            universo.get("portfolios", {}).get("watchlist", [])[:12]
        ) if universo else ()
    _tape_data = _get_tape(_tks_tape)
    if _tape_data:
        _tape_items = "".join([
            f'<span class="ticker-item">'
            f'<span class="ticker-name">{_ti["ticker"]}</span>'
            f'<span style="color:{"#00ff88" if _ti["variacion_pct"] >= 0 else "#ff4444"};">'
            f'&nbsp;${_ti["precio"]:,.2f}&nbsp;{_ti["variacion_pct"]:+.2f}%</span>'
            f'</span>'
            for _ti in _tape_data
        ])
        st.markdown(f"""
<style>
.ticker-wrapper{{background:#1a1a2e;padding:8px 0;overflow:hidden;
  width:100%;border-bottom:1px solid #333;margin-bottom:12px;}}
.ticker-track{{display:flex;animation:scroll-left 30s linear infinite;width:max-content;}}
.ticker-track:hover{{animation-play-state:paused;}}
.ticker-item{{padding:0 24px;font-size:12px;font-weight:600;color:#fff;
  white-space:nowrap;border-right:1px solid #333;}}
.ticker-name{{color:#aaa;margin-right:6px;}}
@keyframes scroll-left{{
  0%{{transform:translateX(0);}}
  100%{{transform:translateX(-50%);}}
}}
</style>
<div class="ticker-wrapper">
  <div class="ticker-track">{_tape_items}{_tape_items}</div>
</div>""", unsafe_allow_html=True)
except Exception:
    pass

# ── BRIEF DIARIO ──────────────────────────────────────────────────────────────
try:
    if _skip_home: raise Exception("__skip__")
    from src.mercado import get_metricas_macro as _get_macro_brief

    _macro = _get_macro_brief()

    # CSS grid para las 6 métricas
    st.markdown("""
<style>
.brief-row{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:0 0 10px 0;}
@media(max-width:768px){.brief-row{grid-template-columns:repeat(3,1fr);}}
</style>""", unsafe_allow_html=True)

    def _brief_card(label, main_val, sub_val, var, var_unidad="%", invert=False):
        if var is not None:
            good = (var >= 0) if not invert else (var <= 0)
            var_color = "#26a69a" if good else "#ef5350"
            if var_unidad == "bp":
                var_txt = f"{var:+.0f}&nbsp;bp"
            else:
                var_txt = f"{var:+.1f}%"
        else:
            var_color, var_txt = "#787b86", "—"
        sub_html = (f"<div style='font-size:10px;color:#787b86;margin-top:1px;'>{sub_val}</div>"
                    if sub_val else "")
        return (
            f"<div style='background:#1e222d;border:1px solid #2a2e39;"
            f"border-radius:8px;padding:10px 12px;'>"
            f"<div style='font-size:10px;color:#787b86;font-weight:600;"
            f"text-transform:uppercase;letter-spacing:.5px;'>{label}</div>"
            f"<div style='font-size:13px;font-weight:700;color:#d1d4dc;"
            f"margin-top:3px;line-height:1.25;white-space:nowrap;"
            f"overflow:hidden;text-overflow:ellipsis;'>{main_val}</div>"
            f"{sub_html}"
            f"<div style='font-size:12px;color:{var_color};font-weight:600;"
            f"margin-top:4px;'>{var_txt}</div>"
            f"</div>"
        )

    def _ars(v):
        return f"${v:,.0f}".replace(",", ".") if v is not None else "—"

    def _usd(v):
        return f"${v:,.0f}" if v is not None else "—"

    _blue_main = (
        f"{_ars(_macro['blue_compra'])} / {_ars(_macro['blue_venta'])}"
        if _macro["blue_compra"] else _ars(_macro["blue_venta"])
    )

    _cards = "".join([
        _brief_card("Dólar Blue",    _blue_main,              "compra / venta",  _macro["blue_var"]),
        _brief_card("Dólar MEP",     _ars(_macro["mep"]),     "venta",           _macro["mep_var"]),
        _brief_card("Dólar CCL",     _ars(_macro["ccl"]),     "venta",           _macro["ccl_var"]),
        _brief_card("Riesgo País",
                    f"{_macro['riesgo_pais']:,}".replace(",", ".") if _macro["riesgo_pais"] else "—",
                    "puntos básicos",  _macro["riesgo_pais_var"],
                    var_unidad="bp", invert=True),
        _brief_card("Merval",        _ars(_macro["merval"]),  "ARS",             _macro["merval_var"]),
        _brief_card("S&amp;P 500",   _usd(_macro["sp500"]),   "USD",             _macro["sp500_var"]),
    ])

    st.markdown(
        f"<div style='font-size:10px;color:#787b86;font-weight:600;"
        f"text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>"
        f"📰 Brief del día</div>"
        f"<div class='brief-row'>{_cards}</div>",
        unsafe_allow_html=True,
    )

except Exception:
    pass  # Sección decorativa; la app continúa si falla

# ── CARD "TU CARTERA HOY" ─────────────────────────────────────────────────────
try:
    if _skip_home: raise Exception("__skip__")
    from src.portfolio import (
        cargar_portfolio          as _cp_brief,
        calcular_metricas_portfolio as _calc_met_brief,
    )
    from src.mercado import get_movers_portfolio as _get_mv_brief

    _port_brief = _cp_brief("pato")
    _pos_brief  = _port_brief.get("posiciones", [])

    if _pos_brief:
        _tks_brief = tuple(p["ticker"] for p in _pos_brief)
        _met_brief = _calc_met_brief(_port_brief)
        _val_total = _met_brief.get("valor_total_ars") or 0

        # Variación del día ponderada por valor de posición
        _movers_b  = _get_mv_brief(_tks_brief) if _tks_brief else {}
        _todos_b   = _movers_b.get("gainers", []) + _movers_b.get("losers", [])
        _var_dia_pct = None
        if _todos_b and _val_total > 0:
            _pos_map = {p["ticker"]: p for p in _pos_brief}
            _num, _den = 0.0, 0.0
            for _mv in _todos_b:
                _pp = _pos_map.get(_mv["ticker"])
                if _pp:
                    _v = (_pp.get("precio_actual_ars") or 0) * (_pp.get("cantidad") or 0)
                    _num += _mv["variacion_pct"] * _v
                    _den += _v
            if _den > 0:
                _var_dia_pct = _num / _den

        _var_dia_ars = (_val_total * _var_dia_pct / 100) if _var_dia_pct is not None else None

        _gainers_b = _movers_b.get("gainers", [])
        _losers_b  = _movers_b.get("losers", [])
        _mejor_b   = _gainers_b[0] if _gainers_b else None
        _peor_b    = _losers_b[0]  if _losers_b  else None

        if _var_dia_pct is not None:
            if _var_dia_pct > 0.5:
                _badge, _badge_col = "📈 Subió", "#26a69a"
            elif _var_dia_pct < -0.5:
                _badge, _badge_col = "📉 Bajó", "#ef5350"
            else:
                _badge, _badge_col = "➡️ Estable", "#787b86"
        else:
            _badge, _badge_col = "—", "#787b86"

        _vc   = "#26a69a" if (_var_dia_pct or 0) >= 0 else "#ef5350"
        _vt   = f"{_var_dia_pct:+.2f}%" if _var_dia_pct is not None else "—"
        _vart = (f"&nbsp;<span style='color:{_vc};font-size:12px;'>"
                 f"${_var_dia_ars:+,.0f}".replace(",", ".") + "</span>"
                 if _var_dia_ars is not None else "")
        _v_total_fmt = f"ARS ${_val_total:,.0f}".replace(",", ".")

        _pos_items = []
        if _mejor_b:
            _pos_items.append(
                f"<span style='color:#26a69a;'>▲ {_mejor_b['ticker']} "
                f"{_mejor_b['variacion_pct']:+.1f}%</span>"
            )
        if _peor_b:
            _pos_items.append(
                f"<span style='color:#ef5350;'>▼ {_peor_b['ticker']} "
                f"{_peor_b['variacion_pct']:+.1f}%</span>"
            )
        _pos_html = (
            f"<div style='margin-top:8px;font-size:12px;'>"
            + "&nbsp;&nbsp;·&nbsp;&nbsp;".join(_pos_items)
            + "</div>"
        ) if _pos_items else ""

        st.markdown(f"""
<div style="background:#1e222d;border:1px solid #2a2e39;border-radius:10px;
            padding:14px 18px;margin-bottom:12px;border-left:3px solid #2962ff;">
  <div style="display:flex;justify-content:space-between;align-items:center;
              margin-bottom:8px;">
    <span style="font-size:13px;font-weight:700;color:#d1d4dc;">
      💼 Tu cartera hoy
    </span>
    <span style="background:rgba(41,98,255,.12);color:{_badge_col};
                 font-size:11px;font-weight:700;padding:3px 10px;
                 border-radius:12px;border:1px solid {_badge_col}55;">
      {_badge}
    </span>
  </div>
  <div style="display:flex;gap:24px;flex-wrap:wrap;align-items:baseline;">
    <span style="color:#787b86;font-size:12px;">Valor total:&nbsp;
      <strong style="color:#d1d4dc;font-size:15px;">{_v_total_fmt}</strong>
    </span>
    <span style="color:#787b86;font-size:12px;">Variación:&nbsp;
      <strong style="color:{_vc};font-size:14px;">{_vt}</strong>{_vart}
    </span>
  </div>
  {_pos_html}
</div>""", unsafe_allow_html=True)

except Exception:
    pass  # Card decorativa; la app continúa si falla

# ── ÍNDICES GLOBALES CON SPARKLINES ───────────────────────────────────────────
try:
    if _skip_home: raise Exception("__skip__")
    import plotly.graph_objects as _go_sp
    from src.mercado import (
        get_indices_globales   as _get_idx_sp,
        get_sparklines_indices as _get_spark,
    )
    _idx_sk = st.empty()
    with _idx_sk:
        show_skeleton(rows=1)
    _idx_sp   = _get_idx_sp()
    _spark_sp = _get_spark()
    _idx_sk.empty()

    _sp_cols1 = st.columns(4)
    _sp_cols2 = st.columns(4)

    for _si, _sidx in enumerate(_idx_sp[:8]):
        _scol = _sp_cols1[_si] if _si < 4 else _sp_cols2[_si - 4]
        with _scol:
            _stk   = _sidx["ticker"]
            _spx   = _sidx.get("precio")
            _svar  = _sidx.get("variacion_pct")
            _spxs  = _spark_sp.get(_stk, [])
            _scol_v = "#26a69a" if (_svar or 0) >= 0 else "#ef5350"
            _svar_t = f"{_svar:+.2f}%" if _svar is not None else "—"
            _spx_t  = f"${_spx:,.2f}" if _spx else "—"
            st.markdown(
                f"<div style='background:#1e222d;border:1px solid #2a2e39;"
                f"border-radius:10px;padding:10px 12px;margin-bottom:4px;'>"
                f"<div style='font-size:11px;color:#787b86;font-weight:600;'>{_sidx['nombre']}</div>"
                f"<div style='font-size:15px;font-weight:700;margin:2px 0;color:#d1d4dc;'>{_spx_t}</div>"
                f"<div style='font-size:13px;color:{_scol_v};font-weight:600;'>{_svar_t}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if len(_spxs) >= 2:
                _positivo = _spxs[-1] >= _spxs[0]
                _fig_sp = _go_sp.Figure(_go_sp.Scatter(
                    y=_spxs,
                    mode="lines",
                    line=dict(
                        color="#00cc66" if _positivo else "#ff3333",
                        width=1.5,
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(0,204,102,0.15)" if _positivo else "rgba(255,51,51,0.15)",
                ))
                _fig_sp.update_layout(
                    height=50,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    xaxis=dict(visible=False),
                    yaxis=dict(
                        visible=False,
                        range=[min(_spxs) * 0.999, max(_spxs) * 1.001],
                    ),
                )
                st.plotly_chart(
                    _fig_sp, use_container_width=True,
                    config={"displayModeBar": False},
                )
except Exception:
    pass

# ── HEATMAP MERCADO (home screen) ─────────────────────────────────────────────
try:
    if _skip_home: raise Exception("__skip__")
    import plotly.express as _px_hm
    from datetime import datetime as _dt_hm
    from src.mercado import get_heatmap_data as _get_hm

    _hm_header_c1, _hm_header_c2 = st.columns([6, 1])
    with _hm_header_c1:
        st.markdown("### 🗺️ Mapa del mercado — hoy")
    with _hm_header_c2:
        if st.button("🔄 Actualizar", key="hm_refresh"):
            st.cache_data.clear()
            st.rerun()

    _hm_data = _get_hm()

    if _hm_data:
        import pandas as _pd_hm
        _df_hm = _pd_hm.DataFrame(_hm_data)

        _fig_hm = _px_hm.treemap(
            _df_hm,
            path=["sector", "ticker"],
            values="market_cap",
            color="variacion_%",
            color_continuous_scale=[
                [0.00, "#8B0000"],
                [0.30, "#FF4444"],
                [0.45, "#882222"],
                [0.50, "#1a1a2e"],
                [0.55, "#224422"],
                [0.70, "#00AA44"],
                [1.00, "#006600"],
            ],
            color_continuous_midpoint=0,
            custom_data=["variacion_%", "precio"],
        )
        _fig_hm.update_traces(
            texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%",
            textfont_size=14,
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Variación: %{customdata[0]:.2f}%<br>"
                "Precio: $%{customdata[1]:.2f}"
                "<extra></extra>"
            ),
        )
        _fig_hm.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(_fig_hm, use_container_width=True)
        st.caption(f"Última actualización: {_dt_hm.now().strftime('%H:%M:%S')} · Merval (BYMA) y CEDEARs principales · Fuente: Yahoo Finance")
    else:
        st.warning("No se pudieron cargar los datos del heatmap.")
except Exception as _e_hm:
    if str(_e_hm) != "__skip__":
        st.warning(f"Heatmap no disponible: {_e_hm}")

# _seccion_activa ya fue leído arriba (al definir _skip_home)
if not ticker and not _seccion_activa:
    st.stop()

st.divider()

if _seccion_activa and not ticker:
    if st.button("← Inicio", key="btn_volver_inicio"):
        st.session_state["seccion_activa"] = ""
        st.rerun()

if ticker:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🏢 Ficha",
        "📊 Fundamental",
        "📈 Tecnico",
        "🗂️ Mi Portfolio",
        "🧮 Calculadoras",
        "🇦🇷 Macro Argentina",
        "📐 DCF & Valuación",
        "📰 Noticias",
        "👁️ Watchlist",
        "⚖️ Comparar",
    ])
elif _seccion_activa == "comparar":
    (tab10,) = st.tabs(["⚖️ Comparar"])
    tab1 = tab2 = tab3 = tab4 = tab5 = tab6 = tab7 = tab8 = tab9 = None
elif _seccion_activa in ("calculadoras", "macro", "watchlist"):
    if _seccion_activa == "calculadoras":
        tab5, tab6, tab9 = st.tabs(["🧮 Calculadoras", "🇦🇷 Macro Argentina", "👁️ Watchlist"])
    elif _seccion_activa == "macro":
        tab6, tab5, tab9 = st.tabs(["🇦🇷 Macro Argentina", "🧮 Calculadoras", "👁️ Watchlist"])
    else:
        tab9, tab5, tab6 = st.tabs(["👁️ Watchlist", "🧮 Calculadoras", "🇦🇷 Macro Argentina"])
    tab1 = tab2 = tab3 = tab4 = tab7 = tab8 = tab10 = None
else:
    _TITULOS_NUEVA = {
        "perfil":   "🎯 Perfil Inversor",
        "screener": "🔎 Screener",
        "earnings": "📅 Earnings",
    }
    _titulo_nueva = _TITULOS_NUEVA.get(_seccion_activa, str(_seccion_activa))
    st.info(f"🚧 **{_titulo_nueva}** está en construcción. Próximamente disponible.")
    st.stop()

# TAB 1: FICHA
if tab1 is not None:
    with tab1:
        if not datos:
            st.info(f"👈 {ticker_error}")
        else:
            # Badge Argentina: muestra relación ADR ↔ local si aplica
            if datos.get('es_argentino'):
                _adr_lbl   = datos.get('ticker_adr')   or "—"
                _local_lbl = datos.get('ticker_local')  or "—"
                _px_mon    = datos.get('precio_moneda') or "USD"
                st.markdown(
                    f"<span style='background:#DBEAFE;color:#1E40AF;padding:4px 10px;"
                    f"border-radius:14px;font-size:12px;font-weight:600;'>"
                    f"🇦🇷 ADR: {_adr_lbl} · Local: {_local_lbl} · "
                    f"Precio {_px_mon} · Fundamentals USD</span>",
                    unsafe_allow_html=True,
                )
                st.write("")

            col1, col2, col3, col4 = st.columns(4)

            precio = datos.get('precio_actual')
            mcap   = datos.get('market_cap_b', 0)
            pe     = datos.get('pe')
            roe    = datos.get('roe')

            if datos.get('es_argentino'):
                # col1: precio ARS (.BA)  col2: precio ADR USD  col3: Mkt Cap USD  col4: PE
                col1.metric("Precio (ARS)", f"${precio:.2f}" if precio else "N/A")
                _px_adr = datos.get('precio_adr_usd')
                if _px_adr:
                    col2.metric("Precio ADR (USD)", f"${_px_adr:.2f}")
                col3.metric("Mkt Cap (USD)", f"${mcap:.1f}B" if mcap else "N/A")
                col4.metric("PE", f"{pe:.1f}" if pe else "N/A")
            else:
                _px_mon_label = datos.get('precio_moneda', 'USD')
                _px_sym = "$" if _px_mon_label in ("USD", "ARS") else _px_mon_label + " "
                col1.metric(
                    f"Precio ({_px_mon_label})",
                    f"{_px_sym}{precio:.2f}" if precio else "N/A",
                )
                col2.metric("Mkt Cap", f"${mcap:.1f}B" if mcap else "N/A")
                col3.metric("PE", f"{pe:.1f}" if pe else "N/A")
                col4.metric("ROE", f"{roe*100:.1f}%" if roe else "N/A")

            # ── FAIR VALUE ───────────────────────────────────────────────────────
            _fv = None
            _upside = None
            try:
                from src.fundamentals import calcular_fair_value as _calc_fv_raw

                _fv_data = _calc_fv_raw(ticker)
                _fv      = _fv_data.get("fair_value_promedio")
                _upside  = _fv_data.get("upside_downside")
                _verdict = _fv_data.get("veredicto", "")
                if _fv and _upside is not None and _verdict != "SIN DATOS":
                    st.info(
                        f"🎯 Fair Value estimado: **${_fv:.2f}** | "
                        f"Upside: **{_upside:+.1f}%** | {_verdict}"
                    )
            except Exception:
                pass

            st.divider()

            col_a, col_b = st.columns(2)

            with col_a:
                st.subheader("📋 Detalles")
                _moneda_display = datos.get('moneda', 'N/A')
                if datos.get('es_argentino') and datos.get('precio_moneda') == 'ARS':
                    _moneda_display = f"ARS (precio local) · USD (fundamentals)"
                st.write(f"**Moneda:** {_moneda_display}")

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

            # ── COMPARTIR ANÁLISIS ───────────────────────────────────────────────
            st.divider()
            st.markdown("#### 📤 Compartir este análisis")

            import urllib.parse as _uparse

            _sh_nombre = datos.get("nombre", ticker)
            _sh_precio = datos.get("precio_actual")
            _sh_pe     = datos.get("pe")
            _sh_roe    = datos.get("roe")
            _sh_mg     = datos.get("margen_op")

            def _nd(v, fmt="{:.1f}"):
                return fmt.format(v) if v is not None else "N/D"

            _sh_lineas = [
                f"📊 {_sh_nombre} ({ticker}) — Mi Bloomberg Personal",
                "",
                f"💰 Precio: ${_sh_precio:.2f}" if _sh_precio else "💰 Precio: N/D",
                (
                    f"📈 PE: {_nd(_sh_pe)} | "
                    f"ROE: {_nd(_sh_roe * 100 if _sh_roe else None)}% | "
                    f"Mg. Op.: {_nd(_sh_mg * 100 if _sh_mg else None)}%"
                ),
            ]
            if _fv is not None and _upside is not None:
                _sh_lineas.append(f"🎯 Fair Value: ${_fv:.2f} ({_upside:+.1f}% upside)")
            _sh_lineas += [
                "📉 Beta: N/D | Div Yield: N/D%",
                "",
                "🔍 Analizalo vos: personalfinances.streamlit.app",
                "#InversionesAR #MiBloombergPersonal",
            ]

            _sh_texto = "\n".join(_sh_lineas)

            _tweet_parts = [f"Analizando ${ticker} con Mi Bloomberg Personal 📊"]
            if _sh_precio:
                _tweet_parts.append(f"Precio: ${_sh_precio:.2f}")
            if _fv is not None and _upside is not None:
                _tweet_parts.append(f"Fair Value: ${_fv:.2f} | {_upside:+.1f}% upside")
            _tweet_parts.append("personalfinances.streamlit.app #InversionesAR")
            _tweet = " | ".join(_tweet_parts[:2]) + " " + " | ".join(_tweet_parts[2:]) if len(_tweet_parts) > 2 else " ".join(_tweet_parts)
            _twitter_url = f"https://twitter.com/intent/tweet?text={_uparse.quote(_tweet)}"

            _sh_col1, _sh_col2 = st.columns([3, 1])

            with _sh_col1:
                st.code(_sh_texto, language=None)
                st.caption("📋 Copiá y compartí en WhatsApp, Twitter o Instagram")

            with _sh_col2:
                st.link_button(
                    "🐦 Compartir en X/Twitter",
                    _twitter_url,
                    use_container_width=True,
                )
                st.link_button(
                    "📱 Abrir app",
                    "https://personalfinances.streamlit.app",
                    use_container_width=True,
                )

# TAB 2: FUNDAMENTAL
if tab2 is not None:
    with tab2:
        if not datos:
            st.info(f"👈 {ticker_error}")
        else:
            st.subheader(f"📊 Analisis Fundamental - {ticker}")

            fsub1, fsub2, fsub3, fsub4 = st.tabs([
                "📊 Ratios",
                "📈 Crecimiento",
                "💰 Estados Financieros",
                "🔍 Comparar Peers",
            ])

            # ── FSUB 1: RATIOS (existente, sin cambios) ──────────────────────────
            with fsub1:
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

                    beta_r = ratios.get('Beta')
                    s4.metric("Beta", f"{beta_r:.2f}" if beta_r else "N/A")

                except Exception as e:
                    st.error(f"❌ Error cargando fundamentals: {e}")

            # ── FSUB 2: CRECIMIENTO ───────────────────────────────────────────────
            with fsub2:
                try:
                    import plotly.graph_objects as _go2
                    from src.fundamentals import (
                        crecimiento_historico,
                        fcf_historico,
                        estados_financieros,
                    )

                    # -- CAGRs --
                    st.markdown("### 📊 CAGRs históricos")
                    with st.spinner(f"Calculando crecimiento de {ticker}..."):
                        _crec = crecimiento_historico(ticker)

                    if not _crec:
                        st.info("No hay datos de crecimiento disponibles para este ticker.")
                    else:
                        def _fmt_cagr(v):
                            return f"{v:+.1f}%" if v is not None else "N/D"

                        _cg1, _cg2, _cg3, _cg4 = st.columns(4)

                        _rv = _crec.get("revenue_cagr_%")
                        _cg1.metric(
                            "CAGR Revenue", _fmt_cagr(_rv),
                            delta=_fmt_cagr(_rv) if _rv is not None else None,
                            delta_color="normal" if _rv is not None else "off",
                        )

                        _ni = _crec.get("net_income_cagr_%")
                        _cg2.metric(
                            "CAGR Net Income", _fmt_cagr(_ni),
                            delta=_fmt_cagr(_ni) if _ni is not None else None,
                            delta_color="normal" if _ni is not None else "off",
                        )

                        _fc = _crec.get("fcf_cagr_%")
                        _cg3.metric(
                            "CAGR FCF", _fmt_cagr(_fc),
                            delta=_fmt_cagr(_fc) if _fc is not None else None,
                            delta_color="normal" if _fc is not None else "off",
                        )

                        _em = _crec.get("expansion_margen_pp")
                        _em_str = f"{_em:+.1f} pp" if _em is not None else "N/D"
                        _cg4.metric(
                            "Expansión margen", _em_str,
                            delta=_em_str if _em is not None else None,
                            delta_color="normal" if _em is not None else "off",
                        )

                        _años_rv = _crec.get("revenue_años")
                        if _años_rv:
                            st.caption(f"CAGRs calculados sobre {_años_rv} años de historia disponible en yfinance.")

                    st.divider()

                    # -- FCF histórico --
                    st.markdown("### 💵 Free Cash Flow histórico")
                    try:
                        _fcf_df = fcf_historico(ticker)
                        if _fcf_df is None or _fcf_df.empty:
                            st.info("No hay datos de FCF disponibles para este ticker.")
                        else:
                            _fcf_cols = ["#16A34A" if v >= 0 else "#EF4444" for v in _fcf_df["FCF_USD_B"]]
                            _fig_fcf = _go2.Figure(_go2.Bar(
                                x=_fcf_df["año"],
                                y=_fcf_df["FCF_USD_B"],
                                marker_color=_fcf_cols,
                                text=[f"${v:.1f}B" for v in _fcf_df["FCF_USD_B"]],
                                textposition="outside",
                                hovertemplate="<b>%{x}</b><br>FCF: $%{y:.2f}B<extra></extra>",
                            ))
                            _fig_fcf.update_layout(
                                title="Free Cash Flow histórico (USD Billones)",
                                xaxis_title="Año",
                                yaxis_title="FCF (USD B)",
                                template="plotly_white",
                                height=400,
                                margin=dict(l=20, r=20, t=50, b=20),
                            )
                            st.plotly_chart(_fig_fcf, use_container_width=True)
                    except Exception as _e_fcf:
                        st.warning(f"No se pudo graficar FCF: {_e_fcf}")

                    st.divider()

                    # -- Revenue vs Net Income --
                    st.markdown("### 📊 Revenue vs Net Income")
                    try:
                        _est2 = estados_financieros(ticker, "resumido")
                        if not _est2:
                            st.info("No hay datos de estados financieros disponibles.")
                        else:
                            _pl2 = _est2["pl"]
                            _años2 = [c.year for c in _pl2.columns]
                            _fig_rev = _go2.Figure()

                            if "Total Revenue" in _pl2.index:
                                _rev2 = (_pl2.loc["Total Revenue"] / 1e9).values
                                _fig_rev.add_trace(_go2.Bar(
                                    x=_años2, y=_rev2,
                                    name="Revenue",
                                    marker_color="#2563EB",
                                    text=[f"${v:.1f}B" for v in _rev2],
                                    textposition="outside",
                                ))

                            if "Net Income" in _pl2.index:
                                _ni2 = (_pl2.loc["Net Income"] / 1e9).values
                                _fig_rev.add_trace(_go2.Bar(
                                    x=_años2, y=_ni2,
                                    name="Net Income",
                                    marker_color="#16A34A",
                                    text=[f"${v:.1f}B" for v in _ni2],
                                    textposition="outside",
                                ))

                            _fig_rev.update_layout(
                                title="Revenue vs Net Income (USD Billones)",
                                xaxis_title="Año",
                                yaxis_title="USD B",
                                template="plotly_white",
                                height=400,
                                barmode="group",
                                margin=dict(l=20, r=20, t=50, b=20),
                            )
                            st.plotly_chart(_fig_rev, use_container_width=True)
                    except Exception as _e_rev:
                        st.warning(f"No se pudo graficar Revenue/NI: {_e_rev}")

                except Exception as e:
                    st.error(f"❌ Error en análisis de crecimiento: {e}")

            # ── FSUB 3: ESTADOS FINANCIEROS ──────────────────────────────────────
            with fsub3:
                try:
                    from src.fundamentals import estados_financieros as _ef3

                    _fmt_sel = st.radio(
                        "Formato",
                        ["Resumido", "Completo"],
                        horizontal=True,
                        key="eeff_formato",
                    )

                    with st.spinner(f"Cargando estados financieros de {ticker}..."):
                        _estados3 = _ef3(ticker, "resumido" if _fmt_sel == "Resumido" else "completo")

                    if not _estados3:
                        st.info("No hay datos de estados financieros disponibles para este ticker.")
                    else:
                        def _render_eeff(df, titulo, fila_hl=None):
                            if df is None or df.empty:
                                st.info(f"Sin datos: {titulo}")
                                return
                            st.markdown(f"#### {titulo}")
                            _df3 = df.copy()
                            try:
                                _df3.columns = [
                                    c.strftime("%Y") if hasattr(c, "strftime") else str(c)
                                    for c in _df3.columns
                                ]
                            except Exception:
                                pass
                            _df3 = _df3 / 1e6

                            def _hl3(row):
                                if fila_hl and row.name == fila_hl:
                                    return ["background-color:#DBEAFE; font-weight:bold;"] * len(row)
                                return [""] * len(row)

                            st.dataframe(
                                _df3.style.apply(_hl3, axis=1).format("{:,.0f}", na_rep="—"),
                                use_container_width=True,
                            )
                            st.caption("Valores en millones USD")

                        with st.expander("📋 Estado de Resultados (P&L)", expanded=True):
                            _render_eeff(_estados3["pl"], "Estado de Resultados", "Net Income")

                        with st.expander("🏛️ Balance General", expanded=False):
                            _render_eeff(_estados3["balance"], "Balance General", "Total Assets")

                        with st.expander("💵 Flujo de Efectivo", expanded=False):
                            _render_eeff(_estados3["cashflow"], "Flujo de Efectivo", "Free Cash Flow")

                except Exception as e:
                    st.error(f"❌ Error cargando estados financieros: {e}")

            # ── FSUB 4: COMPARAR PEERS ────────────────────────────────────────────
            with fsub4:
                try:
                    import pandas as _pd4
                    from src.fundamentals import comparar_peers

                    _RATIOS_LABEL = {
                        "PE_trailing":    "PE Trailing",
                        "PB":             "P/B",
                        "PS":             "P/S",
                        "EV_EBITDA":      "EV/EBITDA",
                        "ROE_%":          "ROE %",
                        "ROA_%":          "ROA %",
                        "Margen_Neto_%":  "Mg Neto %",
                        "Debt_Equity":    "Debt/Equity",
                        "Beta":           "Beta",
                    }
                    _MENOR_ES_MEJOR = {"PE_trailing", "PB", "PS", "EV_EBITDA", "Debt_Equity", "Beta"}

                    st.markdown(
                        "Ingresá tickers adicionales para comparar con **{}**.".format(ticker)
                    )
                    _peers_raw = st.text_input(
                        "Tickers (separados por coma)",
                        value="",
                        placeholder="Ej: AAPL, MSFT, GOOGL",
                        key="peers_input",
                    )
                    _ratios_sel4 = st.multiselect(
                        "Ratios a incluir",
                        options=list(_RATIOS_LABEL.keys()),
                        default=list(_RATIOS_LABEL.keys()),
                        format_func=lambda x: _RATIOS_LABEL[x],
                        key="peers_ratios",
                    )

                    if st.button("🔍 Comparar", key="peers_btn"):
                        _extra = [tk.strip().upper() for tk in _peers_raw.split(",") if tk.strip()]
                        _all_tk = [ticker.upper()] + [tk for tk in _extra if tk != ticker.upper()]

                        if len(_all_tk) < 2:
                            st.warning("Ingresá al menos un ticker adicional para comparar.")
                        elif not _ratios_sel4:
                            st.warning("Seleccioná al menos un ratio.")
                        else:
                            with st.spinner(f"Descargando datos de {', '.join(_all_tk)}..."):
                                _df_peers = comparar_peers(_all_tk, _ratios_sel4)

                            if _df_peers is None or _df_peers.empty:
                                st.warning("No se pudieron obtener datos de los peers.")
                            else:
                                def _hl_peers(df):
                                    styles = _pd4.DataFrame("", index=df.index, columns=df.columns)
                                    for _col in df.columns:
                                        if _col == "Ticker":
                                            continue
                                        _s = _pd4.to_numeric(df[_col], errors="coerce")
                                        if _s.isna().all():
                                            continue
                                        _valid = _s.dropna()
                                        if _valid.empty:
                                            continue
                                        if _col in _MENOR_ES_MEJOR:
                                            _bi = _valid.idxmin()
                                            _wi = _valid.idxmax()
                                        else:
                                            _bi = _valid.idxmax()
                                            _wi = _valid.idxmin()
                                        styles.loc[_bi, _col] = "background-color:#DCFCE7;color:#166534;font-weight:bold;"
                                        styles.loc[_wi, _col] = "background-color:#FEE2E2;color:#991B1B;"
                                    return styles

                                _fmt_peers = {
                                    col: "{:.2f}"
                                    for col in _df_peers.columns if col != "Ticker"
                                }
                                st.dataframe(
                                    _df_peers.style
                                    .apply(_hl_peers, axis=None)
                                    .format(_fmt_peers, na_rep="—"),
                                    use_container_width=True,
                                    hide_index=True,
                                )

                                # Resumen automático
                                st.markdown("---")
                                st.markdown("**Resumen vs peers:**")
                                for _r4 in _ratios_sel4:
                                    if _r4 not in _df_peers.columns:
                                        continue
                                    _s4 = _pd4.to_numeric(_df_peers[_r4], errors="coerce")
                                    if _s4.isna().all():
                                        continue
                                    _vld = _s4.dropna()
                                    if _vld.empty:
                                        continue
                                    if _r4 in _MENOR_ES_MEJOR:
                                        _bi4, _wi4 = _vld.idxmin(), _vld.idxmax()
                                    else:
                                        _bi4, _wi4 = _vld.idxmax(), _vld.idxmin()
                                    _bt4 = _df_peers.loc[_bi4, "Ticker"]
                                    _wt4 = _df_peers.loc[_wi4, "Ticker"]
                                    _lbl4 = _RATIOS_LABEL.get(_r4, _r4)
                                    st.caption(
                                        f"**{_lbl4}**: mejor → {_bt4} ({_s4[_bi4]:.2f}) | "
                                        f"peor → {_wt4} ({_s4[_wi4]:.2f})"
                                    )

                except Exception as e:
                    st.error(f"❌ Error en comparación de peers: {e}")

# TAB 3: TECNICO
if tab3 is not None:
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

                    _boll_ancho = banda_sup - banda_inf
                    posicion_banda = ((precio - banda_inf) / _boll_ancho * 100) if _boll_ancho != 0 else 50.0

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
                        paper_bgcolor='#131722',
                        plot_bgcolor='#1e222d',
                        font_color='#d1d4dc',
                        height=500,
                        hovermode='x unified',
                        xaxis_title='Fecha',
                        yaxis_title='Precio',
                        xaxis=dict(gridcolor='#2a2e39', linecolor='#2a2e39'),
                        yaxis=dict(gridcolor='#2a2e39', linecolor='#2a2e39'),
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
                        paper_bgcolor='#131722',
                        plot_bgcolor='#1e222d',
                        font_color='#d1d4dc',
                        height=300,
                        yaxis_range=[0, 100],
                        xaxis=dict(gridcolor='#2a2e39', linecolor='#2a2e39'),
                        yaxis=dict(gridcolor='#2a2e39', linecolor='#2a2e39'),
                    )
                    st.plotly_chart(fig_rsi, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error en analisis tecnico: {e}")

# TAB 4: MI PORTFOLIO
if tab4 is not None:
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
        except Exception as e:
            st.error(f"❌ Error cargando el portfolio: {e}")
            portfolio = None

        if portfolio is None:
            st.error("Error cargando el portfolio. Recargá la página.")
            st.stop()

        # Aviso sesión: datos no persisten entre visitas
        _tiene_posiciones = len(portfolio.get("posiciones", [])) > 0
        if not _tiene_posiciones:
            st.info(
                "**Tu cartera está vacía.**\n\n"
                "Agregá posiciones en la pestaña **✏️ Gestionar Portfolio** "
                "o importá un JSON guardado previamente.\n\n"
                "⚠️ Los datos se guardan **solo en esta sesión del navegador** — "
                "si cerrás la pestaña, se borran. Usá el botón **Exportar** para guardar tu cartera."
            )
        else:
            st.caption(
                "ℹ️ Los datos se guardan en esta sesión. Usá **Exportar cartera** antes de cerrar."
            )

        if True:  # estructura preservada
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
            _port_sk = st.empty()
            with _port_sk:
                show_skeleton(rows=2)
            try:
                portfolio_live = actualizar_precios_actuales(portfolio)
            except Exception as e:
                st.warning(f"No se pudo refrescar precios desde yfinance: {e}")
                portfolio_live = portfolio
            finally:
                _port_sk.empty()

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
                        template="plotly_dark",
                        paper_bgcolor="#131722",
                        plot_bgcolor="#1e222d",
                        font_color="#d1d4dc",
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
                            template="plotly_dark",
                            paper_bgcolor="#131722",
                            plot_bgcolor="#1e222d",
                            font_color="#d1d4dc",
                            height=420,
                            hovermode="x unified",
                            xaxis_title="Fecha",
                            yaxis_title="Indice (base 100)",
                            xaxis=dict(gridcolor="#2a2e39", linecolor="#2a2e39"),
                            yaxis=dict(gridcolor="#2a2e39", linecolor="#2a2e39"),
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

                # ── EXPORTAR / IMPORTAR ───────────────────────────────────────
                st.markdown("#### 💾 Exportar / Importar cartera")
                _io_c1, _io_c2 = st.columns(2)

                with _io_c1:
                    st.download_button(
                        "📥 Exportar mi cartera",
                        data=_json.dumps(portfolio, ensure_ascii=False, indent=2),
                        file_name=f"mi_cartera_{_date.today()}.json",
                        mime="application/json",
                        use_container_width=True,
                        help="Guardá tu cartera como JSON. Podés reimportarla en tu próxima visita.",
                    )

                with _io_c2:
                    _uploaded_port = st.file_uploader(
                        "📤 Importar cartera",
                        type=["json"],
                        key="upload_portfolio",
                        label_visibility="collapsed",
                        help="Subí un JSON exportado previamente para restaurar tu cartera",
                    )
                    if _uploaded_port is not None:
                        try:
                            _imp_data = _json.loads(_uploaded_port.read())
                            if "posiciones" not in _imp_data:
                                st.error("❌ Formato inválido: falta el campo 'posiciones'.")
                            else:
                                _n_imp = len(_imp_data["posiciones"])
                                _n_act = len(portfolio.get("posiciones", []))
                                st.warning(
                                    f"⚠️ Importar **{_n_imp} posiciones** reemplazará "
                                    f"la cartera actual ({_n_act} posiciones). ¿Confirmás?"
                                )
                                if st.button("✅ Confirmar importación", key="btn_import_port"):
                                    guardar_portfolio("pato", _imp_data)
                                    st.success("✅ Cartera importada exitosamente.")
                                    st.rerun()
                        except Exception:
                            st.error("❌ Archivo JSON inválido.")

                st.divider()

                _pos_list = portfolio.get("posiciones", [])

                # ── SECCIÓN 1: TABLA + ELIMINAR ──────────────────────────────────
                st.markdown("#### 📋 Posiciones actuales")

                if not _pos_list:
                    st.info(
                        "No tenés posiciones cargadas todavía. "
                        "Agregá tu primera posición en la sección de abajo, "
                        "o importá una cartera guardada previamente."
                    )
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
        RATIO_CEDEARS, calcular_ccl_implicito,
    )
    from src.dolar import get_cotizacion_by_casa as _get_dolar_casa

    csub1, csub2, csub3, csub4, csub5 = st.tabs([
        "💵 Billetera Virtual",
        "📅 Plazo Fijo / FCI",
        "📊 Bono / TIR",
        "⚖️ Comparador",
        "💱 CCL & CEDEARs",
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

    # ── SUB-TAB 5: CCL & CEDEARs ──────────────────────────────────────────────
    with csub5:
        st.info(
            "💱 El **CCL implícito** se calcula dividiendo el precio del CEDEAR en BYMA "
            "por el precio del ADR en NYSE multiplicado por el ratio de conversión. "
            "Si el CCL implícito es menor al CCL oficial, el CEDEAR puede estar barato en ARS."
        )

        # ── SECCIÓN 1: TABLA EN TIEMPO REAL ───────────────────────────────────
        st.markdown("### 📊 CCL implícito por CEDEAR — tiempo real")

        _ccl_oficial_data = _get_dolar_casa("contadoconliqui")
        _ccl_oficial_v = _ccl_oficial_data.get("venta") if _ccl_oficial_data else None
        _mep_data = _get_dolar_casa("bolsa")
        _mep_v = _mep_data.get("venta") if _mep_data else None
        _blue_data = _get_dolar_casa("blue")
        _blue_v = _blue_data.get("venta") if _blue_data else None

        if _ccl_oficial_v:
            _ref_cols = st.columns(3)
            _ref_cols[0].metric("CCL Oficial (venta)", f"$ {_ccl_oficial_v:,.0f}")
            _ref_cols[1].metric("MEP (venta)", f"$ {_mep_v:,.0f}" if _mep_v else "—")
            _ref_cols[2].metric("Blue (venta)", f"$ {_blue_v:,.0f}" if _blue_v else "—")
        else:
            st.warning("No se pudo obtener la cotización del CCL oficial.")

        st.divider()

        _tabla_filas = []
        _mejor_diff = None
        _mejor_ticker = None

        for _sym, _info in RATIO_CEDEARS.items():
            _res = calcular_ccl_implicito(_info["adr"], _info["local"], _info["ratio"])
            _ccl_imp = _res["ccl_implicito"]
            if _ccl_imp and _ccl_oficial_v:
                _diff_pct = (_ccl_imp - _ccl_oficial_v) / _ccl_oficial_v * 100
                if _mejor_diff is None or abs(_diff_pct) < abs(_mejor_diff):
                    _mejor_diff = _diff_pct
                    _mejor_ticker = _sym
            else:
                _diff_pct = None
            _tabla_filas.append({
                "Ticker": _sym,
                "Precio NYSE (USD)": _res["precio_nyse"],
                "Precio BYMA (ARS)": _res["precio_byma"],
                "Ratio": _info["ratio"],
                "CCL Implícito": _ccl_imp,
                "vs CCL Oficial (%)": _diff_pct,
            })

        _df_ccl = pd.DataFrame(_tabla_filas)

        def _color_ccl_diff(val):
            if val is None or (isinstance(val, float) and pd.isna(val)):
                return ""
            if val < 0:
                return "color: #166534; font-weight: 600;"
            if val > 0:
                return "color: #991B1B; font-weight: 600;"
            return ""

        def _bg_mejor(row):
            if row["Ticker"] == _mejor_ticker:
                return ["background-color: #FEF9C3;"] * len(row)
            return [""] * len(row)

        _fmt_ccl = {
            "Precio NYSE (USD)": lambda x: f"USD {x:,.2f}" if x else "—",
            "Precio BYMA (ARS)": lambda x: f"$ {x:,.1f}" if x else "—",
            "CCL Implícito": lambda x: f"$ {x:,.2f}" if x else "—",
            "vs CCL Oficial (%)": lambda x: f"{x:+.1f}%" if x is not None and not (isinstance(x, float) and pd.isna(x)) else "—",
        }

        _styled_ccl = (
            _df_ccl.style
            .apply(_bg_mejor, axis=1)
            .map(_color_ccl_diff, subset=["vs CCL Oficial (%)"])
            .format(_fmt_ccl)
        )
        st.dataframe(_styled_ccl, use_container_width=True, hide_index=True)

        if _mejor_ticker:
            _tag = "por debajo" if _mejor_diff < 0 else "por encima"
            st.caption(
                f"⭐ **{_mejor_ticker}** es el CEDEAR con menor diferencia vs CCL oficial "
                f"({_mejor_diff:+.1f}% {_tag}). Fila amarilla en la tabla."
            )
        st.caption("🟢 Verde = CCL implícito < CCL oficial (CEDEAR barato en ARS) | "
                   "🔴 Rojo = CCL implícito > CCL oficial (CEDEAR caro en ARS)")

        # ── SECCIÓN 2: CALCULADORA MANUAL ────────────────────────────────────
        st.divider()
        st.markdown("### 🧮 Calculadora manual de CCL")

        _calc_c1, _calc_c2 = st.columns([1, 1])
        with _calc_c1:
            _modo_calc = st.radio(
                "Modo de ingreso",
                ["Elegir CEDEAR de la lista", "Ingresar manualmente"],
                key="ccl_modo",
                horizontal=True,
            )

        if _modo_calc == "Elegir CEDEAR de la lista":
            with _calc_c1:
                _sel_ticker = st.selectbox(
                    "CEDEAR", list(RATIO_CEDEARS.keys()), key="ccl_sel_ticker"
                )
            _sel_info = RATIO_CEDEARS[_sel_ticker]
            _sel_res = calcular_ccl_implicito(
                _sel_info["adr"], _sel_info["local"], _sel_info["ratio"]
            )
            _inp_nyse = _sel_res["precio_nyse"] or 0.0
            _inp_byma = _sel_res["precio_byma"] or 0.0
            _inp_ratio = float(_sel_info["ratio"])
        else:
            with _calc_c1:
                _inp_nyse = st.number_input(
                    "Precio NYSE (USD)", min_value=0.01, value=10.0, step=0.01, key="ccl_nyse"
                )
                _inp_byma = st.number_input(
                    "Precio BYMA (ARS)", min_value=0.01, value=10000.0, step=10.0, key="ccl_byma"
                )
                _inp_ratio = st.number_input(
                    "Ratio de conversión", min_value=1, value=10, step=1, key="ccl_ratio"
                )

        _calc_ccl_imp = round(_inp_byma / (_inp_nyse * _inp_ratio), 2) if _inp_nyse and _inp_ratio else None

        with _calc_c2:
            st.markdown("**Resultado**")
            if _calc_ccl_imp:
                st.metric("CCL Implícito calculado", f"$ {_calc_ccl_imp:,.2f}")
                _refs = {
                    "CCL Oficial": _ccl_oficial_v,
                    "MEP": _mep_v,
                    "Blue": _blue_v,
                }
                for _nombre_ref, _val_ref in _refs.items():
                    if _val_ref:
                        _d = (_calc_ccl_imp - _val_ref) / _val_ref * 100
                        _texto = f"{_d:+.1f}% {'sobre' if _d > 0 else 'bajo'} el {_nombre_ref}"
                        st.caption(_texto)
                if _ccl_oficial_v:
                    _d_of = (_calc_ccl_imp - _ccl_oficial_v) / _ccl_oficial_v * 100
                    if _d_of < -2:
                        st.success(f"✅ Este CEDEAR cotiza {abs(_d_of):.1f}% **por debajo** del CCL oficial → posible oportunidad.")
                    elif _d_of > 2:
                        st.warning(f"⚠️ Este CEDEAR cotiza {_d_of:.1f}% **por encima** del CCL oficial → está caro en ARS.")
                    else:
                        st.info("↔️ Este CEDEAR cotiza alineado con el CCL oficial (diferencia < 2%).")
            else:
                st.warning("Completá los precios para calcular.")

        # ── SECCIÓN 3: ¿CUÁNTOS CEDEARs NECESITO? ────────────────────────────
        st.divider()
        st.markdown("### 🔢 ¿Cuántos CEDEARs necesito?")

        _need_c1, _need_c2 = st.columns([1, 1])
        with _need_c1:
            _need_ticker = st.selectbox(
                "Empresa (CEDEAR)", list(RATIO_CEDEARS.keys()), key="ccl_need_ticker"
            )
            _need_monto_usd = st.number_input(
                "Monto a invertir (USD)", min_value=1.0, value=1000.0, step=100.0, key="ccl_need_usd"
            )

        _need_info = RATIO_CEDEARS[_need_ticker]
        _need_res = calcular_ccl_implicito(
            _need_info["adr"], _need_info["local"], _need_info["ratio"]
        )
        _need_precio_byma = _need_res["precio_byma"]
        _need_ccl = _calc_ccl_imp if _modo_calc == "Elegir CEDEAR de la lista" and _sel_ticker == _need_ticker else _need_res["ccl_implicito"]
        _ccl_para_conv = _need_ccl or _ccl_oficial_v

        with _need_c2:
            st.markdown("**Resultado**")
            if _need_precio_byma and _ccl_para_conv and _need_precio_byma > 0:
                _monto_ars = _need_monto_usd * _ccl_para_conv
                _cedears_necesarios = int(_monto_ars / _need_precio_byma)
                _acciones_nyse = round(_cedears_necesarios / _need_info["ratio"], 4)
                _costo_ars_real = _cedears_necesarios * _need_precio_byma
                _costo_usd_real = round(_costo_ars_real / _ccl_para_conv, 2)

                _r1, _r2 = st.columns(2)
                _r1.metric("CEDEARs a comprar", f"{_cedears_necesarios:,}")
                _r2.metric("Equivale a (NYSE)", f"{_acciones_nyse} acciones")
                _r3, _r4 = st.columns(2)
                _r3.metric("Costo en ARS", f"$ {_costo_ars_real:,.0f}")
                _r4.metric("Costo en USD (al CCL)", f"USD {_costo_usd_real:,.2f}")
                st.caption(
                    f"Usando CCL {'implícito' if _need_ccl else 'oficial'}: $ {_ccl_para_conv:,.2f} | "
                    f"Precio CEDEAR: $ {_need_precio_byma:,.1f} | Ratio: {_need_info['ratio']}:1"
                )
            else:
                st.warning("No se pudo obtener el precio del CEDEAR. Intentá de nuevo en unos segundos.")

# TAB 6: MACRO ARGENTINA
with tab6:
    import plotly.graph_objects as _go6
    import pandas as _pd6
    from datetime import datetime as _dt6, timedelta as _td6
    from src.macro import get_riesgo_pais, get_dolar_historico, get_tasas_bcra
    from src.dolar import get_cotizaciones as _get_cots6, format_cotizacion as _fmt_cot6

    st.subheader("🇦🇷 Indicadores macro Argentina")

    # ── SECCIÓN 1: MÉTRICAS DEL DÍA ──────────────────────────────────────────
    st.markdown("### 📊 Indicadores del día")

    _m6c1, _m6c2, _m6c3, _m6c4 = st.columns(4)

    # Cargar tasas una vez para usar en métricas y en la tabla de la sección 4
    _tasas6 = get_tasas_bcra()
    if _tasas6 is None:
        _tasas6 = {
            "tasa_politica": None,
            "tasa_politica_fecha": None,
            "tasa_plazo_fijo": None,
            "fallback": True,
        }

    # Riesgo País
    _rp_all = get_riesgo_pais()
    with _m6c1:
        if _rp_all is not None and not _rp_all.empty:
            _rp_actual = int(_rp_all["valor"].iloc[-1])
            _rp_fecha = _rp_all["fecha"].iloc[-1].strftime("%d/%m")
            _rp_delta = None
            if len(_rp_all) >= 2:
                _rp_delta = _rp_actual - int(_rp_all["valor"].iloc[-2])
            st.metric(
                f"Riesgo País — {_rp_fecha}",
                f"{_rp_actual:,} bps",
                delta=f"{_rp_delta:+d}" if _rp_delta is not None else None,
                delta_color="inverse",
                help="EMBI+. Verde = baja (mejora), Rojo = sube (empeora). Dato: argentinadatos.com",
            )
        else:
            st.metric("Riesgo País (EMBI)", "—")
            st.caption("No disponible")

    # Tasa de referencia depósitos 30d (proxy tasa política monetaria)
    with _m6c2:
        _tp = _tasas6["tasa_politica"]
        _tp_fecha = _tasas6.get("tasa_politica_fecha")
        _tp_label = f"Dep. 30d BCRA — {_tp_fecha[5:] if _tp_fecha else 'N/D'}"
        _tp_help = (
            "Tasa de depósitos a 30 días del BCRA (proxy de tasa de referencia). "
            "Fuente: argentinadatos.com"
            if not _tasas6["fallback"] else
            "Dato hardcodeado (API no disponible). Actualizar manualmente si cambia mucho."
        )
        st.metric(
            _tp_label,
            f"{_tp:.1f}% TNA" if _tp is not None else "—",
            help=_tp_help,
        )
        if _tasas6["fallback"]:
            st.caption("⚠ Valor de referencia")

    # Tasa plazo fijo 30d (promedio entidades privadas)
    with _m6c3:
        _tpf = _tasas6["tasa_plazo_fijo"]
        _tpf_help = (
            "Promedio TNA clientes de 30 entidades (argentinadatos.com/v1/finanzas/tasas/plazoFijo)."
            if not _tasas6["fallback"] else
            "Dato hardcodeado (API no disponible). Actualizar manualmente si cambia mucho."
        )
        st.metric(
            "Plazo Fijo 30d (prom.)",
            f"{_tpf:.1f}% TNA" if _tpf is not None else "—",
            help=_tpf_help,
        )
        if _tasas6["fallback"]:
            st.caption("⚠ Valor de referencia")

    # Brecha cambiaria blue/oficial
    with _m6c4:
        try:
            _cots6 = _get_cots6()
            if _cots6:
                _d6 = {item["casa"]: item for item in _cots6}
                _ofic6 = _d6.get("oficial", {}).get("venta")
                _blue6 = _d6.get("blue", {}).get("venta")
                if _ofic6 and _blue6:
                    _brecha6 = ((_blue6 - _ofic6) / _ofic6) * 100
                    st.metric(
                        "Brecha Blue/Oficial",
                        f"{_brecha6:.1f}%",
                        delta=f"Blue {_fmt_cot6(_blue6)} | Ofic {_fmt_cot6(_ofic6)}",
                        delta_color="off",
                        help="((Blue - Oficial) / Oficial) * 100. Fuente: dolarapi.com",
                    )
                else:
                    st.metric("Brecha Blue/Oficial", "—")
            else:
                st.metric("Brecha Blue/Oficial", "—")
                st.caption("Sin conexión")
        except Exception:
            st.metric("Brecha Blue/Oficial", "—")

    st.divider()

    # ── SECCIÓN 2: RIESGO PAÍS HISTÓRICO ─────────────────────────────────────
    st.markdown("### 📈 Riesgo País histórico (EMBI)")

    _periodo_rp = st.radio(
        "Período",
        ["1M", "3M", "6M", "1Y"],
        horizontal=True,
        index=3,
        key="macro_periodo_rp",
    )
    _dias_rp = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365}[_periodo_rp]

    if _rp_all is None or _rp_all.empty:
        st.warning("Datos de riesgo país no disponibles temporalmente.")
    else:
        _desde_rp = _dt6.now() - _td6(days=_dias_rp)
        _rp_hist = _rp_all[_rp_all["fecha"] >= _desde_rp].copy()

        if _rp_hist.empty:
            st.warning("Sin datos para el período seleccionado.")
        else:
            _fig_rp = _go6.Figure()
            _fig_rp.add_trace(_go6.Scatter(
                x=_rp_hist["fecha"],
                y=_rp_hist["valor"],
                line=dict(color="#2563EB", width=2),
                fill="tozeroy",
                fillcolor="rgba(37,99,235,0.08)",
                name="EMBI",
                hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Riesgo País: %{y:,.0f} bps<extra></extra>",
            ))
            _fig_rp.add_hline(
                y=2000,
                line_dash="dot",
                line_color="#EF4444",
                annotation_text="Zona stress (2000 bps)",
                annotation_position="top right",
                annotation_font_color="#EF4444",
                annotation_font_size=11,
            )
            _fig_rp.update_layout(
                title=f"Riesgo País (EMBI) — Últimos {_dias_rp} días",
                xaxis_title="Fecha",
                yaxis_title="Puntos básicos (bps)",
                template="plotly_white",
                height=420,
                hovermode="x unified",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(_fig_rp, use_container_width=True)
            _rp_ult_fecha = _rp_all["fecha"].iloc[-1].strftime("%d/%m/%Y")
            _rp_ult_val = int(_rp_all["valor"].iloc[-1])
            st.caption(
                f"Fuente: argentinadatos.com · Último dato disponible: "
                f"{_rp_ult_fecha} ({_rp_ult_val:,} bps) · Cache: 1 hora"
            )

    st.divider()

    # ── SECCIÓN 3: DÓLAR HISTÓRICO COMPARATIVO ────────────────────────────────
    st.markdown("### 💵 Evolución tipos de cambio")

    _periodo_dol = st.radio(
        "Período",
        ["1M", "3M", "6M", "1Y"],
        horizontal=True,
        index=2,
        key="macro_periodo_dol",
    )
    _dias_dol = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365}[_periodo_dol]

    _chk1, _chk2, _chk3, _chk4 = st.columns(4)
    _show_oficial = _chk1.checkbox("Oficial", value=True, key="dol_oficial")
    _show_blue    = _chk2.checkbox("Blue",    value=True, key="dol_blue")
    _show_mep     = _chk3.checkbox("MEP",     value=True, key="dol_mep")
    _show_ccl     = _chk4.checkbox("CCL",     value=True, key="dol_ccl")

    _casas_config6 = [
        ("oficial",         "Oficial", "#6B7280", _show_oficial),
        ("blue",            "Blue",    "#2563EB", _show_blue),
        ("bolsa",           "MEP",     "#16A34A", _show_mep),
        ("contadoconliqui", "CCL",     "#F59E0B", _show_ccl),
    ]

    _fig_dol = _go6.Figure()
    _hay_datos_dol = False
    _desde_dol = _dt6.now() - _td6(days=_dias_dol)

    for _casa6, _nombre6, _color6, _mostrar6 in _casas_config6:
        if not _mostrar6:
            continue
        try:
            _df6 = get_dolar_historico(casa=_casa6)
            if _df6 is None or _df6.empty:
                continue
            _df6_f = _df6[_df6["fecha"] >= _desde_dol]
            if _df6_f.empty:
                continue
            _hay_datos_dol = True
            _fig_dol.add_trace(_go6.Scatter(
                x=_df6_f["fecha"],
                y=_df6_f["venta"],
                line=dict(color=_color6, width=2),
                name=_nombre6,
                hovertemplate=(
                    f"<b>{_nombre6}</b><br>"
                    "%{x|%d/%m/%Y}<br>"
                    "Venta: $%{y:,.0f}<extra></extra>"
                ),
            ))
        except Exception:
            continue

    if not _hay_datos_dol:
        st.warning("Datos de tipos de cambio no disponibles temporalmente.")
    else:
        _fig_dol.update_layout(
            title="Evolución tipos de cambio (precio venta, ARS/USD)",
            xaxis_title="Fecha",
            yaxis_title="ARS / USD",
            template="plotly_white",
            height=450,
            hovermode="x unified",
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(_fig_dol, use_container_width=True)
        st.caption("Fuente: argentinadatos.com · Precio de venta · Cache: 1 hora")

    st.divider()

    # ── SECCIÓN 4: TASAS ──────────────────────────────────────────────────────
    st.markdown("### 📋 Tasas de referencia")

    if _tasas6["fallback"]:
        st.warning(
            "⚠ Algunos datos son valores de referencia hardcodeados "
            "(API argentinadatos.com no disponible temporalmente). "
            "Actualizá manualmente en src/macro.py si la tasa cambia mucho.",
        )

    def _tea_mensual(tna_pct):
        return ((1 + tna_pct / 100 / 12) ** 12 - 1) * 100

    def _tea_diaria(tna_pct):
        return ((1 + tna_pct / 100 / 365) ** 365 - 1) * 100

    _tp_val  = _tasas6["tasa_politica"]
    _tpf_val = _tasas6["tasa_plazo_fijo"]
    _tp_fecha_str = _tasas6.get("tasa_politica_fecha") or "referencia"
    _es_fb = _tasas6["fallback"]

    def _fmt_tna(v):
        return f"{v:.2f}%" if v is not None else "—"

    def _fmt_tea_m(v):
        return f"{_tea_mensual(v):.2f}%" if v is not None else "—"

    def _fmt_tea_d(v):
        return f"{_tea_diaria(v):.2f}%" if v is not None else "—"

    _tasas_data = [
        {
            "Instrumento":     f"Depósitos 30d BCRA ({_tp_fecha_str})",
            "TNA actual":      _fmt_tna(_tp_val),
            "TEA equivalente": _fmt_tea_m(_tp_val),
            "Capitalización":  "Mensual",
            "Fuente":          "argentinadatos.com" if not _es_fb else "⚠ Hardcodeado",
        },
        {
            "Instrumento":     "Plazo Fijo 30d (prom. entidades)",
            "TNA actual":      _fmt_tna(_tpf_val),
            "TEA equivalente": _fmt_tea_m(_tpf_val),
            "Capitalización":  "Mensual",
            "Fuente":          "argentinadatos.com" if not _es_fb else "⚠ Hardcodeado",
        },
        {
            "Instrumento":     "FCI Money Market (referencia)",
            "TNA actual":      _fmt_tna(_tpf_val),
            "TEA equivalente": _fmt_tea_d(_tpf_val),
            "Capitalización":  "Diaria",
            "Fuente":          "Estimado (misma TNA que plazo fijo)",
        },
    ]
    st.dataframe(
        _pd6.DataFrame(_tasas_data),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "TEA mensual = (1 + TNA/12)^12 − 1 | TEA diaria = (1 + TNA/365)^365 − 1"
    )

    st.markdown("#### Calculadora rápida TNA → TEA")
    st.caption("Ingresá una tasa manualmente para calcular el equivalente anual efectivo.")

    _calc_c1, _calc_c2, _calc_c3 = st.columns(3)
    with _calc_c1:
        _tna_input = st.number_input(
            "TNA %", min_value=0.0, max_value=500.0, value=38.0,
            step=0.5, key="macro_tna_calc",
        )
    with _calc_c2:
        _cap_tipo = st.selectbox(
            "Capitalización",
            ["Diaria (billetera/FCI)", "Mensual (plazo fijo)"],
            key="macro_cap_tipo",
        )
    with _calc_c3:
        st.write("")
        if "Diaria" in _cap_tipo:
            _tea_calc = ((1 + _tna_input / 100 / 365) ** 365 - 1) * 100
        else:
            _tea_calc = ((1 + _tna_input / 100 / 12) ** 12 - 1) * 100
        st.metric("TEA resultante", f"{_tea_calc:.2f}%")

# TAB 7: DCF & VALUACIÓN
if tab7 is not None:
    with tab7:
        if not datos:
            st.info("👈 Escribí un ticker en el buscador para iniciar el DCF.")
        else:
            import plotly.graph_objects as _go7
            import pandas as _pd7
            from src.dcf import (
                get_datos_base_dcf, calcular_dcf as _calc_dcf,
                tabla_sensibilidad as _tabla_sens,
                calcular_escenarios as _calc_esc,
                calcular_wacc_automatico as _calc_wacc_auto,
            )

            st.subheader(f"📐 DCF & Valuación — {ticker}")
            st.caption(
                "Descuento de Flujos de Caja (DCF). Valores en USD salvo indicación. "
                "Los sliders actualizan los resultados en tiempo real."
            )

            # ── SECCIÓN 0: PRIMA DE RIESGO (input antes de cargar WACC) ─────────
            if "dcf_erp" not in st.session_state:
                st.session_state["dcf_erp"] = 4.5
            _erp7 = st.number_input(
                "Prima de riesgo de mercado / ERP (%)",
                min_value=1.0, max_value=15.0,
                step=0.5, format="%.1f",
                key="dcf_erp",
                help=(
                    "Retorno histórico extra del mercado sobre la tasa libre de riesgo. "
                    "Damodaran USA: ~4.5-5.5%. "
                    "Para mercados emergentes puede usarse 6-8%."
                ),
            ) / 100

            # ── SECCIÓN 1: DATOS BASE ─────────────────────────────────────────────
            st.markdown("### 📋 Datos base")

            if st.button("🔄 Recargar datos", key="dcf_reload_btn"):
                get_datos_base_dcf.clear()
                _calc_wacc_auto.clear()

            _db7 = get_datos_base_dcf(ticker)

            if _db7 is None:
                st.error(
                    "No se pudieron cargar los datos base desde yfinance. "
                    "Verificá el ticker o tu conexión."
                )
            else:
                _cur7 = _db7.get("currency", "USD")
                _sym7 = "$"

                _db_c1, _db_c2, _db_c3, _db_c4, _db_c5 = st.columns(5)

                _fcf7_raw = _db7.get("fcf_base")
                _fcf7_anio = _db7.get("fcf_anio", "")
                _fcf7_neg  = _db7.get("fcf_negativo", False) or _fcf7_raw is None
                _fcf7_fmt  = f"{_sym7}{_fcf7_raw/1e9:.3f}B" if _fcf7_raw is not None else "N/D"

                _db_c1.metric(
                    f"FCF {_fcf7_anio} ({_cur7})",
                    _fcf7_fmt,
                    help="Free Cash Flow del estado de flujos. Si es negativo, ingresalo manualmente abajo.",
                )
                if _fcf7_neg:
                    _db_c1.caption("⚠ FCF ≤ 0")

                _sh7_raw = _db7.get("shares")
                _db_c2.metric(
                    "Shares outstanding",
                    f"{_sh7_raw/1e6:.1f}M" if _sh7_raw else "N/D",
                )

                _px7 = _db7.get("precio_actual")
                _db_c3.metric("Precio actual", f"${_px7:.2f}" if _px7 else "N/D")

                _deu7_raw = _db7.get("deuda") or 0
                _csh7_raw = _db7.get("cash") or 0
                _dn7 = _deu7_raw - _csh7_raw
                _db_c4.metric(
                    f"Deuda neta ({_cur7})",
                    f"{_sym7}{_dn7/1e9:.2f}B",
                    delta="Deuda − Cash",
                    delta_color="off",
                )

                _beta7 = _db7.get("beta")
                _db_c5.metric("Beta", f"{_beta7:.2f}" if _beta7 else "N/D")

                # Historial FCF si hay más de un año
                _fcf7_serie = _db7.get("fcf_serie", {})
                if len(_fcf7_serie) > 1:
                    _hist_str = " | ".join(
                        f"{yr}: ${v/1e9:.2f}B" for yr, v in sorted(_fcf7_serie.items(), reverse=True)
                    )
                    st.caption(f"Historial FCF: {_hist_str} ({_cur7})")

                st.caption(
                    "Datos auto-cargados desde yfinance. "
                    "Podés editarlos manualmente en los supuestos de abajo."
                )

                st.divider()

                # ── SECCIÓN 2: SUPUESTOS ──────────────────────────────────────────
                st.markdown("### ⚙️ Supuestos")

                # Años de proyección antes de los sliders (determina si mostrar g2)
                _años7 = st.radio(
                    "Años de proyección",
                    [5, 10],
                    index=1,
                    horizontal=True,
                    key="dcf_años",
                )

                _s2c1, _s2c2, _s2c3 = st.columns(3)

                with _s2c1:
                    st.markdown("**Crecimiento FCF**")

                    if _fcf7_neg:
                        st.warning(
                            "FCF negativo o no disponible. "
                            f"Último registrado: {_fcf7_fmt}. "
                            "Ingresá un valor base normalizado:"
                        )
                        _fcf7_manual = st.number_input(
                            f"FCF base ({_cur7}, en millones)",
                            min_value=1.0,
                            value=max(abs(_fcf7_raw) / 1e6, 10.0) if _fcf7_raw else 100.0,
                            step=10.0,
                            format="%.1f",
                            key="dcf_fcf_manual",
                            help="Ingresá el FCF normalizado que usarás como punto de partida.",
                        )
                        _fcf7_usar = _fcf7_manual * 1e6
                    else:
                        _fcf7_usar = _fcf7_raw

                    _g1_7 = st.slider(
                        "Crecimiento años 1–5 (%)",
                        min_value=0, max_value=50, value=15, step=1,
                        key="dcf_g1",
                    ) / 100

                    if _años7 == 10:
                        _g2_7 = st.slider(
                            "Crecimiento años 6–10 (%)",
                            min_value=0, max_value=30, value=8, step=1,
                            key="dcf_g2",
                        ) / 100
                    else:
                        _g2_7 = _g1_7
                        st.caption(f"Con 5 años se usa {_g1_7*100:.0f}% todo el período.")

                with _s2c2:
                    st.markdown("**WACC (Tasa de descuento)**")

                    # Calcular WACC automático (cacheado 1 h)
                    with st.spinner("Calculando WACC automático..."):
                        _wacc_data7 = _calc_wacc_auto(ticker, erp=_erp7)
                    _wacc_auto7 = _wacc_data7.get("wacc")

                    # Advertencias de datos faltantes
                    _adv7 = _wacc_data7.get("advertencias", [])
                    if _adv7:
                        with st.expander(f"⚠ {len(_adv7)} aviso(s) — datos incompletos", expanded=False):
                            for _a7 in _adv7:
                                st.caption(f"• {_a7}")

                    # Desglose de componentes
                    if _wacc_auto7 is not None:
                        with st.expander("Ver componentes del WACC", expanded=False):
                            _rf7   = _wacc_data7.get("rf", 0)
                            _b7    = _wacc_data7.get("beta", 0)
                            _re7c  = _wacc_data7.get("re", 0)
                            _rd7c  = _wacc_data7.get("rd", 0)
                            _t7c   = _wacc_data7.get("tax_rate", 0)
                            _ew7   = _wacc_data7.get("e_weight", 0)
                            _dw7   = _wacc_data7.get("d_weight", 0)
                            st.markdown(
                                f"| | |\n|---|---|\n"
                                f"| Rf (^TNX 10Y) | {_rf7*100:.2f}% |\n"
                                f"| Beta | {_b7:.2f} |\n"
                                f"| ERP | {_erp7*100:.1f}% |\n"
                                f"| **Re = Rf + β×ERP** | **{_re7c*100:.2f}%** |\n"
                                f"| Rd (costo deuda) | {_rd7c*100:.2f}% |\n"
                                f"| Tasa impositiva T | {_t7c*100:.1f}% |\n"
                                f"| Peso equity E/V | {_ew7*100:.1f}% |\n"
                                f"| Peso deuda D/V | {_dw7*100:.1f}% |\n"
                                f"| **WACC calculado** | **{_wacc_auto7*100:.2f}%** |"
                            )

                    # WACC editable: pre-llenado con el valor calculado.
                    # Resetear al auto-WACC si cambió el ticker.
                    _wacc7_default = round(_wacc_auto7 * 100, 1) if _wacc_auto7 else 10.0
                    if st.session_state.get("dcf_wacc_ticker") != ticker:
                        st.session_state["dcf_wacc_ticker"] = ticker
                        st.session_state["dcf_wacc"] = _wacc7_default
                    elif "dcf_wacc" not in st.session_state:
                        st.session_state["dcf_wacc"] = _wacc7_default

                    _wacc7 = st.number_input(
                        "WACC (%)",
                        min_value=1.0, max_value=40.0,
                        step=0.5, format="%.1f",
                        key="dcf_wacc",
                        help=(
                            "Precalculado con CAPM usando beta, Rf (^TNX) y ERP. "
                            "Podés editarlo manualmente."
                        ),
                    ) / 100
                    if _wacc_auto7:
                        st.caption(f"Auto: {_wacc_auto7*100:.2f}% · Actual: {_wacc7*100:.1f}%")

                    _tg7 = st.slider(
                        "Crecimiento terminal / perpetuidad (%)",
                        min_value=1, max_value=6, value=3, step=1,
                        key="dcf_tg",
                    ) / 100

                with _s2c3:
                    st.markdown("**Otros**")
                    _margen7 = st.slider(
                        "Margen de seguridad (%)",
                        min_value=0, max_value=40, value=20, step=5,
                        key="dcf_margen",
                    ) / 100

                    # Shares: manual si no viene de yfinance
                    if not _sh7_raw:
                        st.warning("Shares no disponibles — ingresá manualmente:")
                        _sh7_usar = st.number_input(
                            "Shares (millones)",
                            min_value=0.1, value=100.0, step=10.0,
                            key="dcf_shares_manual",
                        ) * 1e6
                    else:
                        _sh7_usar = _sh7_raw

                # Validación WACC > tg
                if _wacc7 <= _tg7:
                    st.error(
                        f"WACC ({_wacc7*100:.1f}%) debe ser mayor que la tasa terminal "
                        f"({_tg7*100:.0f}%). Ajustá los valores para continuar."
                    )
                else:
                    st.divider()

                    # ── CÁLCULO CENTRAL ───────────────────────────────────────────
                    try:
                        _res7 = _calc_dcf(
                            _fcf7_usar, _g1_7, _g2_7, _wacc7, _tg7,
                            _años7, _sh7_usar, _deu7_raw, _csh7_raw,
                        )
                        _vi7 = _res7["valor_intrinseco"]
                        _vi7_ms = _vi7 * (1 - _margen7) if _vi7 is not None else None
                        _up7 = ((_vi7 - _px7) / _px7 * 100) if (_vi7 and _px7) else None
                    except Exception as _e_dcf:
                        st.error(f"Error en el cálculo DCF: {_e_dcf}")
                        _res7 = None
                        _vi7 = _vi7_ms = _up7 = None

                    # ── SECCIÓN 3: RESULTADO PRINCIPAL ───────────────────────────
                    st.markdown("### 🎯 Resultado")

                    _r1, _r2, _r3, _r4 = st.columns(4)

                    _r1.metric(
                        "Valor intrínseco",
                        f"${_vi7:.2f}" if _vi7 is not None else "—",
                        help="DCF sin margen de seguridad.",
                    )
                    _r2.metric(
                        f"Con margen {int(_margen7*100)}%",
                        f"${_vi7_ms:.2f}" if _vi7_ms is not None else "—",
                        help="Precio máximo de entrada con margen de seguridad aplicado.",
                    )
                    _r3.metric("Precio mercado", f"${_px7:.2f}" if _px7 else "—")

                    if _up7 is not None:
                        _r4.metric(
                            "Upside / Downside",
                            f"{_up7:+.1f}%",
                            delta=f"{_up7:+.1f}%",
                            delta_color="normal" if _up7 >= 0 else "inverse",
                        )
                    else:
                        _r4.metric("Upside / Downside", "—")

                    # Veredicto
                    if _up7 is not None:
                        if _up7 > _margen7 * 100:
                            st.success(
                                f"SUBVALUADA — Upside {_up7:.1f}% supera el margen de seguridad "
                                f"({_margen7*100:.0f}%). Precio de entrada sugerido: "
                                f"≤ ${_vi7_ms:.2f}."
                            )
                        elif _up7 > -10:
                            st.info(
                                f"EN PRECIO JUSTO — Upside {_up7:+.1f}%. "
                                "El precio de mercado está cerca del valor intrínseco calculado."
                            )
                        else:
                            st.error(
                                f"SOBREVALUADA — Downside {abs(_up7):.1f}% según estos supuestos. "
                                "Revisá si los supuestos de crecimiento son realistas."
                            )

                    # Desglose
                    if _res7:
                        with st.expander("Ver desglose del valor empresa"):
                            _dx1, _dx2, _dx3, _dx4 = st.columns(4)
                            _dx1.metric("VP flujos", f"${_res7['suma_vp_flujos']/1e9:.2f}B")
                            _dx2.metric("VP valor terminal", f"${_res7['vp_terminal']/1e9:.2f}B")
                            _dx3.metric("Deuda neta", f"${_res7['deuda_neta']/1e9:.2f}B")
                            _vt_pct = _res7["vp_terminal"] / _res7["valor_empresa"] * 100 if _res7["valor_empresa"] else 0
                            _dx4.metric("% Valor terminal / EV", f"{_vt_pct:.1f}%",
                                        help="Un % muy alto (>80%) indica que el resultado depende mucho de supuestos lejanos.")

                    st.divider()

                    # ── SECCIÓN 4: ESCENARIOS ─────────────────────────────────────
                    st.markdown("### 🔭 Escenarios Bull / Base / Bear")

                    try:
                        _esc7 = _calc_esc(
                            _fcf7_usar, _g1_7, _g2_7, _wacc7, _tg7,
                            _años7, _sh7_usar, _deu7_raw, _csh7_raw,
                        )

                        _esc_defs = [
                            ("bull", "🐂 Bull",  "#DCFCE7", "#166534"),
                            ("base", "📊 Base",  "#DBEAFE", "#1E40AF"),
                            ("bear", "🐻 Bear",  "#FEE2E2", "#991B1B"),
                        ]
                        _esc_cols = st.columns(3)

                        for (_key, _lbl, _bg, _fg), _col in zip(_esc_defs, _esc_cols):
                            _e = _esc7[_key]
                            _e_vi = _e.get("valor_intrinseco")
                            _e_up = (
                                (_e_vi - _px7) / _px7 * 100
                                if (_e_vi is not None and _px7)
                                else None
                            )
                            with _col:
                                st.markdown(
                                    f"""<div style="background:{_bg};border-radius:8px;
    padding:16px 18px;border:1px solid {_fg}33;margin-bottom:6px;">
    <div style="font-size:17px;font-weight:700;color:{_fg};">{_lbl}</div>
    <div style="margin-top:10px;font-size:13px;color:#374151;line-height:1.7;">
    Crecimiento (1-5): <b>{_e['g1_usado']*100:.1f}%</b><br>
    WACC: <b>{_e['wacc_usado']*100:.1f}%</b><br>
    Valor intrínseco: <b>{'${:.2f}'.format(_e_vi) if _e_vi is not None else '—'}</b><br>
    Upside/Downside: <b>{'{:+.1f}%'.format(_e_up) if _e_up is not None else '—'}</b>
    </div></div>""",
                                    unsafe_allow_html=True,
                                )
                    except Exception as _e_esc:
                        st.warning(f"No se pudieron calcular escenarios: {_e_esc}")

                    st.divider()

                    # ── SECCIÓN 5: SENSIBILIDAD WACC × tg ────────────────────────
                    st.markdown("### 📊 Sensibilidad: WACC × Crecimiento terminal")
                    st.caption(
                        "Verde = acción barata vs precio actual · "
                        "Rojo = cara · "
                        "Celda enmarcada = tus supuestos actuales."
                    )

                    try:
                        _df_sens7 = _tabla_sens(
                            _fcf7_usar, _g1_7, _g2_7, _wacc7, _tg7,
                            _años7, _sh7_usar, _deu7_raw, _csh7_raw,
                        )

                        _z7_raw = _df_sens7.values.tolist()
                        _x7     = list(_df_sens7.columns)   # tg labels
                        _y7     = list(_df_sens7.index)      # wacc labels

                        # Coloreo por upside % vs precio actual
                        # Verde = subvaluado (vi > px), Rojo = sobrevaluado (vi < px)
                        if _px7 and _px7 > 0:
                            _z7_up = [
                                [
                                    round((v - _px7) / _px7 * 100, 1) if v is not None else None
                                    for v in row
                                ]
                                for row in _z7_raw
                            ]
                            _txt7 = [
                                [
                                    (f"${v:.2f}\n{u:+.0f}%" if u is not None else "N/D")
                                    for v, u in zip(row_v, row_u)
                                ]
                                for row_v, row_u in zip(_z7_raw, _z7_up)
                            ]
                            _colorbar_title = "Upside %"
                            _zmid = 0
                        else:
                            _z7_up = _z7_raw
                            _txt7 = [
                                [f"${v:.2f}" if v is not None else "N/D" for v in row]
                                for row in _z7_raw
                            ]
                            _colorbar_title = "USD/acc."
                            _zmid = None

                        _heatmap_kwargs = dict(
                            z=_z7_up,
                            x=_x7,
                            y=_y7,
                            colorscale="RdYlGn",
                            text=_txt7,
                            texttemplate="%{text}",
                            showscale=True,
                            colorbar=dict(title=_colorbar_title),
                            hovertemplate=(
                                "Tg: %{x}<br>WACC: %{y}<br>"
                                "Valor intrínseco: %{text}<extra></extra>"
                            ),
                        )
                        if _zmid is not None:
                            _heatmap_kwargs["zmid"] = _zmid

                        _fig_sens7 = _go7.Figure(_go7.Heatmap(**_heatmap_kwargs))

                        # Recuadro azul = supuestos actuales (centro = índice 2)
                        _fig_sens7.add_shape(
                            type="rect",
                            xref="x", yref="y",
                            x0=1.5, x1=2.5,
                            y0=1.5, y1=2.5,
                            line=dict(color="#2563EB", width=3),
                            fillcolor="rgba(0,0,0,0)",
                        )

                        # Anotación del precio actual
                        if _px7:
                            _fig_sens7.add_annotation(
                                x=0.5, y=1.0, xref="paper", yref="paper",
                                text=f"Precio mercado: ${_px7:.2f}",
                                showarrow=False,
                                font=dict(size=11, color="#2563EB"),
                                bgcolor="rgba(37,99,235,0.1)",
                                bordercolor="#2563EB",
                                borderwidth=1,
                                borderpad=4,
                                xanchor="center",
                            )

                        _fig_sens7.update_layout(
                            xaxis_title="Crecimiento terminal (tg)",
                            yaxis_title="WACC",
                            height=380,
                            template="plotly_white",
                            margin=dict(l=60, r=20, t=50, b=60),
                        )
                        st.plotly_chart(_fig_sens7, use_container_width=True)

                    except Exception as _e_sens:
                        st.warning(f"No se pudo generar la tabla de sensibilidad: {_e_sens}")

                    st.divider()

                    # ── SECCIÓN 6: FLUJOS PROYECTADOS ────────────────────────────
                    st.markdown("### 📈 Flujos de caja proyectados y descontados")

                    if _res7:
                        try:
                            _fl7   = _res7["flujos"]
                            _labs7 = [f"Año {f['año']}" for f in _fl7] + ["Val. Terminal"]
                            _fcf7p = [f["fcf_proyectado"] / 1e9 for f in _fl7] + [_res7["valor_terminal"] / 1e9]
                            _vp7p  = [f["valor_presente"] / 1e9 for f in _fl7] + [_res7["vp_terminal"] / 1e9]

                            _fig_fl7 = _go7.Figure()

                            # Barras FCF proyectado
                            _cols_barras7 = ["#2563EB"] * len(_fl7) + ["#8B5CF6"]
                            _fig_fl7.add_trace(_go7.Bar(
                                x=_labs7,
                                y=_fcf7p,
                                name="FCF proyectado",
                                marker_color=_cols_barras7,
                                opacity=0.75,
                                hovertemplate="%{x}<br>FCF: $%{y:.3f}B<extra></extra>",
                            ))

                            # Línea valor presente
                            _fig_fl7.add_trace(_go7.Scatter(
                                x=_labs7,
                                y=_vp7p,
                                mode="lines+markers",
                                name="Valor presente (descontado)",
                                line=dict(color="#16A34A", width=2.5),
                                marker=dict(size=7),
                                hovertemplate="%{x}<br>VP: $%{y:.3f}B<extra></extra>",
                            ))

                            _fig_fl7.update_layout(
                                xaxis_title="Período",
                                yaxis_title=f"USD Billones ({_cur7})",
                                template="plotly_white",
                                height=420,
                                hovermode="x unified",
                                margin=dict(l=20, r=20, t=20, b=20),
                                legend=dict(
                                    orientation="h", yanchor="bottom",
                                    y=1.02, xanchor="right", x=1,
                                ),
                            )
                            st.plotly_chart(_fig_fl7, use_container_width=True)

                            # Tabla detalle
                            with st.expander("Ver tabla de flujos"):
                                _df_fl7 = _pd7.DataFrame(_fl7)
                                _df_fl7["FCF proy. (B)"] = _df_fl7["fcf_proyectado"] / 1e9
                                _df_fl7["VP (B)"]        = _df_fl7["valor_presente"]  / 1e9
                                st.dataframe(
                                    _df_fl7[["año", "FCF proy. (B)", "VP (B)"]]
                                    .rename(columns={"año": "Año"})
                                    .style.format({
                                        "FCF proy. (B)": "${:.3f}",
                                        "VP (B)":        "${:.3f}",
                                    }),
                                    use_container_width=True,
                                    hide_index=True,
                                )

                        except Exception as _e_fl7:
                            st.warning(f"No se pudo graficar flujos: {_e_fl7}")

                    _wacc_auto_str = (
                        f" (auto {_wacc_auto7*100:.2f}%)"
                        if _wacc_auto7 else ""
                    )
                    st.caption(
                        f"DCF | FCF base: {_sym7}{_fcf7_usar/1e9:.3f}B ({_cur7}) | "
                        f"WACC: {_wacc7*100:.1f}%{_wacc_auto_str} | "
                        f"Crecimiento: {_g1_7*100:.0f}% / {_g2_7*100:.0f}% | "
                        f"Tasa terminal: {_tg7*100:.0f}% | {_años7} años. "
                        "⚠️ Análisis educativo — no constituye asesoramiento financiero."
                    )

# ══════════════════════════════════════════════════════════════════
# TAB 8: NOTICIAS & SENTIMIENTO
# ══════════════════════════════════════════════════════════════════
if tab8 is not None:
    with tab8:
        import pandas as _pd8
        from src.noticias import (
            get_noticias_ticker as _get_noticias_tk,
            get_noticias_portfolio as _get_noticias_port,
            analizar_sentimiento as _analizar_sent,
            sentimiento_portfolio as _sent_portfolio,
        )
        from src.portfolio import cargar_portfolio as _cargar_port8

        # ── helpers UI ─────────────────────────────────────────────────
        def _badge8(label: str) -> str:
            _colores = {
                "Positivo":  ("#DCFCE7", "#16A34A"),
                "Negativo":  ("#FEE2E2", "#DC2626"),
                "Neutro":    ("#F3F4F6", "#6B7280"),
                "Sin datos": ("#F3F4F6", "#9CA3AF"),
            }
            _bg, _fg = _colores.get(label, ("#F3F4F6", "#6B7280"))
            return (
                f"<span style='background:{_bg};color:{_fg};padding:3px 10px;"
                f"border-radius:12px;font-size:12px;font-weight:600;'>{label}</span>"
            )

        def _color_sent_col(s):
            _mapa = {
                "Positivo": "background-color:#DCFCE7;color:#16A34A;font-weight:600",
                "Negativo": "background-color:#FEE2E2;color:#DC2626;font-weight:600",
                "Neutro":   "background-color:#F3F4F6;color:#6B7280",
                "Sin datos":"background-color:#F9FAFB;color:#9CA3AF",
            }
            return [_mapa.get(v, "") for v in s]

        # ── SECCIÓN 1: NOTICIAS DEL TICKER SELECCIONADO ────────────────
        st.markdown("### Noticias recientes")

        if not ticker:
            st.info("Escribe un ticker en el buscador del sidebar para ver noticias.")
        else:
            with st.spinner(f"Cargando noticias de {ticker}..."):
                _noticias_tk8 = _get_noticias_tk(ticker, max_noticias=5)

            if not _noticias_tk8:
                st.warning(f"No se encontraron noticias para **{ticker}** en Yahoo Finance.")
            else:
                st.caption(
                    f"{len(_noticias_tk8)} noticias · cache 30 min · fuente: Yahoo Finance"
                )
                for _n8 in _noticias_tk8:
                    _sent8 = _analizar_sent(f"{_n8['titulo']} {_n8['resumen']}")
                    _c_txt, _c_badge = st.columns([5, 1])
                    with _c_txt:
                        _tit_link = (
                            f"[{_n8['titulo']}]({_n8['url']})"
                            if _n8["url"] else _n8["titulo"]
                        )
                        st.markdown(f"**{_tit_link}**")
                        st.caption(f"{_n8['fecha']} · {_n8['fuente']}")
                        if _n8["resumen"]:
                            _res = (
                                _n8["resumen"][:220] + "…"
                                if len(_n8["resumen"]) > 220
                                else _n8["resumen"]
                            )
                            st.markdown(
                                f"<span style='color:#6B7280;font-size:13px;'>{_res}</span>",
                                unsafe_allow_html=True,
                            )
                    with _c_badge:
                        st.markdown(_badge8(_sent8["label"]), unsafe_allow_html=True)
                        st.markdown(
                            f"<span style='font-size:11px;color:#9CA3AF;'>"
                            f"score: {_sent8['score']:+.2f}</span>",
                            unsafe_allow_html=True,
                        )
                        if _sent8.get("positivas") or _sent8.get("negativas"):
                            _palabras_str = ", ".join(
                                _sent8.get("positivas", [])[:3] + _sent8.get("negativas", [])[:3]
                            )
                            st.markdown(
                                f"<span style='font-size:10px;color:#CBD5E1;'>"
                                f"{_palabras_str}</span>",
                                unsafe_allow_html=True,
                            )
                    st.markdown("---")

        st.divider()

        # ── SECCIÓN 2: RADAR DE SENTIMIENTO DEL PORTFOLIO ──────────────
        st.markdown("### Radar de sentimiento del portfolio")

        _port8_data = None
        _tickers8 = []
        _noticias_port8 = {}
        _sent_port8 = {}

        try:
            _port8_data = _cargar_port8("pato")
            _tickers8 = [_p["ticker"] for _p in _port8_data.get("posiciones", [])]
        except Exception as _e8_port:
            st.warning(f"No se pudo cargar el portfolio: {_e8_port}")

        if _tickers8:
            with st.spinner("Analizando sentimiento del portfolio..."):
                _noticias_port8 = _get_noticias_port(_tickers8, max_por_ticker=3)
                _sent_port8 = _sent_portfolio(_noticias_port8)

            # Métricas resumen
            _labels8 = [_v["label"] for _v in _sent_port8.values()]
            _n8_pos = _labels8.count("Positivo")
            _n8_neg = _labels8.count("Negativo")
            _n8_neu = _labels8.count("Neutro") + _labels8.count("Sin datos")
            _scores8_all = [_v["score_promedio"] for _v in _sent_port8.values()]
            _score8_global = sum(_scores8_all) / len(_scores8_all) if _scores8_all else 0.0

            _km1, _km2, _km3, _km4 = st.columns(4)
            _km1.metric("Positivos", f"{_n8_pos} / {len(_tickers8)}")
            _km2.metric("Neutros",   f"{_n8_neu} / {len(_tickers8)}")
            _km3.metric("Negativos", f"{_n8_neg} / {len(_tickers8)}")
            _km4.metric("Score global", f"{_score8_global:+.2f}")

            st.markdown("")

            # Tabla ticker × sentimiento
            _rows8 = []
            for _pos8 in _port8_data.get("posiciones", []):
                _t8 = _pos8["ticker"]
                _sv8 = _sent_port8.get(_t8, {})
                _rows8.append({
                    "Ticker":      _t8,
                    "Sector":      _pos8.get("sector", "—"),
                    "Noticias":    _sv8.get("n_noticias", 0),
                    "Score":       _sv8.get("score_promedio", 0.0),
                    "Sentimiento": _sv8.get("label", "Sin datos"),
                })
            _df8 = _pd8.DataFrame(_rows8)
            st.dataframe(
                _df8.style
                    .apply(_color_sent_col, subset=["Sentimiento"])
                    .format({"Score": "{:+.3f}"}),
                use_container_width=True,
                hide_index=True,
            )

        st.divider()

        # ── SECCIÓN 3: FEED COMBINADO DEL PORTFOLIO ────────────────────
        st.markdown("### Feed del portfolio")

        if _noticias_port8:
            _feed8 = []
            for _t8f, _nl8 in _noticias_port8.items():
                for _n8f in _nl8:
                    _feed8.append({**_n8f, "ticker": _t8f})

            if not _feed8:
                st.info("No hay noticias disponibles para los tickers del portfolio.")
            else:
                _feed8_sorted = sorted(
                    _feed8,
                    key=lambda x: x.get("fecha_iso", "0000-00-00"),
                    reverse=True,
                )
                st.caption(
                    f"{len(_feed8_sorted)} noticias · últimas 3 por ticker · "
                    f"{len(_tickers8)} activos del portfolio"
                )
                for _nf8 in _feed8_sorted:
                    _sf8 = _analizar_sent(f"{_nf8['titulo']} {_nf8['resumen']}")
                    _cf1, _cf2, _cf3 = st.columns([1, 6, 1])
                    with _cf1:
                        st.markdown(
                            f"<span style='background:#EFF6FF;color:#1D4ED8;"
                            f"padding:3px 8px;border-radius:6px;"
                            f"font-size:12px;font-weight:700;'>{_nf8['ticker']}</span>",
                            unsafe_allow_html=True,
                        )
                    with _cf2:
                        _tit_f = (
                            f"[{_nf8['titulo']}]({_nf8['url']})"
                            if _nf8["url"] else _nf8["titulo"]
                        )
                        st.markdown(f"**{_tit_f}**")
                        st.caption(f"{_nf8['fecha']} · {_nf8['fuente']}")
                    with _cf3:
                        st.markdown(_badge8(_sf8["label"]), unsafe_allow_html=True)
                    st.markdown("---")
        elif not _tickers8:
            st.info("Cargá el portfolio para ver el feed combinado.")

        st.caption(
            "Fuente: Yahoo Finance · Sentimiento: palabras clave financieras hardcodeadas · "
            "No es recomendación de inversión."
        )

# TAB 9: WATCHLIST
with tab9:
    from src.watchlist import (
        cargar_watchlist      as _cargar_wl,
        guardar_watchlist     as _guardar_wl,
        generar_link_compartir as _link_wl,
        get_precios_watchlist  as _precios_wl,
        WATCHLISTS_PREDEFINIDAS as _wl_predef,
    )

    # Detectar watchlist compartida via ?watchlist=nombre en la URL
    _wl_param    = st.query_params.get("watchlist", None)
    _wl_nombre   = _wl_param if _wl_param else "pato"
    _wl_readonly = bool(_wl_param and _wl_param != "pato")

    if _wl_readonly:
        st.info(f"👁️ Viendo la watchlist compartida: **{_wl_nombre}** (solo lectura)")

    # Inicializar en session_state (una sola vez por sesión)
    if "wl_tickers" not in st.session_state or st.session_state.get("wl_nombre") != _wl_nombre:
        st.session_state["wl_tickers"] = _cargar_wl(_wl_nombre)
        st.session_state["wl_nombre"]  = _wl_nombre
    _wl_tickers = st.session_state["wl_tickers"]

    # ── SECCIÓN 1: MI WATCHLIST ──────────────────────────────────────────────
    st.markdown("### 👁️ Mi Watchlist")

    if not _wl_readonly:
        _add_c1, _add_c2, _add_c3 = st.columns([3, 1, 3])
        with _add_c1:
            _new_tk = st.text_input(
                "Agregar ticker:", placeholder="Ej: MELI, AAPL, YPF.BA",
                key="wl_new_ticker", label_visibility="collapsed",
            ).upper().strip()
        with _add_c2:
            if st.button("➕ Agregar", key="wl_add_btn", use_container_width=True):
                if _new_tk and _new_tk not in _wl_tickers:
                    _wl_tickers.append(_new_tk)
                    st.session_state["wl_tickers"] = _wl_tickers
                    _guardar_wl(_wl_nombre, _wl_tickers)
                    st.rerun()
                elif _new_tk in _wl_tickers:
                    st.warning(f"{_new_tk} ya está en la watchlist.")

    # Cargar precios (siempre, aunque el bloque de edición esté oculto)
    _wl_precios_raw = _precios_wl(tuple(_wl_tickers)) if _wl_tickers else []
    _precios_map_wl = {p["ticker"]: p for p in _wl_precios_raw}

    if not _wl_tickers:
        st.info("Tu watchlist está vacía. Agrega tickers arriba o cargá una watchlist predefinida.")
    else:
        _sort_wl = st.selectbox(
            "Ordenar por:",
            ["Variación % (desc)", "Variación % (asc)", "Nombre A–Z", "Precio (desc)"],
            key="wl_sort",
        )

        _filas_wl = []
        for _tk in _wl_tickers:
            _p = _precios_map_wl.get(_tk, {"ticker": _tk, "precio": None, "variacion_pct": None})
            _filas_wl.append({
                "ticker": _tk,
                "precio": _p["precio"],
                "var_pct": _p["variacion_pct"],
            })

        if _sort_wl == "Variación % (desc)":
            _filas_wl.sort(key=lambda x: (x["var_pct"] or -999), reverse=True)
        elif _sort_wl == "Variación % (asc)":
            _filas_wl.sort(key=lambda x: (x["var_pct"] or 999))
        elif _sort_wl == "Nombre A–Z":
            _filas_wl.sort(key=lambda x: x["ticker"])
        else:
            _filas_wl.sort(key=lambda x: (x["precio"] or -1), reverse=True)

        # Cabecera
        _hc1, _hc2, _hc3, _hc4 = st.columns([2, 2, 2, 1])
        _hc1.markdown("**Ticker**")
        _hc2.markdown("**Precio**")
        _hc3.markdown("**Variación hoy**")
        if not _wl_readonly:
            _hc4.markdown("**Eliminar**")

        st.markdown("<hr style='margin:4px 0 8px 0;'>", unsafe_allow_html=True)

        for _f in _filas_wl:
            _fc1, _fc2, _fc3, _fc4 = st.columns([2, 2, 2, 1])
            with _fc1:
                st.write(f"**{_f['ticker']}**")
            with _fc2:
                st.write(f"${_f['precio']:,.2f}" if _f["precio"] else "—")
            with _fc3:
                _v = _f["var_pct"]
                if _v is not None:
                    _col_v = "#16A34A" if _v >= 0 else "#DC2626"
                    st.markdown(
                        f"<span style='color:{_col_v};font-weight:700;'>{_v:+.2f}%</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.write("—")
            with _fc4:
                if not _wl_readonly:
                    if st.button("🗑️", key=f"wl_del_{_f['ticker']}"):
                        _wl_tickers.remove(_f["ticker"])
                        st.session_state["wl_tickers"] = _wl_tickers
                        _guardar_wl(_wl_nombre, _wl_tickers)
                        st.rerun()

    # ── SECCIÓN 2: MINI HEATMAP ──────────────────────────────────────────────
    if _wl_tickers and _filas_wl:
        st.divider()
        st.markdown("### 🎨 Resumen visual")

        def _wl_bg(v):
            if v is None:   return "#64748B"
            if v >= 2:      return "#15803D"
            if v >= 0.5:    return "#16A34A"
            if v >= 0:      return "#4ADE80"
            if v > -0.5:    return "#F87171"
            if v > -2:      return "#DC2626"
            return "#991B1B"

        _boxes = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;">'
        for _f in _filas_wl:
            _v  = _f["var_pct"]
            _bg = _wl_bg(_v)
            _fg = "#1a1a1a" if (_v is not None and -0.5 <= _v < 0.5) else "#ffffff"
            _lbl = f"{_v:+.1f}%" if _v is not None else "—"
            _boxes += (
                f'<div style="background:{_bg};color:{_fg};border-radius:10px;'
                f'padding:14px 18px;min-width:88px;text-align:center;">'
                f'<div style="font-weight:700;font-size:14px;">{_f["ticker"]}</div>'
                f'<div style="font-size:13px;margin-top:2px;">{_lbl}</div>'
                f'</div>'
            )
        _boxes += "</div>"
        st.markdown(_boxes, unsafe_allow_html=True)

    # ── SECCIÓN 3: COMPARTIR ─────────────────────────────────────────────────
    st.divider()
    st.markdown("### 🔗 Compartir watchlist")

    if not _wl_readonly:
        if st.button("🔗 Generar link para compartir", key="wl_share_btn"):
            st.session_state["wl_show_link"] = True

        if st.session_state.get("wl_show_link"):
            _url_wl = _link_wl(_wl_nombre)
            st.code(_url_wl, language=None)
            st.caption("Cualquiera con este link puede ver tu watchlist (solo lectura)")
    else:
        st.info("Estás viendo una watchlist compartida. Para crear la tuya, accedé sin el parámetro `?watchlist=`.")

    # ── SECCIÓN 4: EXPORTAR / IMPORTAR ───────────────────────────────────────
    st.divider()
    st.markdown("### 💾 Exportar / Importar")

    import json as _wl_json
    from datetime import date as _wl_date
    from src.alertas import (
        cargar_alertas  as _cargar_alertas_io,
        guardar_alertas as _guardar_alertas_io,
    )

    _io_wl_c1, _io_wl_c2 = st.columns(2)

    with _io_wl_c1:
        st.caption("**Watchlist**")
        st.download_button(
            "📥 Exportar watchlist",
            data=_wl_json.dumps(_wl_tickers, ensure_ascii=False, indent=2),
            file_name=f"watchlist_pato_{_wl_date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
        _uploaded_wl = st.file_uploader(
            "📤 Importar watchlist",
            type=["json"],
            key="upload_watchlist",
            label_visibility="collapsed",
        )
        if _uploaded_wl is not None and not _wl_readonly:
            try:
                _wl_imp_data = _wl_json.loads(_uploaded_wl.read())
                if not isinstance(_wl_imp_data, list):
                    st.error("❌ Formato inválido: se esperaba lista de tickers.")
                else:
                    st.warning(f"⚠️ Importar **{len(_wl_imp_data)} tickers** reemplazará la watchlist actual.")
                    if st.button("✅ Confirmar", key="btn_import_wl"):
                        _guardar_wl(_wl_nombre, _wl_imp_data)
                        st.session_state["wl_tickers"] = _wl_imp_data
                        st.success("✅ Watchlist importada.")
                        st.rerun()
            except Exception:
                st.error("❌ Archivo JSON inválido.")

    with _io_wl_c2:
        st.caption("**Alertas**")
        _alertas_io = _cargar_alertas_io("pato")
        st.download_button(
            "📥 Exportar alertas",
            data=_wl_json.dumps(_alertas_io, ensure_ascii=False, indent=2),
            file_name=f"alertas_pato_{_wl_date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
        _uploaded_al = st.file_uploader(
            "📤 Importar alertas",
            type=["json"],
            key="upload_alertas",
            label_visibility="collapsed",
        )
        if _uploaded_al is not None:
            try:
                _al_imp_data = _wl_json.loads(_uploaded_al.read())
                if not isinstance(_al_imp_data, list):
                    st.error("❌ Formato inválido: se esperaba lista de alertas.")
                else:
                    st.warning(f"⚠️ Importar **{len(_al_imp_data)} alertas** reemplazará las alertas actuales.")
                    if st.button("✅ Confirmar", key="btn_import_al"):
                        _guardar_alertas_io("pato", _al_imp_data)
                        st.success("✅ Alertas importadas.")
                        st.rerun()
            except Exception:
                st.error("❌ Archivo JSON inválido.")

    # ── SECCIÓN 5: WATCHLISTS PREDEFINIDAS ───────────────────────────────────
    st.divider()
    st.markdown("### 📋 Watchlists predefinidas")
    st.caption("Cargá una como punto de partida y luego personalizala.")

    for _wl_preset_nombre, _wl_preset_lista in _wl_predef.items():
        with st.expander(_wl_preset_nombre):
            st.write(", ".join(_wl_preset_lista))
            if not _wl_readonly:
                if st.button("Usar esta watchlist", key=f"wl_use_{_wl_preset_nombre}"):
                    st.session_state["wl_tickers"] = list(_wl_preset_lista)
                    _guardar_wl(_wl_nombre, list(_wl_preset_lista))
                    st.success(f"✅ Watchlist cargada: {len(_wl_preset_lista)} tickers.")
                    st.rerun()

# TAB 10: COMPARAR
if tab10 is not None:
    with tab10:
        import plotly.graph_objects as _go_cmp
        import pandas as _pd_cmp
        from src.comparador import (
            get_datos_comparador  as _get_comp,
            performance_relativa  as _perf_rel,
            METRICAS              as _METRICAS_CMP,
            _MENOR_ES_MEJOR       as _MEM_CMP,
            _NEUTRAL              as _NEUT_CMP,
        )

        st.subheader("⚖️ Comparador de tickers")
        st.caption("Compará 2 a 4 tickers en una sola vista: métricas, performance y resumen.")

        # ── SECCIÓN 1: Selector ───────────────────────────────────────────────
        _default_cmp = ticker if ticker else "YPF, PAM, TGS"
        _input_cmp = st.text_input(
            "Tickers (separados por coma, máx 4):",
            value=st.session_state.get("comp_last_input", _default_cmp),
            placeholder="Ej: YPF, PAM, TGS, CVX",
            key="comp_input",
        )
        _periodos_cmp = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y"}
        _per_lbl_cmp = st.radio(
            "Período de performance:",
            list(_periodos_cmp.keys()),
            index=3,
            horizontal=True,
            key="comp_periodo",
        )
        _per_code_cmp = _periodos_cmp[_per_lbl_cmp]

        _btn_cmp = st.button("⚖️ Comparar", key="comp_btn", type="primary")

        if _btn_cmp:
            st.session_state["comp_last_input"]   = _input_cmp
            st.session_state["comp_tickers_cache"] = None  # fuerza recarga

        _tks_cmp_raw = st.session_state.get("comp_last_input", _default_cmp)
        _tks_cmp = tuple(t.strip().upper() for t in _tks_cmp_raw.split(",") if t.strip())[:4]

        if len(_tks_cmp) < 2:
            st.info("Ingresá al menos 2 tickers y presioná ⚖️ Comparar.")
        else:
            with st.spinner(f"Cargando {', '.join(_tks_cmp)}..."):
                _df_cmp = _get_comp(_tks_cmp)

            if _df_cmp.empty:
                st.warning("No se pudieron obtener datos. Verificá los tickers.")
            else:
                # ── SECCIÓN 2: Tabla comparativa ──────────────────────────────
                st.markdown(f"### 📊 {' vs '.join(_tks_cmp)}")

                # Función de estilo: verde mejor / rojo peor por fila (usa closure _df_cmp)
                def _cmp_styles(display_df):
                    styles = _pd_cmp.DataFrame(
                        "", index=display_df.index, columns=display_df.columns
                    )
                    for _met in _df_cmp.index:
                        if _met not in display_df.index or _met in _NEUT_CMP:
                            continue
                        _row = _pd_cmp.to_numeric(_df_cmp.loc[_met], errors="coerce")
                        _v   = _row.dropna()
                        if len(_v) < 2:
                            continue
                        _menor = _met in _MEM_CMP
                        _bi = _v.idxmin() if _menor else _v.idxmax()
                        _wi = _v.idxmax() if _menor else _v.idxmin()
                        if _bi != _wi:
                            styles.loc[_met, _bi] = (
                                "background-color:#0d2318;color:#4ade80;font-weight:700;"
                            )
                            styles.loc[_met, _wi] = (
                                "background-color:#2d1010;color:#f87171;"
                            )
                    return styles

                # DataFrame formateado para display
                def _fmt(v, met):
                    if v is None or _pd_cmp.isna(v):
                        return "N/D"
                    if met == "Precio actual":
                        return f"${v:,.2f}"
                    if met == "Market Cap (B USD)":
                        return f"${v:.2f}B"
                    if "%" in met:
                        return f"{v:+.2f}%" if "Var" in met else f"{v:.2f}%"
                    return f"{v:.2f}"

                _df_display = _df_cmp.copy().astype(object)
                for _m in _df_display.index:
                    for _col in _df_display.columns:
                        _df_display.loc[_m, _col] = _fmt(_df_cmp.loc[_m, _col], _m)

                st.dataframe(
                    _df_display.style.apply(_cmp_styles, axis=None),
                    use_container_width=True,
                    height=590,
                )
                st.caption(
                    "🟢 Mejor valor de la fila &nbsp;&nbsp; 🔴 Peor valor · "
                    "Fundamentals: cache 24h · Variaciones: cache 5 min"
                )

                # ── SECCIÓN 3: Performance relativa ───────────────────────────
                st.markdown("---")
                st.markdown(f"### 📈 Performance relativa — base 100 ({_per_lbl_cmp})")

                with st.spinner("Cargando historial de precios..."):
                    _df_perf = _perf_rel(_tks_cmp, _per_code_cmp)

                if not _df_perf.empty:
                    _COLS_CMP = ["#2962ff", "#26a69a", "#ef5350", "#ff9800"]
                    _fig_cmp = _go_cmp.Figure()
                    for _i, _tk_p in enumerate(_tks_cmp):
                        if _tk_p not in _df_perf.columns:
                            continue
                        _ret = float(_df_perf[_tk_p].iloc[-1]) - 100
                        _color_p = _COLS_CMP[_i % len(_COLS_CMP)]
                        _fig_cmp.add_trace(_go_cmp.Scatter(
                            x=_df_perf.index,
                            y=_df_perf[_tk_p],
                            name=f"{_tk_p} ({_ret:+.1f}%)",
                            mode="lines",
                            line=dict(color=_color_p, width=2),
                            hovertemplate="%{y:.1f}<extra>" + _tk_p + "</extra>",
                        ))
                    _fig_cmp.add_hline(
                        y=100, line_dash="dot",
                        line_color="#787b86", line_width=1,
                    )
                    _fig_cmp.update_layout(
                        height=420,
                        paper_bgcolor="#131722",
                        plot_bgcolor="#1e222d",
                        font_color="#d1d4dc",
                        xaxis=dict(gridcolor="#2a2e39", linecolor="#2a2e39"),
                        yaxis=dict(
                            gridcolor="#2a2e39",
                            tickformat=".0f",
                            title="Base 100",
                        ),
                        legend=dict(
                            bgcolor="#1e222d",
                            bordercolor="#2a2e39",
                            borderwidth=1,
                        ),
                        hovermode="x unified",
                        margin=dict(l=10, r=10, t=20, b=10),
                    )
                    st.plotly_chart(
                        _fig_cmp, use_container_width=True,
                        config={"displayModeBar": False},
                    )
                else:
                    st.info("No se pudo obtener historial de precios.")

                # ── SECCIÓN 4: Resumen automático ─────────────────────────────
                st.markdown("---")
                st.markdown("### 🤖 Resumen automático")

                _RESUMEN_CMP = {
                    "PE Trailing":       ("📊", "mejor PE",            "mayor PE"),
                    "ROE %":             ("🏆", "mejor ROE",           "menor ROE"),
                    "Margen Neto %":     ("💹", "mejor margen neto",   "menor margen neto"),
                    "Revenue CAGR 3a %": ("🚀", "mayor crecimiento",   "menor crecimiento"),
                    "Deuda/Equity":      ("⚠️",  "menor deuda",         "mayor deuda"),
                    "Var 1 año %":       ("📈", "mejor retorno 1 año", "peor retorno 1 año"),
                }
                for _met_r, (_emj, _lbl_b, _lbl_w) in _RESUMEN_CMP.items():
                    if _met_r not in _df_cmp.index:
                        continue
                    _row_r = _pd_cmp.to_numeric(
                        _df_cmp.loc[_met_r], errors="coerce"
                    ).dropna()
                    if _row_r.empty or len(_row_r) < 2:
                        continue
                    _menor_r  = _met_r in _MEM_CMP
                    _best_tk  = _row_r.idxmin() if _menor_r else _row_r.idxmax()
                    _worst_tk = _row_r.idxmax() if _menor_r else _row_r.idxmin()
                    _bv = _row_r[_best_tk]
                    _wv = _row_r[_worst_tk]
                    _suf = "%" if "%" in _met_r else "x" if "Equity" in _met_r else ""
                    st.caption(
                        f"{_emj} **{_best_tk}** tiene el {_lbl_b} "
                        f"({_bv:.2f}{_suf}) · "
                        f"**{_worst_tk}** el {_lbl_w} "
                        f"({_wv:.2f}{_suf})"
                    )

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:12px;padding:20px 0">
    <p>
    <b>Mi Bloomberg Personal</b> &middot;
    Educación Financiera AR &middot;
    <a href="https://personalfinances.streamlit.app" style="color:#1f77b4">personalfinances.streamlit.app</a>
    </p>
    <p>
    Datos: Yahoo Finance &middot; DolarAPI &middot; ArgentinaDatos &middot;
    Actualización: tiempo real
    </p>
    <p style="font-size:11px">
    ⚠️ Solo fines educativos.
    No constituye asesoramiento financiero.
    Las inversiones conllevan riesgo de pérdida de capital.
    </p>
</div>
""", unsafe_allow_html=True)

# ── AUTO-REFRESH (al final: la página ya renderizó todo el contenido) ─────────
if st.session_state.get("auto_refresh"):
    import time as _ar_time
    for _ar_rem in range(300, 0, -1):
        _ar_m, _ar_s = divmod(_ar_rem, 60)
        _ar_countdown_slot.caption(f"⏱️ Próxima actualización en: {_ar_m}:{_ar_s:02d}")
        _ar_time.sleep(1)
    st.rerun()