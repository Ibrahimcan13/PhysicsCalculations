import pandas as pd

data = {
    "Symbol": ["ASELS", "THYAO", "EREGL", "GARAN", "TUPRS", "SISE", "PETKM", "AKBNK"],
    "Price": [65.4, 310.2, 30.8, 88.5, 195.0, 39.3, 25.0, 95.0],
    "Sector": ["Tech", "Aviation", "Industrial", "Finance", "Energy", "Glass", "Energy", "Finance"]
}

df = pd.DataFrame(data)

mean_prices = df.groupby("Sector")["Price"].transform("mean")

def advanced_decision(row):
    price = row["Price"]
    mean = row["Sector_Mean"]

    if price < (mean * 0.9):
        return "STRONG BUY"
    elif price > mean:
        return "SELL"
    else:
        return "HOLD"

df["Sector_Mean"] = mean_prices

df["Decision"] = df.apply(advanced_decision, axis=1)

sector_avg = df.groupby("Sector")["Price"].mean()
sector_max = df.groupby("Sector")["Price"].max()

df_sorted = df.sort_values(by="Sector")
print("\n Data Sorted by Sector")
print(df_sorted)

df.to_csv("trading_report.csv", index=False)
print("\n[SUCCESS] Report 'trading_report.csv' has been generated.")

