import pandas as pd
import numpy as np
import plotly.graph_objects as go

np.random.seed(42)
dates = pd.date_range(start="2026-01-01", periods=50, freq="D")
close_prices = 100 + np.random.randn(50).cumsum()

df = pd.DataFrame({
    "Open": close_prices + np.random.uniform(-1, 1, 50),
    "High": close_prices + np.random.uniform(1, 3, 50),
    "Low": close_prices - np.random.uniform(1, 3, 50),
    "Close": close_prices,
    "RSI": np.random.uniform(25, 75, 50),
    "AI_Prob": np.random.uniform(0.45, 0.95, 50)
}, index=dates)

df["SMA_10"] = df["Close"].rolling(window=10).mean()

buy_signals = df.iloc[[12, 28]]
sell_signals = df.iloc[[20, 42]]

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="OHLC",
    text=[f"RSI: {rsi:.1f}<br>AI Prob: %{prob*100:.1f}" for rsi, prob in zip(df["RSI"], df["AI_Prob"])],
    hovertemplate="<b>Date</b>: %{x|%Y-%m-%d}<br>" +
                  "<b>Open</b>: $%{open:.2f}<br>" +
                  "<b>High</b>: $%{high:.2f}<br>" +
                  "<b>Low</b>: $%{low:.2f}<br>" +
                  "<b>Close</b>: $%{close:.2f}<br>" +
                  "<b>%{text}</b><extra></extra>"
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["SMA_10"],
    mode="lines",
    name="SMA 10",
    line=dict(color="gold", width=1.5, dash="dash"),
    hovertemplate="<b>SMA 10</b>: $%{y:.2f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=buy_signals.index,
    y=buy_signals["Low"] - 2,
    mode="markers",
    name="BUY Signal",
    marker=dict(symbol="triangle-up", size=13, color="lime"),
    hovertemplate="<b>BUY SIGNAL</b><br>Date: %{x|%Y-%m-%d}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=sell_signals.index,
    y=sell_signals["High"] + 2,
    mode="markers",
    name="SELL Signal",
    marker=dict(symbol="triangle-down", size=13, color="red"),
    hovertemplate="<b>SELL SIGNAL</b><br>Date: %{x|%Y-%m-%d}<extra></extra>"
))

fig.update_layout(
    title="Sentinel: Day 1 Complete Interactive Baseline",
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    xaxis_rangeslider_visible=False,
    hovermode="x unified"
)

fig.show()