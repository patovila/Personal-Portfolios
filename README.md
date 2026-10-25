# 📊 Mi Bloomberg Personal

> Herramienta de análisis financiero para el inversor argentino — gratis, open-source y sin registro.

**[🚀 Ver app en vivo →](https://mi-bloomberg-personal.streamlit.app)**

---

## ¿Qué es?

Un terminal financiero personal construido en Python + Streamlit. Pensado para quien opera en el mercado argentino: CEDEARs, ADRs, Merval, dólar blue/MEP/CCL, y análisis fundamental al estilo Bloomberg pero sin el costo.

## Features principales

| Módulo | Descripción |
|---|---|
| 🏢 **Ficha** | Precio en tiempo real, métricas clave, Fair Value rápido |
| 📊 **Fundamental** | Estados financieros, ratios (PE, ROE, ROA, PB), CAGR, márgenes |
| 📈 **Técnico** | RSI, MACD, Bollinger Bands, soportes y resistencias |
| 💼 **Mi Portfolio** | P&L en tiempo real, beta ponderada, exposición por sector |
| 📐 **DCF & Valuación** | WACC automático (CAPM), sensibilidad, escenarios Bull/Base/Bear |
| 🇦🇷 **Macro Argentina** | Dólar oficial/blue/MEP/CCL, riesgo país, Merval |
| 🧮 **Calculadoras** | Interés compuesto, inflación, tipos de cambio |
| 📰 **Noticias** | Feed con análisis de sentimiento por ticker |
| ⚖️ **Comparar** | Comparación lado a lado de hasta 5 empresas |

## Stack técnico

- **Python 3.12** · **Streamlit 1.57**
- **yfinance** — datos de mercado
- **Plotly** — visualizaciones interactivas
- **pandas / numpy** — análisis de datos
- **vaderSentiment** — NLP para sentimiento de noticias
- **DolarAPI / ArgentinaDatos** — datos del mercado argentino

## Correrlo localmente

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/mi-bloomberg-personal.git
cd mi-bloomberg-personal

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Configurar API key de Finnhub para earnings
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Editar secrets.toml con tu API key

# 5. Lanzar
streamlit run app.py
```

## Estructura del proyecto

```
├── app.py              # App principal Streamlit
├── src/
│   ├── data_layer.py   # Capa única de acceso a yfinance
│   ├── datos.py        # Mapa de tickers AR ↔ ADR
│   ├── dcf.py          # Valuación DCF + WACC automático
│   ├── fundamentals.py # Ratios y estados financieros
│   ├── portfolio.py    # Gestión de posiciones
│   ├── mercado.py      # Heatmap, índices, ticker tape
│   ├── dolar.py        # Cotizaciones ARS en tiempo real
│   └── tecnico.py      # RSI, MACD, Bollinger
├── data/
│   └── tickers.json    # Universo de tickers (50+)
└── .streamlit/
    └── secrets.toml.example
```

## Disclaimer

**Este proyecto es solo para fines educativos. No constituye asesoramiento financiero. Toda decisión de inversión es responsabilidad exclusiva del usuario.**

---

---

# 📊 Mi Bloomberg Personal (English)

> Personal financial analysis tool for Argentine investors — free, open-source, no sign-up required.

**[🚀 Live app →](https://mi-bloomberg-personal.streamlit.app)**

## What is it?

A personal financial terminal built with Python + Streamlit. Designed for investors operating in the Argentine market: CEDEARs, ADRs, Merval index, blue/MEP/CCL dollar rates, and Bloomberg-style fundamental analysis — without the cost.

## Key Features

| Module | Description |
|---|---|
| 🏢 **Stock Card** | Real-time price, key metrics, quick Fair Value |
| 📊 **Fundamentals** | Financial statements, ratios (PE, ROE, ROA), CAGR, margins |
| 📈 **Technical** | RSI, MACD, Bollinger Bands, support & resistance |
| 💼 **My Portfolio** | Real-time P&L, weighted beta, sector exposure |
| 📐 **DCF & Valuation** | Auto WACC (CAPM), sensitivity table, Bull/Base/Bear scenarios |
| 🇦🇷 **Argentina Macro** | Official/blue/MEP/CCL dollar, country risk, Merval |
| 🧮 **Calculators** | Compound interest, inflation, FX conversion |
| 📰 **News** | News feed with sentiment analysis per ticker |
| ⚖️ **Compare** | Side-by-side comparison of up to 5 companies |

## Tech Stack

- **Python 3.12** · **Streamlit 1.57**
- **yfinance** — market data
- **Plotly** — interactive charts
- **pandas / numpy** — data analysis
- **vaderSentiment** — NLP sentiment analysis
- **DolarAPI / ArgentinaDatos** — Argentine market data

## Running Locally

```bash
git clone https://github.com/tu-usuario/mi-bloomberg-personal.git
cd mi-bloomberg-personal
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

**This project is for educational purposes only. It does not constitute financial advice. All investment decisions are the sole responsibility of the user.**
