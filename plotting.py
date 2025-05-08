import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

#                "sellPrice": 7.1000000000000005,       insta-sell-price
#                "sellVolume": 560532,                  amount in sell offers
#                "sellMovingWeek": 4121573,             insta sells in past 7d
#                "sellOrders": 17,                      number of sell orders
#
#                "buyPrice": 35.5,                      insta-buy-price
#                "buyVolume": 131027,                   amount in buy offfers
#                "buyMovingWeek": 3300774,              insta buys in past 7d
#                "buyOrders": 9                         number of buy orders

# "time": str,
#    "productId": str,
#    #
#    "inst_sellPrice": float,
#    "sellVolume": int,
#    "inst_sellPastWeek": int,
#    "sellOrders": int,
#    #
#    "inst_buyPrice": float,
#    "buyVolume": int,
#    "inst_buyPastWeek": int,
#    "buyOrders": int,


def plot_product_prices(df: pd.DataFrame, product_id: str) -> plt:
    product_data = df[df["productId"] == product_id].sort_values("datetime")

    plt.figure(figsize=(12, 6))

    plt.plot(
        product_data["datetime"],
        product_data["inst_buyPrice"],
        marker="o",
        linestyle="-",
        label="Buy Price",
        color="lime",
    )

    plt.plot(
        product_data["datetime"],
        product_data["inst_sellPrice"],
        marker="x",
        linestyle="-",
        label="Sell Price",
        color="red",
    )

    plt.title(f"Buy and Sell Prices for Product ID: {product_id}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt


def plot_multiple_products(
    df: pd.DataFrame, product_ids: str, metric: str = "inst_buyPrice"
) -> plt:
    plt.figure(figsize=(14, 7))

    for product_id in product_ids:
        product_data = df[df["productId"] == product_id].sort_values("datetime")
        plt.plot(
            product_data["datetime"],
            product_data[metric],
            marker="o",
            linestyle="-",
            label=f"Product {product_id}",
        )

    plt.title(f"{metric} Comparison Across Products")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt


def prophet_forecast(data: pd.DataFrame, forecast: pd.DataFrame) -> plt:
    plt.figure(figsize=(12, 6))

    plt.plot(
        data["ds"],
        data["y"],
        marker="o",
        linestyle="-",
        label="data",
        color="lime",
    )

    plt.plot(
        forecast["ds"],
        forecast["trend"],
        marker="x",
        linestyle="-",
        label="Forecast",
        color="red",
    )

    plt.plot(
        forecast["ds"],
        forecast["trend"],
        marker="x",
        linestyle="-",
        label="Forecast",
        color="red",
    )

    plt.title(f"YEEEEE")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()
