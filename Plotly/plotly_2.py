import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

np.random.seed(42)
periods = 50
dates = pd.date_range(start="2026-01-01", periods=periods, freq="D")
close_prices = 100 + np.random.randn(periods).cumsum()

df = pd.DataFrame({
    "Open": close_prices + np.random.uniform(-1, 1, periods),
    "High": close_prices + np.random.uniform(1, 3, periods),
    "Low": close_prices - np.random.uniform(1, 3, periods),
    "Close": close_prices,
    "Volume": np.random.randint(1000, 5000, periods),
    "Equity": 10000 + np.cumsum(np.random.randn(periods) * 120)
}, index=dates)

fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.5, 0.25, 0.25],
    subplot_titles=("Price (OHLC)", "Volume Grid", "Portfolio Equity ($)")
)

fig.add_trace(
    go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="OHLC"),
    row=1, col=1
)

vol_colors = ["red" if close < open_p else "lime" for close, open_p in zip(df["Close"], df["Open"])]
fig.add_trace(
    go.Bar(
        x=df.index, y=df["Volume"], name="Volume",
        marker_color=vol_colors, opacity=0.8
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=df.index, y=df["Equity"], mode="lines", name="Equity",
        line=dict(color="springgreen", width=2),
        fill="tozeroy",
        fillcolor="rgba(0, 255, 127, 0.15)"
    ),
    row=3, col=1
)

fig.update_layout(
    height=800,
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    showlegend=False
)

fig.show()