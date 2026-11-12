import pandas as pd
import numpy as np

# Simulated messy "vendor" price data
df = pd.DataFrame({
    "date": ["2026-01-02", "2026-01-02", "2026-01-03", "2026-01-04", "not a date", "2026-01-06"],
    "ticker": ["AAA", "AAA", "bbb", "AAA", "BBB", "AAA "],
    "price": [10.5, 10.5, 20.1, -5.0, 19.8, 1000.0],
})

# Clean
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["ticker"] = df["ticker"].str.strip().str.upper()
before = len(df)
df = df.drop_duplicates()

# Validate
issues = {
    "invalid_dates": int(df["date"].isna().sum()),
    "non_positive_prices": int((df["price"] <= 0).sum()),
    "price_outliers": int(
        (np.abs(df["price"] - df["price"].median()) > 5 * df["price"].std()).sum()
    ),
    "duplicates_removed": before - len(df),
}

clean = df.dropna(subset=["date"]).query("price > 0")
print(issues)
print(clean)
