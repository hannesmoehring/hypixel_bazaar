import pandas as pd


def load_timeseries(product: str, DF: pd.DataFrame) -> list[dict]:  
    cols = ['ds', 'inst_sellPrice', 'sellVolume',
       'inst_sellPastWeek', 'sellOrders', 'inst_buyPrice', 'buyVolume',
       'inst_buyPastWeek', 'buyOrders'
    ]
    df = DF.loc[DF["productId"] == product, cols].copy()


    
    return df.sort_values("ds").to_dict(orient="records")