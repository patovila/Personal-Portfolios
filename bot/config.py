"""Configuración del bot. Todos los secrets vienen de variables de entorno."""
import os
from pathlib import Path

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID: str = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── Watchlist a monitorear en el brief diario ─────────────────────────────────
WATCHLIST: list[str] = [
    "YPF", "PAM", "TGS", "MELI",
    "GGAL", "BMA", "NVDA", "AAPL",
    "GOOGL", "AMZN",
]

# ── Paths ─────────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).parent.parent
ALERTAS_FILE = _REPO_ROOT / "data" / "alertas" / "pato.json"

# ── App URL (sin https:// para usar en texto y en links) ─────────────────────
APP_URL = "personalfinances.streamlit.app"
APP_URL_FULL = f"https://{APP_URL}"
