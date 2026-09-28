import pandas as pd

# Load dataset
df = pd.read_csv("data/Atlantic_United_Kingdom.csv")

print("Original Shape:", df.shape)

# -----------------------------
# 1. Convert date column
# -----------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -----------------------------
# 2. Clean text columns
# -----------------------------
text_columns = ["song", "artist", "album_type"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# -----------------------------
# 3. Standardize album type
# -----------------------------
df["album_type"] = df["album_type"].str.title()

# -----------------------------
# 4. Standardize explicit column
# -----------------------------
df["is_explicit"] = df["is_explicit"].astype(bool)

# -----------------------------
# 5. Remove exact duplicates
# -----------------------------
duplicate_count = df.duplicated().sum()

print("Duplicate rows found:", duplicate_count)

df = df.drop_duplicates().reset_index(drop=True)

# -----------------------------
# 6. Check missing values
# -----------------------------
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# -----------------------------
# 7. Check date range
# -----------------------------
print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

# -----------------------------
# 8. Check playlist positions
# -----------------------------
print("\nPosition Range:")
print(df["position"].min(), "to", df["position"].max())

# -----------------------------
# 9. Final shape
# -----------------------------
print("\nCleaned Shape:", df.shape)

# -----------------------------
# 10. Save cleaned dataset
# -----------------------------
df.to_csv("data/UK_Top50_Cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")