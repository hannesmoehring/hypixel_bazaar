import warnings

import pandas as pd
from neuralprophet import NeuralProphet, set_log_level
from prophet import Prophet

import data_prep

warnings.simplefilter(action='ignore', category=FutureWarning)
set_log_level("ERROR")


def propheting_prophet(model: Prophet, periods: int = 10):
    future = model.make_future_dataframe(periods, freq="h")
    forecast = model.predict(future)

    return forecast


def prophet_routine(df: pd.DataFrame, productId: str, periods: int = 6):
    train = data_prep.prep_prophet(df, productId)

    m = Prophet()
    m.fit(train) # , trainer=custom_trainer
    forecast = propheting_prophet(model=m, periods=periods)

    return m.plot(forecast)



def neuralProphet_train(train: pd.DataFrame, forecast_window: int = 24):
    m = NeuralProphet(n_lags=12, n_forecasts=forecast_window) # autoregressive=True,
    m.set_plotting_backend("plotly-static")

    m = m.add_lagged_regressor("buyVolume")
    m = m.add_lagged_regressor("sellVolume")

    if "inst_sellPrice" in train.columns: m = m.add_lagged_regressor("inst_sellPrice")
    
    metrics = m.fit(train, freq='10min', checkpointing=False) # , trainer=custom_trainer
    print(metrics)

    return m


def neuralProphet_predicting(m: NeuralProphet, train: pd.DataFrame, periods: int=60):
    future = m.make_future_dataframe(train, n_historic_predictions=True) # periods=periods
#    future["buyVolume"] = future["buyVolume"].fillna(method="ffill")
#    future["sellVolume"] = future["sellVolume"].fillna(method="ffill")
    # or
#    future["lagged_regressor_buyVolume1"] = future["lagged_regressor_buyVolume1"].fillna(method="ffill")
#    future["lagged_regressor_sellVolume1"] = future["lagged_regressor_sellVolume1"].fillna(method="ffill")

# ich gucke mir im notebook nur forecast an nicht future, die lagged regressors müssen irgendwie anders gesetzt werden
# vielleicht mit n_forecast höher (!!) wenn das nicht gut ist den lag von regressors erhöh
    forecast = m.predict(future)

    return forecast


