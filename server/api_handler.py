import os

import data_prep
import mathing
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utility import load_timeseries

app = FastAPI(title="Minecraft-Stocks API")

dataframe = pd.read_pickle(os.path.join("data", "local_pickle", "cached_df.pkl"))
pivot_data = data_prep.prep_pivot_data(dataframe)
corr_data = mathing.calculate_corr(pivot_data, method="pearson")

# origins = ["http://localhost:3000"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)



@app.get("/api/ticker")
async def ticker(product: str = Query(...)):
    return "alive"

@app.get("/api/product/{prodId}")
async def getProduct(prodId : str):
    return load_timeseries(product=prodId, DF=dataframe)

@app.get("/api/correlation/{prodId}")
async def getTopCorrelation(prodId : str, metric : str = "sellPrice", method : str = "pearson"):
    return mathing.get_top_correlated(corr_data[metric], prodId, use_abs=True)

@app.get("/api/lagged_correlation/{prodId}")
async def getTopLaggedCorrelation(prodId : str, metric : str = "sellPrice", method : str = "pearson", lagSteps : int = 0):
    return mathing.calculate_lagged_corr(pivot_data=pivot_data, productId=prodId, n_lags=lagSteps, metric=metric, use_abs=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_handler:app", port=8000, reload=True)