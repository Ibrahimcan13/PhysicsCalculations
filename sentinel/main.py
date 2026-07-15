from analysis import get_market_data, calculate_signals
from visualizer import plot_market_data

def main():
    df = get_market_data()

    df = calculate_signals(df)

    print(df)

    plot_market_data(df)

if __name__ == "__main__":
    main()