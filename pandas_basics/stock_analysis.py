import pandas as pd

stock_data = {
    "Stock": ["ASELS", "THYAO", "EREGL"],
    "Price": [65.40, 310.25, 45.10],
    "Volume": [100, 50, 200]
}

df = pd.DataFrame(stock_data)

df["State"] = ["Buy", "Sell", "Stay still"]

print("STOCK TRACKING TABLE")
print(df)

print("\n DATA INFO")
df.info()

print("\n STATISTICAL SUMMARY")
print(df.describe(percentiles=[0.3, 0.5, 0.8]))