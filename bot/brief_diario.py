"""
Brief financiero diario — standalone, sin Streamlit.

Ejecutar:  python bot/brief_diario.py
Schedule:  12:00 UTC = 9:00 AM ART, lunes-viernes
"""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

sys.path.insert(0, str(Path(__file__).parent))
from config import APP_URL, APP_URL_FULL, WATCHLIST
from telegram_utils import enviar_mensaje


# ---------------------------------------------------------------------------
# Data fetchers — sin @st.cache_data, ejecutan una vez por run
# ---------------------------------------------------------------------------

def get_dolares() -> dict:
    """Cotizaciones actuales desde dolarapi.com."""
    try:
        r = requests.get("https://dolarapi.com/v1/dolares", timeout=8)
        r.raise_for_status()
        por_casa = {item["casa"]: item for item in r.json()}
        return {
            "oficial": por_casa.get("oficial", {}).get("venta"),
            "blue":    por_casa.get("blue", {}).get("venta"),
            "mep":     por_casa.get("bolsa", {}).get("venta"),
            "ccl":     por_casa.get("contadoconliqui", {}).get("venta"),
        }
    except Exception as e:
        print(f"  Error dólares: {e}")
        return {}


def get_riesgo_pais() -> tuple:
    """(valor_hoy: int | None, delta_bps: int | None)."""
    try:
        r = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais",
            timeout=10,
        )
        r.raise_for_status()
        df = pd.DataFrame(r.json()).dropna(subset=["valor"])
        if len(df) >= 2:
            return int(df["valor"].iloc[-1]), int(df["valor"].iloc[-1]) - int(df["valor"].iloc[-2])
        if len(df) == 1:
            return int(df["valor"].iloc[-1]), None
    except Exception as e:
        print(f"  Error riesgo país: {e}")
    return None, None


def get_indices() -> dict:
    """Merval y S&P500 via yfinance batch."""
    try:
        data = yf.download(
            "^MERV ^GSPC",
            period="2d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
        )
        result = {}
        for tk, nombre in [("^MERV", "merval"), ("^GSPC", "sp500")]:
            try:
                close = data[tk]["Close"].dropna()
                if len(close) >= 2:
                    precio = float(close.iloc[-1])
                    var = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
                    result[nombre] = {"precio": precio, "var": var}
            except Exception:
                pass
        return result
    except Exception as e:
        print(f"  Error índices: {e}")
        return {}


def get_movers_watchlist() -> list:
    """Top movers de WATCHLIST, ordenados de mayor a menor variación."""
    if not WATCHLIST:
        return []
    try:
        data = yf.download(
            " ".join(WATCHLIST),
            period="2d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
        )
        if data is None or data.empty:
            return []
        items = []
        for tk in WATCHLIST:
            try:
                if len(WATCHLIST) == 1:
                    close = data["Close"].dropna()
                else:
                    close = data[tk]["Close"].dropna()
                if len(close) >= 2:
                    var = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
                    items.append({"ticker": tk, "var": var})
            except Exception:
                pass
        return sorted(items, key=lambda x: x["var"], reverse=True)
    except Exception as e:
        print(f"  Error watchlist: {e}")
        return []


# ---------------------------------------------------------------------------
# Construcción del mensaje
# ---------------------------------------------------------------------------

_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
_MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _ars(v) -> str:
    """Formatea precio ARS estilo argentino: $1.455"""
    if v is None:
        return "—"
    return f"${v:,.0f}".replace(",", ".")


def _pct(v) -> str:
    """Formatea variación con signo."""
    if v is None:
        return ""
    signo = "+" if v >= 0 else ""
    return f" ({signo}{v:.2f}%)"


def construir_mensaje() -> str:
    ahora = datetime.now()
    fecha_str = f"{_DIAS[ahora.weekday()]} {ahora.day} de {_MESES[ahora.month - 1]}"

    lines: list[str] = [
        "🌅 <b>Buenos días — Brief Financiero AR</b>",
        f"📅 {fecha_str}",
        "",
    ]

    # Sección 1: Dólares
    print("  Obteniendo dólares...")
    dolares = get_dolares()
    if dolares:
        lines += [
            "💵 <b>Dólares:</b>",
            (
                f"- Oficial: {_ars(dolares.get('oficial'))} | "
                f"Blue: {_ars(dolares.get('blue'))} | "
                f"MEP: {_ars(dolares.get('mep'))} | "
                f"CCL: {_ars(dolares.get('ccl'))}"
            ),
            "",
        ]

    # Sección 2: Mercados
    print("  Obteniendo riesgo país...")
    rp, rp_delta = get_riesgo_pais()
    print("  Obteniendo índices...")
    indices = get_indices()

    mercado_lines = ["📊 <b>Mercados:</b>"]

    merval = indices.get("merval")
    if merval:
        precio_fmt = f"{merval['precio']:,.0f}".replace(",", ".")
        mercado_lines.append(f"- Merval: {precio_fmt}{_pct(merval['var'])}")

    sp500 = indices.get("sp500")
    if sp500:
        # &amp; es el escape HTML para & en Telegram
        mercado_lines.append(f"- S&amp;P 500: {sp500['precio']:,.0f}{_pct(sp500['var'])}")

    if rp is not None:
        rp_str = f"{rp} bps"
        if rp_delta is not None:
            rp_str += f" ({rp_delta:+d})"
        mercado_lines.append(f"- Riesgo País: {rp_str}")

    if len(mercado_lines) > 1:
        lines += mercado_lines + [""]

    # Sección 3: Watchlist movers
    print("  Obteniendo watchlist...")
    movers = get_movers_watchlist()
    if movers:
        # Mejor, 2do mejor, peor
        top = movers[:2]
        peor = [movers[-1]] if movers[-1] not in top else []
        mostrar = top + peor
        movers_str = " | ".join(f"{m['ticker']} {m['var']:+.2f}%" for m in mostrar)
        lines += [
            "🚀 <b>Tu watchlist hoy:</b>",
            f"- {movers_str}",
            "",
        ]

    lines.append(f"🔗 <a href='{APP_URL_FULL}'>{APP_URL}</a>")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"=== Brief diario — {datetime.now():%Y-%m-%d %H:%M} ===")
    print("Recopilando datos...")

    msg = construir_mensaje()
    print("\nMensaje a enviar:")
    print("-" * 50)
    print(msg)
    print("-" * 50)

    print("\nEnviando a Telegram...")
    ok = enviar_mensaje(msg)
    print("✅ Enviado correctamente" if ok else "❌ Error al enviar")
    sys.exit(0 if ok else 1)
