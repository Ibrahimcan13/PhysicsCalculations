import pandas as pd
import numpy as np


def calculate_moving_average(df: pd.DataFrame, window: int = 20):
    """Calculates Simple Moving Average (SMA) for price and volume."""
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    df[f'Vol_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
    print(f"[Sentinel] Calculated {window}-day Moving Average and Volume SMA.")
    return df


def add_rsi(df: pd.DataFrame, window: int = 14):
    """Calculates Relative Strength Index (RSI) using vectorized operations."""
    delta = df['Close'].diff()
    gain = (delta.clip(lower=0)).rolling(window=window).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window).mean()

    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    print(f"[Sentinel] RSI indicator added (window={window}).")
    return df


def get_dynamic_margin(df: pd.DataFrame, window: int = 20):
    """Calculates dynamic margin based on standard deviation of closing prices."""
    std_dev = df['Close'].rolling(window=window).std()
    margin = std_dev / df[f'SMA_{window}']
    return margin.clip(0.01, 0.05)


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0):
    """Calculates Bollinger Bands using vectorized operations."""
    sma = df['Close'].rolling(window=window).mean()
    std_dev = df['Close'].rolling(window=window).std()

    df[f'BB_Upper_{window}'] = sma + (num_std * std_dev)
    df[f'BB_Lower_{window}'] = sma - (num_std * std_dev)
    print(f"[Sentinel] Added Bollinger Bands (window={window}, std={num_std}).")
    return df


def generate_signals(df: pd.DataFrame, window: int = 20):
    """Generates BUY/SELL/HOLD signals using high-speed vectorized logic."""
    sma_col = f'SMA_{window}'
    vol_sma_col = f'Vol_SMA_{window}'
    margins = get_dynamic_margin(df, window)

    buy_condition = (
            (df['Close'] < df[sma_col] * (1 - margins)) &
            (df['Volume'] > df[vol_sma_col]) &
            (df['RSI'] < 30)
    )

    sell_condition = (
            (df['Close'] > df[sma_col] * (1 + margins)) &
            (df['Volume'] > df[vol_sma_col]) &
            (df['RSI'] > 70)
    )


    conditions = [buy_condition, sell_condition]
    choices = ["BUY", "SELL"]

    df['Signal'] = np.select(conditions, choices, default="HOLD")

    print("[Sentinel] Signals generated with Vectorized Dynamic Margin & RSI confirmation.")
    return df


def calculate_performance(df: pd.DataFrame):
    """Filters data to extract non-HOLD signals for performance metrics."""
    trades = df[df['Signal'] != 'HOLD'].copy()
    print(f"[Sentinel] Performance analysis ready. Found {len(trades)} trade signals.")
    return trades


def calculate_pnl(trades: pd.DataFrame):
    """Calculates historical Profit and Loss (PnL) using array differences."""
    if trades.empty:
        return 0.0

    trades['PnL'] = trades['Close'].diff()
    total_pnl = trades[trades['Signal'] == 'SELL']['PnL'].sum()
    print(f"[Sentinel] Total PnL calculated: {total_pnl:.2f}")
    return total_pnl
