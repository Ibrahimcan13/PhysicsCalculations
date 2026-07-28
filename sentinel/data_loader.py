from datetime import datetime, timedelta
import os
import pandas as pd
import yfinance as yf

_DATA_CACHE = {}


def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:
    """Removes weekend data and completely empty rows from the DataFrame."""
    if df.empty:
        return df

    df = df[df.index.dayofweek < 5]
    df = df.dropna(how="all")

    return df


def fetch_market_data(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Fetches historical market data from Yahoo Finance API with error handling.
    Defaults to the last 1 year if start_date/end_date are not provided.
    Uses in-memory cache for fast repeated calls.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    cache_key = f"{ticker}_{start_date}_{end_date}"
    if cache_key in _DATA_CACHE:
        print(f"[Sentinel] [Cache Hit] Returning memory-cached data for {ticker}...")
        return _DATA_CACHE[cache_key].copy()

    print(f"[Sentinel] Attempting to fetch data from API for ticker: {ticker} ({start_date} to {end_date})...")

    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if df.empty:
            print(
                f"[Error] No data returned for ticker '{ticker}'. Please check the symbol or date range.")
            return pd.DataFrame()

        df.columns = [
            col[0] if isinstance(col, tuple) else col for col in df.columns]

        df = clean_market_data(df)

        print(
            f"[Sentinel] Successfully downloaded {len(df)} rows of data for {ticker}.")

        _DATA_CACHE[cache_key] = df.copy()

        return df

    except Exception as e:
        print(f"[Error] An unexpected error occurred while fetching data ({type(e).__name__}): {e}")
        return pd.DataFrame()


def save_data_to_csv(
        df: pd.DataFrame, ticker: str, filename: str = None, folder: str = "data") -> str:
    """Saves the fetched DataFrame to a local CSV file with clean naming and rounded values."""
    if df.empty:
        print("[Warning] DataFrame is empty. Aborting local save operation.")
        return ""

    try:
        os.makedirs(folder, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{ticker}_{timestamp}.csv"

        filepath = os.path.join(folder, filename)

        df.round(2).to_csv(filepath)
        print(f"[Sentinel] Data successfully cached locally at: {filepath}")
        return filepath

    except IOError as e:
        print(f"[Error] Disk I/O failed. Could not write file to disk: {e}")
        return ""
    except Exception as e:
        print(f"[Error] Unexpected error during save operation: {e}")
        return ""


def load_local_data(filename: str, folder: str = "data") -> pd.DataFrame:
    """Loads historical data from a locally cached CSV file with existence checks."""
    filepath = os.path.join(folder, filename)

    try:
        if os.path.exists(filepath):
            print(f"[Sentinel] Loading local data from: {filepath}")
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        else:
            print(f"[Warning] Local cache file not found at: {filepath}")
            return pd.DataFrame()

    except pd.errors.EmptyDataError:
        print(f"[Error] The local cache file at {filepath} is empty or corrupted.")
        return pd.DataFrame()
    except Exception as e:
        print(f"[Error] Unexpected error while reading local file: {e}")
        return pd.DataFrame()