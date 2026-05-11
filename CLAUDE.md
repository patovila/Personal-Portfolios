# Proyecto: Mi Bloomberg Personal

## Sobre el usuario
- **Nombre**: Pato
- **Perfil**: Estudiante de finanzas con conocimientos intermedios de inversión (acciones, ETFs, dólar, DCF, VAN, TIR)
- **Nivel Python**: Principiante. Está aprendiendo desde cero, recién instaló Python 3.14
- **Ubicación**: Argentina. Opera con inflación, restricciones cambiarias, múltiples tipos de cambio
- **Horizonte de inversión**: Largo plazo (2026-2040)

## Objetivo del proyecto
Construir un sistema personal estilo "mini-Bloomberg" en Python para análisis financiero. Eventualmente integrarlo a la página educativa "Educación Financiera AR".

## Stack técnico
- Python 3.14.4 (en venv local)
- VS Code como IDE
- Librerías: yfinance, pandas, numpy, matplotlib, plotly, notebook, ipykernel
- Estructura modular: archivos .py en src/ + notebooks .ipynb en raíz
- Datos en data/ (incluyendo tickers.json con universo de papeles)

## Estructura actual del proyecto
PROYECTO/
- data/
  - tickers.json (portfolios, categorias, sectores, benchmarks)
- src/
  - __init__.py
  - datos.py: formatear, cargar_ticker, mostrar_ticker, cargar_universo, listar_categorias, buscar_ticker, diagnostico_entorno
  - metricas.py: variaciones, metricas_avanzadas, matriz_correlacion
  - graficos.py: graficar_precio, comparar_tickers, grafico_candlestick, heatmap_correlacion, graficar_revenue_eps, graficar_fcf_historico, graficar_margenes, heatmap_peers
  - fundamentals.py: estados_financieros, mostrar_estados, calcular_cagr, crecimiento_historico, ratios_avanzados, mostrar_ratios_completos, comparar_peers, fcf_historico, analisis_completo (+ helper interno _pct)
- venv/
- 01_exploracion.ipynb
- 02_dashboard.ipynb
- 03_fundamentals.ipynb

## Portfolio personal del usuario
- Tickers principales: YPF, PAM, TGS, MELI
- Sector concentrado: energia argentina (YPF, PAM, TGS correlacionados ~0.85)
- Tesis activa: Vaca Muerta + reformas argentinas (RIGI, RQT)
- Maneja 2 portfolios: personal + familiar

## Plan de trabajo (cronograma 12 semanas)
- Semana 1: Setup + funciones basicas + metricas avanzadas - COMPLETADA
- Semana 2: Estados financieros + ratios fundamentales - COMPLETADA (cierre 2026-05-05)
- Semana 3: Analisis tecnico (RSI, MACD, Bollinger Bands, soportes/resistencias) - COMPLETADA (cierre 2026-05-11)
- Semana 4: Comparacion sectorial profunda - PROXIMA
- Semana 5-6: DCF (modo simple + avanzado con sliders)
- Semana 7-8: Migracion a Streamlit (web app)
- Semana 9+: Integracion con Educacion Financiera AR

## Preferencias de respuesta del usuario
- Respuestas claras, directas, sin relleno
- Explicaciones practicas, no teoria innecesaria
- Ejemplos aplicados a Argentina cuando posible
- Si hay opciones, comparar y recomendar una
- Marcar riesgos, supuestos, errores potenciales
- Si algo esta mal planteado, corregir sin suavizar
- Priorizar eficiencia, costo-beneficio, toma de decisiones

## Estilo de ensenanza
- Pato esta aprendiendo. Explicar el "por que" detras del codigo, no solo el "como"
- Indicar pegado paso a paso (que archivo, que lineas)
- Cuando hay error, explicar la causa antes de la solucion
- No asumir conocimiento previo de Git, Streamlit, APIs

## Estado actual (cierre Semana 3 - 2026-05-11)
Nuevo modulo src/tecnico.py:
- rsi(ticker, ventana=14) con suavizado Wilder (EMA alpha=1/n)
- macd(ticker, 12, 26, 9) devuelve DataFrame con MACD/Senal/Histograma
- bollinger(ticker, ventana=20, desv=2) devuelve precio + bandas + ancho %
- soportes_resistencias(ticker) por max/min locales con ventana centrada
- señales_tecnicas / mostrar_señales: resumen interpretado de los 3 indicadores
- _cargar_close helper acepta ticker (str) o DataFrame para no duplicar logica

Nuevas funciones en src/graficos.py:
- graficar_rsi (subplot precio + RSI con bandas 30/70)
- graficar_macd (subplot precio + MACD con histograma coloreado)
- graficar_bollinger (precio + bandas + media + area sombreada)
- graficar_soportes_resistencias (velas + hlines de S/R)

Notebook 04_tecnico.ipynb con 7 secciones: senales YPF, RSI, MACD, Bollinger,
S/R, comparacion del portfolio, cross-check vs candlestick.

Bug corregido en src/fundamentals.py:
- crecimiento_historico() dropea NaN antes de calcular CAGR. Antes, empresas
  con menos de 4 años de historia (ej MELI con NaN en 2021) daban None en
  todos los CAGR. Ahora calcula años reales por diferencia de fechas.
- Helper _cagr_de_serie centraliza la logica. Tambien se arreglo
  expansion_margen_pp con la misma logica de NaN-handling.

## Proxima tarea concreta - Arranque Semana 4
- Comparacion sectorial profunda: agregar metricas relativas (PE vs sector,
  margen vs peers), ranking de papeles dentro de un sector, dispersion
  intra-sector. Usar universo['sectores'] como input. Posibles nuevos archivos:
  src/sectorial.py + funciones de viz tipo box plot / scatter en graficos.py.