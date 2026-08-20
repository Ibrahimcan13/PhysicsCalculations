from datetime import datetime, timedelta
import os
import pandas as pd
import yfinance as yf

_DATA_CACHE = {}


def _normalize_yfinance_columns(df: pd.DataFrame, ticker: str = "") -> pd.DataFrame:

    if df.empty:
        return df

    if isinstance(df.columns, pd.MultiIndex):
        if ticker and ticker in df.columns.levels[1]:
            df = df.xs(ticker, axis=1, level=1)
        elif ticker and ticker in df.columns.levels[0]:
            df = df.xs(ticker, axis=1, level=0)
        else:
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    else:
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    return df


def clean_market_data(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    if hasattr(df.index, 'tz') and df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df = df[df.index.dayofweek < 5]
    df = df.dropna(how="all")

    return df


def align_market_data(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    if df1.empty or df2.empty:
        return df1, df2

    common_dates = df1.index.intersection(df2.index)

    if common_dates.empty:
        print("[Warning] No common dates found between the provided DataFrames.")
        return pd.DataFrame(), pd.DataFrame()

    df1_aligned = df1.loc[common_dates].copy()
    df2_aligned = df2.loc[common_dates].copy()

    return df1_aligned, df2_aligned


def _fetch_single_ticker(ticker: str, start_date: str, end_date: str, folder: str = "data") -> pd.DataFrame:
    """Internal helper to handle memory cache, local disk cache, and yfinance fetching."""
    cache_key = f"{ticker}_{start_date}_{end_date}"

    if cache_key in _DATA_CACHE:
        print(f"[Sentinel] [Memory Cache Hit] Returning cached data for {ticker}...")
        return _DATA_CACHE[cache_key].copy()

    filename = f"{cache_key}.csv"
    local_df = load_local_data(filename, folder=folder)
    if not local_df.empty:
        print(f"[Sentinel] [Disk Cache Hit] Loaded {ticker} from local storage ({filename}).")
        _DATA_CACHE[cache_key] = local_df.copy()
        return local_df

    print(f"[Sentinel] Fetching data from API for ticker: {ticker} ({start_date} to {end_date})...")

    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if df.empty:
            print(f"[Error] No data returned for ticker '{ticker}'. Please check symbol or date range.")
            return pd.DataFrame()

        df = _normalize_yfinance_columns(df, ticker=ticker)
        df = clean_market_data(df)

        print(f"[Sentinel] Successfully downloaded {len(df)} rows for {ticker}.")

        save_data_to_csv(df, ticker=ticker, filename=filename, folder=folder)

        _DATA_CACHE[cache_key] = df.copy()
        return df

    except Exception as e:
        print(f"[Error] An unexpected error occurred while fetching {ticker} ({type(e).__name__}): {e}")
        return pd.DataFrame()


def fetch_market_data(
        tickers: str | list[str],
        start_date: str = None,
        end_date: str = None,
        folder: str = "data"
) -> pd.DataFrame | dict[str, pd.DataFrame]:
    """
    Fetches historical market data for one or multiple tickers.
    First checks local CSV cache before falling back to Yahoo Finance API.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")

    if isinstance(tickers, str):
        ticker_list = [t.strip().upper() for t in tickers.replace(",", " ").split() if t.strip()]
    else:
        ticker_list = [t.strip().upper() for t in tickers if t.strip()]

    if not ticker_list:
        print("[Error] No valid ticker symbol provided.")
        return pd.DataFrame()

    if len(ticker_list) == 1:
        return _fetch_single_ticker(ticker_list[0], start_date, end_date, folder=folder)

    results = {}
    for ticker in ticker_list:
        df = _fetch_single_ticker(ticker, start_date, end_date, folder=folder)
        if not df.empty:
            results[ticker] = df

    return results


def save_data_to_csv(
        df: pd.DataFrame, ticker: str, filename: str = None, folder: str = "data"
) -> str:
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
            df = pd.read_csv(filepath, index_col=0, parse_dates=True)
            return clean_market_data(df)
        else:
            return pd.DataFrame()

    except pd.errors.EmptyDataError:
        print(f"[Error] The local cache file at {filepath} is empty or corrupted.")
        return pd.DataFrame()
    except Exception as e:
        print(f"[Error] Unexpected error while reading local file: {e}")
        return pd.DataFrame()