import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

total_entries = len(df)

# --------------------------------
# 1. Unique Artist Count
# --------------------------------

unique_artist_count = df["artist"].nunique()

# --------------------------------
# 2. Diversity Score
# --------------------------------

diversity_score = unique_artist_count / total_entries

# --------------------------------
# 3. Artist Concentration Index
# --------------------------------

artist_counts = df["artist"].value_counts()

artist_shares = artist_counts / total_entries

artist_concentration_index = (artist_shares ** 2).sum()

# --------------------------------
# 4. Top 5 Artist Share
# --------------------------------

top5_artist_share = (
    artist_counts.head(5).sum() / total_entries
)

# --------------------------------
# 5. Collaboration Ratio
# --------------------------------

collab_pattern = r"&|\bfeat\.?\b|\bfeaturing\b|\bwith\b|,|\bx\b"

df["is_collaboration"] = df["artist"].str.contains(
    collab_pattern,
    case=False,
    regex=True
)

collaboration_ratio = df["is_collaboration"].mean()

# --------------------------------
# 6. Explicit Content Share
# --------------------------------

df["is_explicit"] = (
    df["is_explicit"]
    .astype(str)
    .str.lower()
    .map({
        "true": True,
        "false": False
    })
)

explicit_share = df["is_explicit"].mean()

# --------------------------------
# 7. Single vs Album Ratio
# --------------------------------

album_ratio = (
    df["album_type"]
    .value_counts(normalize=True)
    * 100
)

# --------------------------------
# 8. Content Variety Index
# --------------------------------

unique_songs = df["song"].nunique()
unique_albums = df["album_type"].nunique()
unique_artists = df["artist"].nunique()

content_variety_index = (
    unique_songs + unique_artists
) / total_entries

# --------------------------------
# 9. Display KPI Summary
# --------------------------------

print("\n" + "=" * 50)
print("       UK TOP 50 MARKET STRUCTURE KPIs")
print("=" * 50)

print(f"\nTotal Playlist Entries       : {total_entries:,}")
print(f"Unique Artist Count         : {unique_artist_count:,}")

print(
    f"Artist Concentration Index  : "
    f"{artist_concentration_index:.4f}"
)

print(
    f"Top 5 Artist Share          : "
    f"{top5_artist_share * 100:.2f}%"
)

print(
    f"Diversity Score             : "
    f"{diversity_score:.4f}"
)

print(
    f"Collaboration Ratio         : "
    f"{collaboration_ratio * 100:.2f}%"
)

print(
    f"Explicit Content Share      : "
    f"{explicit_share * 100:.2f}%"
)

print("\nSingle vs Album:")
print(album_ratio)

print(
    f"\nContent Variety Index       : "
    f"{content_variety_index:.4f}"
)

print("\n" + "=" * 50)

# --------------------------------
# 10. Save KPI summary
# --------------------------------

kpi_summary = pd.DataFrame({
    "KPI": [
        "Unique Artist Count",
        "Artist Concentration Index",
        "Top 5 Artist Share",
        "Diversity Score",
        "Collaboration Ratio",
        "Explicit Content Share",
        "Content Variety Index"
    ],
    "Value": [
        unique_artist_count,
        artist_concentration_index,
        top5_artist_share,
        diversity_score,
        collaboration_ratio,
        explicit_share,
        content_variety_index
    ]
})

kpi_summary.to_csv(
    "reports/market_structure_kpis.csv",
    index=False
)

print("\nMarket structure analysis completed successfully!")