import pandas as pd
import numpy as np

data = {
    "Stock": ["ASELS", "THYAO", "EREGL", "GARAN", "TUPRS", "SISE"],
    "Price": [65.4, 310.2, 45.1, 88.5, 195.0, 42.3],
    "Volume": [1000, 500, 2000, 1500, 800, 1200],
    "Change": [1.2, -0.5, 2.1, 0.8, -1.2, 0.5],
    "PE_Ratio": [12.5, 8.2, 10.1, 6.5, 15.2, 9.8],
    "Market_Cap": [50000, 120000, 45000, 90000, 110000, 60000]
}

df = pd.DataFrame(data)
df["State"] = ["Buy", "Sell", "Hold", "Buy", "Sell", "Hold"]

average_price = df["Price"].mean()

print("FULL PORTFOLIO TABLE")
print(df)

print("\n STATISTICAL SUMMARY ")
print(df.describe(percentiles=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]))