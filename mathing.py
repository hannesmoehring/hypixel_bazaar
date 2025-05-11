import numpy as np
import pandas as pd

DATA_FREQUENCY = 600

def fft_analysis(
    df: pd.DataFrame, productId: str, metric: str = "inst_sellPrice"
) -> tuple[float, float]:

    product_data: pd.DataFrame = df[df["productId"] == productId].sort_values(
        "datetime"
    )

    N: int = len(product_data)
    dt: int = 600  # 600 seconds = 10 minutes
    t = np.arange(N) * dt  # for plotting
    values: list[float | int] = list(product_data[metric])

    fft_vals = np.fft.fft(values)  # time domain to frequency domain
    fft_freqs = np.fft.fftfreq(N, dt)  # freq computation

    pos_mask = fft_freqs > 0  # only pos frequencies
    fft_freqs = fft_freqs[pos_mask]
    fft_magnitude = np.abs(fft_vals[pos_mask])
    power_spectrum = np.abs(fft_vals[pos_mask]) ** 2

    score: float = np.max(power_spectrum) / np.sum(
        power_spectrum
    )  # score 0 to 1, 0 not periodic, 1 yes

    dominant_idx = np.argmax(fft_magnitude)
    dominant_freq = fft_freqs[dominant_idx]
    dominant_period_seconds: float = 1 / dominant_freq
    # dominant_period_minutes = dominant_period_seconds / 60
    dominant_period_hours: float = dominant_period_seconds / 3600

    return score, dominant_period_hours


def calculate_corr(df: pd.DataFrame, method: str = "pearson") -> dict[str, pd.DataFrame]:   
    df_sellPrice = df.pivot(index="ds", columns="productId", values="inst_sellPrice")
    df_buyPrice = df.pivot(index="ds", columns="productId", values="inst_buyPrice")

    df_sellVolume = df.pivot(index="ds", columns="productId", values="sellVolume")
    df_buyVolume = df.pivot(index="ds", columns="productId", values="buyVolume")


    corr_sP = df_sellPrice.corr(method)
    corr_bP = df_buyPrice.corr(method)

    corr_sV = df_sellVolume.corr(method)
    corr_bV = df_buyVolume.corr(method)

    np.fill_diagonal(corr_sP.values, 0)
    np.fill_diagonal(corr_bP. values, 0)

    np.fill_diagonal(corr_sV.values, 0)
    np.fill_diagonal(corr_bV.values, 0)
    
    corr_data = {
        "sellPrice" : corr_sP,
        "buyPrice" : corr_bP,

        "sellVolume" : corr_sV,
        "buyVolume" : corr_bV,
    }

    return corr_data, df_sellPrice


def get_top_correlated(corr_df: pd.DataFrame, productId: str, positive_corr: bool = True, top_n: int = 10) -> pd.Series:
    return corr_df[productId].sort_values(ascending= not positive_corr).head(top_n)


def get_top_correlated_pairs(corr_df: pd.DataFrame, positive_corr: bool = True, top_n: int = 10) -> pd.DataFrame:
    temp = corr_df.unstack()
    if temp.index.names[0] == temp.index.names[1]:
        temp.index = temp.index.set_names(["product_1", "product_2"])

    temp = temp.reset_index()
    temp.columns = ["product_1", "product_2", "correlation"]

    temp = temp[temp["product_1"] != temp["product_2"]]

    temp["pair"] = temp.apply(lambda row: tuple(sorted([row["product_1"], row["product_2"]])), axis=1)
    temp = temp.drop_duplicates("pair")

    top_pairs = temp.sort_values("correlation", ascending=not positive_corr).head(top_n)

    return top_pairs[["product_1", "product_2", "correlation"]]


def calculate_lagged_corr(df: pd.DataFrame, productId: str, n_lags: int, positive_corr: bool = True, method: str = "pearson"):
    temp = df[productId].shift(n_lags)
    correlations = df.corrwith(temp, method=method)
    correlations[productId] = 0 # no self thing
    return correlations.sort_values(ascending= not positive_corr)