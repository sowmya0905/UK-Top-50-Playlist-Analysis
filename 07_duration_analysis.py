import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# Convert duration from milliseconds to minutes
df["duration_minutes"] = df["duration_ms"] / 60000

# --------------------------------
# 1. Duration statistics
# --------------------------------

duration_stats = df["duration_minutes"].describe()

print("\n===== TRACK DURATION STATISTICS =====")
print(duration_stats)

# --------------------------------
# 2. Short / Medium / Long tracks
# --------------------------------

def duration_category(minutes):
    if minutes < 2.5:
        return "Short (<2.5 min)"
    elif minutes <= 4:
        return "Medium (2.5-4 min)"
    else:
        return "Long (>4 min)"

df["duration_category"] = df["duration_minutes"].apply(
    duration_category
)

duration_distribution = (
    df["duration_category"]
    .value_counts()
    .reset_index()
)

duration_distribution.columns = [
    "duration_category",
    "track_count"
]

duration_distribution["percentage"] = (
    duration_distribution["track_count"]
    / len(df) * 100
)

print("\n===== DURATION CATEGORY =====")
print(duration_distribution.to_string(index=False))

# --------------------------------
# 3. Duration vs Popularity
# --------------------------------

duration_popularity = (
    df.groupby("duration_category")["popularity"]
    .agg(["mean", "median"])
    .reset_index()
)

print("\n===== DURATION VS POPULARITY =====")
print(duration_popularity.to_string(index=False))

# --------------------------------
# 4. Correlation
# --------------------------------

correlation = df[
    ["duration_minutes", "popularity"]
].corr().iloc[0, 1]

print(
    "\nDuration-Popularity Correlation:",
    round(correlation, 4)
)

# --------------------------------
# 5. Save results
# --------------------------------

duration_distribution.to_csv(
    "reports/duration_distribution.csv",
    index=False
)

duration_popularity.to_csv(
    "reports/duration_vs_popularity.csv",
    index=False
)

# Save updated dataset
df.to_csv(
    "data/UK_Top50_Duration_Analysis.csv",
    index=False
)

print("\nDuration analysis completed successfully!")