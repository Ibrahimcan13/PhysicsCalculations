from datetime import datetime
from analysis import (add_bollinger_bands, add_rsi, calculate_moving_average, calculate_performance, calculate_pnl, generate_signals,)
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
            print(
                "[Error] Invalid format! Please use YYYY-MM-DD (e.g., 2026-01-01)."
            )


def run_sentinel():
    print("=== PROJECT SENTINEL: SECURITY PIPELINE ===")

    user_ticker = (
        input("Enter asset ticker (e.g., RACE, AAPL): ").strip().upper()
    )
    if not user_ticker:
        print("[Error] Ticker cannot be empty. Aborting.")
        return

    print("\n--- Date Configuration ---")
    today = datetime.now()

    while True:
        start_dt = get_valid_date("Enter Start Date (YYYY-MM-DD): ")
        end_dt = get_valid_date("Enter End Date (YYYY-MM-DD): ")

        if start_dt > today or end_dt > today:
            print(
                "[Security Alert] Dates cannot be in the future! Today is current."
            )
            print(f"Current System Date: {today.strftime('%Y-%m-%d')}\n")
            continue

        if start_dt >= end_dt:
            print("[Security Alert] Start date must be BEFORE the end date!\n")
            continue

        days_difference = (end_dt - start_dt).days
        if days_difference < 20:
            print(
                f"[Security Alert] Date range is too short ({days_difference} days)."
            )
            print(
                "Sentinel requires AT LEAST 20 days of data to compute SMA and Bollinger Bands!\n"
            )
            continue

        break

    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")
    window_size = 20

    print(
        f"\n[Sentinel] Validation Successful! Processing {user_ticker} from {start_date} to {end_date}..."
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
    df = generate_signals(df, window=window_size)

    trade_log = calculate_performance(df)
    total_pnl = calculate_pnl(df)
    total_signals = len(trade_log)

    plot_signals(df, ticker=user_ticker, window=window_size,   total_signals=total_signals,total_pnl=total_pnl, )

    print(f"\n SENTINEL STATUS REPORT")
    print(f"Target Asset       : {user_ticker}")
    print(f"Total Trade Signals: {total_signals}")
    print(f"Total Realized PnL : {total_pnl:.3f}")

if __name__ == "__main__":
    run_sentinel()