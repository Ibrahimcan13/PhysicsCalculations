import numpy as np
import pandas as pd



def calculate_moving_average(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Calculates Simple Moving Average (SMA) for price and volume."""
    df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()
    df[f"Vol_SMA_{window}"] = df["Volume"].rolling(window=window).mean()
    print(f"[Sentinel] Calculated {window}-day Moving Average and Volume SMA.")
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Calculates Relative Strength Index (RSI) using Wilder's Exponential Moving Average (EMA).
    This provides higher responsiveness to recent price movements compared to SMA.
    """
    if df.empty or "Close" not in df.columns:
        print("[Warning] DataFrame is empty or missing 'Close' column. Skipping RSI calculation.")
        return df

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


def get_dynamic_margin(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculates dynamic volatility margin based on standard deviation of closing prices."""
    std_dev = df["Close"].rolling(window=window).std()
    margin = std_dev / df[f"SMA_{window}"]
    return margin.clip(0.01, 0.05)


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """Calculates upper and lower Bollinger Bands based on price standard deviation."""
    sma = df["Close"].rolling(window=window).mean()
    std_dev = df["Close"].rolling(window=window).std()

    df[f"BB_Upper_{window}"] = sma + (num_std * std_dev)
    df[f"BB_Lower_{window}"] = sma - (num_std * std_dev)
    print(f"[Sentinel] Added Bollinger Bands (window={window}, std={num_std}).")
    return df



def add_trend_predictor(df: pd.DataFrame, train_ratio: float = 0.8) -> tuple[pd.DataFrame, dict]:
    """
    Fits a linear trend line on the training portion of historical data (default 80%)
    and projects the trend into the test set. Calculates Root Mean Squared Error (RMSE).
    """
    if df.empty or "Close" not in df.columns:
        print("[Warning] DataFrame is empty or missing 'Close'. Skipping predictor.")
        return df, {"rmse": 0.0}

    df_clean = df.dropna(subset=["Close"]).copy()
    n = len(df_clean)
    train_size = int(n * train_ratio)

    x = np.arange(n)
    y = df_clean["Close"].values

    x_train, y_train = x[:train_size], y[:train_size]
    poly = np.polyfit(x_train, y_train, deg=1)

    trend_predictions = np.polyval(poly, x)
    df_clean["Trend_Predictor"] = trend_predictions

    y_test = y[train_size:]
    pred_test = trend_predictions[train_size:]

    if len(y_test) > 0:
        rmse = np.sqrt(np.mean((y_test - pred_test) ** 2))
    else:
        rmse = 0.0

    print(f"[Sentinel] Linear Predictor fitted on {train_ratio*100:.0f}% data. Test RMSE: ${rmse:.2f}")

    predictor_metrics = {"rmse": rmse,"split_index": train_size,"split_date": df_clean.index[train_size] if train_size < n else df_clean.index[-1]}

    return df_clean, predictor_metrics


def generate_signals(
        df: pd.DataFrame,
        window: int = 20,
        rsi_lower: float = 30.0,
        rsi_upper: float = 70.0
) -> pd.DataFrame:
    """
    Generates clean BUY/SELL/HOLD signals using a Position State Machine.
    Accepts dynamic RSI thresholds (rsi_lower, rsi_upper).
    """
    sma_col = f"SMA_{window}"
    vol_sma_col = f"Vol_SMA_{window}"
    margins = get_dynamic_margin(df, window)

    raw_buy = (
            (df["Close"] < df[sma_col] * (1 - margins))
            & (df["Volume"] > df[vol_sma_col])
            & (df["RSI"] < rsi_lower)
    )

    raw_sell = (
            (df["Close"] > df[sma_col] * (1 + margins))
            & (df["Volume"] > df[vol_sma_col])
            & (df["RSI"] > rsi_upper)
    )

    signals = []
    current_position = False

    for i in range(len(df)):
        if raw_buy.iloc[i] and not current_position:
            signals.append("BUY")
            current_position = True
        elif raw_sell.iloc[i] and current_position:
            signals.append("SELL")
            current_position = False
        else:
            signals.append("HOLD")

    df["Signal"] = signals
    print(f"[Sentinel] Signals generated (RSI Buy: <{rsi_lower}, RSI Sell: >{rsi_upper}).")
    return df


def calculate_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts trade signals (excluding HOLD) for evaluation."""
    trades = df[df["Signal"] != "HOLD"].copy()
    print(f"[Sentinel] Performance analysis ready. Found {len(trades)} trade signals.")
    return trades


def calculate_pnl(df: pd.DataFrame, commission_rate: float = 0.001) -> dict:
    """
    Calculates Realized Net PnL considering transaction fees (commission/slippage),
    computes advanced strategy metrics, and returns time-indexed equity curve.
    """
    trades = df[df["Signal"] != "HOLD"].copy()
    if trades.empty:
        return {"total_pnl": 0.0,"win_rate": 0.0,"total_trades": 0,"winning_trades": 0,"max_drawdown": 0.0,"equity_curve": pd.Series([100.0], index=[df.index[0] if not df.empty else 0])
        }

    total_pnl = 0.0
    buy_price = None
    trade_results = []

    equity = 100.0
    equity_dict = {df.index[0]: equity}

    for idx, row in trades.iterrows():
        if row["Signal"] == "BUY" and buy_price is None:
            buy_price = row["Close"] * (1 + commission_rate)
        elif row["Signal"] == "SELL" and buy_price is not None:
            sell_price = row["Close"] * (1 - commission_rate)

            pnl = sell_price - buy_price
            total_pnl += pnl
            trade_results.append(pnl)

            equity += pnl
            equity_dict[idx] = equity
            buy_price = None

    total_completed_trades = len(trade_results)
    winning_trades = sum(1 for pnl in trade_results if pnl > 0)
    win_rate = (winning_trades / total_completed_trades * 100) if total_completed_trades > 0 else 0.0

    equity_series = pd.Series(equity_dict).reindex(df.index).ffill().fillna(100.0)

    peak = equity_series.cummax()
    drawdown = (equity_series - peak) / peak
    max_drawdown = drawdown.min() * 100

    metrics = {"total_pnl": total_pnl,"win_rate": win_rate,"total_trades": total_completed_trades,"winning_trades": winning_trades,"max_drawdown": abs(max_drawdown),"equity_curve": equity_series}

    print(
        f"[Sentinel] Advanced Metrics Computed -> Net PnL: {total_pnl:.2f} | Win Rate: {win_rate:.1f}% | Max DD: {abs(max_drawdown):.2f}%")
    return metrics