"""
Verificador de alertas de precio — standalone, sin Streamlit.

Ejecutar:  python bot/check_alertas.py
Schedule:  cada 15 min, lun-vie 13:00-21:00 UTC (10:00-18:00 ART)
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

sys.path.insert(0, str(Path(__file__).parent))
from config import ALERTAS_FILE, APP_URL_FULL
from telegram_utils import enviar_mensaje


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def cargar_alertas() -> list:
    if not ALERTAS_FILE.exists():
        print(f"Archivo no encontrado: {ALERTAS_FILE}")
        return []
    try:
        with open(ALERTAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando alertas: {e}")
        return []


def guardar_alertas(alertas: list) -> None:
    try:
        ALERTAS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ALERTAS_FILE, "w", encoding="utf-8") as f:
            json.dump(alertas, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando alertas: {e}")


# ---------------------------------------------------------------------------
# Precios batch
# ---------------------------------------------------------------------------

def get_precios_batch(tickers: list) -> dict:
    """Retorna {ticker: {precio, variacion_dia}} via yf.download batch."""
    if not tickers:
        return {}
    unique = list(set(tickers))
    try:
        data = yf.download(
            " ".join(unique),
            period="2d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception as e:
        print(f"Error descargando precios: {e}")
        return {}

    if data is None or data.empty:
        return {}

    result: dict = {}
    for tk in unique:
        try:
            if len(unique) == 1:
                close = data["Close"].dropna() if "Close" in data.columns else pd.Series(dtype=float)
            else:
                close = data[tk]["Close"].dropna()
            if close.empty:
                continue
            precio = float(close.iloc[-1])
            variacion = 0.0
            if len(close) >= 2:
                prev = float(close.iloc[-2])
                if prev:
                    variacion = (precio - prev) / prev * 100
            result[tk] = {"precio": precio, "variacion_dia": variacion}
        except Exception as e:
            print(f"  Error procesando {tk}: {e}")

    return result


# ---------------------------------------------------------------------------
# Verificación y notificación
# ---------------------------------------------------------------------------

def _mensaje_alerta(alerta: dict, precio: float, variacion: float) -> str:
    """Arma el HTML para Telegram."""
    tk = alerta["ticker"]
    valor = alerta["valor"]
    tipo = alerta["tipo"]

    if tipo == "take_profit":
        icono = "📈"
        desc = f"{tk} superó el objetivo de <b>${valor:,.2f}</b>"
    elif tipo == "stop_loss":
        icono = "🛑"
        desc = f"{tk} cayó bajo el stop-loss de <b>${valor:,.2f}</b>"
    else:  # variacion_dia
        icono = "⚡"
        desc = f"{tk} tuvo una variación de <b>{variacion:+.2f}%</b> (umbral: ±{valor:.0f}%)"

    return (
        f"🚨 <b>ALERTA DISPARADA</b>\n"
        f"{icono} {desc}\n"
        f"Precio actual: <b>${precio:,.2f}</b>\n"
        f"🔗 <a href='{APP_URL_FULL}'>{APP_URL_FULL}</a>"
    )


def verificar_alertas(alertas: list, precios: dict) -> tuple[list, int]:
    """Verifica condiciones, envía mensajes y retorna (lista_actualizada, n_disparadas)."""
    disparadas = 0
    for alerta in alertas:
        if not alerta.get("activa") or alerta.get("disparada"):
            continue
        datos = precios.get(alerta["ticker"])
        if not datos:
            continue

        precio = datos["precio"]
        variacion = datos["variacion_dia"]
        tipo = alerta["tipo"]
        valor = alerta["valor"]

        triggered = False
        if tipo == "take_profit" and precio >= valor:
            triggered = True
        elif tipo == "stop_loss" and precio <= valor:
            triggered = True
        elif tipo == "variacion_dia" and abs(variacion) >= valor:
            triggered = True

        if triggered:
            msg = _mensaje_alerta(alerta, precio, variacion)
            print(f"  Disparada: {alerta['ticker']} ({tipo})")
            if enviar_mensaje(msg):
                alerta["disparada"] = True
                alerta["activa"] = False
                alerta["fecha_disparo"] = datetime.now().isoformat()
                disparadas += 1

    return alertas, disparadas


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"=== Check de alertas — {datetime.now():%Y-%m-%d %H:%M} ===")

    alertas = cargar_alertas()
    activas = [a for a in alertas if a.get("activa") and not a.get("disparada")]
    print(f"Alertas activas: {len(activas)}")

    if not activas:
        print("Sin alertas activas. Saliendo.")
        sys.exit(0)

    tickers = list({a["ticker"] for a in activas})
    print(f"Descargando precios: {', '.join(tickers)}")
    precios = get_precios_batch(tickers)
    print(f"Precios obtenidos: {list(precios.keys())}")

    alertas_actualizadas, n = verificar_alertas(alertas, precios)

    if n > 0:
        guardar_alertas(alertas_actualizadas)
        print(f"✅ {n} alerta(s) disparada(s) y guardadas.")
    else:
        print("Sin alertas disparadas en este ciclo.")

    sys.exit(0)
