import matplotlib.pyplot as plt

def plot_market_data(df):
    """Visualizes the stock prices and sector averages."""
    plt.figure(figsize=(10, 6))
    plt.bar(df['Ticker'], df['Price'], label='Price', color='skyblue')
    plt.plot(df['Ticker'], df['Sector_Average'], color='red', marker='o',
             linestyle='dashed', label='Sector Avg')
    plt.title('Stock Price vs Sector Average')
    plt.xlabel('Tickers')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()