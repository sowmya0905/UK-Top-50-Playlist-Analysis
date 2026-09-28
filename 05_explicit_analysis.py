import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# Convert explicit column safely
df["is_explicit"] = df["is_explicit"].astype(str).str.lower().map({
    "true": True,
    "false": False
})

# --------------------------------
# 1. Explicit vs Clean
# --------------------------------

content_counts = (
    df["is_explicit"]
    .value_counts()
    .reset_index()
)

content_counts.columns = ["is_explicit", "track_count"]

content_counts["percentage"] = (
    content_counts["track_count"] / len(df) * 100
)

print("\n===== EXPLICIT CONTENT =====")
print(content_counts.to_string(index=False))

# --------------------------------
# 2. Explicit share
# --------------------------------

explicit_share = df["is_explicit"].mean() * 100

print(
    "\nExplicit Content Share:",
    round(explicit_share, 2),
    "%"
)

# --------------------------------
# 3. Explicit content by rank
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

rank_explicit = (
    df.groupby("rank_group", observed=False)["is_explicit"]
    .mean()
    .reset_index()
)

rank_explicit["explicit_percentage"] = (
    rank_explicit["is_explicit"] * 100
)

print("\n===== EXPLICIT CONTENT BY RANK =====")
print(
    rank_explicit[
        ["rank_group", "explicit_percentage"]
    ].to_string(index=False)
)

# --------------------------------
# 4. Explicit content by album type
# --------------------------------

album_explicit = (
    df.groupby("album_type")["is_explicit"]
    .mean()
    .reset_index()
)

album_explicit["explicit_percentage"] = (
    album_explicit["is_explicit"] * 100
)

print("\n===== EXPLICIT CONTENT BY ALBUM TYPE =====")
print(
    album_explicit[
        ["album_type", "explicit_percentage"]
    ].to_string(index=False)
)

# --------------------------------
# 5. Save results
# --------------------------------

content_counts.to_csv(
    "reports/explicit_content_summary.csv",
    index=False
)

rank_explicit.to_csv(
    "reports/explicit_by_rank.csv",
    index=False
)

album_explicit.to_csv(
    "reports/explicit_by_album_type.csv",
    index=False
)

print("\nExplicit content analysis completed successfully!")