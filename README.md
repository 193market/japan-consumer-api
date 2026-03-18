# Japan Consumer Data API

Japan consumer data including household spending, consumption growth, inflation/deflation trends, CPI index, gross savings rate, and income inequality. Powered by World Bank Open Data.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All consumer indicators snapshot |
| `GET /household-spending` | Household consumption (% of GDP) |
| `GET /spending-per-capita` | Consumption per capita (USD) |
| `GET /spending-growth` | Consumption growth rate |
| `GET /inflation` | Inflation rate (CPI annual %) |
| `GET /cpi-index` | CPI index level (2010=100) |
| `GET /savings` | Gross savings rate (% of GDP) |
| `GET /income-inequality` | Gini coefficient |

## Data Source

World Bank Open Data
https://data.worldbank.org/country/JP

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
