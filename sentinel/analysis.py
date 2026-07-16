import pandas as pd

def load_market_data(file_path: str) -> pd.DataFrame:
    """Loads market data from a CSV file and returns a Pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"[SUCCESS] Data successfully loaded from: {file_path}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] The file at {file_path} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while loading data: {e}")
        return pd.DataFrame()


def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates BUY/SELL/HOLD signals based on price deviation AND volume filter."""
    if df.empty or "Price" not in df.columns or "Volume" not in df.columns:
        print("[WARNING] Cannot calculate signals. DataFrame is empty or required columns are missing.")
        return df

    avg_price = df["Price"].mean()
    avg_volume = df["Volume"].mean()

    print(f"[ANALYSIS] Global Average Price: {avg_price:.3f}")
    print(f"[ANALYSIS] Global Average Volume: {avg_volume:.2f}")

    def get_smart_signal(row):
        price = row["Price"]
        volume = row["Volume"]

        if volume > avg_volume:
            if price < avg_price * 0.98:
                return "BUY"
            elif price > avg_price * 1.02:
                return "SELL"

        return "HOLD"

    df["Signal"] = df.apply(get_smart_signal, axis=1)
    return df

def save_signals_to_csv(df: pd.DataFrame, output_path: str) -> bool:
    """Saves the processed DataFrame with signals to a CSV file."""
    if df.empty:
        print("[WARNING] DataFrame is empty. Nothing to save.")
        return False
    try:

        df.to_csv(output_path, index=False)
        print(f"[SUCCESS] Signals successfully saved to: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save signals to CSV: {e}")
        return False