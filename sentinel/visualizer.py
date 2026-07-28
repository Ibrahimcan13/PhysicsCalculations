import matplotlib.pyplot as plt
import pandas as pd


def plot_signals(
    df: pd.DataFrame,
    ticker: str,
    window: int,
    metrics: dict,
    predictor_metrics: dict = None,
    save_path: str = None
) -> None:
    """
    Plots historical price, SMA, Bollinger Bands, Linear Trend Predictor, RSI, Volume,
    Buy/Sell signals, a summary metrics table, and Strategy Equity Curve (Portfolio Balance).
    """
    plt.style.use("dark_background")

    fig, ax = plt.subplots(
        4, 1,
        figsize=(14, 12),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1.2, 1, 1.2]}
    )

    ax[0].plot(df.index, df["Close"], label="Price", color="lightgray", alpha=0.8, linewidth=1.5)

    sma_col = f"SMA_{window}"
    bb_upper_col = f"BB_Upper_{window}"
    bb_lower_col = f"BB_Lower_{window}"

    if sma_col in df.columns:
        ax[0].plot(df.index, df[sma_col], label=f"SMA {window}", color="gold", linestyle="--", linewidth=1.5)

    if bb_upper_col in df.columns and bb_lower_col in df.columns:
        ax[0].plot(df.index, df[bb_upper_col], label="BB Upper", color="purple", linestyle=":", alpha=0.7)
        ax[0].plot(df.index, df[bb_lower_col], label="BB Lower", color="purple", linestyle=":", alpha=0.7)
        ax[0].fill_between(df.index, df[bb_upper_col], df[bb_lower_col], color="cyan", alpha=0.03, label="BB Range")

    if "Trend_Predictor" in df.columns:
        ax[0].plot(df.index, df["Trend_Predictor"], label="Trend Predictor", color="skyblue", linewidth=1.8, linestyle="-")

        if predictor_metrics and "split_date" in predictor_metrics:
            split_date = predictor_metrics["split_date"]
            ax[0].axvline(x=split_date, color="crimson", linestyle="--", alpha=0.8, linewidth=1.5, label="Train/Test Split")


    buy_signals = df[df["Signal"] == "BUY"] if "Signal" in df.columns else pd.DataFrame()
    sell_signals = df[df["Signal"] == "SELL"] if "Signal" in df.columns else pd.DataFrame()

    if not buy_signals.empty:
        ax[0].scatter(
            buy_signals.index, buy_signals["Close"], label="BUY", color="lime", marker="^", s=120, zorder=5
        )
    if not sell_signals.empty:
        ax[0].scatter(
            sell_signals.index, sell_signals["Close"], label="SELL", color="red", marker="v", s=120, zorder=5
        )

    ax[0].set_title(f"Sentinel: {ticker} Market Analysis (Signals & Performance)", fontsize=14, pad=15)
    ax[0].set_ylabel("Price (USD)", fontsize=11)
    ax[0].grid(True, linestyle=":", alpha=0.3)
    ax[0].legend(loc="upper left", framealpha=0.5)

    table_data = [
        ["Asset Ticker", ticker],
        ["Total Trades", str(metrics.get("total_trades", 0))],
        ["Win Rate", f"%{metrics.get('win_rate', 0.0):.1f}"],
        ["Max Drawdown", f"%{metrics.get('max_drawdown', 0.0):.2f}"],
        ["Net PnL", f"${metrics.get('total_pnl', 0.0):.2f}"],
    ]

    if predictor_metrics and "rmse" in predictor_metrics:
        table_data.append(["Test RMSE", f"${predictor_metrics['rmse']:.2f}"])

    summary_table = ax[0].table(cellText=table_data, cellLoc="center", loc="upper right", bbox=[0.75, 0.50, 0.22, 0.40])
    summary_table.auto_set_font_size(False)
    summary_table.set_fontsize(9)

    for (row, col), cell in summary_table.get_celld().items():
        cell.set_facecolor("#1e1e1e")
        cell.set_text_props(color="white", weight="bold")
        cell.set_edgecolor("#444444")

    if "RSI" in df.columns:
        ax[1].plot(df.index, df["RSI"], color="magenta", linewidth=1.2, label="RSI")
        ax[1].axhline(70, linestyle="--", color="red", alpha=0.6, label="Overbought (70)")
        ax[1].axhline(30, linestyle="--", color="lime", alpha=0.6, label="Oversold (30)")
        ax[1].fill_between(df.index, 70, 30, color="purple", alpha=0.08)
        ax[1].set_ylim(0, 100)
        ax[1].set_ylabel("RSI", fontsize=11)
        ax[1].grid(True, linestyle=":", alpha=0.3)
        ax[1].legend(loc="upper left", framealpha=0.5)

    ax[2].bar(df.index, df["Volume"], color="skyblue", alpha=0.4, width=0.8, label="Volume")

    vol_sma_col = f"Vol_SMA_{window}"
    if vol_sma_col in df.columns:
        ax[2].plot(df.index, df[vol_sma_col], color="orange", linestyle="-.", linewidth=1.2, label=f"Vol SMA {window}")

    ax[2].set_ylabel("Volume", fontsize=11)
    ax[2].grid(True, linestyle=":", alpha=0.3)
    ax[2].legend(loc="upper left", framealpha=0.5)

    if "equity_curve" in metrics and isinstance(metrics["equity_curve"], pd.Series):
        equity = metrics["equity_curve"]
        ax[3].plot(equity.index, equity.values, color="gold", linewidth=1.8, label="Portfolio Equity ($)")
        ax[3].axhline(100, linestyle="--", color="gray", alpha=0.5, label="Initial Capital ($100)")

        ax[3].fill_between(equity.index, equity.values, 100, where=(equity.values >= 100), color="lime", alpha=0.15)
        ax[3].fill_between(equity.index, equity.values, 100, where=(equity.values < 100), color="red", alpha=0.15)

        ax[3].set_ylabel("Equity ($)", fontsize=11)
        ax[3].grid(True, linestyle=":", alpha=0.3)
        ax[3].legend(loc="upper left", framealpha=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Sentinel] Plot saved to {save_path}")

    plt.show()