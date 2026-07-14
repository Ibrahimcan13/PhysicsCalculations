import pandas as pd

data = {
    "Symbol": ["ASELS", "THYAO", "EREGL", "GARAN", "TUPRS", "SISE"],
    "Price": [65.4, 310.2, 30.8, 88.5, 195.0, 39.3]
}

df = pd.DataFrame(data)

average_price = df["Price"].mean()

undervalued_stocks = df[df["Price"] < average_price]
overvalued_stocks = df[df["Price"] > average_price]

safe_undervalued = df[(df["Price"] < average_price) & (df["Price"] > 40.0)]

df["Expected_Price"] = (df["Price"] * 1.05).round(2)

def decide_action(price):
    if price < 50:
        return "Strong Buy"
    elif price > 150:
        return "Sell"
    else:
        return "Hold"

df["Action"] = df["Price"].apply(decide_action)

print("\n Market Analysis with Decision Logic ")
print(df[["Symbol", "Price", "Expected_Price", "Action"]])

print(f"\n Market Average Price: {average_price:.2f}")

print("\nStocks below average (Undervalued candidate pool):")
print(undervalued_stocks)

print("\nSafe Undervalued Stocks (Price between 40 and Average):")
print(safe_undervalued)

print("\nStocks above average (Overvalued candidate pool):")
print(overvalued_stocks)