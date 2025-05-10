import pandas as pd
import torch
import torch.optim.adamw
import torch.serialization
from neuralprophet import NeuralProphet
from neuralprophet.configure import Train
from prophet import Prophet
from pytorch_lightning import Trainer

import data_prep

#torch.serialization.add_safe_globals([torch.nn.modules.loss.SmoothL1Loss])
#torch.serialization.add_safe_globals([torch.optim.AdamW])
#torch.serialization.add_safe_globals([torch.optim.lr_scheduler.OneCycleLR])
#torch.serialization.add_safe_globals([neuralprophet.configure.Trend])


custom_trainer = Trainer(
    accelerator='mps', 
    devices=1,
    max_epochs=220,     # Optional: override auto epoch setting
    enable_model_summary=True, 
)

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



def neuralProphet_train(train: pd.DataFrame, useSellPriceRegressor: bool = True):
    m = NeuralProphet(n_lags=6, n_forecasts=1) # autoregressive=True,
    m = m.add_lagged_regressor("buyVolume")
    m = m.add_lagged_regressor("sellVolume")

    if useSellPriceRegressor: m = m.add_lagged_regressor("inst_sellPrice")
    else: train.drop("inst_sellPrice")
    
    metrics = m.fit(train, freq='10min', checkpointing=False) # , trainer=custom_trainer
    print(metrics)


def neuralProphet_predicting(m: NeuralProphet, train: pd.DataFrame):
    future = m.make_future_dataframe(train, n_historic_predictions=True)
    forecast = m.predict(future)

    return m.plot(forecast)

