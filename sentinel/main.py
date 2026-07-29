from datetime import datetime
from analysis import (
    add_bollinger_bands,
    add_rsi,
    add_trend_predictor,
    calculate_moving_average,
    calculate_performance,
    calculate_pnl,
    generate_signals,
)
from data_loader import fetch_market_data, save_data_to_csv
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


def get_valid_window_size(default: int = 20) -> int:
    """Prompts the user for a window size with fallback to default."""
    window_str = input(
        f"Enter analysis window size in days [Press Enter for Default: {default}]: "
    ).strip()

    if not window_str:
        print(f"[Sentinel] Using default window size: {default} days.")
        return default

    if window_str.isdigit() and int(window_str) > 0:
        window_size = int(window_str)
        print(f"[Sentinel] Window size set to: {window_size} days.")
        return window_size
    else:
        print(f"[Warning] Invalid input. Falling back to default window size: {default} days.")
        return default


def run_sentinel():
    print("PROJECT SENTINEL: SECURITY PIPELINE")

    user_ticker = input("Enter asset ticker (e.g., RACE, AAPL): ").strip().upper()
    if not user_ticker:
        print("[Error] Ticker cannot be empty. Aborting.")
        return

    print("\n--- Configuration ---")
    window_size = get_valid_window_size(default=20)

    print("\n--- Date Configuration ---")
    today = datetime.now()

    while True:
        start_dt = get_valid_date("Enter Start Date (YYYY-MM-DD): ")
        end_dt = get_valid_date("Enter End Date (YYYY-MM-DD): ")

        if start_dt > today or end_dt > today:
            print("[Security Alert] Dates cannot be in the future! Today is current.")
            print(f"Current System Date: {today.strftime('%Y-%m-%d')}\n")
            continue

        if start_dt >= end_dt:
            print("[Security Alert] Start date must be BEFORE the end date!\n")
            continue

        days_difference = (end_dt - start_dt).days
        if days_difference < window_size:
            print(f"[Security Alert] Date range is too short ({days_difference} days).")
            print(f"Sentinel requires AT LEAST {window_size} days of data to compute SMA and Bollinger Bands!\n")
            continue

        break

    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")

    print(
        f"\n[Sentinel] Validation Successful! Processing {user_ticker} (Window: {window_size}d) from {start_date} to {end_date}..."
    )

    df = fetch_market_data(user_ticker, start_date, end_date)
    if df.empty:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dynamic_filename = f"{user_ticker}_{timestamp}.csv"
    save_data_to_csv(df, dynamic_filename)

    df = calculate_moving_average(df, window=window_size)
    df = add_rsi(df, window=14)
    df = add_bollinger_bands(df, window=window_size, num_std=2.0)

    df, predictor_metrics = add_trend_predictor(df, train_ratio=0.8, future_days=15)

    df = generate_signals(df, window=window_size)
    trade_log = calculate_performance(df)
    metrics = calculate_pnl(df, commission_rate=0.001)


    print(f"         SENTINEL STATUS REPORT           ")
    print(f"Target Asset       : {user_ticker}")
    print(f"Window Size        : {window_size} days")
    print(f"Total Trades       : {metrics['total_trades']}")
    print(f"Winning Trades     : {metrics['winning_trades']}")
    print(f"Win Rate           : %{metrics['win_rate']:.1f}")
    print(f"Max Drawdown       : %{metrics['max_drawdown']:.2f}")
    print(f"Net Realized PnL   : ${metrics['total_pnl']:.2f}")
    print(f"Trend Test RMSE    : ${predictor_metrics['rmse']:.2f}")

    if "future_df" in predictor_metrics and not predictor_metrics["future_df"].empty:
        future_df = predictor_metrics["future_df"]
        print(f"Future Projection  : {len(future_df)} Business Days generated.")


    plot_signals(
        df,
        ticker=user_ticker,
        window=window_size,
        metrics=metrics,
        predictor_metrics=predictor_metrics
    )


if __name__ == "__main__":
    run_sentinel()