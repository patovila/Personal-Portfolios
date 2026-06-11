"""Utilidades para enviar mensajes via Telegram Bot API."""
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import TELEGRAM_TOKEN, CHAT_ID


def enviar_mensaje(texto: str, chat_id: str | None = None) -> bool:
    """Envía mensaje HTML por Telegram. Retorna True si tuvo éxito."""
    token = TELEGRAM_TOKEN
    cid = chat_id or CHAT_ID

    if not token:
        print("ERROR: TELEGRAM_TOKEN no configurado")
        return False
    if not cid:
        print("ERROR: TELEGRAM_CHAT_ID no configurado")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": cid,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        print(f"ERROR HTTP Telegram: {e.response.status_code} — {e.response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR enviando mensaje Telegram: {e}")
    return False


def enviar_alerta(titulo: str, cuerpo: str) -> bool:
    """Helper para alertas con formato fijo."""
    msg = f"🚨 <b>{titulo}</b>\n{cuerpo}"
    return enviar_mensaje(msg)
