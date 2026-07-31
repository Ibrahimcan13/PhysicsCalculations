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
    sma_col = f"SMA_{window}" if f"SMA_{window}" in df.columns else "Close"
    std_dev = df["Close"].rolling(window=window).std()

    if sma_col in df.columns:
        margin = std_dev / df[sma_col]
    else:
        margin = std_dev / df["Close"]

    return margin.clip(0.01, 0.05)


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """Calculates upper and lower Bollinger Bands based on price standard deviation."""
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
        rsi_upper: float = 70.0
) -> pd.DataFrame:
    """
    Generates clean BUY/SELL/HOLD signals using a Position State Machine.
    Integrates AI Probability if available in the dataframe.
    """
    sma_col = f"SMA_{window}"
    vol_sma_col = f"Vol_SMA_{window}"

    if sma_col not in df.columns or vol_sma_col not in df.columns:
        df = calculate_moving_average(df, window=window)

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

    if "AI_Probability" in df.columns:
        raw_buy = raw_buy & (df["AI_Probability"] > 0.50)

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
    Calculates Realized Net PnL and Mark-to-Market Portfolio Equity Curve.
    Auto-closes open positions at the last available price.
    """
    if df.empty or "Signal" not in df.columns:
        return {
            "total_pnl": 0.0, "win_rate": 0.0, "total_trades": 0,
            "winning_trades": 0, "max_drawdown": 0.0,
            "equity_curve": pd.Series([100.0], index=[df.index[0] if not df.empty else 0])
        }

    capital = 100.0
    cash = capital
    shares = 0.0

    total_pnl = 0.0
    trade_results = []
    buy_price = None

    equity_list = []

    for idx, row in df.iterrows():
        signal = row["Signal"]
        close_price = row["Close"]

        if signal == "BUY" and shares == 0.0:
            buy_price = close_price * (1 + commission_rate)
            shares = cash / buy_price
            cash = 0.0

        elif signal == "SELL" and shares > 0.0:
            sell_price = close_price * (1 - commission_rate)
            cash = shares * sell_price

            pnl = (sell_price - buy_price) * shares
            total_pnl += pnl
            trade_results.append(pnl)

            shares = 0.0
            buy_price = None

        current_equity = cash + (shares * close_price if shares > 0.0 else 0.0)
        equity_list.append(current_equity)

    if shares > 0.0:
        last_close = df["Close"].iloc[-1]
        sell_price = last_close * (1 - commission_rate)
        cash = shares * sell_price
        pnl = (sell_price - buy_price) * shares
        total_pnl += pnl
        trade_results.append(pnl)
        shares = 0.0
        equity_list[-1] = cash
        print(
            f"[Sentinel] Auto-closed open BUY position at last available close price: ${last_close:.2f} (PnL: ${pnl:.2f})")

    total_completed_trades = len(trade_results)
    winning_trades = sum(1 for pnl in trade_results if pnl > 0)
    win_rate = (winning_trades / total_completed_trades * 100) if total_completed_trades > 0 else 0.0

    equity_series = pd.Series(equity_list, index=df.index)

    peak = equity_series.cummax()
    drawdown = (equity_series - peak) / peak
    max_drawdown = drawdown.min() * 100

    metrics = {
        "total_pnl": total_pnl,
        "win_rate": win_rate,
        "total_trades": total_completed_trades,
        "winning_trades": winning_trades,
        "max_drawdown": abs(max_drawdown),
        "equity_curve": equity_series
    }

    print(
        f"[Sentinel] Advanced Metrics Computed -> Net PnL: ${total_pnl:.2f} | Win Rate: {win_rate:.1f}% | Max DD: {abs(max_drawdown):.2f}%")
    return metrics