# Bot de Telegram — Mi Bloomberg

Bot standalone (sin Streamlit) que envía alertas de precio y un brief financiero diario.

## Archivos

| Archivo | Descripción |
|---|---|
| `config.py` | Variables de entorno, paths, watchlist |
| `telegram_utils.py` | `enviar_mensaje()` via Telegram Bot API |
| `check_alertas.py` | Lee alertas del JSON y notifica si se disparan |
| `brief_diario.py` | Mensaje con dólares, mercados y watchlist |

---

## Setup — Una sola vez

### 1. Crear el bot con BotFather

1. En Telegram, buscá `@BotFather`
2. Enviá `/newbot` y seguí las instrucciones
3. Copiá el **token** que te da (formato `1234567890:ABCdef...`)

### 2. Obtener tu CHAT_ID

1. Mandá cualquier mensaje a tu nuevo bot
2. Abrí este link en el browser (reemplazá `<TOKEN>` con el tuyo):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. En el JSON, buscá `"chat": {"id": 123456789}` — ese número es tu `CHAT_ID`

### 3. Configurar GitHub Secrets

En tu repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Valor |
|---|---|
| `TELEGRAM_TOKEN` | El token del paso 1 |
| `TELEGRAM_CHAT_ID` | El chat_id del paso 2 |

### 4. Activar los workflows

- Ir a **Actions** en tu repo de GitHub
- Si dice "Workflows are disabled", hacer click en **Enable** 
- El cron se activa automáticamente al hacer push al branch `main`

---

## Schedule

| Job | Cuándo | Horario ART |
|---|---|---|
| `check-alertas` | Cada 15 min, lun-vie | 10:00 — 18:00 |
| `brief-diario` | Diario, lun-vie | 9:00 AM |

> GitHub Actions usa UTC. ART = UTC−3.

---

## Prueba manual

Desde la pestaña **Actions** → seleccioná el workflow **"Mi Bloomberg Bot"** → **Run workflow**.

Ambos jobs corren juntos en la ejecución manual.

---

## Probar localmente

```bash
# Requiere TELEGRAM_TOKEN y TELEGRAM_CHAT_ID como variables de entorno
$env:TELEGRAM_TOKEN="tu_token"
$env:TELEGRAM_CHAT_ID="tu_chat_id"

python bot/check_alertas.py
python bot/brief_diario.py
```

---

## Cómo funcionan las alertas

El bot lee `data/alertas/pato.json` (el mismo archivo que usa la app Streamlit).

| `tipo` | Se dispara cuando |
|---|---|
| `take_profit` | `precio >= valor` |
| `stop_loss` | `precio <= valor` |
| `variacion_dia` | `abs(variacion%) >= valor` |

Al dispararse, el bot:
1. Envía el mensaje a Telegram
2. Marca `activa: false` y `disparada: true` en el JSON
3. GitHub Actions hace commit del JSON actualizado (con `[skip ci]` para no loops)

---

## Agregar tickers a la watchlist del brief

Editá `bot/config.py`, sección `WATCHLIST`:

```python
WATCHLIST: list[str] = [
    "YPF", "PAM", "TGS", "MELI",
    # Agregá acá los tickers que quieras
]
```
