"""Funciones para cargar datos de yfinance."""
import json
import time
from pathlib import Path
import yfinance as yf


def _fetch_info(ticker: str) -> dict:
    """Descarga yf.Ticker.info con reintentos ante rate-limit (429)."""
    for intento in range(3):
        try:
            return yf.Ticker(ticker).info
        except Exception as e:
            if "too many requests" in str(e).lower() or "429" in str(e):
                time.sleep(2 ** intento)   # 1 s, 2 s, 4 s
            else:
                raise
    return yf.Ticker(ticker).info  # último intento sin captura

# ---------------------------------------------------------------------------
# Mapa de tickers argentinos: ADR NYSE ↔ local BYMA (.BA)
# ---------------------------------------------------------------------------
TICKERS_AR = {
    "YPF":     {"adr": "YPF",  "local": "YPF.BA",  "nombre": "YPF"},
    "YPF.BA":  {"adr": "YPF",  "local": "YPF.BA",  "nombre": "YPF"},
    "PAMP":    {"adr": "PAM",  "local": "PAMP.BA", "nombre": "Pampa Energía"},
    "PAMP.BA": {"adr": "PAM",  "local": "PAMP.BA", "nombre": "Pampa Energía"},
    "PAM":     {"adr": "PAM",  "local": "PAMP.BA", "nombre": "Pampa Energía"},
    "TGS":     {"adr": "TGS",  "local": "TGS.BA",  "nombre": "TGS"},
    "TGS.BA":  {"adr": "TGS",  "local": "TGS.BA",  "nombre": "TGS"},
    "TGN":     {"adr": None,   "local": "TGN.BA",  "nombre": "TGN"},
    "TGN.BA":  {"adr": None,   "local": "TGN.BA",  "nombre": "TGN"},
    "GGAL":    {"adr": "GGAL", "local": "GGAL.BA", "nombre": "Galicia"},
    "GGAL.BA": {"adr": "GGAL", "local": "GGAL.BA", "nombre": "Galicia"},
    "BMA":     {"adr": "BMA",  "local": "BMA.BA",  "nombre": "Macro"},
    "BMA.BA":  {"adr": "BMA",  "local": "BMA.BA",  "nombre": "Macro"},
    "CEPU":    {"adr": "CEPU", "local": "CEPU.BA", "nombre": "CEPU"},
    "CEPU.BA": {"adr": "CEPU", "local": "CEPU.BA", "nombre": "CEPU"},
}


def get_ticker_adr(ticker: str) -> str:
    """Retorna el ticker ADR si existe en el mapa, sino el ticker original."""
    entry = TICKERS_AR.get(ticker.upper())
    if entry and entry["adr"]:
        return entry["adr"]
    return ticker


def get_ticker_local(ticker: str) -> str:
    """Retorna el ticker local .BA si existe en el mapa, sino el ticker original."""
    entry = TICKERS_AR.get(ticker.upper())
    if entry:
        return entry["local"]
    return ticker


def is_ticker_argentino(ticker: str) -> bool:
    """True si el ticker está en el mapa de tickers argentinos."""
    return ticker.upper() in TICKERS_AR


# ---------------------------------------------------------------------------

def formatear(valor, decimales=2, prefijo="", sufijo=""):
    """Formatea un número o devuelve N/A si es None."""
    if valor is None:
        return "N/A"
    try:
        return f"{prefijo}{valor:,.{decimales}f}{sufijo}"
    except (TypeError, ValueError):
        return "N/A"


def cargar_ticker(ticker):
    """Carga datos básicos de un ticker.

    Para tickers argentinos:
    - Fundamentals (PE, ROE, etc.) y nombre → ADR en NYSE (datos en USD)
    - Precio actual → intenta .BA (ARS) vía history(); fallback al ADR (USD)
    """
    t_upper = ticker.upper()
    es_ar = is_ticker_argentino(t_upper)

    if es_ar:
        _entry   = TICKERS_AR[t_upper]
        _real_adr = _entry["adr"]              # None si no tiene ADR (TGN)
        tk_local  = _entry["local"]            # p.ej. "PAMP.BA"
        tk_adr    = _real_adr or tk_local      # lo que usamos para fundamentals

        # Fundamentals y metadatos desde el ADR si existe, si no desde local
        info = _fetch_info(tk_adr)

        # Precio local en ARS vía history() — más robusto que info para .BA
        precio_local = None
        precio_moneda = None
        try:
            hist_local = yf.Ticker(tk_local).history(period="2d")
            if not hist_local.empty:
                precio_local  = float(hist_local["Close"].iloc[-1])
                precio_moneda = "ARS"
        except Exception:
            pass

        # Fallback: precio del ADR en USD
        if precio_local is None:
            precio_local  = info.get("currentPrice") or info.get("regularMarketPrice")
            precio_moneda = info.get("currency", "USD") if precio_local else None

        # Precio ADR en USD y Mkt Cap calculado price×shares (evita mezcla ARS/USD de Yahoo)
        _px_usd     = info.get("currentPrice") or info.get("regularMarketPrice")
        _shares_out = info.get("sharesOutstanding")
        _mcap_b     = (_shares_out * _px_usd / 1e9) if (_shares_out and _px_usd) else (info.get("marketCap") or 0) / 1e9

        return {
            "ticker":         ticker,
            "ticker_adr":     _real_adr,
            "ticker_local":   tk_local,
            "es_argentino":   True,
            "precio_moneda":  precio_moneda,
            "precio_adr_usd": _px_usd if _real_adr else None,
            "nombre":         info.get("longName") or TICKERS_AR[t_upper]["nombre"],
            "sector":         info.get("sector",   "N/A"),
            "industria":      info.get("industry", "N/A"),
            "pais":           info.get("country",  "Argentina"),
            "moneda":         info.get("currency", "USD"),
            "precio_actual":  precio_local,
            "market_cap_b":   _mcap_b,
            "max_52w":       info.get("fiftyTwoWeekHigh"),
            "min_52w":       info.get("fiftyTwoWeekLow"),
            "pe":            info.get("trailingPE"),
            "pb":            info.get("priceToBook"),
            "roe":           info.get("returnOnEquity"),
            "margen_op":     info.get("operatingMargins"),
            "empleados":     info.get("fullTimeEmployees"),
        }

    # Ticker internacional — comportamiento original sin cambios
    info = _fetch_info(ticker)
    return {
        "ticker":        ticker,
        "ticker_adr":    None,
        "ticker_local":  None,
        "es_argentino":  False,
        "precio_moneda": info.get("currency", "USD"),
        "nombre":        info.get("longName", "N/A"),
        "sector":        info.get("sector",   "N/A"),
        "industria":     info.get("industry", "N/A"),
        "pais":          info.get("country",  "N/A"),
        "moneda":        info.get("currency", "N/A"),
        "precio_actual": info.get("currentPrice"),
        "market_cap_b":  (info.get("marketCap") or 0) / 1e9,
        "max_52w":       info.get("fiftyTwoWeekHigh"),
        "min_52w":       info.get("fiftyTwoWeekLow"),
        "pe":            info.get("trailingPE"),
        "pb":            info.get("priceToBook"),
        "roe":           info.get("returnOnEquity"),
        "margen_op":     info.get("operatingMargins"),
        "empleados":     info.get("fullTimeEmployees"),
    }


def mostrar_ticker(ticker):
    """Imprime ficha completa de un ticker."""
    d = cargar_ticker(ticker)
    
    print(f"=== {d['nombre']} ({d['ticker']}) ===")
    print(f"Sector: {d['sector']} | Industria: {d['industria']}")
    print(f"País: {d['pais']} | Moneda: {d['moneda']}")
    print(f"Precio actual: {formatear(d['precio_actual'], prefijo='$')}")
    print(f"Market Cap: {formatear(d['market_cap_b'], prefijo='$', sufijo='B')}")
    print(f"Rango 52w: {formatear(d['min_52w'], prefijo='$')} - {formatear(d['max_52w'], prefijo='$')}")
    print(f"PE: {formatear(d['pe'])}")
    print(f"PB: {formatear(d['pb'])}")
    if d['roe'] is not None:
        print(f"ROE: {formatear(d['roe']*100, sufijo='%')}")
    if d['margen_op'] is not None:
        print(f"Margen operativo: {formatear(d['margen_op']*100, sufijo='%')}")
    print("=" * 50)


def cargar_universo(ruta="data/tickers.json"):
    """Carga el archivo JSON con todos los tickers organizados."""
    archivo = Path(ruta)
    if not archivo.exists():
        print(f"No se encontro el archivo {ruta}")
        return None
    
    with open(archivo, "r", encoding="utf-8") as f:
        universo = json.load(f)
    
    return universo


def listar_categorias(universo):
    """Imprime un resumen de qué hay en el universo."""
    print("UNIVERSO DE TICKERS\n")
    
    if "portfolios" in universo:
        print("=== PORTFOLIOS ===")
        for nombre, tickers in universo["portfolios"].items():
            print(f"  {nombre}: {len(tickers)} tickers -> {', '.join(tickers[:5])}{'...' if len(tickers) > 5 else ''}")
    
    if "categorias" in universo:
        print("\n=== CATEGORIAS ===")
        for nombre, tickers in universo["categorias"].items():
            print(f"  {nombre}: {len(tickers)} tickers")
    
    if "sectores" in universo:
        print("\n=== SECTORES ===")
        for nombre, tickers in universo["sectores"].items():
            print(f"  {nombre}: {len(tickers)} tickers -> {', '.join(tickers)}")


def buscar_ticker(universo, ticker):
    """Busca en qué categorías/sectores aparece un ticker."""
    ticker = ticker.upper()
    encontrado_en = []
    
    for tipo in ["portfolios", "categorias", "sectores"]:
        if tipo in universo:
            for nombre, tickers in universo[tipo].items():
                if ticker in tickers:
                    encontrado_en.append(f"{tipo}/{nombre}")
    
    if encontrado_en:
        print(f"{ticker} aparece en:")
        for ubic in encontrado_en:
            print(f"   - {ubic}")
    else:
        print(f"{ticker} no esta en el universo. Considera agregarlo a tickers.json")

    return encontrado_en


def diagnostico_entorno():
    """Imprime info del entorno Python para debugging de imports.

    Util cuando un notebook tira ImportError: ayuda a verificar que el kernel
    apunta al venv correcto y que el CWD es la raiz del proyecto.
    """
    import sys
    import os

    print("=" * 60)
    print("DIAGNOSTICO DE ENTORNO")
    print("=" * 60)
    print(f"CWD: {os.getcwd()}")
    print(f"Python ejecutable: {sys.executable}")
    print(f"Version Python: {sys.version.split()[0]}")
    print(f"Plataforma: {sys.platform}")
    print()
    print("sys.path (rutas donde Python busca modulos):")
    for i, p in enumerate(sys.path):
        marca = "  <- raiz proyecto" if p and os.path.basename(p) == "Proyecto_mi bloomberg" else ""
        print(f"  [{i}] {p}{marca}")
    print("=" * 60)