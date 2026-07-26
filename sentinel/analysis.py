import numpy as np
import pandas as pd


def calculate_moving_average(
    df: pd.DataFrame, window: int = 20
) -> pd.DataFrame:
    """Calculates Simple Moving Average (SMA) for price and volume."""
    df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
    df[f"Vol_SMA_{window}"] = df["Volume"].rolling(window=window).mean()
    print(f"[Sentinel] Calculated {window}-day Moving Average and Volume SMA.")
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """Calculates Relative Strength Index (RSI) using vectorized operations with zero-division safety."""
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(window=window).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window).mean()

    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["RSI"] = df["RSI"].fillna(50)

    print(f"[Sentinel] RSI indicator added (window={window}).")
    return df


def get_dynamic_margin(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculates dynamic volatility margin based on standard deviation of closing prices."""
    std_dev = df["Close"].rolling(window=window).std()
    margin = std_dev / df[f"SMA_{window}"]
    return margin.clip(0.01, 0.05)


def add_bollinger_bands(
    df: pd.DataFrame, window: int = 20, num_std: float = 2.0
) -> pd.DataFrame:
    """Calculates upper and lower Bollinger Bands based on price standard deviation."""
    sma = df["Close"].rolling(window=window).mean()
    std_dev = df["Close"].rolling(window=window).std()

    df[f"BB_Upper_{window}"] = sma + (num_std * std_dev)
    df[f"BB_Lower_{window}"] = sma - (num_std * std_dev)
    print(
        f"[Sentinel] Added Bollinger Bands (window={window}, std={num_std})."
    )
    return df


def generate_signals(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Generates BUY/SELL/HOLD signals using dynamic volatility margins and volume confirmation."""
    sma_col = f"SMA_{window}"
    vol_sma_col = f"Vol_SMA_{window}"
    margins = get_dynamic_margin(df, window)

    buy_condition = (
        (df["Close"] < df[sma_col] * (1 - margins))
        & (df["Volume"] > df[vol_sma_col])
        & (df["RSI"] < 30)
    )

    sell_condition = (
        (df["Close"] > df[sma_col] * (1 + margins))
        & (df["Volume"] > df[vol_sma_col])
        & (df["RSI"] > 70)
    )

    conditions = [buy_condition, sell_condition]
    choices = ["BUY", "SELL"]

    df["Signal"] = np.select(conditions, choices, default="HOLD")
    print(
        "[Sentinel] Signals generated with Vectorized Dynamic Margin & RSI confirmation."
    )
    return df


def calculate_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts trade signals (excluding HOLD) for evaluation."""
    trades = df[df["Signal"] != "HOLD"].copy()
    print(
        f"[Sentinel] Performance analysis ready. Found {len(trades)} trade signals."
    )
    return trades


def calculate_pnl(df: pd.DataFrame) -> float:
    """Calculates realized Profit and Loss (PnL) by pairing sequential BUY and SELL trades."""
    trades = df[df["Signal"] != "HOLD"].copy()
    if trades.empty:
        return 0.0

    total_pnl = 0.0
    buy_price = None

    for _, row in trades.iterrows():
        if row["Signal"] == "BUY" and buy_price is None:
            buy_price = row["Close"]
        elif row["Signal"] == "SELL" and buy_price is not None:
            pnl = row["Close"] - buy_price
            total_pnl += pnl
            buy_price = None

    print(f"[Sentinel] Total Realized PnL calculated: {total_pnl:.2f}")
    return total_pnl