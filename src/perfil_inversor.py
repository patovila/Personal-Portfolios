"""Quiz de perfil inversor y análisis vs portfolio real."""

PREGUNTAS = [
    {
        "id": 1,
        "pregunta": "¿Cuál es tu horizonte de inversión?",
        "opciones": [
            {"texto": "Menos de 1 año",    "puntaje": 1},
            {"texto": "1 a 3 años",         "puntaje": 2},
            {"texto": "3 a 7 años",         "puntaje": 3},
            {"texto": "Más de 7 años",      "puntaje": 4},
        ],
    },
    {
        "id": 2,
        "pregunta": "Si tu portfolio cae 20% en un mes, ¿qué hacés?",
        "opciones": [
            {"texto": "Vendo todo para no perder más",       "puntaje": 1},
            {"texto": "Vendo una parte para reducir riesgo", "puntaje": 2},
            {"texto": "No hago nada, espero recuperación",   "puntaje": 3},
            {"texto": "Compro más, es una oportunidad",      "puntaje": 4},
        ],
    },
    {
        "id": 3,
        "pregunta": "¿Qué porcentaje de tus ahorros tenés invertido?",
        "opciones": [
            {"texto": "Menos del 10%",       "puntaje": 1},
            {"texto": "Entre 10% y 30%",     "puntaje": 2},
            {"texto": "Entre 30% y 60%",     "puntaje": 3},
            {"texto": "Más del 60%",         "puntaje": 4},
        ],
    },
    {
        "id": 4,
        "pregunta": "¿Cuál es tu objetivo principal?",
        "opciones": [
            {"texto": "Preservar capital contra inflación",    "puntaje": 1},
            {"texto": "Crecimiento moderado y estable",        "puntaje": 2},
            {"texto": "Crecimiento agresivo a largo plazo",    "puntaje": 3},
            {"texto": "Máximo retorno, acepto alta volatilidad", "puntaje": 4},
        ],
    },
    {
        "id": 5,
        "pregunta": "¿Tenés ingresos estables (trabajo fijo, etc.)?",
        "opciones": [
            {"texto": "No, mis ingresos son variables",          "puntaje": 1},
            {"texto": "Parcialmente estables",                   "puntaje": 2},
            {"texto": "Sí, ingresos estables",                   "puntaje": 3},
            {"texto": "Sí, con margen amplio de ahorro mensual", "puntaje": 4},
        ],
    },
    {
        "id": 6,
        "pregunta": "¿Cuánto sabés sobre inversiones?",
        "opciones": [
            {"texto": "Casi nada, estoy empezando",              "puntaje": 1},
            {"texto": "Conozco lo básico (plazos fijos, FCI)",   "puntaje": 2},
            {"texto": "Manejo acciones, ETFs y bonos",           "puntaje": 3},
            {"texto": "Análisis técnico, derivados, opciones",   "puntaje": 4},
        ],
    },
    {
        "id": 7,
        "pregunta": "¿Cómo reaccionás ante noticias negativas del mercado?",
        "opciones": [
            {"texto": "Me preocupo mucho y reviso seguido",       "puntaje": 1},
            {"texto": "Me preocupo pero no actúo impulsivamente", "puntaje": 2},
            {"texto": "Lo analizo con calma",                     "puntaje": 3},
            {"texto": "Lo veo como oportunidad",                  "puntaje": 4},
        ],
    },
    {
        "id": 8,
        "pregunta": "¿Cuál de estos rendimientos preferís?",
        "opciones": [
            {"texto": "Seguro +5% anual",                        "puntaje": 1},
            {"texto": "Probable +15% (puede ser -5%)",           "puntaje": 2},
            {"texto": "Posible +30% (puede ser -15%)",           "puntaje": 3},
            {"texto": "Potencial +60% (puede ser -30%)",         "puntaje": 4},
        ],
    },
    {
        "id": 9,
        "pregunta": "¿Necesitás el dinero invertido en menos de 2 años?",
        "opciones": [
            {"texto": "Sí, es muy probable",        "puntaje": 1},
            {"texto": "Tal vez en parte",            "puntaje": 2},
            {"texto": "Poco probable",               "puntaje": 3},
            {"texto": "No, es capital a largo plazo","puntaje": 4},
        ],
    },
    {
        "id": 10,
        "pregunta": "¿Cómo describís tu situación financiera actual?",
        "opciones": [
            {"texto": "Ajustada, necesito liquidez",           "puntaje": 1},
            {"texto": "Estable, con poco margen",              "puntaje": 2},
            {"texto": "Cómoda, con ahorro mensual",            "puntaje": 3},
            {"texto": "Sólida, con ahorro significativo",      "puntaje": 4},
        ],
    },
]

PORTFOLIOS_MODELO = {
    "Conservador": {
        "descripcion": "Capital preservado con inflación cubierta",
        "disclaimer": "⚠️ Referencia educativa, no asesoramiento financiero",
        "allocacion": [
            {"activo": "Plazo Fijo / FCI Money Market", "porcentaje": 40, "razon": "Liquidez y tasa"},
            {"activo": "Bonos CER (inflación)",          "porcentaje": 25, "razon": "Cobertura inflación"},
            {"activo": "CEDEARs defensivos (KO, JNJ)",   "porcentaje": 20, "razon": "Dolarización parcial"},
            {"activo": "Oro (GOLD CEDEAR)",              "porcentaje": 15, "razon": "Reserva de valor"},
        ],
    },
    "Moderado": {
        "descripcion": "Crecimiento estable con riesgo controlado",
        "disclaimer": "⚠️ Referencia educativa, no asesoramiento financiero",
        "allocacion": [
            {"activo": "CEDEARs tech (GOOGL, MSFT, AAPL)", "porcentaje": 35, "razon": "Crecimiento USD"},
            {"activo": "ETF SPY / QQQ",                     "porcentaje": 25, "razon": "Diversificación global"},
            {"activo": "Acciones AR energía (YPF, PAM)",    "porcentaje": 20, "razon": "Alpha local"},
            {"activo": "Bonos / FCI",                       "porcentaje": 20, "razon": "Estabilidad"},
        ],
    },
    "Agresivo": {
        "descripcion": "Máximo crecimiento a largo plazo",
        "disclaimer": "⚠️ Referencia educativa, no asesoramiento financiero",
        "allocacion": [
            {"activo": "CEDEARs tech (NVDA, META, AMZN)",   "porcentaje": 40, "razon": "Alto crecimiento"},
            {"activo": "Acciones AR (YPF, PAM, TGS, GGAL)", "porcentaje": 30, "razon": "Alpha Argentina"},
            {"activo": "ETF emergentes / MELI",              "porcentaje": 20, "razon": "LATAM growth"},
            {"activo": "Crypto / especulativos",             "porcentaje": 10, "razon": "High risk/reward"},
        ],
    },
    "Especulador": {
        "descripcion": "Alto riesgo, alto retorno potencial",
        "disclaimer": "⚠️ Referencia educativa, no asesoramiento financiero",
        "allocacion": [
            {"activo": "Acciones AR small caps",       "porcentaje": 35, "razon": "Máximo alpha local"},
            {"activo": "CEDEARs tech concentrado",     "porcentaje": 30, "razon": "Concentración en winners"},
            {"activo": "Crypto (BTC, ETH)",            "porcentaje": 20, "razon": "Alto potencial"},
            {"activo": "Opciones / apalancamiento",    "porcentaje": 15, "razon": "Leverage"},
        ],
    },
}

MAX_PUNTAJE = 40


def calcular_perfil(puntajes: list) -> dict:
    total = sum(puntajes)
    if total <= 15:
        perfil      = "Conservador"
        descripcion = ("Priorizás preservar capital y minimizar pérdidas. "
                       "Preferís instrumentos seguros aunque el retorno sea menor. "
                       "Horizonte corto a mediano plazo.")
        color       = "#2196F3"
        emoji       = "🛡️"
    elif total <= 25:
        perfil      = "Moderado"
        descripcion = ("Buscás equilibrio entre rendimiento y seguridad. "
                       "Aceptás cierta volatilidad a cambio de mejores retornos. "
                       "Horizonte mediano a largo plazo.")
        color       = "#4CAF50"
        emoji       = "⚖️"
    elif total <= 33:
        perfil      = "Agresivo"
        descripcion = ("Buscás máximo crecimiento y tolerás caídas importantes. "
                       "Tenés convicción en tus inversiones y horizonte largo. "
                       "Capacidad financiera para absorber volatilidad.")
        color       = "#FF9800"
        emoji       = "🚀"
    else:
        perfil      = "Especulador"
        descripcion = ("Aceptás alta volatilidad a cambio de retornos extraordinarios. "
                       "Operás con convicción fuerte y horizonte flexible. "
                       "Solo apto para inversores con experiencia y colchón financiero.")
        color       = "#F44336"
        emoji       = "⚡"

    return {
        "perfil":        perfil,
        "descripcion":   descripcion,
        "color":         color,
        "emoji":         emoji,
        "puntaje_total": total,
        "porcentaje":    round(total / MAX_PUNTAJE * 100),
    }


def _clasificar_posicion(pos: dict) -> str:
    """Mapea una posición del portfolio a una categoría de análisis."""
    tipo    = (pos.get("tipo") or "").upper()
    sector  = (pos.get("sector") or "").lower()
    activo  = (pos.get("activo") or "").lower()
    ticker  = (pos.get("ticker") or "").upper()

    if tipo in ("FCI", "BOND", "BONO") or any(k in activo for k in ("fci", "bono", "plazo", "letras")):
        return "Bonos / FCI"
    if tipo == "CRYPTO" or any(k in activo for k in ("bitcoin", "crypto", "ethereum")):
        return "Crypto"
    if tipo == "ETF" or ticker in ("SPY", "QQQ", "EEM", "GLD", "IAU", "VWO"):
        return "ETFs"
    if tipo == "LOCAL":
        return "Acciones AR"
    if tipo == "CEDEAR":
        if "technology" in sector:
            return "CEDEARs tech"
        if "consumer" in sector or ticker in ("MELI",):
            return "CEDEARs otros"
        return "CEDEARs otros"
    return "Otros"


# Mapeo categorías del portfolio real → categorías del modelo por perfil
_MODELO_MAP = {
    "Conservador": {
        "Bonos / FCI":   65,   # Plazo Fijo (40) + Bonos CER (25)
        "CEDEARs tech":   0,
        "CEDEARs otros": 20,   # CEDEARs defensivos
        "ETFs":           0,
        "Acciones AR":    0,
        "Crypto":         0,
        "Otros":         15,   # Oro
    },
    "Moderado": {
        "Bonos / FCI":   20,
        "CEDEARs tech":  35,
        "CEDEARs otros":  0,
        "ETFs":          25,
        "Acciones AR":   20,
        "Crypto":         0,
        "Otros":          0,
    },
    "Agresivo": {
        "Bonos / FCI":    0,
        "CEDEARs tech":  40,
        "CEDEARs otros": 20,   # MELI / emergentes
        "ETFs":           0,
        "Acciones AR":   30,
        "Crypto":        10,
        "Otros":          0,
    },
    "Especulador": {
        "Bonos / FCI":    0,
        "CEDEARs tech":  30,
        "CEDEARs otros":  0,
        "ETFs":           0,
        "Acciones AR":   35,
        "Crypto":        20,
        "Otros":         15,   # Opciones / leverage
    },
}


def analizar_portfolio_actual(posiciones: list, perfil_usuario: str) -> dict:
    """Compara el portfolio real con el modelo del perfil."""
    if not posiciones:
        return {"observaciones": [], "composicion_real": {}}

    # Valor total y composición por categoría
    total_valor = sum(
        (p.get("precio_actual_ars") or 0) * (p.get("cantidad") or 0)
        for p in posiciones
    )
    if total_valor == 0:
        return {"observaciones": [], "composicion_real": {}}

    composicion: dict[str, float] = {}
    for pos in posiciones:
        cat   = _clasificar_posicion(pos)
        valor = (pos.get("precio_actual_ars") or 0) * (pos.get("cantidad") or 0)
        composicion[cat] = composicion.get(cat, 0) + valor

    composicion_pct = {cat: round(v / total_valor * 100, 1) for cat, v in composicion.items()}

    modelo = _MODELO_MAP.get(perfil_usuario, {})
    observaciones = []

    # Concentración individual (cualquier posición > 25% es alerta)
    for pos in posiciones:
        valor_pos = (pos.get("precio_actual_ars") or 0) * (pos.get("cantidad") or 0)
        peso = valor_pos / total_valor * 100
        if peso > 25:
            observaciones.append({
                "tipo": "rojo",
                "texto": (f"🔴 Concentración alta: {pos.get('activo', pos.get('ticker', '?'))} "
                          f"representa {peso:.1f}% del total"),
            })

    # Comparación por categoría vs modelo
    todas_cats = set(list(composicion_pct.keys()) + list(modelo.keys()))
    for cat in todas_cats:
        real   = composicion_pct.get(cat, 0)
        ideal  = modelo.get(cat, 0)
        gap    = real - ideal
        if ideal == 0 and real == 0:
            continue
        if ideal == 0 and real > 5:
            observaciones.append({
                "tipo": "amarillo",
                "texto": f"⚠️ Tu perfil no contempla {cat} pero tenés {real:.1f}%",
            })
        elif real == 0 and ideal >= 15:
            observaciones.append({
                "tipo": "amarillo",
                "texto": (f"⚠️ Tenés 0% en {cat} — "
                          f"tu perfil sugiere al menos {ideal}%"),
            })
        elif gap > 15:
            observaciones.append({
                "tipo": "amarillo",
                "texto": (f"⚠️ Sobreexposición en {cat}: "
                          f"tenés {real:.1f}% vs {ideal}% sugerido"),
            })
        elif -10 <= gap <= 15:
            if real > 0:
                observaciones.append({
                    "tipo": "verde",
                    "texto": (f"✅ Tu exposición a {cat} ({real:.1f}%) "
                              f"es adecuada para tu perfil"),
                })

    if not observaciones:
        observaciones.append({
            "tipo": "verde",
            "texto": "✅ Tu portfolio está bien alineado con tu perfil inversor",
        })

    return {"observaciones": observaciones, "composicion_real": composicion_pct}
