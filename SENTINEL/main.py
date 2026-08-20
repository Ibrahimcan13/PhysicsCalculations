from datetime import datetime
from analysis import (
    add_bollinger_bands,
    add_rsi,
    calculate_average_true_range,
    calculate_moving_average,
    calculate_performance,
    calculate_pnl,
    generate_signals,
)
from data_loader import fetch_market_data, save_data_to_csv
from predictor import train_and_predict
from visualizer import plot_signals


def get_valid_date(prompt: str) -> datetime:
    """Prompts the user for a date and validates the YYYY-MM-DD format."""
    while True:
        date_str = input(prompt).strip()
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt
        except ValueError:
            print("[Error] Invalid format! Please use YYYY-MM-DD (e.g., 2026-01-01).")


def get_valid_window_size(prompt: str, default: int) -> int:
    """Prompts the user for a custom window size with fallback to default."""
    window_str = input(
        f"{prompt} [Press Enter for Default: {default}]: "
    ).strip()

    if not window_str:
        print(f"[Sentinel] Using default size: {default} days.")
        return default

    if window_str.isdigit() and int(window_str) > 0:
        window_size = int(window_str)
        print(f"[Sentinel] Window size set to: {window_size} days.")
        return window_size
    else:
        print(f"[Warning] Invalid input. Falling back to default: {default} days.")
        return default


def run_sentinel():
    print("       PROJECT SENTINEL      ")

    user_ticker = input("Enter asset ticker (e.g., RACE, AAPL): ").strip().upper()
    if not user_ticker:
        print("[Error] Ticker cannot be empty. Aborting.")
        return

    print("\n[Configuration]")
    window_size = get_valid_window_size("Enter analysis SMA window size in days", default=20)
    rsi_window = get_valid_window_size("Enter RSI window size in days", default=14)

    print("\n[Date Configuration]")
    today = datetime.now()

    while True:
        start_dt = get_valid_date("Enter Start Date (YYYY-MM-DD): ")
        end_dt = get_valid_date("Enter End Date (YYYY-MM-DD): ")

        if start_dt > today or end_dt > today:
            print("[Security Alert] Dates cannot be in the future!")
            print(f"Current System Date: {today.strftime('%Y-%m-%d')}\n")
            continue

        if start_dt >= end_dt:
            print("[Security Alert] Start date must be BEFORE the end date!\n")
            continue

        days_difference = (end_dt - start_dt).days
        min_required = max(window_size, rsi_window) + 14
        if days_difference < min_required:
            print(f"[Security Alert] Date range is too short ({days_difference} days).")
            print(f"Sentinel requires AT LEAST {min_required} days of data to compute indicators!\n")
            continue

        break

    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")

    print(
        f"\n[Sentinel] Validation Successful! Processing {user_ticker} "
        f"(SMA: {window_size}d, RSI: {rsi_window}d) from {start_date} to {end_date}..."
    )

    df = fetch_market_data(user_ticker, start_date, end_date)
    if df.empty:
        return

    df = calculate_moving_average(df, window=window_size)
    df = add_rsi(df, window=rsi_window)
    df = calculate_average_true_range(df, window=14)
    df = add_bollinger_bands(df, window=window_size, num_std=2.0)

    forecast_days = 5
    print("\n[AI Engine]")
    df = train_and_predict(df, forecast_days=forecast_days, train_window=200)

    print("\n[Backtest Engine]")
    df = generate_signals(df, window=window_size)
    trade_log = calculate_performance(df)
    metrics = calculate_pnl(df, commission_rate=0.001)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dynamic_filename = f"{user_ticker}_{timestamp}.csv"
    save_data_to_csv(df, dynamic_filename)

    latest_prob = df["AI_Probability"].iloc[-1] if "AI_Probability" in df.columns else None
    latest_price = df["Close"].iloc[-1]

    print("          SENTINEL STATUS REPORT         ")
    print(f"Target Asset       : {user_ticker}")
    print(f"Latest Close Price : ${latest_price:.2f}")
    print(f"Analysis Window    : SMA {window_size}d | RSI {rsi_window}d | ATR 14d")
    print(f"Total Trades       : {metrics['total_trades']}")
    print(f"Winning Trades     : {metrics['winning_trades']}")
    print(f"Win Rate           : {metrics['win_rate']:.1f}%")
    print(f"Max Drawdown       : {metrics['max_drawdown']:.2f}%")
    print(f"Net Realized PnL   : ${metrics['total_pnl']:.2f}")

    if latest_prob is not None:
        bullish_pct = latest_prob * 100
        bearish_pct = (1 - latest_prob) * 100
        direction = "BULLISH" if bullish_pct >= 50 else "BEARISH"

        print(f"AI FORECAST ({forecast_days}-Day Horizon) : {direction}")
        print(f"Bullish Probability ({forecast_days}d ahead) : {bullish_pct:.1f}%")
        print(f"Bearish Probability ({forecast_days}d ahead) : {bearish_pct:.1f}%")

    plot_signals(
        df,
        ticker=user_ticker,
        window=window_size,
        metrics=metrics,
        train_window=200
    )


if __name__ == "__main__":
    run_sentinel()