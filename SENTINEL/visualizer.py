import matplotlib.pyplot as plt
import pandas as pd


def plot_signals(
        df: pd.DataFrame,
        ticker: str,
        window: int,
        metrics: dict,
        trade_log: list = None,
        train_window: int = 200,
        save_path: str = None
) -> None:

    plt.style.use("dark_background")

    fig, ax = plt.subplots(
        5, 1,
        figsize=(14, 16),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1.2, 1, 1, 1.2]}
    )

    if "Close" in df.columns:
        ax[0].plot(df.index, df["Close"], label="Price", color="lightgray", alpha=0.8, linewidth=1.5)

    if "Kalman" in df.columns:
        ax[0].plot(df.index, df["Kalman"], label="Kalman Filter (Trend)", color="cyan", linestyle="-", linewidth=1.2, alpha=0.9)

    sma_col = f"SMA_{window}"
    bb_upper_col = f"BB_Upper_{window}"
    bb_lower_col = f"BB_Lower_{window}"

    if sma_col in df.columns:
        ax[0].plot(df.index, df[sma_col], label=f"SMA {window}", color="gold", linestyle="--", linewidth=1.5)

    if bb_upper_col in df.columns and bb_lower_col in df.columns:
        ax[0].plot(df.index, df[bb_upper_col], label="BB Upper", color="purple", linestyle=":", alpha=0.7)
        ax[0].plot(df.index, df[bb_lower_col], label="BB Lower", color="purple", linestyle=":", alpha=0.7)
        ax[0].fill_between(df.index, df[bb_upper_col], df[bb_lower_col], color="cyan", alpha=0.03, label="BB Range")

    buy_signals = df[df["Signal"] == 1] if "Signal" in df.columns else pd.DataFrame()
    sell_signals = df[df["Signal"] == -1] if "Signal" in df.columns else pd.DataFrame()

    if not buy_signals.empty and "Close" in buy_signals.columns:
        ax[0].scatter(buy_signals.index, buy_signals["Close"], label="BUY", color="lime", marker="^", s=120, zorder=5)
        for idx, row in buy_signals.iterrows():
            rsi_val = f"{row['RSI']:.1f}" if "RSI" in row else "N/A"
            ai_val = f"{row['AI_Probability']*100:.1f}%" if "AI_Probability" in row else "N/A"
            ax[0].annotate(
                f"BUY\nRSI:{rsi_val}\nAI:{ai_val}",
                (idx, row["Close"]),
                xytext=(0, -35), textcoords="offset points",
                ha='center', fontsize=7, color='lime',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.6, edgecolor="lime"),
                arrowprops=dict(arrowstyle="->", color="lime", lw=0.8)
            )

    if not sell_signals.empty and "Close" in sell_signals.columns:
        ax[0].scatter(sell_signals.index, sell_signals["Close"], label="SELL", color="red", marker="v", s=120, zorder=5)
        for idx, row in sell_signals.iterrows():
            ax[0].annotate(
                "SELL",
                (idx, row["Close"]),
                xytext=(0, 25), textcoords="offset points",
                ha='center', fontsize=7, color='red',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.6, edgecolor="red"),
                arrowprops=dict(arrowstyle="->", color="red", lw=0.8)
            )

    if trade_log:
        for trade in trade_log:
            exit_reason = trade.get("Reason", trade.get("exit_reason", ""))
            exit_date = trade.get("Exit_Date", trade.get("exit_date"))
            exit_price = trade.get("Exit_Price", trade.get("exit_price"))

            if exit_date and exit_price and "STOP" in str(exit_reason).upper():
                ax[0].scatter(exit_date, exit_price, color="orange", marker="X", s=140, zorder=6, label="Stop-Loss Hit")

    if len(df) > train_window and "Close" in df.columns:
        split_date = df.index[train_window]
        for a in ax:
            a.axvline(split_date, color="yellow", linestyle="--", alpha=0.5, linewidth=1.2)
        ax[0].text(split_date, df["Close"].max(), "  Live Walk-Forward Start", color="yellow", fontsize=9, verticalalignment="top")

    ax[0].set_title(f"Sentinel: {ticker} Market Analysis (AI-Enhanced Signals & Kalman Filter)", fontsize=14, pad=15)
    ax[0].set_ylabel("Price (USD)", fontsize=11)
    ax[0].grid(True, linestyle=":", alpha=0.3)
    ax[0].legend(loc="upper left", framealpha=0.5)

    if "AI_Probability" in df.columns:
        ai_prob = df["AI_Probability"] * 100
        ax[1].plot(df.index, ai_prob, color="cyan", linewidth=1.5, label="AI Bullish Probability (%)")
        ax[1].axhline(50, linestyle="--", color="gray", alpha=0.7, label="Neutral (50%)")
        ax[1].axhline(55, linestyle=":", color="lime", alpha=0.8, label="Buy Threshold (55%)")
        ax[1].fill_between(df.index, ai_prob, 50, where=(ai_prob >= 50), color="lime", alpha=0.15)
        ax[1].fill_between(df.index, ai_prob, 50, where=(ai_prob < 50), color="red", alpha=0.15)
        ax[1].set_ylim(0, 100)
        ax[1].set_ylabel("AI Prob (%)", fontsize=11)
        ax[1].grid(True, linestyle=":", alpha=0.3)
        ax[1].legend(loc="upper left", framealpha=0.5)

    if "RSI" in df.columns:
        ax[2].plot(df.index, df["RSI"], color="magenta", linewidth=1.2, label="RSI")
        ax[2].axhline(70, linestyle="--", color="red", alpha=0.6, label="Overbought (70)")
        ax[2].axhline(30, linestyle="--", color="lime", alpha=0.6, label="Oversold (30)")
        ax[2].fill_between(df.index, 70, 30, color="purple", alpha=0.08)
        ax[2].set_ylim(0, 100)
        ax[2].set_ylabel("RSI", fontsize=11)
        ax[2].grid(True, linestyle=":", alpha=0.3)
        ax[2].legend(loc="upper left", framealpha=0.5)

    if "Volume" in df.columns:
        ax[3].bar(df.index, df["Volume"], color="skyblue", alpha=0.3, width=0.8, label="Volume")
        vol_sma_col = f"Vol_SMA_{window}"
        if vol_sma_col in df.columns:
            ax[3].plot(df.index, df[vol_sma_col], color="orange", linestyle="-.", linewidth=1.2, label=f"Vol SMA {window}")
        ax[3].set_ylabel("Volume", fontsize=11)
        ax[3].grid(True, linestyle=":", alpha=0.3)
        ax[3].legend(loc="upper left", framealpha=0.5)

    if "ATR" in df.columns:
        ax_atr = ax[3].twinx()
        ax_atr.plot(df.index, df["ATR"], color="orange", linewidth=1.2, linestyle=":", label="ATR (Volatility)")
        ax_atr.set_ylabel("ATR ($)", fontsize=10, color="orange")
        ax_atr.tick_params(axis='y', labelcolor="orange")
        ax_atr.legend(loc="upper right", framealpha=0.5)

    if "equity_curve" in metrics and isinstance(metrics["equity_curve"], pd.Series):
        equity = metrics["equity_curve"]
        ax[4].plot(equity.index, equity.values, color="gold", linewidth=1.8, label="Portfolio Equity ($)")
        ax[4].axhline(100, linestyle="--", color="gray", alpha=0.5, label="Initial Capital ($100)")

        peak_idx = equity.idxmax()
        peak_val = equity.max()
        ax[4].scatter(peak_idx, peak_val, color="cyan", s=100, zorder=6, label=f"Peak (${peak_val:.1f})")

        ax[4].fill_between(equity.index, equity.values, 100, where=(equity.values >= 100), color="lime", alpha=0.15)
        ax[4].fill_between(equity.index, equity.values, 100, where=(equity.values < 100), color="red", alpha=0.15)

        sharpe = metrics.get("sharpe_ratio", 0.0)
        max_dd = metrics.get("max_drawdown", 0.0)
        win_rate = metrics.get("win_rate", 0.0)
        total_pnl = metrics.get("total_pnl", 0.0)

        stats_text = (
            f"Net PnL: ${total_pnl:.2f}\n"
            f"Win Rate: %{win_rate:.1f}\n"
            f"Max DD: %{max_dd:.2f}\n"
            f"Sharpe: {sharpe:.2f}"
        )

        ax[4].text(
            0.98, 0.90, stats_text,
            transform=ax[4].transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="black", alpha=0.7, edgecolor="gold")
        )

        ax[4].set_ylabel("Equity ($)", fontsize=11)
        ax[4].grid(True, linestyle=":", alpha=0.3)
        ax[4].legend(loc="upper left", framealpha=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Sentinel] Plot saved to {save_path}")

    plt.show()
    plt.close(fig)