import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# -----------------------------
# 1. Basic artist analysis
# -----------------------------

# Number of unique artists
unique_artists = df["artist"].nunique()

# Total playlist entries
total_entries = len(df)

# Artist appearance count
artist_counts = (
    df["artist"]
    .value_counts()
    .reset_index()
)

artist_counts.columns = ["artist", "appearances"]

# -----------------------------
# 2. Top 20 dominating artists
# -----------------------------

top_artists = artist_counts.head(20)

print("\n===== TOP 20 ARTISTS =====")
print(top_artists.to_string(index=False))

# -----------------------------
# 3. Unique artists per day
# -----------------------------

daily_unique_artists = (
    df.groupby("date")["artist"]
    .nunique()
    .reset_index(name="unique_artists")
)

print("\n===== DAILY ARTIST DIVERSITY =====")
print(daily_unique_artists.head())

print(
    "\nAverage unique artists per day:",
    round(daily_unique_artists["unique_artists"].mean(), 2)
)

# -----------------------------
# 4. Diversity Score
# -----------------------------

diversity_score = unique_artists / total_entries

print("\n===== MARKET DIVERSITY =====")
print("Unique Artist Count:", unique_artists)
print("Total Entries:", total_entries)
print("Diversity Score:", round(diversity_score, 4))

# -----------------------------
# 5. Artist Concentration Index
# -----------------------------

artist_shares = artist_counts["appearances"] / total_entries

artist_concentration_index = (artist_shares ** 2).sum()

print(
    "Artist Concentration Index:",
    round(artist_concentration_index, 4)
)

# -----------------------------
# 6. Top 5 Artist Share
# -----------------------------

top5_share = (
    artist_counts.head(5)["appearances"].sum()
    / total_entries
)

print(
    "Top 5 Artist Share:",
    round(top5_share * 100, 2),
    "%"
)

# -----------------------------
# 7. Save results
# -----------------------------

top_artists.to_csv(
    "reports/top_20_artists.csv",
    index=False
)

daily_unique_artists.to_csv(
    "reports/daily_artist_diversity.csv",
    index=False
)

print("\nArtist analysis completed successfully!")
