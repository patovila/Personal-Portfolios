"""Métricas financieras avanzadas."""
import numpy as np
import pandas as pd

from src.data_layer import get_precios


def variaciones(ticker):
    """Variaciones de precio en distintos períodos."""
    hist = get_precios([ticker], "5y").get(ticker, pd.DataFrame())

    if hist.empty:
        return None
    
    precio_actual = hist["Close"].iloc[-1]
    
    def var_desde(dias_atras):
        if len(hist) < dias_atras:
            return None
        precio_pasado = hist["Close"].iloc[-dias_atras]
        return ((precio_actual / precio_pasado) - 1) * 100
    
    año_actual = hist.index[-1].year
    inicio_año = hist[hist.index.year == año_actual]
    var_ytd = ((precio_actual / inicio_año["Close"].iloc[0]) - 1) * 100 if not inicio_año.empty else None
    
    def _r(v):
        return round(v, 2) if v is not None else None

    return {
        "ticker": ticker,
        "precio_actual": round(precio_actual, 2),
        "1_dia_%": _r(var_desde(2)),
        "1_semana_%": _r(var_desde(6)),
        "1_mes_%": _r(var_desde(22)),
        "YTD_%": _r(var_ytd),
        "1_año_%": _r(var_desde(252)),
        "5_años_%": _r(var_desde(1260)),
    }


def metricas_avanzadas(ticker, periodo="5y", tasa_libre_riesgo=0.04):
    """Calcula CAGR, volatilidad, Sharpe, max drawdown, etc."""
    hist = get_precios([ticker], periodo).get(ticker, pd.DataFrame())

    if hist.empty:
        return None
    
    precios = hist["Close"]
    retornos_diarios = precios.pct_change().dropna()
    
    precio_inicio = precios.iloc[0]
    precio_fin = precios.iloc[-1]
    retorno_total = (precio_fin / precio_inicio - 1) * 100
    
    años = len(precios) / 252
    cagr = ((precio_fin / precio_inicio) ** (1/años) - 1) * 100
    
    vol_diaria = retornos_diarios.std()
    vol_anual = vol_diaria * np.sqrt(252) * 100
    
    retorno_anual_promedio = retornos_diarios.mean() * 252
    sharpe = (retorno_anual_promedio - tasa_libre_riesgo) / (vol_diaria * np.sqrt(252))
    
    precio_max_acumulado = precios.cummax()
    drawdown = (precios - precio_max_acumulado) / precio_max_acumulado * 100
    max_dd = drawdown.min()
    fecha_max_dd = drawdown.idxmin().strftime("%d %b %Y")
    
    mejor_dia = retornos_diarios.max() * 100
    peor_dia = retornos_diarios.min() * 100
    fecha_mejor = retornos_diarios.idxmax().strftime("%d %b %Y")
    fecha_peor = retornos_diarios.idxmin().strftime("%d %b %Y")
    
    dias_positivos = (retornos_diarios > 0).sum() / len(retornos_diarios) * 100
    
    return {
        "ticker": ticker,
        "periodo": periodo,
        "retorno_total_%": round(retorno_total, 2),
        "CAGR_%": round(cagr, 2),
        "volatilidad_anual_%": round(vol_anual, 2),
        "sharpe_ratio": round(sharpe, 2),
        "max_drawdown_%": round(max_dd, 2),
        "fecha_max_dd": fecha_max_dd,
        "mejor_dia_%": round(mejor_dia, 2),
        "fecha_mejor_dia": fecha_mejor,
        "peor_dia_%": round(peor_dia, 2),
        "fecha_peor_dia": fecha_peor,
        "%_dias_positivos": round(dias_positivos, 2),
    }


def matriz_correlacion(tickers, periodo="2y"):
    """Calcula correlaciones entre activos usando batch download."""
    batch = get_precios(list(tickers), periodo)
    data = {}
    for ticker in tickers:
        df_tk = batch.get(ticker, pd.DataFrame())
        if not df_tk.empty and "Close" in df_tk.columns:
            data[ticker] = df_tk["Close"].pct_change().dropna()

    df = pd.DataFrame(data)
    return df.corr()