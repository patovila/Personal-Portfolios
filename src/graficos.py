"""Funciones de visualización."""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.data_layer import get_precios, get_fundamentals
from src.metricas import matriz_correlacion


def graficar_precio(ticker, periodo="1y"):
    """Gráfico de precio con línea horizontal de precio actual."""
    hist = get_precios([ticker], periodo).get(ticker, pd.DataFrame())
    
    if hist.empty:
        print(f"No hay datos para {ticker}")
        return
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name=ticker,
        line=dict(color="#00CC96", width=2),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Precio: $%{y:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=f"<b>{ticker}</b> — Evolución de precio ({periodo})",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
        template="plotly_dark",
        height=500,
        hovermode="x unified",
        showlegend=False,
    )
    
    precio_actual = hist["Close"].iloc[-1]
    fig.add_hline(
        y=precio_actual,
        line_dash="dot",
        line_color="yellow",
        annotation_text=f"Actual: ${precio_actual:.2f}",
        annotation_position="right"
    )
    
    fig.show()


def comparar_tickers(tickers, periodo="1y", normalizar=True):
    """Compara varios tickers en mismo gráfico (base 100 si normalizado)."""
    fig = go.Figure()
    colores = ["#00CC96", "#EF553B", "#636EFA", "#FFA15A", "#AB63FA"]
    
    batch = get_precios(list(tickers), periodo)
    for i, ticker in enumerate(tickers):
        hist = batch.get(ticker, pd.DataFrame())
        if hist.empty:
            continue
        
        valores = hist["Close"]
        if normalizar:
            valores = (valores / valores.iloc[0]) * 100
        
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=valores,
            mode="lines",
            name=ticker,
            line=dict(color=colores[i % len(colores)], width=2),
        ))
    
    titulo_y = "Base 100 (comparación %)" if normalizar else "Precio (USD)"
    fig.update_layout(
        title=f"<b>Comparación</b> ({periodo})",
        xaxis_title="Fecha",
        yaxis_title=titulo_y,
        template="plotly_dark",
        height=500,
        hovermode="x unified",
    )
    fig.show()


def grafico_candlestick(ticker, periodo="6mo"):
    """Gráfico de velas con volumen."""
    hist = get_precios([ticker], periodo).get(ticker, pd.DataFrame())
    
    if hist.empty:
        return
    
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.05, row_heights=[0.75, 0.25],
        subplot_titles=("Precio", "Volumen")
    )
    
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"],
        increasing_line_color="#00CC96", decreasing_line_color="#EF553B"
    ), row=1, col=1)
    
    colores = ["#00CC96" if c >= o else "#EF553B" 
               for o, c in zip(hist["Open"], hist["Close"])]
    fig.add_trace(go.Bar(
        x=hist.index, y=hist["Volume"],
        marker_color=colores, showlegend=False
    ), row=2, col=1)
    
    fig.update_layout(
        title=f"<b>{ticker}</b> — Análisis técnico ({periodo})",
        template="plotly_dark", height=700,
        xaxis_rangeslider_visible=False, showlegend=False,
    )
    fig.show()


def heatmap_correlacion(tickers, periodo="2y"):
    """Matriz de correlación visual."""
    corr = matriz_correlacion(tickers, periodo)
    
    fig = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdYlGn_r",
        zmin=-1, zmax=1,
        title=f"Matriz de correlación ({periodo})"
    )
    fig.update_layout(template="plotly_dark", height=500, width=600)
    fig.show()


def graficar_revenue_eps(ticker):
    """Revenue y Net Income en barras a través de los años."""
    pl = get_fundamentals(ticker)["pl"]

    if pl.empty:
        print(f"Sin datos para {ticker}")
        return
    
    años = [c.year for c in pl.columns]
    
    fig = go.Figure()
    
    if "Total Revenue" in pl.index:
        revenue = pl.loc["Total Revenue"] / 1e9
        fig.add_trace(go.Bar(
            x=años, y=revenue.values,
            name="Revenue",
            marker_color="#00CC96",
            text=[f"${v:.1f}B" for v in revenue.values],
            textposition="outside"
        ))
    
    if "Net Income" in pl.index:
        ni = pl.loc["Net Income"] / 1e9
        fig.add_trace(go.Bar(
            x=años, y=ni.values,
            name="Net Income",
            marker_color="#636EFA",
            text=[f"${v:.1f}B" for v in ni.values],
            textposition="outside"
        ))
    
    fig.update_layout(
        title=f"<b>{ticker}</b> - Revenue vs Net Income (USD Billones)",
        xaxis_title="Año",
        yaxis_title="USD Billones",
        template="plotly_dark",
        height=500,
        barmode="group",
        hovermode="x unified",
    )
    fig.show()


def graficar_fcf_historico(ticker):
    """Gráfico de barras del FCF histórico."""
    from src.fundamentals import fcf_historico
    
    fcf = fcf_historico(ticker)
    if fcf is None:
        return
    
    colores = ["#00CC96" if v >= 0 else "#EF553B" for v in fcf["FCF_USD_B"]]
    
    fig = go.Figure(go.Bar(
        x=fcf["año"],
        y=fcf["FCF_USD_B"],
        marker_color=colores,
        text=[f"${v:.1f}B" for v in fcf["FCF_USD_B"]],
        textposition="outside"
    ))
    
    fig.update_layout(
        title=f"<b>{ticker}</b> - Free Cash Flow Historico",
        xaxis_title="Año",
        yaxis_title="FCF (USD Billones)",
        template="plotly_dark",
        height=450,
    )
    fig.show()


def graficar_margenes(ticker):
    """Evolución de los márgenes en el tiempo."""
    pl = get_fundamentals(ticker)["pl"]

    if pl.empty or "Total Revenue" not in pl.index:
        print(f"Sin datos para {ticker}")
        return
    
    revenue = pl.loc["Total Revenue"]
    años = [c.year for c in pl.columns]
    
    fig = go.Figure()
    
    if "Gross Profit" in pl.index:
        margen_bruto = (pl.loc["Gross Profit"] / revenue * 100).values
        fig.add_trace(go.Scatter(
            x=años, y=margen_bruto,
            mode="lines+markers", name="Margen Bruto",
            line=dict(color="#00CC96", width=3),
            marker=dict(size=10)
        ))
    
    if "Operating Income" in pl.index:
        margen_op = (pl.loc["Operating Income"] / revenue * 100).values
        fig.add_trace(go.Scatter(
            x=años, y=margen_op,
            mode="lines+markers", name="Margen Operativo",
            line=dict(color="#636EFA", width=3),
            marker=dict(size=10)
        ))
    
    if "Net Income" in pl.index:
        margen_neto = (pl.loc["Net Income"] / revenue * 100).values
        fig.add_trace(go.Scatter(
            x=años, y=margen_neto,
            mode="lines+markers", name="Margen Neto",
            line=dict(color="#FFA15A", width=3),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title=f"<b>{ticker}</b> - Evolucion de margenes (%)",
        xaxis_title="Año",
        yaxis_title="Margen (%)",
        template="plotly_dark",
        height=500,
        hovermode="x unified",
    )
    fig.show()


def heatmap_peers(tickers, ratios=None):
    """Heatmap de comparación de ratios entre empresas."""
    from src.fundamentals import comparar_peers
    
    df = comparar_peers(tickers, ratios)
    df_num = df.set_index("Ticker").select_dtypes(include=[float, int])
    
    fig = px.imshow(
        df_num.T,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        title="Comparacion de Ratios - Peer Analysis"
    )
    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Empresas",
        yaxis_title="Ratios"
    )
    fig.show()