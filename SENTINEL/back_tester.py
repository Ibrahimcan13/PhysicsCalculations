import numpy as np
import pandas as pd


def run_backtest(
    df: pd.DataFrame,
    initial_capital: float = 100.0,
    commission_rate: float = 0.001,
    slippage_rate: float = 0.0005,
    use_atr_stop: bool = True,
    atr_multiplier: float = 2.0,
    ai_exit_threshold: float = 0.50,
) -> tuple[pd.DataFrame, list[dict], dict]:
    if df.empty or "Signal" not in df.columns:
        print("[Warning] DataFrame is empty or missing 'Signal' column.")
        empty_metrics = {
            "total_pnl": 0.0,
            "win_rate": 0.0,
            "total_trades": 0,
            "winning_trades": 0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
            "profit_factor": 0.0,
            "equity_curve": pd.Series([initial_capital]),
        }
        return df, [], empty_metrics

    df = df.copy()

    cash = initial_capital
    shares = 0.0
    entry_price = 0.0
    highest_price_since_entry = 0.0

    trade_log = []
    equity_list = []

    for i in range(len(df)):
        current_date = df.index[i]
        current_close = df["Close"].iloc[i]
        current_high = df["High"].iloc[i]
        signal = df["Signal"].iloc[i]
        ai_prob = (
            df["AI_Probability"].iloc[i]
            if "AI_Probability" in df.columns
            else None
        )
        atr_val = df["ATR"].iloc[i] if "ATR" in df.columns else 0.0

        if shares > 0.0:
            highest_price_since_entry = max(
                highest_price_since_entry, current_high
            )

            stop_loss_price = (
                highest_price_since_entry - (atr_val * atr_multiplier)
                if use_atr_stop and not np.isnan(atr_val)
                else 0.0
            )

            hit_stop_loss = use_atr_stop and (
                current_close <= stop_loss_price
            )
            ai_bearish_exit = (
                ai_prob is not None
                and not np.isnan(ai_prob)
                and (ai_prob < ai_exit_threshold)
            )
            standard_sell_signal = signal == "SELL"

            if hit_stop_loss or ai_bearish_exit or standard_sell_signal:
                sell_price = current_close * (1 - slippage_rate)
                gross_cash = shares * sell_price
                commission = gross_cash * commission_rate
                net_cash = gross_cash - commission

                pnl = net_cash - (shares * entry_price)
                pnl_pct = (pnl / (shares * entry_price)) * 100

                cash = net_cash

                reason = "SELL Signal"
                if hit_stop_loss:
                    reason = "ATR Stop Loss"
                elif ai_bearish_exit:
                    reason = "AI Bearish Exit"

                trade_log.append(
                    {
                        "Exit_Date": current_date,
                        "Entry_Price": entry_price,
                        "Exit_Price": sell_price,
                        "PnL": pnl,
                        "PnL_Pct": pnl_pct,
                        "Reason": reason,
                    }
                )

                shares = 0.0
                entry_price = 0.0
                highest_price_since_entry = 0.0

        elif shares == 0.0 and signal == "BUY":
            buy_price = current_close * (1 + slippage_rate)
            commission = cash * commission_rate
            investable_cash = cash - commission

            shares = investable_cash / buy_price
            entry_price = buy_price
            highest_price_since_entry = current_close
            cash = 0.0

        current_equity = cash + (
            shares * current_close if shares > 0.0 else 0.0
        )
        equity_list.append(current_equity)

    if shares > 0.0:
        last_close = df["Close"].iloc[-1]
        sell_price = last_close * (1 - slippage_rate)
        gross_cash = shares * sell_price
        commission = gross_cash * commission_rate
        cash = gross_cash - commission

        pnl = cash - (shares * entry_price)
        pnl_pct = (pnl / (shares * entry_price)) * 100

        trade_log.append(
            {
                "Exit_Date": df.index[-1],
                "Entry_Price": entry_price,
                "Exit_Price": sell_price,
                "PnL": pnl,
                "PnL_Pct": pnl_pct,
                "Reason": "End of Data (Auto Close)",
            }
        )
        shares = 0.0
        equity_list[-1] = cash
        print(
            f"[Sentinel] Auto-closed open BUY position at last available close price: ${last_close:.2f} (PnL: ${pnl:.2f})"
        )

    equity_series = pd.Series(equity_list, index=df.index)
    df["Portfolio_Equity"] = equity_series

    metrics = calculate_backtest_metrics(
        df, trade_log, initial_capital, equity_series
    )

    return df, trade_log, metrics


def calculate_backtest_metrics(
    df: pd.DataFrame,
    trade_log: list[dict],
    initial_capital: float,
    equity_series: pd.Series,
) -> dict:
    total_trades = len(trade_log)
    winning_trades = sum(1 for t in trade_log if t["PnL"] > 0)
    win_rate = (
        (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
    )

    total_pnl = equity_series.iloc[-1] - initial_capital

    peak = equity_series.cummax()
    drawdown = (equity_series - peak) / peak
    max_drawdown = drawdown.min() * 100

    daily_returns = equity_series.pct_change().dropna()
    mean_return = daily_returns.mean()
    std_return = daily_returns.std()

    sharpe_ratio = (
        (mean_return / std_return) * np.sqrt(252) if std_return > 0 else 0.0
    )

    gross_profits = sum(t["PnL"] for t in trade_log if t["PnL"] > 0)
    gross_losses = abs(sum(t["PnL"] for t in trade_log if t["PnL"] < 0))
    profit_factor = (
        (gross_profits / gross_losses) if gross_losses > 0 else 0.0
    )

    metrics = {
        "total_pnl": total_pnl,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "max_drawdown": abs(max_drawdown),
        "sharpe_ratio": sharpe_ratio,
        "profit_factor": profit_factor,
        "equity_curve": equity_series,
    }

    print(
        f"[Sentinel] Backtest Completed -> Net PnL: ${total_pnl:.2f} | Win Rate: {win_rate:.1f}% | "
        f"Max DD: {abs(max_drawdown):.2f}% | Sharpe: {sharpe_ratio:.2f}"
    )

    return metrics