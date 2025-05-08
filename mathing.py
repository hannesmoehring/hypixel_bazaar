import numpy as np
import pandas as pd


def fft_analysis(
    df: pd.DataFrame, productId: str, metric: str = "inst_sellPrice"
) -> tuple[float, float]:

    product_data: pd.DataFrame = df[df["productId"] == productId].sort_values(
        "datetime"
    )

    N: int = len(product_data)
    dt: int = 1800  # 1800 seconds = 30 minutes
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

    # calculating the dominant period, where a pattern repeats strongly
    dominant_idx = np.argmax(fft_magnitude)
    dominant_freq = fft_freqs[dominant_idx]
    dominant_period_seconds: float = 1 / dominant_freq
    # dominant_period_minutes = dominant_period_seconds / 60
    dominant_period_hours: float = dominant_period_seconds / 3600

    return score, dominant_period_hours
