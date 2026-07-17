from data_loader import fetch_market_data, save_data_to_csv
from visualizer import plot_signals
from analysis import (
    calculate_moving_average,
    add_rsi,
    generate_signals,
    calculate_performance,
    calculate_pnl
)

def run_sentinel():

    ticker = "RACE"
    start_date = "2026-01-01"
    end_date = "2026-07-17"

    df = fetch_market_data(ticker, start_date, end_date)

    if df.empty:
        print("[Error] Pipeline aborted: No data retrieved.")
        return

    save_data_to_csv(df, f"{ticker}_data.csv")

    df = calculate_moving_average(df, window=20)
    df = add_rsi(df, window=14)
    df = generate_signals(df, window=20)

    plot_signals(df)

    trade_log = calculate_performance(df)
    total_pnl = calculate_pnl(trade_log)

    print(f"\n--- SENTINEL STATUS ---")
    print(f"Total Trade Signals: {len(trade_log)}")
    print(f"Total PnL: {total_pnl:.2f}")


if __name__ == "__main__":
    run_sentinel()