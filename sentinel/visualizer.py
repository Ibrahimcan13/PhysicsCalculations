import matplotlib.pyplot as plt
import pandas as pd

def plot_market_data(file_path: str):
    """Plots market price on primary y-axis, volume on secondary y-axis, and highlights BUY/SELL signals."""
    try:
        df = pd.read_csv(file_path)

        fig, ax1 = plt.subplots(figsize=(12, 7))

        color_price = "deepskyblue"
        ax1.set_xlabel("Date", fontsize=12, fontweight="bold", labelpad=12)
        ax1.set_ylabel("Price ($)", color="white", fontsize=12, fontweight="bold")

        ax1.plot(df["Date"], df["Price"], label="Market Price", color=color_price, marker="o", linewidth=2.5, zorder=3)
        ax1.tick_params(axis="y", labelcolor="white")

        buy_signals = df[df["Signal"] == "BUY"]
        ax1.scatter(buy_signals["Date"], buy_signals["Price"], color="lime", label="BUY Signal", marker="^", s=200, edgecolors="black", zorder=5)

        sell_signals = df[df["Signal"] == "SELL"]
        ax1.scatter(sell_signals["Date"], sell_signals["Price"], color="red", label="SELL Signal", marker="v", s=200, edgecolors="black", zorder=5)

        ax2 = ax1.twinx()
        ax2.set_ylabel("Volume", color="gray", fontsize=12, fontweight="bold")
        ax2.bar(df["Date"], df["Volume"], alpha=0.2, color="skyblue", label="Volume", width=0.5, zorder=1)
        ax2.tick_params(axis="y", labelcolor="gray")


        fig.patch.set_facecolor("#121212")
        ax1.set_facecolor("#1e1e1e")
        ax2.set_facecolor("#1e1e1e")

        ax1.spines["bottom"].set_color("white")
        ax1.spines["top"].set_color("#333333")
        ax1.spines["left"].set_color("white")
        ax1.spines["right"].set_color("white")
        ax1.tick_params(axis="x", colors="white", rotation=30)
        ax1.tick_params(axis="y", colors="white")

        ax1.grid(True, which="both", linestyle=":", alpha=0.3, color="gray")

        plt.title("Sentinel Market Tracker - Advanced Pro Decision Dashboard", fontsize=15, fontweight="bold",
                  color="white", pad=15)

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper left", facecolor="#1e1e1e", edgecolor="white",
                   labelcolor="white")

        plt.tight_layout()
        print("[SUCCESS] Rendering Pro Dashboard... Close the window to finish.")
        plt.show()

    except FileNotFoundError:
        print(f"[ERROR] Could not find the file: {file_path}")
    except Exception as e:
        print(f"[ERROR] An error occurred while plotting: {e}")