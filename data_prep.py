import json
import os
from datetime import datetime

import pandas as pd

DATA_DIR = "data"

# "productId": "SUPERBOOM_TNT",
#                "sellPrice": 7.1000000000000005,       insta-sell-price
#                "sellVolume": 560532,                  amount in sell offers
#                "sellMovingWeek": 4121573,             insta sells in past 7d
#                "sellOrders": 17,                      number of sell orders
#
#                "buyPrice": 35.5,                      insta-buy-price
#                "buyVolume": 131027,                   amount in buy offfers
#                "buyMovingWeek": 3300774,              insta buys in past 7d
#                "buyOrders": 9                         number of buy orders


col_structure = {
    "time": str,
    "productId": str,
    #
    "inst_sellPrice": float,
    "sellVolume": int,
    "inst_sellPastWeek": int,
    "sellOrders": int,
    #
    "inst_buyPrice": float,
    "buyVolume": int,
    "inst_buyPastWeek": int,
    "buyOrders": int,
}


def load_all_json(dir: str) -> dict[int, dict]:
    raw_data: dict[int, dict] = {}

    files = os.listdir(dir)

    for filename in files:
        time = filename.removeprefix("data_").removesuffix(".json")
        try:
            with open(os.path.join(dir, filename)) as f:
                d: dict = json.load(f)
                raw_data[time] = d
        except Exception as e:
            print(f"Error occured for: {filename}")
            print(e)
            print("Skippping... \n")

    return raw_data


def init_dataframe(data: dict[int, dict]) -> pd.DataFrame:
    keys: list[str] = list(data.keys())
    df = pd.DataFrame({col: pd.Series(dtype=typ) for col, typ in col_structure.items()})

    bazaarItems: list[str] = list(
        data[keys[0]]["products"].keys()
    )  # if more items are added during data gathering it has to be updated
    # t_df = pd.DataFrame({col: pd.Series(dtype=typ) for col, typ in col_structure.items()})
    for time in keys:
        # t_df.clear() # meant as an intermediate dataframe
        # print("starting import for time:", time)
        for item in bazaarItems:

            tempVal = data[time]["products"][item]["quick_status"]

            prodId: str = tempVal["productId"]

            inst_SP: float = tempVal["sellPrice"]
            sellVol: int = tempVal["sellVolume"]
            instSellPast: int = tempVal["sellMovingWeek"]
            sellOrd: int = tempVal["sellOrders"]

            inst_BP: float = tempVal["buyPrice"]
            buyVol: int = tempVal["buyVolume"]
            instBuyPast: int = tempVal["buyMovingWeek"]
            buyOrd: int = tempVal["buyOrders"]

            new_row = pd.DataFrame(
                [
                    {
                        "time": time,
                        "productId": prodId,
                        #
                        "inst_sellPrice": inst_SP,
                        "sellVolume": sellVol,
                        "inst_sellPastWeek": instSellPast,
                        "sellOrders": sellOrd,
                        #
                        "inst_buyPrice": inst_BP,
                        "buyVolume": buyVol,
                        "inst_buyPastWeek": instBuyPast,
                        "buyOrders": buyOrd,
                    }
                ]
            )
            df = pd.concat([df, new_row], ignore_index=True)
        # print("finished import for time:", time)
        # print("\n")
    df["datetime"] = df["time"].apply(convert_time)
    return df


def convert_time(time_str: str):
    day, month = time_str.split("_")[0].split("-")
    hour, minute = time_str.split("_")[1].split("-")
    return datetime(2025, int(month), int(day), int(hour), int(minute))


def prep_prophet(
    df: pd.DataFrame, productId: str, metric: str = "inst_buyPrice") -> pd.DataFrame:

    train = pd.DataFrame()

    train["y"] = df.loc[df["productId"] == productId, metric]
    train["ds"] = df["time"].apply(convert_time)

    return train.sort_values("ds")


def prep_neuralprophet(df: pd.DataFrame, productId: str, useSellPriceRegressor: bool = True) -> pd.DataFrame:

    train = pd.DataFrame()

    if useSellPriceRegressor: train["inst_sellPrice"] = df.loc[df["productId"] == productId, "inst_sellPrice"]
    train["buyVolume"] = df.loc[df["productId"] == productId, "buyVolume"]
    train["sellVolume"] = df.loc[df["productId"] == productId, "sellVolume"]

    train["y"] = df.loc[df["productId"] == productId, "inst_buyPrice"] 
    train["ds"] = df["time"].apply(convert_time)

    return train.sort_values("ds")
