"""Noticias financieras y análisis de sentimiento via yfinance + VADER."""
import streamlit as st
import yfinance as yf
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Léxico financiero argentino: VADER no conoce estos términos.
# Valores en escala VADER: positivo > 0, negativo < 0, rango típico ±3.
LEXICO_FINANCIERO_AR = {
    "vaca muerta": 2.0,
    "rigi": 1.5,
    "cepo": -2.0,
    "default": -3.0,
    "reestructuración": -1.5,
    "acuerdo fmi": 1.0,
    "reservas": 0.5,
    "devaluación": -2.5,
    "inflación": -1.5,
    "brecha": -1.0,
    "blanqueo": 0.5,
    "inversión": 1.5,
    "exportaciones": 1.0,
    "superávit": 2.0,
    "déficit": -2.0,
    "privatización": 0.5,
    "subsidios": -0.5,
}

# Singleton: se crea una vez al importar el módulo, no en cada llamada.
_analyzer = SentimentIntensityAnalyzer()
_analyzer.lexicon.update(LEXICO_FINANCIERO_AR)


def _parsear_noticia(item: dict) -> dict:
    """Normaliza un item de yfinance.news (formato v1 legacy o v2 con content)."""
    content = item.get("content", {})
    if content:
        titulo = content.get("title", "Sin título")
        pub = content.get("pubDate", "")
        if pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                fecha = dt.strftime("%d/%m/%Y %H:%M")
                fecha_iso = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                fecha = pub[:10]
                fecha_iso = pub[:10]
        else:
            fecha = "—"
            fecha_iso = "0000-00-00"
        provider = content.get("provider", {})
        fuente = provider.get("displayName", "—") if isinstance(provider, dict) else str(provider)
        url = (
            (content.get("canonicalUrl") or {}).get("url")
            or (content.get("clickThroughUrl") or {}).get("url")
            or ""
        )
        resumen = content.get("summary", "") or ""
    else:
        titulo = item.get("title", "Sin título")
        ts = item.get("providerPublishTime")
        if ts:
            try:
                dt = datetime.fromtimestamp(int(ts))
                fecha = dt.strftime("%d/%m/%Y %H:%M")
                fecha_iso = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                fecha = "—"
                fecha_iso = "0000-00-00"
        else:
            fecha = "—"
            fecha_iso = "0000-00-00"
        fuente = item.get("publisher", "—")
        url = item.get("link", "")
        resumen = item.get("summary", "") or ""

    return {
        "titulo": titulo,
        "url": url,
        "fecha": fecha,
        "fecha_iso": fecha_iso,
        "fuente": fuente,
        "resumen": resumen,
    }


@st.cache_data(ttl=1800)
def get_noticias_ticker(ticker: str, max_noticias: int = 5) -> list:
    """Noticias recientes de un ticker via yfinance. Cache 30 min."""
    try:
        raw = yf.Ticker(ticker).news or []
        return [_parsear_noticia(item) for item in raw[:max_noticias]]
    except Exception:
        return []


def get_noticias_portfolio(tickers: list, max_por_ticker: int = 3) -> dict:
    """Noticias para cada ticker del portfolio. Retorna {ticker: [noticias]}."""
    return {t: get_noticias_ticker(t, max_por_ticker) for t in tickers}


def analizar_sentimiento(texto: str) -> dict:
    """Sentimiento VADER con léxico financiero AR extendido.

    compound en [-1, 1]: >= 0.05 Positivo, <= -0.05 Negativo, resto Neutro.
    Retorna score, label, y el desglose completo de VADER (pos/neu/neg/compound).
    """
    scores = _analyzer.polarity_scores(texto)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positivo"
    elif compound <= -0.05:
        label = "Negativo"
    else:
        label = "Neutro"

    return {
        "score": round(compound, 3),
        "label": label,
        "detalle": scores,
    }


def sentimiento_portfolio(noticias_por_ticker: dict) -> dict:
    """Score de sentimiento promedio por ticker. Retorna {ticker: {score_promedio, label, n_noticias}}."""
    resultado = {}
    for ticker, noticias in noticias_por_ticker.items():
        if not noticias:
            resultado[ticker] = {"score_promedio": 0.0, "label": "Sin datos", "n_noticias": 0}
            continue
        scores = [
            analizar_sentimiento(f"{n['titulo']} {n['resumen']}")["score"]
            for n in noticias
        ]
        prom = sum(scores) / len(scores)
        label = "Positivo" if prom >= 0.05 else ("Negativo" if prom <= -0.05 else "Neutro")
        resultado[ticker] = {
            "score_promedio": round(prom, 3),
            "label": label,
            "n_noticias": len(noticias),
        }
    return resultado
