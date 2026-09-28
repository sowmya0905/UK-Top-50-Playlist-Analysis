import pandas as pd
import re

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# Make sure artist column is text
df["artist"] = df["artist"].astype(str).str.strip()

# Collaboration indicators
collab_pattern = r"&|\bfeat\.?\b|\bfeaturing\b|\bwith\b|,|\bx\b"

df["is_collaboration"] = df["artist"].str.contains(
    collab_pattern,
    case=False,
    regex=True
)

# Count artists in each track
def count_artists(artist_text):
    parts = re.split(collab_pattern, artist_text, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]
    return len(parts)

df["artist_count"] = df["artist"].apply(count_artists)

# --------------------------------
# Overall collaboration metrics
# --------------------------------

total_tracks = len(df)
collaborative_tracks = df["is_collaboration"].sum()
solo_tracks = total_tracks - collaborative_tracks

collaboration_ratio = collaborative_tracks / total_tracks

average_artists = df["artist_count"].mean()

print("\n===== COLLABORATION ANALYSIS =====")
print("Total Playlist Entries:", total_tracks)
print("Solo Entries:", solo_tracks)
print("Collaborative Entries:", collaborative_tracks)
print("Collaboration Ratio:", round(collaboration_ratio * 100, 2), "%")
print("Average Artists per Track:", round(average_artists, 2))

# --------------------------------
# Collaboration by rank group
# --------------------------------

df["rank_group"] = pd.cut(
    df["position"],
    bins=[0, 10, 50],
    labels=["Top 10", "11-50"]
)

rank_collaboration = (
    df.groupby("rank_group", observed=False)["is_collaboration"]
    .mean()
    .reset_index()
)

rank_collaboration["collaboration_percentage"] = (
    rank_collaboration["is_collaboration"] * 100
)

print("\n===== COLLABORATION BY RANK =====")
print(
    rank_collaboration[
        ["rank_group", "collaboration_percentage"]
    ].to_string(index=False)
)

# --------------------------------
# Save results
# --------------------------------

df.to_csv(
    "data/UK_Top50_Collaboration_Analysis.csv",
    index=False
)

rank_collaboration.to_csv(
    "reports/collaboration_by_rank.csv",
    index=False
)

print("\nCollaboration analysis completed successfully!")