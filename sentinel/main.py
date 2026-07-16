from analysis import load_market_data, calculate_signals, save_signals_to_csv
from visualizer import plot_market_data 

def main():
    print(" Sentinel Market Tracker Initiated ")

    data_file = "data.csv"
    output_file = "sentinel_signals.csv"

    market_df = load_market_data(data_file)

    if not market_df.empty:
        processed_df = calculate_signals(market_df)

        print("\n Processed Market Data with Sentinel Signals ")
        print(processed_df)

        if save_signals_to_csv(processed_df, output_file):
            print("\n Generating Market Visualizations ")
            plot_market_data(output_file)

    else:
        print("[ERROR] No data available to process.")

    print("\n Sentinel Execution Finished")


if __name__ == "__main__":
    main()