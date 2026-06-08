"""Datos de mercado en tiempo real para la home screen."""
import yfinance as yf
import pandas as pd
import streamlit as st

_HEATMAP_TICKERS = [
    {"ticker": "GGAL.BA", "nombre": "GGAL",  "sector": "Merval"},
    {"ticker": "YPF.BA",  "nombre": "YPF",   "sector": "Merval"},
    {"ticker": "PAMP.BA", "nombre": "PAMP",  "sector": "Merval"},
    {"ticker": "TGS.BA",  "nombre": "TGS",   "sector": "Merval"},
    {"ticker": "BMA.BA",  "nombre": "BMA",   "sector": "Merval"},
    {"ticker": "ALUA.BA", "nombre": "ALUA",  "sector": "Merval"},
    {"ticker": "TXAR.BA", "nombre": "TXAR",  "sector": "Merval"},
    {"ticker": "SUPV.BA", "nombre": "SUPV",  "sector": "Merval"},
    {"ticker": "CEPU.BA", "nombre": "CEPU",  "sector": "Merval"},
    {"ticker": "GGAL",    "nombre": "GGAL",  "sector": "CEDEARs"},
    {"ticker": "MELI",    "nombre": "MELI",  "sector": "CEDEARs"},
    {"ticker": "AMZN",    "nombre": "AMZN",  "sector": "CEDEARs"},
    {"ticker": "GOOGL",   "nombre": "GOOGL", "sector": "CEDEARs"},
    {"ticker": "NVDA",    "nombre": "NVDA",  "sector": "CEDEARs"},
    {"ticker": "META",    "nombre": "META",  "sector": "CEDEARs"},
    {"ticker": "AAPL",    "nombre": "AAPL",  "sector": "CEDEARs"},
    {"ticker": "MSFT",    "nombre": "MSFT",  "sector": "CEDEARs"},
    {"ticker": "TSLA",    "nombre": "TSLA",  "sector": "CEDEARs"},
]

INDICES = [
    {"ticker": "^GSPC",   "nombre": "S&P 500"},
    {"ticker": "^DJI",    "nombre": "Dow Jones"},
    {"ticker": "^IXIC",   "nombre": "Nasdaq"},
    {"ticker": "^RUT",    "nombre": "Russell 2000"},
    {"ticker": "^MERV",   "nombre": "Merval"},
    {"ticker": "GC=F",    "nombre": "Oro"},
    {"ticker": "CL=F",    "nombre": "Petróleo WTI"},
    {"ticker": "BTC-USD", "nombre": "Bitcoin"},
]

_TAPE_INDICES    = ["^GSPC", "^IXIC", "^MERV"]
_INDICES_TICKERS = [i["ticker"] for i in INDICES]


def _batch_download(tickers: list) -> dict:
    """Una sola request HTTP para N tickers. Retorna {ticker: DataFrame}."""
    if not tickers:
        return {}
    unique = list(dict.fromkeys(tickers))  # deduplica preservando orden
    try:
        data = yf.download(
            tickers=" ".join(unique),
            period="2d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        return {tk: pd.DataFrame() for tk in unique}

    if data is None or data.empty:
        return {tk: pd.DataFrame() for tk in unique}

    result = {}
    if len(unique) == 1:
        # Un solo ticker: yf.download devuelve DataFrame plano (sin MultiIndex)
        df = data.dropna(subset=["Close"]) if "Close" in data.columns else pd.DataFrame()
        result[unique[0]] = df
    else:
        for tk in unique:
            try:
                sub = data[tk].dropna(subset=["Close"])
                result[tk] = sub
            except (KeyError, TypeError):
                result[tk] = pd.DataFrame()
    return result


def _var_pct(df) -> float | None:
    """Variación % del día desde un DataFrame con columna Close (period='2d')."""
    if df is None or df.empty or "Close" not in df.columns:
        return None
    close = df["Close"].dropna()
    if len(close) >= 2:
        return float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
    return None


@st.cache_data(ttl=600)
def get_indices_globales() -> list:
    """8 índices globales en una sola request. Cache 5 min."""
    data = _batch_download(_INDICES_TICKERS)
    result = []
    for idx in INDICES:
        df = data.get(idx["ticker"], pd.DataFrame())
        precio = float(df["Close"].iloc[-1]) if not df.empty else None
        result.append({**idx, "precio": precio, "variacion_pct": _var_pct(df)})
    return result


@st.cache_data(ttl=600)
def get_movers_portfolio(tickers: tuple) -> dict:
    """Gainers y losers del portfolio en una sola request. Cache 5 min."""
    data = _batch_download(list(tickers))
    items = []
    for tk in tickers:
        df = data.get(tk, pd.DataFrame())
        if df.empty:
            continue
        precio = float(df["Close"].iloc[-1])
        var    = _var_pct(df) or 0.0
        vol    = int(df["Volume"].iloc[-1]) if "Volume" in df.columns else 0
        items.append({"ticker": tk, "precio": precio, "variacion_pct": var, "volumen": vol})
    gainers = sorted([i for i in items if i["variacion_pct"] >= 0],
                     key=lambda x: x["variacion_pct"], reverse=True)[:5]
    losers  = sorted([i for i in items if i["variacion_pct"] < 0],
                     key=lambda x: x["variacion_pct"])[:5]
    return {"gainers": gainers, "losers": losers}


def generar_resumen_dia(portfolio_data: dict, indices: list, dolar) -> dict:
    """Genera el resumen diario personalizado para la home screen.

    portfolio_data: {"gainers": [...], "losers": [...]} de get_movers_portfolio()
    indices:        lista de get_indices_globales()
    dolar:          lista de get_cotizaciones() o None
    """
    from datetime import datetime
    ahora   = datetime.now()
    hora    = ahora.hour
    weekday = ahora.weekday()  # 0=lunes … 6=domingo

    if 6 <= hora < 12:
        saludo = "Buenos días"
    elif 12 <= hora < 19:
        saludo = "Buenas tardes"
    else:
        saludo = "Buenas noches"

    gainers = (portfolio_data or {}).get("gainers", [])
    losers  = (portfolio_data or {}).get("losers", [])
    todos   = gainers + losers

    mejor      = gainers[0] if gainers else None
    peor       = losers[0]  if losers  else None
    var_total  = sum(i["variacion_pct"] for i in todos) / len(todos) if todos else None

    def _idx(nombre_parcial):
        return next((i for i in (indices or []) if nombre_parcial in i["ticker"]), None)

    sp500  = _idx("GSPC")
    merval = _idx("MERV")
    blue   = next((i for i in (dolar or []) if i.get("casa", "").lower() == "blue"), None)

    # Texto principal
    partes = [f"{saludo} 👋"]
    if var_total is not None:
        dir_p = "subió" if var_total >= 0 else "bajó"
        partes.append(f"Tu portfolio {dir_p} {abs(var_total):.1f}% hoy.")
    if mejor and peor:
        partes.append(
            f"{mejor['ticker']} lidera con {mejor['variacion_pct']:+.1f}%"
            f" y {peor['ticker']} es la más débil ({peor['variacion_pct']:+.1f}%)."
        )
    elif mejor:
        partes.append(f"{mejor['ticker']} lidera con {mejor['variacion_pct']:+.1f}%.")

    if blue and blue.get("venta"):
        partes.append(f"El dólar blue cotiza a ${blue['venta']:,.0f}.")

    sp500_var  = sp500.get("variacion_pct")  if sp500  else None
    merval_var = merval.get("variacion_pct") if merval else None

    if sp500_var is not None and abs(sp500_var) > 1:
        dir_sp = "sube" if sp500_var >= 0 else "baja"
        partes.append(f"El S&P500 {dir_sp} {abs(sp500_var):.1f}%.")
    if merval_var is not None and abs(merval_var) > 2:
        dir_m = "sube" if merval_var >= 0 else "baja"
        partes.append(f"El Merval {dir_m} {abs(merval_var):.1f}%.")

    fin_de_semana  = weekday >= 5
    pre_market     = not fin_de_semana and hora < 10
    horas_apertura = (10 - hora) if pre_market else None

    _dias  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    _meses = ["enero","febrero","marzo","abril","mayo","junio",
              "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    fecha_str = f"{_dias[weekday]} {ahora.day} de {_meses[ahora.month - 1]}"

    return {
        "saludo":          saludo,
        "fecha_str":       fecha_str,
        "texto":           " ".join(partes),
        "var_total_pct":   var_total,
        "mejor":           mejor,
        "peor":            peor,
        "sp500_var":       sp500_var,
        "blue_precio":     blue.get("venta") if blue else None,
        "pre_market":      pre_market,
        "fin_de_semana":   fin_de_semana,
        "horas_apertura":  horas_apertura,
        "weekday":         weekday,
    }


@st.cache_data(ttl=300)
def get_heatmap_data() -> list:
    """Precios y variaciones para el treemap de mercado. Cache 5 min."""
    tickers = [t["ticker"] for t in _HEATMAP_TICKERS]
    data = _batch_download(tickers)
    result = []
    for item in _HEATMAP_TICKERS:
        tk = item["ticker"]
        df = data.get(tk, pd.DataFrame())
        if df.empty:
            continue
        precio = float(df["Close"].iloc[-1])
        var = _var_pct(df) or 0.0
        try:
            info = yf.Ticker(tk).fast_info
            mcap = info.get("marketCap") or info.get("market_cap") or 1e9
        except Exception:
            mcap = 1e9
        result.append({
            "ticker":      item["nombre"],
            "sector":      item["sector"],
            "precio":      round(precio, 2),
            "variacion_%": round(var, 2),
            "market_cap":  max(mcap, 1e6),
        })
    return result


@st.cache_data(ttl=600)
def get_ticker_tape(portfolio_tickers: tuple) -> list:
    """Banda de precios: portfolio + índices principales. Cache 3 min."""
    all_tks = list(portfolio_tickers) + [t for t in _TAPE_INDICES if t not in portfolio_tickers]
    data = _batch_download(all_tks)
    result = []
    for tk in all_tks:
        df = data.get(tk, pd.DataFrame())
        if df.empty:
            continue
        precio = float(df["Close"].iloc[-1])
        var    = _var_pct(df) or 0.0
        nombre = tk.replace("^", "").replace("-USD", "").replace("=F", "")
        result.append({"ticker": nombre, "precio": precio, "variacion_pct": var})
    return result
