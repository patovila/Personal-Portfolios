"""Buscador de tickers con autocomplete por ticker y nombre de empresa."""

TICKERS_CONOCIDOS = [
    # USA Tech
    {"ticker": "AAPL",    "nombre": "Apple Inc",              "sector": "Tech"},
    {"ticker": "GOOGL",   "nombre": "Alphabet (Google)",       "sector": "Tech"},
    {"ticker": "MSFT",    "nombre": "Microsoft",               "sector": "Tech"},
    {"ticker": "NVDA",    "nombre": "NVIDIA",                  "sector": "Tech"},
    {"ticker": "META",    "nombre": "Meta Platforms",          "sector": "Tech"},
    {"ticker": "AMZN",    "nombre": "Amazon",                  "sector": "Tech"},
    {"ticker": "TSLA",    "nombre": "Tesla",                   "sector": "Auto/Tech"},
    {"ticker": "NFLX",    "nombre": "Netflix",                 "sector": "Tech"},
    {"ticker": "AMD",     "nombre": "AMD",                     "sector": "Tech"},
    {"ticker": "INTC",    "nombre": "Intel",                   "sector": "Tech"},
    # USA Finance
    {"ticker": "JPM",     "nombre": "JPMorgan Chase",          "sector": "Finanzas"},
    {"ticker": "BAC",     "nombre": "Bank of America",         "sector": "Finanzas"},
    {"ticker": "GS",      "nombre": "Goldman Sachs",           "sector": "Finanzas"},
    {"ticker": "V",       "nombre": "Visa",                    "sector": "Finanzas"},
    {"ticker": "MA",      "nombre": "Mastercard",              "sector": "Finanzas"},
    # USA Consumer/Other
    {"ticker": "KO",      "nombre": "Coca-Cola",               "sector": "Consumo"},
    {"ticker": "PEP",     "nombre": "PepsiCo",                 "sector": "Consumo"},
    {"ticker": "MCD",     "nombre": "McDonald's",              "sector": "Consumo"},
    {"ticker": "WMT",     "nombre": "Walmart",                 "sector": "Retail"},
    {"ticker": "DIS",     "nombre": "Disney",                  "sector": "Entretenimiento"},
    # ETFs
    {"ticker": "SPY",     "nombre": "S&P 500 ETF",             "sector": "ETF"},
    {"ticker": "QQQ",     "nombre": "Nasdaq 100 ETF",          "sector": "ETF"},
    {"ticker": "GLD",     "nombre": "Gold ETF",                "sector": "ETF"},
    {"ticker": "EEM",     "nombre": "Emerging Markets ETF",    "sector": "ETF"},
    # LATAM
    {"ticker": "MELI",    "nombre": "MercadoLibre",            "sector": "Tech LATAM"},
    {"ticker": "BABA",    "nombre": "Alibaba",                 "sector": "Tech China"},
    # Argentina ADR
    {"ticker": "YPF",     "nombre": "YPF S.A.",                "sector": "Energía AR"},
    {"ticker": "PAM",     "nombre": "Pampa Energía",           "sector": "Energía AR"},
    {"ticker": "TGS",     "nombre": "Transportadora Gas Sur",  "sector": "Energía AR"},
    {"ticker": "GGAL",    "nombre": "Grupo Galicia",           "sector": "Banco AR"},
    {"ticker": "BMA",     "nombre": "Banco Macro",             "sector": "Banco AR"},
    {"ticker": "CEPU",    "nombre": "CEPU Holdings",           "sector": "Energía AR"},
    {"ticker": "LOMA",    "nombre": "Loma Negra",              "sector": "Construcción AR"},
    # Argentina Local (BYMA)
    {"ticker": "YPF.BA",  "nombre": "YPF (BYMA)",              "sector": "Energía AR"},
    {"ticker": "PAMP.BA", "nombre": "Pampa Energía (BYMA)",    "sector": "Energía AR"},
    {"ticker": "TGS.BA",  "nombre": "TGS (BYMA)",              "sector": "Energía AR"},
    {"ticker": "TGN.BA",  "nombre": "TGN (BYMA)",              "sector": "Energía AR"},
    {"ticker": "GGAL.BA", "nombre": "Galicia (BYMA)",          "sector": "Banco AR"},
    {"ticker": "BMA.BA",  "nombre": "Macro (BYMA)",            "sector": "Banco AR"},
    {"ticker": "ALUA.BA", "nombre": "Aluar (BYMA)",            "sector": "Industria AR"},
    {"ticker": "TXAR.BA", "nombre": "Ternium Argentina (BYMA)","sector": "Acero AR"},
    {"ticker": "SUPV.BA", "nombre": "Supervielle (BYMA)",      "sector": "Banco AR"},
    # Crypto
    {"ticker": "BTC-USD", "nombre": "Bitcoin",                 "sector": "Crypto"},
    {"ticker": "ETH-USD", "nombre": "Ethereum",                "sector": "Crypto"},
]


def buscar_tickers(query: str) -> list:
    query_up = query.upper().strip()
    query_lo = query.lower().strip()
    if len(query_lo) < 1:
        return []

    resultados = []
    for t in TICKERS_CONOCIDOS:
        if t["ticker"].startswith(query_up):
            resultados.append({**t, "match": "ticker", "score": 10})
        elif query_lo in t["nombre"].lower():
            resultados.append({**t, "match": "nombre", "score": 5})

    resultados.sort(key=lambda x: -x["score"])
    return resultados[:8]
