import os

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utility import load_timeseries

app = FastAPI(title="Minecraft-Stocks API")

dataframe = pd.read_pickle(os.path.join("data", "local_pickle", "cached_df.pkl"))

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)



@app.get("/api/ticker")
async def ticker(product: str = Query(...)):
    df = load_timeseries(product)
    return df.reset_index()             \
             .rename(columns={"index": "time"}) \
             .to_dict(orient="records")

@app.get("/api/product/{prodId}")
async def getProduct(prodId : str):
    return load_timeseries(product=prodId, DF=dataframe)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_handler:app", port=8000, reload=True)