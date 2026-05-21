"""Análisis fundamental: estados financieros, ratios avanzados y crecimiento."""
import yfinance as yf
import pandas as pd

from src.datos import formatear, get_ticker_adr, is_ticker_argentino


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
    
    # P/S y EV/Revenue: Yahoo Finance mezcla precio ARS con revenue USD para tickers AR
    # → calcular manualmente usando precio del ADR (USD) × shares / revenue
    if is_ticker_argentino(ticker):
        _px   = info.get("currentPrice") or info.get("regularMarketPrice")
        _sh   = info.get("sharesOutstanding")
        _rev  = info.get("totalRevenue")
        _debt = info.get("totalDebt") or 0
        _cash = info.get("totalCash") or 0
        if _px and _sh and _rev and _rev > 0:
            _mc  = _px * _sh
            _ps  = round(_mc / _rev, 4)
            _evr = round((_mc + _debt - _cash) / _rev, 4)
        else:
            _ps  = info.get("priceToSalesTrailing12Months")
            _evr = info.get("enterpriseToRevenue")
    else:
        _ps  = info.get("priceToSalesTrailing12Months")
        _evr = info.get("enterpriseToRevenue")

    return {
        "ticker": ticker,
        "PE_trailing": info.get("trailingPE"),
        "PE_forward": info.get("forwardPE"),
        "PEG": info.get("pegRatio"),
        "PB": info.get("priceToBook"),
        "PS": _ps,
        "EV_EBITDA": info.get("enterpriseToEbitda"),
        "EV_Revenue": _evr,
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


_SECTOR_PB_TARGET: dict[str, float] = {
    "Technology":             6.0,
    "Communication Services": 4.0,
    "Consumer Cyclical":      3.5,
    "Consumer Defensive":     4.5,
    "Healthcare":             4.5,
    "Industrials":            3.5,
    "Financial Services":     1.5,
    "Energy":                 2.0,
    "Basic Materials":        2.0,
    "Utilities":              1.8,
    "Real Estate":            2.0,
}


def calcular_fair_value(ticker: str) -> dict:
    """Fair value por PE histórico × EPS forward y PB sector × Book Value.

    Retorna dict con precio_actual, fair_value_pe, fair_value_pb,
    fair_value_promedio, upside_downside %, veredicto, confianza,
    metodos_usados. Nunca lanza excepción — devuelve veredicto='SIN DATOS'
    si faltan datos.
    """
    import pandas as pd

    _vacio = {
        "precio_actual": None, "fair_value_pe": None, "fair_value_pb": None,
        "fair_value_promedio": None, "upside_downside": None,
        "veredicto": "SIN DATOS", "confianza": "Baja", "metodos_usados": 0,
        "pe_promedio": None, "pe_fuente": "", "pb_target": None, "sector": "",
    }

    try:
        adr  = get_ticker_adr(ticker)
        t    = yf.Ticker(adr)
        info = t.info

        precio_actual = info.get("currentPrice") or info.get("regularMarketPrice")
        if not precio_actual:
            return _vacio

        eps_forward = info.get("forwardEps")
        pe_trailing = info.get("trailingPE")
        book_value  = info.get("bookValue")
        sector      = info.get("sector", "")

        # ── Método 1: PE histórico promedio × EPS forward ─────────────────
        fair_value_pe = None
        pe_promedio   = None
        pe_fuente     = ""

        # Intento: PE anual de los últimos 4 años (precio / EPS calculado)
        try:
            fin    = t.financials   # columnas = años, filas = P&L
            hist   = t.history(period="5y", interval="1mo")
            shares = info.get("sharesOutstanding") or 0

            if (fin is not None and not fin.empty and
                    hist is not None and not hist.empty and shares > 0):

                ni_key = next((k for k in fin.index if "Net Income" in str(k)), None)
                if ni_key:
                    pes: list[float] = []
                    for col in fin.columns:
                        try:
                            ni     = float(fin.loc[ni_key, col])
                            eps_yr = ni / shares
                            if eps_yr <= 0:
                                continue
                            ts       = pd.Timestamp(col)
                            price_at = float(hist["Close"].asof(ts))
                            if not price_at or price_at <= 0:
                                continue
                            pe = price_at / eps_yr
                            if 0 < pe < 300:
                                pes.append(pe)
                        except Exception:
                            continue
                    if pes:
                        pe_promedio = round(sum(pes) / len(pes), 1)
                        pe_fuente   = f"histórico ({len(pes)} años)"
        except Exception:
            pass

        # Fallback: PE trailing como proxy del múltiplo habitual
        if pe_promedio is None and pe_trailing and 0 < pe_trailing < 200:
            pe_promedio = pe_trailing
            pe_fuente   = "trailing actual"

        if pe_promedio and eps_forward and eps_forward > 0:
            fair_value_pe = round(pe_promedio * eps_forward, 2)

        # ── Método 2: PB sector target × Book Value ───────────────────────
        fair_value_pb = None
        pb_target     = _SECTOR_PB_TARGET.get(sector, 2.5)

        if book_value and book_value > 0:
            fair_value_pb = round(pb_target * book_value, 2)

        # ── Consolidar ────────────────────────────────────────────────────
        metodos_validos = [v for v in [fair_value_pe, fair_value_pb] if v and v > 0]
        if not metodos_validos:
            return {**_vacio, "precio_actual": round(float(precio_actual), 2),
                    "sector": sector}

        fv_prom = round(sum(metodos_validos) / len(metodos_validos), 2)
        upside  = round((fv_prom / precio_actual - 1) * 100, 1)

        veredicto = ("SUBVALUADA"   if upside >  15 else
                     "SOBREVALUADA" if upside < -15 else
                     "PRECIO JUSTO")

        confianza = ("Alta"  if len(metodos_validos) == 2 and "histórico" in pe_fuente else
                     "Media" if len(metodos_validos) >= 1 else "Baja")

        return {
            "precio_actual":       round(float(precio_actual), 2),
            "fair_value_pe":       fair_value_pe,
            "fair_value_pb":       fair_value_pb,
            "fair_value_promedio": fv_prom,
            "upside_downside":     upside,
            "veredicto":           veredicto,
            "confianza":           confianza,
            "metodos_usados":      len(metodos_validos),
            "pe_promedio":         pe_promedio,
            "pe_fuente":           pe_fuente,
            "pb_target":           pb_target,
            "sector":              sector,
        }
    except Exception:
        return _vacio


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