import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


np.random.seed(42)
periods = 60
dates = pd.date_range(start="2026-01-01", periods=periods, freq="D")
close_prices = 100 + np.random.randn(periods).cumsum()

df = pd.DataFrame({
    "Open": close_prices + np.random.uniform(-1, 1, periods),
    "High": close_prices + np.random.uniform(1, 3, periods),
    "Low": close_prices - np.random.uniform(1, 3, periods),
    "Close": close_prices,
    "Volume": np.random.randint(1000, 5000, periods),
    "RSI": np.random.uniform(20, 80, periods),
    "Z_Score": np.random.uniform(-2.5, 2.5, periods),
    "Equity": 10000 + np.cumsum(np.random.randn(periods) * 150)
}, index=dates)

df["SMA_10"] = df["Close"].rolling(window=10).mean()

buy_signals = df.iloc[[12, 28, 45]]
sell_signals = df.iloc[[20, 38, 52]]

fig = make_subplots(
    rows=5, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    row_heights=[0.38, 0.15, 0.15, 0.15, 0.17],
    subplot_titles=(
        "Panel 1: Main Price & Signal Overlays",
        "Panel 2: Volume Grid",
        "Panel 3: RSI Momentum",
        "Panel 4: Z-Score / Kalman Spread",
        "Panel 5: Portfolio Equity ($)"
    )
)

fig.add_trace(
    go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="OHLC"),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=df.index, y=df["SMA_10"], mode="lines", name="SMA 10", line=dict(color="gold", width=1.5)),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=buy_signals.index, y=buy_signals["Low"] - 2, mode="markers", name="BUY",
        marker=dict(symbol="triangle-up", size=12, color="lime"),
        hovertemplate="<b>BUY SIGNAL</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>"
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=sell_signals.index, y=sell_signals["High"] + 2, mode="markers", name="SELL",
        marker=dict(symbol="triangle-down", size=12, color="red"),
        hovertemplate="<b>SELL SIGNAL</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>"
    ),
    row=1, col=1
)

vol_colors = ["red" if c < o else "lime" for c, o in zip(df["Close"], df["Open"])]
fig.add_trace(
    go.Bar(x=df.index, y=df["Volume"], name="Volume", marker_color=vol_colors, opacity=0.75),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI", line=dict(color="magenta", width=1.5)),
    row=3, col=1
)
fig.add_hline(y=70, line=dict(color="red", dash="dash", width=1), row=3, col=1)
fig.add_hline(y=30, line=dict(color="lime", dash="dash", width=1), row=3, col=1)

fig.add_trace(
    go.Scatter(x=df.index, y=df["Z_Score"], mode="lines", name="Z-Score", line=dict(color="cyan", width=1.5)),
    row=4, col=1
)
fig.add_hline(y=2.0, line=dict(color="red", dash="dot", width=1), row=4, col=1)
fig.add_hline(y=-2.0, line=dict(color="lime", dash="dot", width=1), row=4, col=1)

fig.add_trace(
    go.Scatter(
        x=df.index, y=df["Equity"], mode="lines", name="Equity",
        line=dict(color="springgreen", width=2),
        fill="tozeroy",
        fillcolor="rgba(0, 255, 127, 0.12)"
    ),
    row=5, col=1
)

fig.update_layout(
    height=950,
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    showlegend=False
)

output_path = "learning_report.html"
fig.write_html(output_path, auto_open=True)

print(f"[SUCCESS] Interactive report generated: {os.path.abspath(output_path)}")