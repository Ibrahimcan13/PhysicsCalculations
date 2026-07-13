import pandas as pd

data = {
    "Stock": ["ASELS", "THYAO", "EREGL", "GARAN", "TUPRS", "SISE"],
    "Price": [65.4, 310.2, 45.1, 88.5, 195.0, 42.3]
}

df = pd.DataFrame(data)

average_price = df["Price"].mean()

cheapest_index = df["Price"].idxmin()
cheapest_stock = df.loc[cheapest_index, "Stock"]

most_expensive_index = df["Price"].idxmax()
most_expensive_stock = df.loc[most_expensive_index, "Stock"]

df["Purchase"] = (df["Price"] * 1.07).round(2)
df["Sale"] = (df["Purchase"] * 0.93).round(2)

print(f"Market Average Price: {average_price:.2f}")

print(f"Cheapest Stock: {cheapest_stock}")
print(f" The Most Expensive Stock: {most_expensive_stock}")

print("\n PRICE LIST WITH FEES")
print(df[["Stock", "Price", "Purchase", "Sale"]])