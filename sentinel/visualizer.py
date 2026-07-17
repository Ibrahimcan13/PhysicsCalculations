import matplotlib.pyplot as plt


def plot_signals(df):
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(14, 8))

    ax1.plot(df.index, df['Close'], label='Price', color='white', zorder=2, alpha=0.7)
    ax1.plot(df.index, df['SMA_20'], label='SMA 20', color='yellow', linestyle='--', zorder=3)

    buy_signals = df[df['Signal'] == 'BUY']
    sell_signals = df[df['Signal'] == 'SELL']

    ax1.scatter(buy_signals.index, buy_signals['Close'], color='lime', marker='^', label='BUY', zorder=5, s=100)
    ax1.scatter(sell_signals.index, sell_signals['Close'], color='red', marker='v', label='SELL', zorder=5, s=100)

    ax1.set_ylabel('Price', color='white')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.bar(df.index, df['Volume'], color='skyblue', alpha=0.4, label='Volume', zorder=1)
    ax2.set_ylabel('Volume', color='gray')
    ax2.set_ylim(0, df['Volume'].max() * 3)

    plt.title('Sentinel: Ferrari Analysis (Signals & Volume)', fontsize=14)
    plt.grid(True, alpha=0.1)
    plt.tight_layout()
    plt.show()