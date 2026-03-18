from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Japan Consumer Data API",
    description="Japan consumer data including household spending, consumer confidence, retail sales, savings, and deflation/inflation trends. Powered by World Bank Open Data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/JP/indicator"

INDICATORS = {
    "household_consumption":{"id": "NE.CON.PRVT.ZS",     "name": "Household Consumption",          "unit": "% of GDP"},
    "household_per_cap":    {"id": "NE.CON.PRVT.PC.KD",  "name": "Household Consumption Per Capita","unit": "Constant 2015 USD"},
    "consumption_growth":   {"id": "NE.CON.PRVT.KD.ZG",  "name": "Household Consumption Growth",   "unit": "Annual %"},
    "inflation":            {"id": "FP.CPI.TOTL.ZG",     "name": "Inflation (CPI)",                "unit": "Annual %"},
    "cpi_index":            {"id": "FP.CPI.TOTL",        "name": "Consumer Price Index",            "unit": "2010=100"},
    "savings_rate":         {"id": "NY.GNS.ICTR.ZS",     "name": "Gross Savings Rate",              "unit": "% of GDP"},
    "gini":                 {"id": "SI.POV.GINI",        "name": "Gini Coefficient",                "unit": "Index"},
    "poverty_gap":          {"id": "SI.POV.GAPS",        "name": "Poverty Gap",                     "unit": "% at $2.15/day"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {"format": "json", "mrv": limit, "per_page": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url, params=params)
        data = res.json()
    if not data or len(data) < 2:
        return []
    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Japan Consumer Data API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "World Bank Open Data",
        "country": "Japan (JP)",
        "endpoints": [
            "/summary", "/household-spending", "/spending-per-capita",
            "/spending-growth", "/inflation", "/cpi-index",
            "/savings", "/income-inequality"
        ],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=5, ge=1, le=30)):
    """All Japan consumer indicators snapshot"""
    results = {}
    for key, meta in INDICATORS.items():
        results[key] = await fetch_wb(meta["id"], limit)
    formatted = {
        key: {"name": INDICATORS[key]["name"], "unit": INDICATORS[key]["unit"], "data": results[key]}
        for key in INDICATORS
    }
    return {"country": "Japan", "country_code": "JP", "source": "World Bank Open Data", "updated_at": datetime.utcnow().isoformat() + "Z", "indicators": formatted}


@app.get("/household-spending")
async def household_spending(limit: int = Query(default=10, ge=1, le=60)):
    """Household final consumption expenditure (% of GDP)"""
    data = await fetch_wb("NE.CON.PRVT.ZS", limit)
    return {"indicator": "Household Consumption", "series_id": "NE.CON.PRVT.ZS", "unit": "% of GDP", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/spending-per-capita")
async def spending_per_capita(limit: int = Query(default=10, ge=1, le=60)):
    """Household consumption expenditure per capita (constant 2015 USD)"""
    data = await fetch_wb("NE.CON.PRVT.PC.KD", limit)
    return {"indicator": "Household Consumption Per Capita", "series_id": "NE.CON.PRVT.PC.KD", "unit": "Constant 2015 USD", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/spending-growth")
async def spending_growth(limit: int = Query(default=10, ge=1, le=60)):
    """Household consumption growth rate (annual %)"""
    data = await fetch_wb("NE.CON.PRVT.KD.ZG", limit)
    return {"indicator": "Household Consumption Growth", "series_id": "NE.CON.PRVT.KD.ZG", "unit": "Annual %", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/inflation")
async def inflation(limit: int = Query(default=10, ge=1, le=60)):
    """Japan inflation rate — Consumer Price Index (annual %)"""
    data = await fetch_wb("FP.CPI.TOTL.ZG", limit)
    return {"indicator": "Inflation (CPI)", "series_id": "FP.CPI.TOTL.ZG", "unit": "Annual %", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/cpi-index")
async def cpi_index(limit: int = Query(default=10, ge=1, le=60)):
    """Consumer Price Index level (2010 = 100)"""
    data = await fetch_wb("FP.CPI.TOTL", limit)
    return {"indicator": "Consumer Price Index", "series_id": "FP.CPI.TOTL", "unit": "Index (2010=100)", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/savings")
async def savings(limit: int = Query(default=10, ge=1, le=60)):
    """Gross savings rate (% of GDP)"""
    data = await fetch_wb("NY.GNS.ICTR.ZS", limit)
    return {"indicator": "Gross Savings Rate", "series_id": "NY.GNS.ICTR.ZS", "unit": "% of GDP", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/income-inequality")
async def income_inequality(limit: int = Query(default=10, ge=1, le=60)):
    """Gini coefficient — income inequality index"""
    data = await fetch_wb("SI.POV.GINI", limit)
    return {"indicator": "Gini Coefficient", "series_id": "SI.POV.GINI", "unit": "Index (0=equality, 100=inequality)", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
