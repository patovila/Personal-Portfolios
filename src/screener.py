"""Screener de acciones por ratios fundamentales."""
import time
import pandas as pd
import streamlit as st
import yfinance as yf

UNIVERSO_ACCIONES = [
    "AAPL", "GOOGL", "MSFT", "NVDA", "META", "AMZN",
    "TSLA", "NFLX", "JPM", "BAC", "KO", "PEP", "V", "MA",
    "SPY", "QQQ", "MELI", "BABA",
    "YPF", "PAM", "TGS", "GGAL", "BMA", "CEPU",
]

_NOMBRES = {
    "AAPL": "Apple",          "GOOGL": "Alphabet",       "MSFT": "Microsoft",
    "NVDA": "NVIDIA",         "META": "Meta",             "AMZN": "Amazon",
    "TSLA": "Tesla",          "NFLX": "Netflix",          "JPM": "JPMorgan",
    "BAC": "Bank of America", "KO": "Coca-Cola",          "PEP": "PepsiCo",
    "V": "Visa",              "MA": "Mastercard",         "SPY": "S&P 500 ETF",
    "QQQ": "Nasdaq 100 ETF",  "MELI": "MercadoLibre",    "BABA": "Alibaba",
    "YPF": "YPF S.A.",        "PAM": "Pampa Energía",    "TGS": "Trans. Gas Sur",
    "GGAL": "Grupo Galicia",  "BMA": "Banco Macro",      "CEPU": "CEPU Holdings",
}


@st.cache_data(ttl=3600)
def get_datos_screener(tickers: tuple) -> pd.DataFrame:
    """Descarga ratios fundamentales en batches de 5. Cache 1h."""
    # Batch price download para variacion diaria (una sola request)
    try:
        _price_raw = yf.download(
            list(tickers), period="2d", interval="1d",
            group_by="ticker", auto_adjust=True, progress=False, threads=True,
        )
    except Exception:
        _price_raw = None

    filas = []
    grupos = [list(tickers)[i:i + 5] for i in range(0, len(tickers), 5)]

    for idx_g, grupo in enumerate(grupos):
        if idx_g > 0:
            time.sleep(1)  # evitar rate limit

        for tk in grupo:
            fila = {"Ticker": tk, "Empresa": _NOMBRES.get(tk, tk)}
            try:
                info = yf.Ticker(tk).info
                pe   = info.get("trailingPE")
                pb   = info.get("priceToBook")
                roe  = info.get("returnOnEquity")
                mgn  = info.get("profitMargins")
                # debtToEquity en yfinance viene como porcentaje (ej: 183 = 1.83x)
                de   = info.get("debtToEquity")
                div  = info.get("dividendYield")
                beta = info.get("beta")
                mcap = info.get("marketCap")

                fila.update({
                    "PE":           round(pe, 1)          if pe   is not None else None,
                    "PB":           round(pb, 2)          if pb   is not None else None,
                    "ROE_%":        round(roe * 100, 1)   if roe  is not None else None,
                    "Mg_Neto_%":    round(mgn * 100, 1)   if mgn  is not None else None,
                    "Beta":         round(beta, 2)         if beta is not None else None,
                    "Market_Cap_B": round(mcap / 1e9, 2)  if mcap is not None else None,
                    "Div_Yield_%":  round(div * 100, 2)   if div  is not None else None,
                    "Debt_Equity":  round(de / 100, 2)    if de   is not None else None,
                })
            except Exception:
                pass  # fila queda con solo Ticker + Empresa

            # Variación diaria desde batch download
            try:
                if _price_raw is not None and not _price_raw.empty:
                    if len(tickers) == 1:
                        close = _price_raw["Close"].dropna()
                    else:
                        close = _price_raw[tk]["Close"].dropna()
                    if len(close) >= 2:
                        fila["Var_Dia_%"] = round(
                            float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100), 2
                        )
            except Exception:
                pass

            filas.append(fila)

    return pd.DataFrame(filas)


def aplicar_filtros(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    """Aplica rangos numéricos al df. Filas con NaN en una métrica pasan siempre.
    Retorna ordenado por Market Cap desc."""
    out = df.copy()

    for col, lo_key, hi_key in [
        ("PE",          "pe_min",   "pe_max"),
        ("PB",          "pb_min",   "pb_max"),
        ("ROE_%",       "roe_min",  "roe_max"),
        ("Mg_Neto_%",   "mg_min",   "mg_max"),
        ("Beta",        "beta_min", "beta_max"),
        ("Debt_Equity", "de_min",   "de_max"),
        ("Div_Yield_%", "div_min",  "div_max"),
    ]:
        if col not in out.columns:
            continue
        lo = filtros.get(lo_key, -9999)
        hi = filtros.get(hi_key,  9999)
        out = out[out[col].isna() | ((out[col] >= lo) & (out[col] <= hi))]

    mcap_sel = filtros.get("mcap", "Todas")
    if "Market_Cap_B" in out.columns:
        if mcap_sel == "Small (<$2B)":
            out = out[out["Market_Cap_B"].isna() | (out["Market_Cap_B"] < 2)]
        elif mcap_sel == "Mid ($2-10B)":
            out = out[out["Market_Cap_B"].isna() | (
                (out["Market_Cap_B"] >= 2) & (out["Market_Cap_B"] <= 10)
            )]
        elif mcap_sel == "Large (>$10B)":
            out = out[out["Market_Cap_B"].isna() | (out["Market_Cap_B"] > 10)]

    if "Market_Cap_B" in out.columns:
        out = out.sort_values("Market_Cap_B", ascending=False, na_position="last")

    return out.reset_index(drop=True)
