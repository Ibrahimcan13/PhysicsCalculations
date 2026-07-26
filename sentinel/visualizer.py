import matplotlib.pyplot as plt
import pandas as pd


def plot_signals(
    df: pd.DataFrame,
    ticker: str,
    window: int,
    total_signals: int,
    total_pnl: float,
    save_path: str = None,
) -> None:
    """Plots historical price, SMA, Bollinger Bands, Volume, Buy/Sell signals, and a dynamic summary table."""
    plt.style.use("dark_background")

    fig, ax = plt.subplots(
        2,1,figsize=(14, 8),sharex=True,gridspec_kw={"height_ratios": [3, 1]},)

    ax[0].plot( df.index,df["Close"], label="Price", color="lightgray", alpha=0.8, linewidth=1.5,)
    ax[0].plot(df.index,df[f"SMA_{window}"], label=f"SMA {window}", color="gold", linestyle="--", linewidth=1.5,)
    ax[0].plot( df.index, df[f"BB_Upper_{window}"], label="BB Upper", color="purple", linestyle=":", alpha=0.7,)
    ax[0].plot( df.index,  df[f"BB_Lower_{window}"],  label="BB Lower",  color="purple",  linestyle=":", alpha=0.7,)

    ax[0].fill_between(df.index,df[f"BB_Upper_{window}"],df[f"BB_Lower_{window}"],color="cyan",alpha=0.03,label="BB Range",)

    buy_signals = df[df["Signal"] == "BUY"]
    sell_signals = df[df["Signal"] == "SELL"]

    ax[0].scatter(
        buy_signals.index,buy_signals["Close"], label="BUY",color="lime", marker="^",s=120,zorder=5,)
    ax[0].scatter( sell_signals.index, sell_signals["Close"], label="SELL", color="red", marker="v", s=120, zorder=5,)

    ax[0].set_title(
        f"Sentinel: {ticker} Market Analysis (Signals & Volatility)",
        fontsize=14,
        pad=15,
    )
    ax[0].set_ylabel("Price (USD)", fontsize=11)
    ax[0].grid(True, linestyle=":", alpha=0.3)
    ax[0].legend(loc="upper left", framealpha=0.5)

    table_data = [
        ["Asset Ticker", ticker],
        ["Total Signals", str(total_signals)],
        ["Realized PnL", f"{total_pnl:.2f}"],
    ]

    summary_table = ax[0].table(  cellText=table_data, cellLoc="center", loc="upper right",  bbox=[0.75, 0.65, 0.22, 0.25],
    )

    summary_table.auto_set_font_size(False)
    summary_table.set_fontsize(10)

    for (row, col), cell in summary_table.get_celld().items():
        cell.set_facecolor("#1e1e1e")
        cell.set_text_props(color="white", weight="bold")
        cell.set_edgecolor("#444444")

    ax[1].bar( df.index, df["Volume"], color="skyblue", alpha=0.4, width=0.8, label="Volume",
    )
    if f"Vol_SMA_{window}" in df.columns:
        ax[1].plot( df.index, df[f"Vol_SMA_{window}"], color="orange", linestyle="-.", linewidth=1.2, label=f"Vol SMA {window}",
        )
    ax[1].set_ylabel("Volume", fontsize=11)
    ax[1].grid(True, linestyle=":", alpha=0.3)
    ax[1].legend(loc="upper left", framealpha=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Sentinel] Plot saved to {save_path}")

    plt.show()