import pandas as pd
def get_market_data():
    """Fetches the raw market data."""
    market_data = {
        'Ticker': ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT'],
        'Price': [150, 2800, 700, 3400, 300],
        'Sector_Average': [155, 2750, 720, 3350, 290]
    }
    return pd.DataFrame(market_data)

def calculate_signals(df):
    """Calculates BUY/SELL/HOLD signals based on price deviation."""
    def get_signal(row):
        if row['Price'] < row['Sector_Average'] * 0.95:
            return 'BUY'
        elif row['Price'] > row['Sector_Average'] * 1.05:
            return 'SELL'
        else:
            return 'HOLD'

    df['Signal'] = df.apply(get_signal, axis=1)
    return df