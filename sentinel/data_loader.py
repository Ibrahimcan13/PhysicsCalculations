import os
import pandas as pd
import yfinance as yf


def fetch_market_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches historical market data from Yahoo Finance API with error handling."""
    print(f"[Sentinel] Attempting to fetch data from API for ticker: {ticker}...")

    try:
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            print(
                f"[Error] No data returned for ticker '{ticker}'. Please check the symbol or date range."
            )
            return pd.DataFrame()

        # Flattens MultiIndex column headers if present
        df.columns = [
            col[0] if isinstance(col, tuple) else col for col in df.columns
        ]

        print(
            f"[Sentinel] Successfully downloaded {len(df)} rows of data for {ticker}."
        )
        return df

    except Exception as e:
        print(f"[Error] An unexpected error occurred while fetching data ({type(e).__name__}): {e}")
        return pd.DataFrame()


def save_data_to_csv(
    df: pd.DataFrame, filename: str, folder: str = "data"
) -> None:
    """Saves the fetched DataFrame to a local CSV file for caching with safety checks."""
    if df.empty:
        print("[Warning] DataFrame is empty. Aborting local save operation.")
        return

    try:
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)

        df.to_csv(filepath)
        print(f"[Sentinel] Data successfully cached locally at: {filepath}")

    except IOError as e:
        print(f"[Error] Disk I/O failed. Could not write file to disk: {e}")
    except Exception as e:
        print(f"[Error] Unexpected error during save operation: {e}")


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