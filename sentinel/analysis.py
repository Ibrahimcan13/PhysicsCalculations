import pandas as pd

def calculate_moving_average(df: pd.DataFrame, window: int = 20):
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    df[f'Vol_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
    print(f"[Sentinel] Calculated {window}-day Moving Average and Volume SMA.")
    return df


def add_rsi(df: pd.DataFrame, window: int = 14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    print(f"[Sentinel] RSI indicator added (window={window}).")
    return df


def get_dynamic_margin(df: pd.DataFrame, window: int = 20):
    """Calculates dynamic margin based on standard deviation of closing prices."""
    std_dev = df['Close'].rolling(window=window).std()
    margin = std_dev / df[f'SMA_{window}']
    return margin.clip(0.01, 0.05)


def generate_signals(df: pd.DataFrame, window: int = 20):
    sma_col = f'SMA_{window}'
    vol_sma_col = f'Vol_SMA_{window}'
    margins = get_dynamic_margin(df, window)

    def get_signal(row):
        price = row['Close']
        sma = row[sma_col]
        margin = margins[row.name]
        volume = row['Volume']
        vol_sma = row[vol_sma_col]
        rsi = row['RSI']

        if price < sma * (1 - margin) and volume > vol_sma and rsi < 30:
            return "BUY"
        elif price > sma * (1 + margin) and volume > vol_sma and rsi > 70:
            return "SELL"
        return "HOLD"

    df['Signal'] = df.apply(get_signal, axis=1)
    print("[Sentinel] Signals generated with Dynamic Margin & RSI confirmation.")
    return df


def calculate_performance(df: pd.DataFrame):
    trades = df[df['Signal'] != 'HOLD'].copy()
    print(f"[Sentinel] Performance analysis ready. Found {len(trades)} trade signals.")
    return trades


def calculate_pnl(trades: pd.DataFrame):
    trades['PnL'] = trades['Close'].diff()
    total_pnl = trades[trades['Signal'] == 'SELL']['PnL'].sum()
    print(f"[Sentinel] Total PnL calculated: {total_pnl:.2f}")
    return total_pnl