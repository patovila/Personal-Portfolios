"""Indicadores tecnicos: RSI, MACD, Bollinger Bands, soportes/resistencias.

Convencion: todas las funciones reciben un ticker (str) o un DataFrame de
precios con columna 'Close'. Las que reciben ticker bajan datos via yfinance.
"""
import numpy as np
import pandas as pd

from src.data_layer import get_precios


def _cargar_close(ticker_o_df, periodo="1y"):
    """Acepta un ticker (str) o un DataFrame con columna Close.

    Devuelve siempre una Series de cierres indexada por fecha.
    Centraliza la logica para no repetirla en cada indicador.
    """
    if isinstance(ticker_o_df, pd.DataFrame):
        if "Close" not in ticker_o_df.columns:
            raise ValueError("El DataFrame debe tener columna 'Close'")
        return ticker_o_df["Close"]
    if isinstance(ticker_o_df, pd.Series):
        return ticker_o_df
    data = get_precios([ticker_o_df], periodo)
    hist = data.get(ticker_o_df, pd.DataFrame())
    if hist.empty:
        raise ValueError(f"Sin datos para {ticker_o_df}")
    return hist["Close"]


def rsi(ticker_o_df, ventana=14, periodo="1y"):
    """Relative Strength Index. Default 14 dias (estandar Wilder).

    >70 = sobrecompra (posible correccion). <30 = sobreventa (posible rebote).
    Usa suavizado de Wilder (EMA con alpha=1/ventana) - es el RSI 'clasico',
    no el de SMA simple.
    """
    close = _cargar_close(ticker_o_df, periodo)
    delta = close.diff()

    ganancia = delta.where(delta > 0, 0.0)
    perdida = -delta.where(delta < 0, 0.0)

    avg_ganancia = ganancia.ewm(alpha=1/ventana, adjust=False, min_periods=ventana).mean()
    avg_perdida = perdida.ewm(alpha=1/ventana, adjust=False, min_periods=ventana).mean()

    rs = avg_ganancia / avg_perdida
    rsi_val = 100 - (100 / (1 + rs))
    rsi_val.name = f"RSI_{ventana}"
    return rsi_val


def macd(ticker_o_df, rapida=12, lenta=26, señal=9, periodo="1y"):
    """MACD = EMA(12) - EMA(26). Senal = EMA(9) del MACD. Histograma = MACD - Senal.

    Cruce MACD por encima de Senal = senal alcista. Cruce por debajo = bajista.
    Histograma creciente = momentum aumentando.
    """
    close = _cargar_close(ticker_o_df, periodo)

    ema_rapida = close.ewm(span=rapida, adjust=False).mean()
    ema_lenta = close.ewm(span=lenta, adjust=False).mean()

    macd_line = ema_rapida - ema_lenta
    signal_line = macd_line.ewm(span=señal, adjust=False).mean()
    histograma = macd_line - signal_line

    return pd.DataFrame({
        "MACD": macd_line,
        "Senal": signal_line,
        "Histograma": histograma,
    })


def bollinger(ticker_o_df, ventana=20, desv=2, periodo="1y"):
    """Bandas de Bollinger: media movil ± k desviaciones estandar.

    Precio cerca de banda superior = caro (relativo). Cerca de banda inferior
    = barato. Estrechamiento de bandas suele preceder movimientos fuertes.
    """
    close = _cargar_close(ticker_o_df, periodo)

    media = close.rolling(window=ventana).mean()
    std = close.rolling(window=ventana).std()

    return pd.DataFrame({
        "Close": close,
        "Media": media,
        "Banda_Superior": media + desv * std,
        "Banda_Inferior": media - desv * std,
        "Ancho_%": (4 * desv * std / media) * 100,
    })


def soportes_resistencias(ticker_o_df, ventana=10, periodo="6mo", top_n=5):
    """Detecta soportes (minimos locales) y resistencias (maximos locales).

    Un punto es maximo local si es el maximo en una ventana centrada de
    (2*ventana+1) dias. Devuelve top_n soportes y resistencias mas relevantes
    (los mas cercanos al precio actual).
    """
    close = _cargar_close(ticker_o_df, periodo)
    n = len(close)
    if n < 2 * ventana + 1:
        return {"soportes": [], "resistencias": [], "precio_actual": float(close.iloc[-1])}

    valores = close.values
    es_max = np.zeros(n, dtype=bool)
    es_min = np.zeros(n, dtype=bool)

    for i in range(ventana, n - ventana):
        ventana_slice = valores[i - ventana:i + ventana + 1]
        if valores[i] == ventana_slice.max():
            es_max[i] = True
        if valores[i] == ventana_slice.min():
            es_min[i] = True

    resistencias_raw = [(close.index[i], float(valores[i])) for i in range(n) if es_max[i]]
    soportes_raw = [(close.index[i], float(valores[i])) for i in range(n) if es_min[i]]

    precio_actual = float(close.iloc[-1])

    resistencias = sorted([r for r in resistencias_raw if r[1] >= precio_actual],
                          key=lambda x: x[1])[:top_n]
    soportes = sorted([s for s in soportes_raw if s[1] <= precio_actual],
                      key=lambda x: x[1], reverse=True)[:top_n]

    return {
        "precio_actual": precio_actual,
        "soportes": soportes,
        "resistencias": resistencias,
    }


def señales_tecnicas(ticker, periodo="1y"):
    """Resumen de las senales actuales: RSI, MACD, Bollinger.

    Devuelve un dict con interpretacion lista para mostrar. Util para chequear
    el estado tecnico de un papel en un vistazo.
    """
    data = get_precios([ticker], periodo)
    hist = data.get(ticker, pd.DataFrame())
    if hist.empty or "Close" not in hist.columns:
        return None

    close = hist["Close"]
    precio = float(close.iloc[-1])

    rsi_serie = rsi(close, periodo=periodo).dropna()
    macd_df = macd(close, periodo=periodo).dropna()
    bb = bollinger(close, periodo=periodo).dropna()

    if rsi_serie.empty or macd_df.empty or bb.empty:
        return None

    rsi_actual = float(rsi_serie.iloc[-1])
    if rsi_actual >= 70:
        interp_rsi = "SOBRECOMPRA - posible correccion"
    elif rsi_actual <= 30:
        interp_rsi = "SOBREVENTA - posible rebote"
    else:
        interp_rsi = "Zona neutral"

    macd_actual = float(macd_df["MACD"].iloc[-1])
    signal_actual = float(macd_df["Senal"].iloc[-1])
    hist_actual = float(macd_df["Histograma"].iloc[-1])
    hist_anterior = float(macd_df["Histograma"].iloc[-2])

    if macd_actual > signal_actual and hist_actual > hist_anterior:
        interp_macd = "Alcista (MACD>Senal, momentum subiendo)"
    elif macd_actual > signal_actual:
        interp_macd = "Alcista (MACD>Senal)"
    elif macd_actual < signal_actual and hist_actual < hist_anterior:
        interp_macd = "Bajista (MACD<Senal, momentum bajando)"
    else:
        interp_macd = "Bajista (MACD<Senal)"

    bb_sup = float(bb["Banda_Superior"].iloc[-1])
    bb_inf = float(bb["Banda_Inferior"].iloc[-1])
    bb_media = float(bb["Media"].iloc[-1])
    posicion_bb = (precio - bb_inf) / (bb_sup - bb_inf) * 100 if bb_sup > bb_inf else 50

    if precio >= bb_sup:
        interp_bb = "Sobre banda superior - extension alcista"
    elif precio <= bb_inf:
        interp_bb = "Bajo banda inferior - extension bajista"
    elif posicion_bb > 80:
        interp_bb = "Cerca de banda superior"
    elif posicion_bb < 20:
        interp_bb = "Cerca de banda inferior"
    else:
        interp_bb = "Zona media"

    return {
        "ticker": ticker,
        "precio_actual": round(precio, 2),
        "RSI": round(rsi_actual, 2),
        "RSI_interpretacion": interp_rsi,
        "MACD": round(macd_actual, 4),
        "MACD_senal": round(signal_actual, 4),
        "MACD_histograma": round(hist_actual, 4),
        "MACD_interpretacion": interp_macd,
        "BB_superior": round(bb_sup, 2),
        "BB_media": round(bb_media, 2),
        "BB_inferior": round(bb_inf, 2),
        "BB_posicion_%": round(posicion_bb, 1),
        "BB_interpretacion": interp_bb,
    }


def mostrar_señales(ticker, periodo="1y"):
    """Imprime las senales tecnicas formateadas."""
    s = señales_tecnicas(ticker, periodo)
    if s is None:
        print(f"Sin datos para {ticker}")
        return

    print(f"\n{'='*60}")
    print(f"  SENALES TECNICAS - {s['ticker']} (precio ${s['precio_actual']})")
    print(f"{'='*60}\n")

    print(f"RSI(14): {s['RSI']}")
    print(f"  -> {s['RSI_interpretacion']}\n")

    print(f"MACD: {s['MACD']} | Senal: {s['MACD_senal']} | Hist: {s['MACD_histograma']}")
    print(f"  -> {s['MACD_interpretacion']}\n")

    print(f"Bollinger: inf ${s['BB_inferior']} | media ${s['BB_media']} | sup ${s['BB_superior']}")
    print(f"Posicion en banda: {s['BB_posicion_%']}%")
    print(f"  -> {s['BB_interpretacion']}\n")
    print("=" * 60)
