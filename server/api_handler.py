from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utility import load_timeseries

app = FastAPI(title="Minecraft-Stocks API")

origins = ["http://localhost:3000", "https://your-frontend.tld"]
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