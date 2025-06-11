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


def calculate_corr(pivot_data: dict, method: str = "pearson") -> dict[str, pd.DataFrame]:   
    df_sellPrice = pivot_data["sellPrice"]
    df_buyPrice = pivot_data["buyPrice"]

    df_sellVolume = pivot_data["sellVolume"]
    df_buyVolume = pivot_data["buyVolume"]


    corr_sP = df_sellPrice.corr(method)
    corr_bP = df_buyPrice.corr(method)

    corr_sV = df_sellVolume.corr(method)
    corr_bV = df_buyVolume.corr(method)

    np.fill_diagonal(corr_sP.values, 0)
    np.fill_diagonal(corr_bP.values, 0)

    np.fill_diagonal(corr_sV.values, 0)
    np.fill_diagonal(corr_bV.values, 0)
    
    corr_data = {
        "sellPrice" : corr_sP,
        "buyPrice" : corr_bP,

        "sellVolume" : corr_sV,
        "buyVolume" : corr_bV,
    }

    return corr_data


def get_top_correlated(corr_df: pd.DataFrame, productId: str, positive_corr: bool = True, top_n: int = 5, use_abs: bool = False) -> pd.Series:
    series = corr_df[productId]
    sorted_series = series.abs().sort_values(ascending=False) if use_abs else series.sort_values(ascending=False)
    return series.loc[sorted_series.index[:top_n]]


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



def calculate_lagged_corr(pivot_data : dict, productId: str, n_lags: int, positive_corr: bool = True, metric: str = "buyPrice", method: str = "pearson"):
    # if a product has a good corr it might predict productId n steps into the future 
    df = pivot_data[metric]
    shifted = df[productId].shift(-n_lags)
    correlations = df.corrwith(shifted, method=method) 
    correlations[productId] = 0
    return correlations.sort_values(ascending=not positive_corr)