import yfinance as yf
import pandas as pd
import os


def fetch_market_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical market data from Yahoo Finance API.
    Example tickers: 'AAPL' (Apple), 'RACE' (Ferrari), 'BTC-USD' (Bitcoin)"""

    print(f"[Sentinel] Fetching data from API for ticker: {ticker}...")
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        print(f"[Error] No data found for ticker: {ticker}! Please check the symbol.")
        return pd.DataFrame()

    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    return df


def save_data_to_csv(df: pd.DataFrame, filename: str):
    """Saves the fetched DataFrame to a local CSV file for caching."""

    if df.empty:
        print("[Warning] DataFrame is empty. Aborting save operation.")
        return

    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)

    df.to_csv(filepath)
    print(f"[Sentinel] Data successfully cached locally at: {filepath}")


def load_local_data(filename: str) -> pd.DataFrame:
    """Loads historical data from a locally cached CSV file."""

    filepath = os.path.join("data", filename)
    if os.path.exists(filepath):
        print(f"[Sentinel] Loading local data from: {filepath}")
        return pd.read_csv(filepath, index_col=0, parse_dates=True)
    else:
        print(f"[Error] Local file not found at: {filepath}")
        return pd.DataFrame()