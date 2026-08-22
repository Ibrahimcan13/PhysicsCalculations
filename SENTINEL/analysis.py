import numpy as np
import pandas as pd


def calculate_moving_average(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = df.copy()
    df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
    df[f"Vol_SMA_{window}"] = df["Volume"].rolling(window=window).mean()
    print(f"[Sentinel] Calculated {window}-day Moving Average and Volume SMA.")
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    if df.empty or "Close" not in df.columns:
        print("[Warning] DataFrame is empty or missing 'Close' column. Skipping RSI calculation.")
        return df

    df = df.copy()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["RSI"] = df["RSI"].fillna(50)

    print(f"[Sentinel] RSI indicator added using {window}-period EMA.")
    return df


def calculate_average_true_range(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    required_cols = {"High", "Low", "Close"}
    if df.empty or not required_cols.issubset(df.columns):
        print(f"[Warning] DataFrame missing required columns {required_cols}. Skipping ATR calculation.")
        return df

    df = df.copy()
    high_low = df["High"] - df["Low"]
    high_prev_close = (df["High"] - df["Close"].shift(1)).abs()
    low_prev_close = (df["Low"] - df["Close"].shift(1)).abs()

    true_range = pd.concat([high_low, high_prev_close, low_prev_close], axis=1).max(axis=1)

    df["ATR"] = true_range.ewm(alpha=1 / window, adjust=False).mean()
    print(f"[Sentinel] Calculated {window}-period Average True Range (ATR).")
    return df


def get_dynamic_margin(df: pd.DataFrame, window: int = 20) -> pd.Series:
    sma_col = f"SMA_{window}" if f"SMA_{window}" in df.columns else "Close"
    std_dev = df["Close"].rolling(window=window).std()

    if sma_col in df.columns:
        margin = std_dev / df[sma_col]
    else:
        margin = std_dev / df["Close"]

    return margin.clip(0.01, 0.05)


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    df = df.copy()
    sma = df["Close"].rolling(window=window).mean()
    std_dev = df["Close"].rolling(window=window).std()

    df[f"BB_Upper_{window}"] = sma + (num_std * std_dev)
    df[f"BB_Lower_{window}"] = sma - (num_std * std_dev)
    print(f"[Sentinel] Added Bollinger Bands (window={window}, std={num_std}).")
    return df


def generate_signals(
    df: pd.DataFrame,
    window: int = 20,
    rsi_lower: float = 30.0,
    rsi_upper: float = 70.0,
    max_vol_zscore: float = 3.0
) -> pd.DataFrame:
    df = df.copy()
    sma_col = f"SMA_{window}"
    vol_sma_col = f"Vol_SMA_{window}"

    if sma_col not in df.columns or vol_sma_col not in df.columns:
        df = calculate_moving_average(df, window=window)

    margins = get_dynamic_margin(df, window)

    vol_std = df["Volume"].rolling(window=window).std().replace(0, 1e-9)
    vol_zscore = (df["Volume"] - df[vol_sma_col]) / vol_std
    valid_volume_mask = (df["Volume"] > df[vol_sma_col]) & (vol_zscore <= max_vol_zscore)

    raw_buy = (
        (df["Close"] < df[sma_col] * (1 - margins))
        & valid_volume_mask
        & (df["RSI"] < rsi_lower)
    )

    raw_sell = (
        (df["Close"] > df[sma_col] * (1 + margins))
        & valid_volume_mask
        & (df["RSI"] > rsi_upper)
    )

    if "AI_Probability" in df.columns:
        raw_buy = raw_buy & (df["AI_Probability"] > 0.50)

    buy_arr = raw_buy.to_numpy()
    sell_arr = raw_sell.to_numpy()
    n = len(df)

    pos_change = np.zeros(n, dtype=int)
    pos_change[buy_arr] = 1
    pos_change[sell_arr] = -1

    current_pos = False
    final_signals = np.full(n, "HOLD", dtype=object)

    for i in range(n):
        if pos_change[i] == 1 and not current_pos:
            final_signals[i] = "BUY"
            current_pos = True
        elif pos_change[i] == -1 and current_pos:
            final_signals[i] = "SELL"
            current_pos = False

    df["Signal"] = final_signals
    print(f"[Sentinel] Signals generated via vectorized NumPy pipeline (RSI Buy: <{rsi_lower}, Sell: >{rsi_upper}).")
    return df