import pandas as pd
import matplotlib.pyplot as plt

def get_market_data():
    market_data = {
        'Ticker': ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT'],
        'Price': [150, 2800, 700, 3400, 300],
        'Sector_Average': [155, 2750, 720, 3350, 290]
    }
    return pd.DataFrame(market_data)

def get_trading_signal(price, sector_avg):
    if price < sector_avg * 0.95:
        return 'BUY'
    elif price > sector_avg * 1.05:
        return 'SELL'
    else:
        return 'HOLD'


def visualize_data(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['Ticker'], df['Price'], label='Price', color='skyblue')
    plt.plot(df['Ticker'], df['Sector_Average'], color='red', marker='o', linestyle='dashed', label='Sector Avg')
    plt.title('Stock Price vs Sector Average')
    plt.legend()
    plt.grid(True)
    plt.show()

def save_report(df):
    filename = 'market_analysis_report.csv'
    df.to_csv(filename, index=False)
    print(f" Report successfully saved as: {filename} ")

def run_analysis():
    df = get_market_data()
    df['Signal'] = df.apply(lambda row: get_trading_signal(row['Price'], row['Sector_Average']), axis=1)

    print(" Market Analysis Report ")
    print(df)

    visualize_data(df)

    return df

if __name__ == "__main__":
    market_df = run_analysis()

