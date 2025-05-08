import pandas as pd
from prophet import Prophet

import data_prep


def train_prophet(df: pd.DataFrame) -> Prophet:
    model = Prophet()
    model.fit(df)

    return model


def propheting_prophet(model: Prophet, periods: int = 10):
    future = model.make_future_dataframe(periods, freq="h")
    forecast = model.predict(future)

    return forecast


def prophet_routine(df: pd.DataFrame, productId: str, periods: int = 6):
    temp = data_prep.prep_prophet(df, productId)

    model = train_prophet(df=temp)
    forecast = propheting_prophet(model=model, periods=periods)

    return model.plot(forecast)
