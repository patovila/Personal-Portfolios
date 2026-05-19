"""Análisis fundamental: estados financieros, ratios avanzados y crecimiento."""
import yfinance as yf
import pandas as pd

from src.datos import formatear, get_ticker_adr


def _pct(info, key):
    """Helper: extrae un valor de info y lo multiplica x100, preservando None y 0."""
    v = info.get(key)
    return v * 100 if v is not None else None


def estados_financieros(ticker, formato="resumido"):
    """Devuelve los 3 estados financieros principales."""
    t = yf.Ticker(get_ticker_adr(ticker))
    
    pl = t.financials
    balance = t.balance_sheet
    cashflow = t.cashflow
    
    if pl.empty:
        print(f"Sin datos financieros para {ticker}")
        return None
    
    if formato == "resumido":
        lineas_pl = ["Total Revenue", "Gross Profit", "Operating Income", 
                     "Net Income", "EBITDA", "Basic EPS"]
        pl_filtrado = pl.loc[pl.index.intersection(lineas_pl)]
        
        lineas_bs = ["Total Assets", "Current Assets", "Cash And Cash Equivalents",
                     "Total Debt", "Long Term Debt", "Stockholders Equity"]
        bs_filtrado = balance.loc[balance.index.intersection(lineas_bs)]
        
        lineas_cf = ["Operating Cash Flow", "Free Cash Flow", "Capital Expenditure",
                     "Cash Dividends Paid", "Repurchase Of Capital Stock"]
        cf_filtrado = cashflow.loc[cashflow.index.intersection(lineas_cf)]
        
        return {
            "pl": pl_filtrado,
            "balance": bs_filtrado,
            "cashflow": cf_filtrado
        }
    
    return {
        "pl": pl,
        "balance": balance,
        "cashflow": cashflow
    }


def mostrar_estados(ticker):
    """Imprime los estados financieros formateados."""
    estados = estados_financieros(ticker, "resumido")
    if not estados:
        return
    
    print(f"\n{'='*60}")
    print(f"  ESTADOS FINANCIEROS - {ticker}")
    print(f"{'='*60}\n")
    
    print("ESTADO DE RESULTADOS (P&L)")
    print("-" * 60)
    pl = estados["pl"] / 1e9
    pl.columns = [c.strftime("%Y") for c in pl.columns]
    print(pl.round(2).to_string())
    print("(valores en miles de millones USD)\n")
    
    print("BALANCE GENERAL")
    print("-" * 60)
    bs = estados["balance"] / 1e9
    bs.columns = [c.strftime("%Y") for c in bs.columns]
    print(bs.round(2).to_string())
    print("(valores en miles de millones USD)\n")
    
    print("FLUJO DE EFECTIVO")
    print("-" * 60)
    cf = estados["cashflow"] / 1e9
    cf.columns = [c.strftime("%Y") for c in cf.columns]
    print(cf.round(2).to_string())
    print("(valores en miles de millones USD)\n")


def calcular_cagr(valor_inicial, valor_final, años):
    """Tasa de crecimiento anual compuesta."""
    if pd.isna(valor_inicial) or pd.isna(valor_final):
        return None
    if valor_inicial <= 0 or valor_final <= 0 or años <= 0:
        return None
    return ((valor_final / valor_inicial) ** (1/años) - 1) * 100


def _cagr_de_serie(serie):
    """CAGR sobre una serie newest-first de yfinance, dropeando NaN.

    yfinance entrega columnas con la mas reciente primero. Si la columna mas
    vieja viene como NaN (empresas con pocos años de historia, como MELI), el
    iloc[-1] crudo metia un None y rompia todos los CAGR. Acá filtramos NaN y
    calculamos años reales entre primera y última observación.
    """
    s = serie.dropna()
    if len(s) < 2:
        return None, None
    valor_final = s.iloc[0]
    valor_inicial = s.iloc[-1]
    años = abs(s.index[0].year - s.index[-1].year)
    cagr = calcular_cagr(valor_inicial, valor_final, años)
    return cagr, años


def crecimiento_historico(ticker):
    """Calcula crecimiento de revenue, net income y FCF."""
    t = yf.Ticker(get_ticker_adr(ticker))

    pl = t.financials
    cf = t.cashflow

    if pl.empty:
        return None

    resultados = {"ticker": ticker}

    def _agregar(nombre, serie):
        cagr, años = _cagr_de_serie(serie)
        resultados[f"{nombre}_cagr_%"] = round(cagr, 2) if cagr is not None else None
        resultados[f"{nombre}_años"] = años

    if "Total Revenue" in pl.index:
        _agregar("revenue", pl.loc["Total Revenue"])

    if "Net Income" in pl.index:
        _agregar("net_income", pl.loc["Net Income"])

    if "Free Cash Flow" in cf.index:
        _agregar("fcf", cf.loc["Free Cash Flow"])

    if "Total Revenue" in pl.index and "Net Income" in pl.index:
        rev = pl.loc["Total Revenue"].dropna()
        ni = pl.loc["Net Income"].dropna()
        comunes = rev.index.intersection(ni.index)
        if len(comunes) >= 2:
            fecha_act, fecha_ant = comunes[0], comunes[-1]
            rev_act, rev_ant = rev.loc[fecha_act], rev.loc[fecha_ant]
            ni_act, ni_ant = ni.loc[fecha_act], ni.loc[fecha_ant]
            if rev_act and rev_ant:
                margen_actual = (ni_act / rev_act) * 100
                margen_anterior = (ni_ant / rev_ant) * 100
                resultados["margen_neto_actual_%"] = round(margen_actual, 2)
                resultados["margen_neto_inicio_%"] = round(margen_anterior, 2)
                resultados["expansion_margen_pp"] = round(margen_actual - margen_anterior, 2)

    return resultados


def ratios_avanzados(ticker):
    """15+ ratios organizados en 4 categorías."""
    t = yf.Ticker(get_ticker_adr(ticker))
    info = t.info
    
    return {
        "ticker": ticker,
        "PE_trailing": info.get("trailingPE"),
        "PE_forward": info.get("forwardPE"),
        "PEG": info.get("pegRatio"),
        "PB": info.get("priceToBook"),
        "PS": info.get("priceToSalesTrailing12Months"),
        "EV_EBITDA": info.get("enterpriseToEbitda"),
        "EV_Revenue": info.get("enterpriseToRevenue"),
        "Dividend_Yield_%": _pct(info, "dividendYield"),
        "ROE_%": _pct(info, "returnOnEquity"),
        "ROA_%": _pct(info, "returnOnAssets"),
        "Margen_Bruto_%": _pct(info, "grossMargins"),
        "Margen_Operativo_%": _pct(info, "operatingMargins"),
        "Margen_Neto_%": _pct(info, "profitMargins"),
        "Debt_Equity": info.get("debtToEquity"),
        "Current_Ratio": info.get("currentRatio"),
        "Quick_Ratio": info.get("quickRatio"),
        "Beta": info.get("beta"),
        "Payout_Ratio_%": _pct(info, "payoutRatio"),
    }


def mostrar_ratios_completos(ticker):
    """Imprime los ratios organizados por categoría."""
    r = ratios_avanzados(ticker)
    
    print(f"\n{'='*60}")
    print(f"  ANALISIS FUNDAMENTAL - {ticker}")
    print(f"{'='*60}\n")
    
    fmt = formatear  # alias: misma firma que la formatear() de src.datos
    
    print("VALUACION")
    print(f"  PE (trailing):      {fmt(r['PE_trailing'])}")
    print(f"  PE (forward):       {fmt(r['PE_forward'])}")
    print(f"  PEG:                {fmt(r['PEG'])}")
    print(f"  P/B:                {fmt(r['PB'])}")
    print(f"  P/S:                {fmt(r['PS'])}")
    print(f"  EV/EBITDA:          {fmt(r['EV_EBITDA'])}")
    print(f"  EV/Revenue:         {fmt(r['EV_Revenue'])}")
    print(f"  Dividend Yield:     {fmt(r['Dividend_Yield_%'], sufijo='%')}")
    
    print("\nRENTABILIDAD")
    print(f"  ROE:                {fmt(r['ROE_%'], sufijo='%')}")
    print(f"  ROA:                {fmt(r['ROA_%'], sufijo='%')}")
    print(f"  Margen Bruto:       {fmt(r['Margen_Bruto_%'], sufijo='%')}")
    print(f"  Margen Operativo:   {fmt(r['Margen_Operativo_%'], sufijo='%')}")
    print(f"  Margen Neto:        {fmt(r['Margen_Neto_%'], sufijo='%')}")
    
    print("\nSOLVENCIA")
    print(f"  Debt/Equity:        {fmt(r['Debt_Equity'])}")
    print(f"  Current Ratio:      {fmt(r['Current_Ratio'])}")
    print(f"  Quick Ratio:        {fmt(r['Quick_Ratio'])}")
    
    print("\nOTROS")
    print(f"  Beta:               {fmt(r['Beta'])}")
    print(f"  Payout Ratio:       {fmt(r['Payout_Ratio_%'], sufijo='%')}")
    print(f"\n{'='*60}\n")


def comparar_peers(tickers, ratios_seleccionados=None):
    """Compara múltiples empresas en una tabla con ratios clave."""
    if ratios_seleccionados is None:
        ratios_seleccionados = [
            "PE_trailing", "PB", "EV_EBITDA", 
            "ROE_%", "Margen_Operativo_%", "Margen_Neto_%",
            "Debt_Equity", "Dividend_Yield_%"
        ]
    
    resultados = []
    for t in tickers:
        r = ratios_avanzados(t)   # internamente ya usa get_ticker_adr
        fila = {"Ticker": t}      # label original (PAMP.BA, no PAM)
        for ratio in ratios_seleccionados:
            fila[ratio] = r.get(ratio)
        resultados.append(fila)
    
    df = pd.DataFrame(resultados)
    return df


def fcf_historico(ticker):
    """Devuelve el Free Cash Flow histórico."""
    t = yf.Ticker(get_ticker_adr(ticker))
    cf = t.cashflow
    
    if cf.empty or "Free Cash Flow" not in cf.index:
        if "Operating Cash Flow" in cf.index and "Capital Expenditure" in cf.index:
            ocf = cf.loc["Operating Cash Flow"]
            capex = cf.loc["Capital Expenditure"]
            fcf = ocf + capex
        else:
            print(f"Sin datos de FCF para {ticker}")
            return None
    else:
        fcf = cf.loc["Free Cash Flow"]

    fcf = fcf.dropna()
    if fcf.empty:
        print(f"Sin datos validos de FCF para {ticker}")
        return None

    df = pd.DataFrame({
        "año": [c.year for c in fcf.index],
        "FCF_USD_M": (fcf / 1e6).round(0).astype(int).values,
        "FCF_USD_B": (fcf / 1e9).round(2).values,
    })
    
    df["variacion_%"] = df["FCF_USD_B"].pct_change(periods=-1).round(4) * 100
    df = df.iloc[::-1].reset_index(drop=True)
    
    return df


def analisis_completo(ticker):
    """Tira el análisis fundamental completo de una empresa."""
    from src.datos import mostrar_ticker
    
    print(f"\n{'#'*60}")
    print(f"#  ANALISIS COMPLETO - {ticker.upper()}")
    print(f"{'#'*60}")
    
    mostrar_ticker(ticker)
    mostrar_ratios_completos(ticker)
    mostrar_estados(ticker)
    
    print("CRECIMIENTO HISTORICO")
    print("-" * 60)
    crec = crecimiento_historico(ticker)
    if crec:
        for k, v in crec.items():
            if k != "ticker":
                print(f"  {k}: {v}")
    print()
    
    print("FREE CASH FLOW HISTORICO")
    print("-" * 60)
    fcf = fcf_historico(ticker)
    if fcf is not None:
        print(fcf.to_string(index=False))
    print(f"\n{'#'*60}\n")