"""Score de salud del portfolio: 6 métricas, recomendaciones automáticas."""

# Agrupaciones por tipo de activo (por ticker)
GRUPOS_TIPO: dict[str, set] = {
    "Tech":        {"GOOGL", "NVDA", "META", "AMZN", "MSFT", "AAPL"},
    "Energía AR":  {"YPF", "PAM", "TGS", "TGN", "CEPU", "PAMP"},
    "LATAM":       {"MELI", "BABA"},
    "ETF":         {"SPY", "QQQ", "GLD", "IAU", "EEM"},
    "Crypto":      {"BTC", "ETH", "BTC-USD", "ETH-USD"},
}

# Exposición geográfica por ticker (normalizado a uppercase)
_GEO_AR    = {"YPF", "PAM", "TGS", "TGN", "CEPU", "PAMP", "GGAL", "BMA",
              "TGNO4.BA", "TGS.BA", "YPF.BA", "PAMP.BA"}
_GEO_LATAM = {"MELI", "BABA"}
_GEO_USA   = {"GOOGL", "NVDA", "META", "AMZN", "MSFT", "AAPL",
              "SPY", "QQQ", "GLD", "IAU", "EEM"}

PESOS = {
    "diversificacion": 0.25,
    "concentracion":   0.25,
    "geografica":      0.15,
    "riesgo_retorno":  0.15,
    "posiciones":      0.10,
    "performance":     0.10,
}


def _valor_posicion(pos: dict) -> float:
    return (pos.get("precio_actual_ars") or 0) * (pos.get("cantidad") or 0)


def _score_diversificacion(posiciones: list) -> tuple[int, dict]:
    tickers_up = {(p.get("ticker") or "").upper() for p in posiciones}
    tipos_presentes = sum(
        1 for _tipo, _set in GRUPOS_TIPO.items()
        if tickers_up & _set
    )
    # Si hay LOCAL que no caen en ningún grupo definido, cuenta como "Otros AR"
    locales_sin_grupo = any(
        p.get("tipo", "").upper() == "LOCAL"
        and (p.get("ticker") or "").upper() not in {t for s in GRUPOS_TIPO.values() for t in s}
        for p in posiciones
    )
    if locales_sin_grupo:
        tipos_presentes = max(tipos_presentes, 1)

    if tipos_presentes >= 5:
        score = 100
    elif tipos_presentes == 4:
        score = 80
    elif tipos_presentes == 3:
        score = 60
    elif tipos_presentes == 2:
        score = 40
    else:
        score = 20
    return score, {"n_tipos": tipos_presentes}


def _score_concentracion(posiciones: list) -> tuple[int, dict]:
    valores = [(p.get("ticker", "?"), _valor_posicion(p)) for p in posiciones]
    total   = sum(v for _, v in valores)
    if total == 0:
        return 50, {}
    max_tk, max_val = max(valores, key=lambda x: x[1])
    pct_max = max_val / total * 100
    if pct_max > 40:
        score = 20
    elif pct_max > 30:
        score = 40
    elif pct_max > 20:
        score = 60
    elif pct_max > 10:
        score = 80
    else:
        score = 100
    return score, {"ticker_mayor": max_tk, "pct_mayor": round(pct_max, 1)}


def _score_geografica(posiciones: list) -> tuple[int, dict]:
    tickers = {(p.get("ticker") or "").upper() for p in posiciones}
    has_ar    = bool(tickers & _GEO_AR) or any(
        p.get("tipo", "").upper() == "LOCAL" for p in posiciones
    )
    has_usa   = bool(tickers & _GEO_USA) or any(
        p.get("tipo", "").upper() in ("CEDEAR", "ETF") for p in posiciones
    )
    has_latam = bool(tickers & _GEO_LATAM)
    has_otro  = any(
        p.get("tipo", "").upper() not in ("LOCAL", "CEDEAR", "ETF", "CRYPTO")
        and (p.get("ticker") or "").upper() not in _GEO_AR | _GEO_USA | _GEO_LATAM
        for p in posiciones
    )
    zonas = sum([has_ar, has_usa, has_latam, has_otro])
    if zonas >= 4:
        score = 100
    elif zonas == 3 and has_ar and has_usa and has_latam:
        score = 80
    elif zonas == 2 and has_ar and has_usa:
        score = 60
    elif zonas == 1 and has_ar:
        score = 30
    else:
        score = 50
    return score, {"zonas": zonas, "ar": has_ar, "usa": has_usa, "latam": has_latam}


def _score_riesgo_retorno(posiciones: list) -> tuple[int, dict]:
    total  = sum(_valor_posicion(p) for p in posiciones)
    if total == 0:
        return 50, {}
    beta_w = sum(
        (p.get("beta") or 1.0) * _valor_posicion(p)
        for p in posiciones
    ) / total
    if beta_w < 0.3:
        score = 40          # demasiado defensivo
    elif beta_w < 0.5:
        score = 80
    elif beta_w <= 1.0:
        score = 80
    elif beta_w <= 1.5:
        score = 60
    elif beta_w <= 2.0:
        score = 40
    else:
        score = 20
    return score, {"beta_promedio": round(beta_w, 2)}


def _score_posiciones(posiciones: list) -> tuple[int, dict]:
    n = len(posiciones)
    if n < 3:
        score = 20
    elif n <= 5:
        score = 50
    elif n <= 10:
        score = 80
    elif n <= 15:
        score = 100
    else:
        score = 70   # demasiadas
    return score, {"n_posiciones": n}


def _score_performance(posiciones: list) -> tuple[int, dict]:
    costo  = sum((p.get("precio_promedio_compra_ars") or 0) * (p.get("cantidad") or 0) for p in posiciones)
    actual = sum(_valor_posicion(p) for p in posiciones)
    if costo == 0:
        return 50, {}
    retorno_pct = (actual - costo) / costo * 100
    if retorno_pct < -20:
        score = 10
    elif retorno_pct < 0:
        score = 40
    elif retorno_pct <= 10:
        score = 60
    elif retorno_pct <= 30:
        score = 80
    else:
        score = 100
    return score, {"retorno_pct": round(retorno_pct, 1)}


def calcular_score_salud(posiciones: list) -> dict:
    """Devuelve score 0-100 y detalle de 6 métricas."""
    if not posiciones:
        return {"score_final": 0, "metricas": {}, "detalle": {}}

    s_div,  d_div  = _score_diversificacion(posiciones)
    s_conc, d_conc = _score_concentracion(posiciones)
    s_geo,  d_geo  = _score_geografica(posiciones)
    s_rr,   d_rr   = _score_riesgo_retorno(posiciones)
    s_pos,  d_pos  = _score_posiciones(posiciones)
    s_perf, d_perf = _score_performance(posiciones)

    metricas = {
        "Diversificación": {"score": s_div,  "peso": 0.25, "emoji": "🌐"},
        "Concentración":   {"score": s_conc, "peso": 0.25, "emoji": "🎯"},
        "Geográfica":      {"score": s_geo,  "peso": 0.15, "emoji": "🗺️"},
        "Riesgo/Retorno":  {"score": s_rr,   "peso": 0.15, "emoji": "⚖️"},
        "N° posiciones":   {"score": s_pos,  "peso": 0.10, "emoji": "📊"},
        "Performance":     {"score": s_perf, "peso": 0.10, "emoji": "📈"},
    }
    score_final = round(sum(v["score"] * v["peso"] for v in metricas.values()))

    detalle = {
        "diversificacion": d_div,
        "concentracion":   d_conc,
        "geografica":      d_geo,
        "riesgo_retorno":  d_rr,
        "posiciones":      d_pos,
        "performance":     d_perf,
    }
    return {"score_final": score_final, "metricas": metricas, "detalle": detalle}


def get_recomendaciones(metricas: dict, detalle: dict) -> list:
    """Genera lista de recomendaciones basadas en las métricas calculadas."""
    recomendaciones = []

    conc  = metricas.get("Concentración", {}).get("score", 100)
    divs  = metricas.get("Diversificación", {}).get("score", 100)
    perf  = metricas.get("Performance", {}).get("score", 100)
    pos   = metricas.get("N° posiciones", {}).get("score", 100)
    geo   = metricas.get("Geográfica", {}).get("score", 100)
    rr    = metricas.get("Riesgo/Retorno", {}).get("score", 100)

    d_conc = detalle.get("concentracion", {})
    d_div  = detalle.get("diversificacion", {})
    d_perf = detalle.get("performance", {})
    d_pos  = detalle.get("posiciones", {})

    if conc < 60:
        recomendaciones.append(
            f"⚠️ **{d_conc.get('ticker_mayor', '?')}** representa "
            f"**{d_conc.get('pct_mayor', 0):.1f}%** de tu portfolio. "
            f"Considerá reducir para bajar el riesgo de concentración."
        )
    if divs < 60:
        recomendaciones.append(
            f"📊 Solo tenés **{d_div.get('n_tipos', '?')} tipos** de activos. "
            f"Diversificar en más sectores/geografías reduce el riesgo total."
        )
    if perf < 40:
        recomendaciones.append(
            f"📉 Tu portfolio está en **{d_perf.get('retorno_pct', 0):+.1f}%**. "
            f"Revisá si la tesis de cada posición sigue vigente."
        )
    if d_pos.get("n_posiciones", 0) > 15:
        recomendaciones.append(
            "🔢 Tenés demasiadas posiciones, lo que dificulta el seguimiento. "
            "Considerá consolidar en tus convicciones más fuertes."
        )
    if geo < 60:
        recomendaciones.append(
            "🗺️ Tu exposición geográfica es muy concentrada. "
            "Agregar activos de otras regiones reduce el riesgo-país."
        )
    if rr == 40 and detalle.get("riesgo_retorno", {}).get("beta_promedio", 1) < 0.3:
        recomendaciones.append(
            "🛡️ Tu beta promedio es muy baja. El portfolio puede estar "
            "demasiado defensivo y perder retorno a largo plazo."
        )
    elif rr < 40:
        beta = detalle.get("riesgo_retorno", {}).get("beta_promedio", 0)
        recomendaciones.append(
            f"⚡ Beta ponderada elevada ({beta:.2f}). "
            f"Tu portfolio tiene alta volatilidad — asegurate de tolerarla."
        )

    return recomendaciones
