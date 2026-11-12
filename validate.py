import pandas as pd

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
# IQR method: robust to extreme values, unlike a standard deviation check
q1, q3 = df["price"].quantile([0.25, 0.75])
iqr = q3 - q1
is_outlier = (df["price"] < q1 - 1.5 * iqr) | (df["price"] > q3 + 1.5 * iqr)

issues = {
    "invalid_dates": int(df["date"].isna().sum()),
    "non_positive_prices": int((df["price"] <= 0).sum()),
    "price_outliers": int(is_outlier.sum()),
    "duplicates_removed": before - len(df),
}

# Keep only valid rows
clean = df.dropna(subset=["date"]).query("price > 0")
clean = clean[~is_outlier.loc[clean.index]]

print(issues)
print(clean)
