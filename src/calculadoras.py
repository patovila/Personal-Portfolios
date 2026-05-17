"""Calculadoras financieras para el mercado argentino."""
import pandas as pd


def calc_billetera(monto: float, tna: float, dias: int, inflacion_mensual: float) -> dict:
    """Billetera virtual: capitalizacion diaria."""
    tasa_diaria = tna / 100 / 365
    monto_final = monto * (1 + tasa_diaria) ** dias
    intereses = monto_final - monto
    tea = (1 + tasa_diaria) ** 365 - 1
    inflacion_periodo = (1 + inflacion_mensual / 100) ** (dias / 30) - 1
    rendimiento_nominal = monto_final / monto - 1
    rendimiento_real = (1 + rendimiento_nominal) / (1 + inflacion_periodo) - 1
    return {
        "monto_inicial": monto,
        "monto_final": monto_final,
        "intereses": intereses,
        "tea_pct": tea * 100,
        "tna_pct": tna,
        "rendimiento_nominal_pct": rendimiento_nominal * 100,
        "rendimiento_real_pct": rendimiento_real * 100,
        "inflacion_periodo_pct": inflacion_periodo * 100,
        "tipo": "billetera",
    }


def calc_plazo_fijo(monto: float, tna: float, dias: int, inflacion_mensual: float) -> dict:
    """Plazo fijo: capitalizacion al vencimiento (interes simple)."""
    monto_final = monto * (1 + (tna / 100) * (dias / 365))
    intereses = monto_final - monto
    tea = (monto_final / monto) ** (365 / dias) - 1
    inflacion_periodo = (1 + inflacion_mensual / 100) ** (dias / 30) - 1
    rendimiento_nominal = monto_final / monto - 1
    rendimiento_real = (1 + rendimiento_nominal) / (1 + inflacion_periodo) - 1
    return {
        "monto_inicial": monto,
        "monto_final": monto_final,
        "intereses": intereses,
        "tea_pct": tea * 100,
        "tna_pct": tna,
        "rendimiento_nominal_pct": rendimiento_nominal * 100,
        "rendimiento_real_pct": rendimiento_real * 100,
        "inflacion_periodo_pct": inflacion_periodo * 100,
        "tipo": "plazo_fijo",
    }


def calc_fci(monto: float, tna: float, dias: int, inflacion_mensual: float) -> dict:
    """FCI Money Market: capitalizacion diaria."""
    tasa_diaria = tna / 100 / 365
    monto_final = monto * (1 + tasa_diaria) ** dias
    intereses = monto_final - monto
    tea = (1 + tasa_diaria) ** 365 - 1
    inflacion_periodo = (1 + inflacion_mensual / 100) ** (dias / 30) - 1
    rendimiento_nominal = monto_final / monto - 1
    rendimiento_real = (1 + rendimiento_nominal) / (1 + inflacion_periodo) - 1
    return {
        "monto_inicial": monto,
        "monto_final": monto_final,
        "intereses": intereses,
        "tea_pct": tea * 100,
        "tna_pct": tna,
        "rendimiento_nominal_pct": rendimiento_nominal * 100,
        "rendimiento_real_pct": rendimiento_real * 100,
        "inflacion_periodo_pct": inflacion_periodo * 100,
        "tipo": "fci",
    }


def calc_bono(precio_compra: float, valor_cobro: float, dias: int) -> dict:
    """Bono simple: rendimiento total y TIR anualizada."""
    if precio_compra <= 0 or dias <= 0:
        return {}
    rendimiento_total = (valor_cobro / precio_compra - 1) * 100
    rendimiento_diario = (valor_cobro / precio_compra) ** (1 / dias) - 1
    tir_anualizada = (1 + rendimiento_diario) ** 365 - 1
    ganancia = valor_cobro - precio_compra
    return {
        "precio_compra": precio_compra,
        "valor_cobro": valor_cobro,
        "ganancia": ganancia,
        "rendimiento_total_pct": rendimiento_total,
        "rendimiento_diario_pct": rendimiento_diario * 100,
        "tir_anualizada_pct": tir_anualizada * 100,
        "dias": dias,
    }


def comparar_todas(monto: float, dias: int, tasas_dict: dict, inflacion_mensual: float) -> pd.DataFrame:
    """Compara todas las opciones para un monto y plazo. Devuelve DataFrame ordenado por rendimiento."""
    inflacion_periodo = (1 + inflacion_mensual / 100) ** (dias / 30) - 1

    filas = []

    r = calc_billetera(monto, tasas_dict.get("billetera", 32), dias, inflacion_mensual)
    filas.append({
        "Instrumento": "💵 Billetera Virtual",
        "Monto final": r["monto_final"],
        "Intereses": r["intereses"],
        "TEA %": r["tea_pct"],
        "Rend. real %": r["rendimiento_real_pct"],
        "_orden": r["rendimiento_nominal_pct"],
    })

    r = calc_plazo_fijo(monto, tasas_dict.get("plazo_fijo", 38), dias, inflacion_mensual)
    filas.append({
        "Instrumento": "📅 Plazo Fijo",
        "Monto final": r["monto_final"],
        "Intereses": r["intereses"],
        "TEA %": r["tea_pct"],
        "Rend. real %": r["rendimiento_real_pct"],
        "_orden": r["rendimiento_nominal_pct"],
    })

    r = calc_fci(monto, tasas_dict.get("fci", 40), dias, inflacion_mensual)
    filas.append({
        "Instrumento": "📊 FCI Money Market",
        "Monto final": r["monto_final"],
        "Intereses": r["intereses"],
        "TEA %": r["tea_pct"],
        "Rend. real %": r["rendimiento_real_pct"],
        "_orden": r["rendimiento_nominal_pct"],
    })

    rend_bono_pct = tasas_dict.get("bono", 8)
    valor_cobro_bono = monto * (1 + rend_bono_pct / 100)
    r_bono = calc_bono(monto, valor_cobro_bono, dias)
    rend_real_bono = (1 + rend_bono_pct / 100) / (1 + inflacion_periodo) - 1
    filas.append({
        "Instrumento": "📈 Bono",
        "Monto final": valor_cobro_bono,
        "Intereses": valor_cobro_bono - monto,
        "TEA %": r_bono.get("tir_anualizada_pct", 0),
        "Rend. real %": rend_real_bono * 100,
        "_orden": rend_bono_pct,
    })

    df = pd.DataFrame(filas)
    df = df.sort_values("_orden", ascending=False).reset_index(drop=True)
    return df.drop(columns=["_orden"])


def evolucion_diaria(monto: float, tna: float, dias: int, tipo: str = "diaria") -> pd.DataFrame:
    """Evolucion dia a dia del monto. tipo='diaria' o 'vencimiento'."""
    dias_arr = list(range(0, dias + 1))
    if tipo == "diaria":
        tasa_diaria = tna / 100 / 365
        montos = [monto * (1 + tasa_diaria) ** d for d in dias_arr]
    else:
        montos = [monto * (1 + (tna / 100) * (d / 365)) for d in dias_arr]
    return pd.DataFrame({"dia": dias_arr, "monto": montos})
