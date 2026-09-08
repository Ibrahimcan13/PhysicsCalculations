import numpy as np
import pandas as pd


def calculate_backtest_metrics(
        df: pd.DataFrame,
        trade_log: list[dict],
        initial_capital: float,
        equity_series: pd.Series,
) -> dict:
    total_trades = len(trade_log)
    winning_trades = sum(1 for t in trade_log if t["PnL"] > 0)
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

    total_pnl = equity_series.iloc[-1] - initial_capital

    equity_arr = equity_series.to_numpy(dtype=np.float64)
    peak = np.maximum.accumulate(equity_arr)
    drawdown = (equity_arr - peak) / (peak + 1e-9)
    max_drawdown = np.min(drawdown) * 100.0

    daily_returns = np.diff(equity_arr) / (equity_arr[:-1] + 1e-9)
    mean_return = np.mean(daily_returns) if len(daily_returns) > 0 else 0.0
    std_return = np.std(daily_returns) if len(daily_returns) > 0 else 0.0

    sharpe_ratio = (
        (mean_return / (std_return + 1e-9)) * np.sqrt(252) if std_return > 0 else 0.0
    )

    gross_profits = sum(t["PnL"] for t in trade_log if t["PnL"] > 0)
    gross_losses = abs(sum(t["PnL"] for t in trade_log if t["PnL"] < 0))
    profit_factor = (gross_profits / gross_losses) if gross_losses > 0 else 0.0

    avg_duration = (
        sum(t["Duration_Days"] for t in trade_log) / total_trades
        if total_trades > 0 else 0.0
    )

    metrics = {
        "total_pnl": total_pnl,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "max_drawdown": abs(max_drawdown),
        "sharpe_ratio": sharpe_ratio,
        "profit_factor": profit_factor,
        "avg_duration_days": avg_duration,
        "equity_curve": equity_series,
    }

    print(
        f"[Sentinel] Backtest Completed -> Net PnL: ${total_pnl:.2f} | Win Rate: {win_rate:.1f}% | "
        f"Max DD: {abs(max_drawdown):.2f}% | Sharpe: {sharpe_ratio:.2f} | Avg Duration: {avg_duration:.1f} days"
    )

    return metrics


def run_backtest(
        df: pd.DataFrame,
        initial_capital: float = 1000.0,
        risk_per_trade: float = 0.02,
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
            "avg_duration_days": 0.0,
            "equity_curve": pd.Series([initial_capital]),
        }
        return df, [], empty_metrics

    df = df.copy()

    dates = df.index.to_numpy()
    close_arr = df["Close"].to_numpy(dtype=np.float64)
    high_arr = df["High"].to_numpy(dtype=np.float64)
    signal_arr = df["Signal"].to_numpy(dtype=np.int8)

    ai_prob_arr = (
        df["AI_Probability"].to_numpy(dtype=np.float64)
        if "AI_Probability" in df.columns
        else np.full(len(df), np.nan)
    )

    atr_arr = (
        df["ATR"].to_numpy(dtype=np.float64)
        if "ATR" in df.columns
        else np.zeros(len(df), dtype=np.float64)
    )

    cash = initial_capital
    shares = 0.0
    entry_price = 0.0
    entry_cost = 0.0
    entry_date = None
    highest_price_since_entry = 0.0

    trade_log = []
    equity_list = np.zeros(len(df), dtype=np.float64)

    for i in range(len(df)):
        current_date = dates[i]
        current_close = close_arr[i]
        current_high = high_arr[i]
        signal = signal_arr[i]
        ai_prob = ai_prob_arr[i]
        atr_val = atr_arr[i]

        if shares > 0.0:
            highest_price_since_entry = max(highest_price_since_entry, current_high)

            stop_loss_price = (
                highest_price_since_entry - (atr_val * atr_multiplier)
                if use_atr_stop and not np.isnan(atr_val)
                else 0.0
            )

            hit_stop_loss = use_atr_stop and (current_close <= stop_loss_price)
            ai_bearish_exit = (
                    not np.isnan(ai_prob) and (ai_prob < ai_exit_threshold)
            )
            standard_sell_signal = (signal == -1)

            if hit_stop_loss or ai_bearish_exit or standard_sell_signal:
                sell_price = current_close * (1.0 - slippage_rate)
                gross_cash = shares * sell_price
                commission = gross_cash * commission_rate
                net_returned_cash = gross_cash - commission

                pnl = net_returned_cash - entry_cost
                pnl_pct = (pnl / (entry_cost + 1e-9)) * 100.0

                cash += net_returned_cash

                duration_days = (
                    (pd.Timestamp(current_date) - pd.Timestamp(entry_date)).days
                    if entry_date is not None
                    else 0
                )

                reason = "SELL Signal"
                if hit_stop_loss:
                    reason = "ATR Stop Loss"
                elif ai_bearish_exit:
                    reason = "AI Bearish Exit"

                trade_log.append(
                    {
                        "Entry_Date": entry_date,
                        "Exit_Date": current_date,
                        "Entry_Price": entry_price,
                        "Exit_Price": sell_price,
                        "PnL": pnl,
                        "PnL_Pct": pnl_pct,
                        "Duration_Days": duration_days,
                        "Reason": reason,
                    }
                )

                shares = 0.0
                entry_price = 0.0
                entry_cost = 0.0
                entry_date = None
                highest_price_since_entry = 0.0

        elif shares == 0.0 and signal == 1:
            buy_price = current_close * (1.0 + slippage_rate)

            if atr_val > 0.0 and use_atr_stop:
                risk_amount = cash * risk_per_trade
                stop_distance = atr_val * atr_multiplier
                raw_shares = risk_amount / (stop_distance + 1e-9)

                allocated_cash = min(cash * 0.95, raw_shares * buy_price)
            else:
                allocated_cash = cash * 0.10

            commission = allocated_cash * commission_rate
            investable_cash = allocated_cash - commission

            shares = investable_cash / buy_price
            entry_price = buy_price
            entry_cost = allocated_cash
            entry_date = current_date
            highest_price_since_entry = current_close
            cash -= allocated_cash

        equity_list[i] = cash + (shares * current_close if shares > 0.0 else 0.0)

    if shares > 0.0:
        last_close = close_arr[-1]
        sell_price = last_close * (1.0 - slippage_rate)
        gross_cash = shares * sell_price
        commission = gross_cash * commission_rate
        net_returned_cash = gross_cash - commission

        pnl = net_returned_cash - entry_cost
        pnl_pct = (pnl / (entry_cost + 1e-9)) * 100.0

        cash += net_returned_cash
        duration_days = (
            (pd.Timestamp(dates[-1]) - pd.Timestamp(entry_date)).days
            if entry_date is not None
            else len(df)
        )

        trade_log.append(
            {
                "Entry_Date": entry_date,
                "Exit_Date": dates[-1],
                "Entry_Price": entry_price,
                "Exit_Price": sell_price,
                "PnL": pnl,
                "PnL_Pct": pnl_pct,
                "Duration_Days": duration_days,
                "Reason": "End of Data (Auto Close)",
            }
        )
        shares = 0.0
        equity_list[-1] = cash
        print(
            f"[Sentinel] Auto-closed open position at last available price: ${last_close:.2f} (PnL: ${pnl:.2f})"
        )

    equity_series = pd.Series(equity_list, index=df.index)
    df["Portfolio_Equity"] = equity_series

    metrics = calculate_backtest_metrics(
        df, trade_log, initial_capital, equity_series
    )

    return df, trade_log, metrics