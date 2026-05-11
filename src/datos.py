"""Funciones para cargar datos de yfinance."""
import json
from pathlib import Path
import yfinance as yf


def formatear(valor, decimales=2, prefijo="", sufijo=""):
    """Formatea un número o devuelve N/A si es None."""
    if valor is None:
        return "N/A"
    try:
        return f"{prefijo}{valor:,.{decimales}f}{sufijo}"
    except (TypeError, ValueError):
        return "N/A"


def cargar_ticker(ticker):
    """Carga datos básicos de un ticker."""
    t = yf.Ticker(ticker)
    info = t.info
    
    return {
        "ticker": ticker,
        "nombre": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industria": info.get("industry", "N/A"),
        "pais": info.get("country", "N/A"),
        "moneda": info.get("currency", "N/A"),
        "precio_actual": info.get("currentPrice"),
        "market_cap_b": (info.get("marketCap") or 0) / 1e9,
        "max_52w": info.get("fiftyTwoWeekHigh"),
        "min_52w": info.get("fiftyTwoWeekLow"),
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "margen_op": info.get("operatingMargins"),
        "empleados": info.get("fullTimeEmployees"),
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