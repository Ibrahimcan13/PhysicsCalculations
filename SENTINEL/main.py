import logging
import traceback
from datetime import datetime
import pandas as pd

from analysis import (
    add_bollinger_bands,
    add_kalman_filter,
    add_rsi,
    calculate_average_true_range,
    calculate_moving_average,
    generate_signals,
)
from back_tester import run_backtest
from data_loader import fetch_market_data, save_data_to_parquet
from predictor import train_and_predict
from visualizer import plot_signals

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def get_valid_date(prompt: str) -> datetime:
    while True:
        date_str = input(prompt).strip()
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt
        except ValueError:
            logging.error("Invalid format! Please use YYYY-MM-DD (e.g., 2026-01-01).")


def get_valid_window_size(prompt: str, default: int, min_val: int = 1) -> int:
    window_str = input(
        f"{prompt} [Press Enter for Default: {default}]: "
    ).strip()

    if not window_str:
        logging.info(f"Using default size: {default}.")
        return default

    if window_str.isdigit() and int(window_str) >= min_val:
        window_size = int(window_str)
        logging.info(f"Window size set to: {window_size}.")
        return window_size
    else:
        logging.warning(f"Invalid input (Must be >= {min_val}). Falling back to default: {default}.")
        return default


def get_valid_float(prompt: str, default: float) -> float:
    val_str = input(f"{prompt} [Press Enter for Default: ${default:.2f}]: ").strip()
    if not val_str:
        logging.info(f"Using default initial capital: ${default:.2f}")
        return default
    try:
        val = float(val_str)
        if val > 0:
            logging.info(f"Initial capital set to: ${val:.2f}")
            return val
        else:
            logging.warning(f"Must be greater than 0. Using default: ${default:.2f}")
            return default
    except ValueError:
        logging.warning(f"Invalid number. Using default: ${default:.2f}")
        return default


def run_sentinel():
    print("           PROJECT SENTINEL             ")

    try:
        user_ticker = input("Enter asset ticker (e.g., RACE, AAPL): ").strip().upper()
        if not user_ticker:
            logging.error("Ticker cannot be empty. Aborting.")
            return

        print("\n[Configuration]")
        initial_capital = get_valid_float("Enter starting capital in USD", default=1000.0)
        window_size = get_valid_window_size("Enter analysis SMA window size in days", default=20)
        rsi_window = get_valid_window_size("Enter RSI window size in days", default=14)

        train_window = get_valid_window_size(
            "Enter AI Training Window size (bars/days)", default=200, min_val=100
        )

        forecast_days = 5
        retrain_step = 20
        risk_per_trade = 0.02

        print("\n[Date Configuration]")
        today = datetime.now()

        while True:
            start_dt = get_valid_date("Enter Start Date (YYYY-MM-DD): ")
            end_dt = get_valid_date("Enter End Date (YYYY-MM-DD): ")

            if start_dt > today or end_dt > today:
                logging.warning(f"Dates cannot be in the future! Current System Date: {today.strftime('%Y-%m-%d')}\n")
                continue

            if start_dt >= end_dt:
                logging.warning("Start date must be BEFORE the end date!\n")
                continue

            days_difference = (end_dt - start_dt).days
            min_required = train_window + max(window_size, rsi_window) + 14
            if days_difference < min_required:
                logging.warning(
                    f"Date range is too short ({days_difference} days). Requires AT LEAST {min_required} days!\n")
                continue

            break

        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

        logging.info(f"Fetching {user_ticker} data from {start_date} to {end_date}...")
        df = fetch_market_data(user_ticker, start_date, end_date)
        if df.empty:
            logging.error("Failed to fetch market data. Terminating.")
            return

        logging.info("Calculating technical indicators & Kalman Filter...")
        df = add_kalman_filter(df)
        df = calculate_moving_average(df, window=window_size)
        df = add_rsi(df, window=rsi_window)
        df = calculate_average_true_range(df, window=14)
        df = add_bollinger_bands(df, window=window_size, num_std=2.0)

        logging.info("Executing Walk-Forward AI Training & Inference Pipeline...")
        df = train_and_predict(
            df,
            forecast_days=forecast_days,
            train_window=train_window,
            retrain_step=retrain_step
        )

        logging.info("Generating Trading Signals & Executing Backtest Engine...")
        df = generate_signals(df, window=window_size)

        df, trade_log, metrics = run_backtest(
            df,
            initial_capital=initial_capital,
            risk_per_trade=risk_per_trade,
            commission_rate=0.001,
            slippage_rate=0.0005,
            use_atr_stop=True,
            atr_multiplier=2.0
        )

        save_data_to_parquet(df, ticker=user_ticker)

        latest_prob = (
            df["AI_Probability"].iloc[-1]
            if "AI_Probability" in df.columns and not pd.isna(df["AI_Probability"].iloc[-1])
            else None
        )
        latest_price = df["Close"].iloc[-1]

        print("\n          SENTINEL STATUS REPORT                  ")
        print(f"Target Asset       : {user_ticker}")
        print(f"Starting Capital   : ${initial_capital:.2f}")
        print(f"Latest Close Price : ${latest_price:.2f}")
        print(f"Analysis Pipeline  : Kalman | SMA {window_size}d | RSI {rsi_window}d | ATR 14d")
        print(f"Total Trades       : {metrics.get('total_trades', 0)}")
        print(f"Winning Trades     : {metrics.get('winning_trades', 0)}")
        print(f"Win Rate           : %{metrics.get('win_rate', 0.0):.1f}")
        print(f"Max Drawdown       : %{metrics.get('max_drawdown', 0.0):.2f}")
        print(f"Sharpe Ratio       : {metrics.get('sharpe_ratio', 0.0):.2f}")
        print(f"Avg Holding Period : {metrics.get('avg_duration_days', 0.0):.1f} days")
        print(f"Net Realized PnL   : ${metrics.get('total_pnl', 0.0):.2f}")

        if latest_prob is not None:
            bullish_pct = latest_prob * 100
            bearish_pct = (1 - latest_prob) * 100
            direction = "BULLISH" if bullish_pct >= 50 else "BEARISH"

            print(f"AI FORECAST ({forecast_days}-Day Horizon) : {direction}")
            print(f"Bullish Probability ({forecast_days}d ahead) : %{bullish_pct:.1f}")
            print(f"Bearish Probability ({forecast_days}d ahead) : %{bearish_pct:.1f}")
        else:
            print("AI FORECAST            : Insufficient data for prediction window.")

        logging.info("Rendering signals & portfolio performance plot...")
        plot_signals(
            df,
            ticker=user_ticker,
            window=window_size,
            metrics=metrics,
            trade_log=trade_log,
            train_window=train_window,
            initial_capital=initial_capital
        )

    except KeyboardInterrupt:
        logging.warning("Operation cancelled by user. Exiting safely.")
    except Exception as e:
        logging.error(f"Fatal error encountered: {e}")
        logging.debug(traceback.format_exc())


if __name__ == "__main__":
    run_sentinel()