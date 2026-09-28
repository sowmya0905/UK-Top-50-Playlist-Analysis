import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# --------------------------------
# 1. Album type distribution
# --------------------------------

album_counts = (
    df["album_type"]
    .value_counts()
    .reset_index()
)

album_counts.columns = ["album_type", "track_count"]

album_counts["percentage"] = (
    album_counts["track_count"] / len(df) * 100
)

print("\n===== ALBUM TYPE DISTRIBUTION =====")
print(album_counts.to_string(index=False))

# --------------------------------
# 2. Average album size
# --------------------------------

album_size = (
    df.groupby("album_type")["total_tracks"]
    .agg(["count", "mean", "median", "min", "max"])
    .reset_index()
)

print("\n===== ALBUM SIZE ANALYSIS =====")
print(album_size.to_string(index=False))

# --------------------------------
# 3. Album type by playlist rank
# --------------------------------

df["rank_group"] = pd.cut(
    df["position"],
    bins=[0, 10, 20, 30, 40, 50],
    labels=[
        "Top 10",
        "11-20",
        "21-30",
        "31-40",
        "41-50"
    ]
)

rank_album = (
    df.groupby(
        ["rank_group", "album_type"],
        observed=False
    )
    .size()
    .reset_index(name="track_count")
)

print("\n===== ALBUM TYPE BY RANK =====")
print(rank_album.to_string(index=False))

# --------------------------------
# 4. Popularity by album type
# --------------------------------

popularity_album = (
    df.groupby("album_type")["popularity"]
    .agg(["mean", "median"])
    .reset_index()
)

print("\n===== POPULARITY BY ALBUM TYPE =====")
print(popularity_album.to_string(index=False))

# --------------------------------
# 5. Save results
# --------------------------------

album_counts.to_csv(
    "reports/album_type_distribution.csv",
    index=False
)

album_size.to_csv(
    "reports/album_size_analysis.csv",
    index=False
)

rank_album.to_csv(
    "reports/album_type_by_rank.csv",
    index=False
)

popularity_album.to_csv(
    "reports/popularity_by_album_type.csv",
    index=False
)

print("\nAlbum analysis completed successfully!")