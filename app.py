import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import re

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="UK Top 50 Playlist Intelligence",
    page_icon="🎵",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/UK_Top50_Cleaned.csv")

    df["date"] = pd.to_datetime(df["date"])

    df["duration_minutes"] = (
        df["duration_ms"] / 60000
    )

    df["is_explicit"] = (
        df["is_explicit"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )

    return df


df = load_data()

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🎵 UK Top 50 Playlist Intelligence Dashboard")

st.markdown(
    """
    **Artist Dominance | Collaboration | Explicit Content | 
    Album Structure | Track Duration**
    """
)

st.divider()

# =========================================================
# ARTIST NAME NORMALIZATION
# =========================================================

df["artist_normalized"] = (
    df["artist"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Standardize common capitalization differences
df["artist_normalized"] = df["artist_normalized"].str.title()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

# --------------------------------------------------
# Sidebar Dataset Information
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader("📊 Dataset Information")

# Calculate dataset date range
min_date = df["date"].min().date()
max_date = df["date"].max().date()

st.sidebar.metric(
    "Total Records",
    f"{len(df):,}"
)

st.sidebar.metric(
    "Unique Songs",
    f"{df['song'].nunique():,}"
)

st.sidebar.metric(
    "Unique Artists",
    f"{df['artist'].nunique():,}"
)

st.sidebar.write(
    f"📅 **From:** {min_date}"
)

st.sidebar.write(
    f"📅 **To:** {max_date}"
)

# Date filter
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

artists = sorted(df["artist_normalized"].unique())

selected_artists = st.sidebar.multiselect(
    "Artist",
    artists
)

# Solo / Collaboration filter
track_type = st.sidebar.multiselect(
    "Track Type",
    ["Solo", "Collaboration"],
    default=["Solo", "Collaboration"]
)

# Album type filter
album_types = sorted(df["album_type"].unique())

selected_album_types = st.sidebar.multiselect(
    "Album Type",
    album_types,
    default=album_types
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df.copy()

# Date
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= date_range[0])
        &
        (filtered_df["date"].dt.date <= date_range[1])
    ]

# Artist
if selected_artists:
    filtered_df = filtered_df[
        filtered_df["artist_normalized"].isin(selected_artists)
    ]

# Collaboration detection
collab_pattern = r"&|\bfeat\.?\b|\bfeaturing\b|\bwith\b|,|\bx\b"

filtered_df["track_type"] = filtered_df["artist"].str.contains(
    collab_pattern,
    case=False,
    regex=True
).map({
    True: "Collaboration",
    False: "Solo"
})

if track_type:
    filtered_df = filtered_df[
        filtered_df["track_type"].isin(track_type)
    ]

# Album type
if selected_album_types:
    filtered_df = filtered_df[
        filtered_df["album_type"].isin(selected_album_types)
    ]

# Check after all filters
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please change your filters.")
    st.stop()

    # Collaboration Ratio
collaboration_ratio = (
    (filtered_df["track_type"] == "Collaboration").mean()
    if len(filtered_df) > 0 else 0
)

# Explicit Content Share
explicit_content_share = (
    filtered_df["is_explicit"].mean()
    if len(filtered_df) > 0 else 0
)
# =========================================================
# SPLIT COLLABORATING ARTISTS
# =========================================================

def split_artist_names(artist_text):
    return [
        artist.strip()
        for artist in re.split(
            r"&|\bfeat\.?\b|\bfeaturing\b|\bwith\b|,|\bx\b",
            str(artist_text),
            flags=re.IGNORECASE
        )
        if artist.strip()
    ]

artist_analysis_df = filtered_df.copy()

artist_analysis_df["artist_list"] = (
    artist_analysis_df["artist"]
    .apply(split_artist_names)
)

artist_analysis_df = artist_analysis_df.explode(
    "artist_list"
)

artist_analysis_df["artist_analysis"] = (
    artist_analysis_df["artist_list"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

# Average artists per track
artist_count_per_track = (
    filtered_df["artist"]
    .astype(str)
    .str.count(
        r"&|,|\bfeat\.?\b|\bfeaturing\b|\bwith\b|\bx\b"
    )
    + 1
)

average_artists_per_track = artist_count_per_track.mean()
## --------------------------------------------------
# KPI Section
# --------------------------------------------------
unique_artist_count = filtered_df["artist_normalized"].nunique()
total_entries = len(filtered_df)

st.subheader("📌 Key Market KPIs")

total_entries = len(filtered_df)

unique_artists_daily = filtered_df.groupby("date")["artist_normalized"].nunique()

# Artist-level analysis using individual collaborators
artist_counts_all = (
    artist_analysis_df["artist_analysis"]
    .value_counts()
)

# Total individual artist appearances
artist_total_appearances = len(artist_analysis_df)

# Artist Concentration Index
artist_concentration_index = (
    ((artist_counts_all / artist_total_appearances) ** 2).sum()
    if artist_total_appearances > 0 else 0
)

# Top 5 Artist Share
top5_artist_share = (
    artist_counts_all.head(5).sum() / artist_total_appearances
    if artist_total_appearances > 0 else 0
)
unique_artist_count = (
    artist_analysis_df["artist_analysis"].nunique()
)

diversity_score = (
    unique_artist_count / total_entries
) if total_entries > 0 else 0

# Collaboration ratio
collaboration_ratio = (
    filtered_df["track_type"]
    .eq("Collaboration")
    .mean()
)

# Explicit share
explicit_share = (
    filtered_df["is_explicit"]
    .mean()
)

# Content variety
unique_songs = filtered_df["song"].nunique()

content_variety_index = (
    unique_songs + unique_artist_count
) / total_entries

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Unique Artists",
        f"{unique_artist_count:,}"
    )

with col2:
    st.metric(
        "Artist Concentration Index",
        f"{artist_concentration_index:.4f}"
    )

with col3:
    st.metric(
        "Top 5 Artist Share",
        f"{top5_artist_share * 100:.1f}%"
    )

with col4:
    st.metric(
        "Diversity Score",
        f"{diversity_score:.4f}"
    )

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Collaboration Ratio",
        f"{collaboration_ratio * 100:.1f}%"
    )

with col6:
    st.metric(
        "Explicit Content Share",
        f"{explicit_share * 100:.1f}%"
    )

with col7:
    st.metric(
        "Content Variety Index",
        f"{content_variety_index:.4f}"
    )
col8 = st.columns(1)[0]

with col8:
    st.metric(
        "Avg Artists / Track",
        f"{average_artists_per_track:.2f}"
    )
st.divider()

# --------------------------------------------------
# Market Trend Over Time
# --------------------------------------------------

st.subheader("📈 Playlist Market Trend")

daily_metrics = (
    filtered_df
    .groupby("date")
    .agg(
        unique_artists=("artist", "nunique"),
        average_popularity=("popularity", "mean"),
        explicit_share=("is_explicit", "mean")
    )
    .reset_index()
)

daily_metrics["explicit_share"] = (
    daily_metrics["explicit_share"] * 100
)

fig_trend = px.line(
    daily_metrics,
    x="date",
    y="unique_artists",
    title="Unique Artists Over Time",
    labels={
        "date": "Date",
        "unique_artists": "Unique Artists"
    }
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# Average popularity trend
fig_popularity = px.line(
    daily_metrics,
    x="date",
    y="average_popularity",
    title="Average Playlist Popularity Over Time",
    labels={
        "date": "Date",
        "average_popularity": "Average Popularity"
    }
)

st.plotly_chart(
    fig_popularity,
    use_container_width=True
)

# =========================================================
# RANK GROUP ANALYSIS
# =========================================================

st.subheader("📊 Rank Group Analysis")

rank_df = filtered_df.copy()

rank_df["rank_group"] = pd.cut(
    rank_df["position"],
    bins=[0, 10, 20, 30, 40, 50],
    labels=[
        "Top 10",
        "11-20",
        "21-30",
        "31-40",
        "41-50"
    ]
)

rank_analysis = (
    rank_df
    .groupby("rank_group", observed=False)
    .agg(
        tracks=("song", "count"),
        unique_artists=("artist", "nunique"),
        collaboration_rate=(
            "track_type",
            lambda x: (x == "Collaboration").mean() * 100
        ),
        explicit_rate=(
            "is_explicit",
            "mean"
        ),
        average_popularity=(
            "popularity",
            "mean"
        )
    )
    .reset_index()
)

rank_analysis["explicit_rate"] = (
    rank_analysis["explicit_rate"] * 100
)


# Collaboration by rank
fig_rank_collab = px.bar(
    rank_analysis,
    x="rank_group",
    y="collaboration_rate",
    title="Collaboration Rate by Playlist Rank",
    labels={
        "rank_group": "Playlist Rank",
        "collaboration_rate": "Collaboration (%)"
    }
)

st.plotly_chart(
    fig_rank_collab,
    use_container_width=True
)
# Top 10 vs Top 50 collaboration summary
top10_collaboration = (
    rank_df[rank_df["position"] <= 10]["track_type"]
    .eq("Collaboration")
    .mean() * 100
)

top50_collaboration = (
    rank_df["track_type"]
    .eq("Collaboration")
    .mean() * 100
)

col_a, col_b = st.columns(2)

with col_a:
    st.metric(
        "Top 10 Collaboration Rate",
        f"{top10_collaboration:.1f}%"
    )

with col_b:
    st.metric(
        "Top 50 Collaboration Rate",
        f"{top50_collaboration:.1f}%"
    )

# Explicit content by rank
fig_rank_explicit = px.bar(
    rank_analysis,
    x="rank_group",
    y="explicit_rate",
    title="Explicit Content by Playlist Rank",
    labels={
        "rank_group": "Playlist Rank",
        "explicit_rate": "Explicit Content (%)"
    }
)

st.plotly_chart(
    fig_rank_explicit,
    use_container_width=True
)


# Popularity by rank
fig_rank_popularity = px.line(
    rank_analysis,
    x="rank_group",
    y="average_popularity",
    markers=True,
    title="Average Popularity by Playlist Rank",
    labels={
        "rank_group": "Playlist Rank",
        "average_popularity": "Average Popularity"
    }
)

st.plotly_chart(
    fig_rank_popularity,
    use_container_width=True
)


# Detailed table
st.write("### Rank Group Metrics")

display_rank = rank_analysis.copy()

display_rank["collaboration_rate"] = (
    display_rank["collaboration_rate"].round(2)
)

display_rank["explicit_rate"] = (
    display_rank["explicit_rate"].round(2)
)

display_rank["average_popularity"] = (
    display_rank["average_popularity"].round(2)
)

st.dataframe(
    display_rank,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Artist Dominance
# --------------------------------------------------

st.subheader("🏆 Artist Dominance")

# Artist Dominance using individual artists
artist_counts = (
    artist_analysis_df["artist_analysis"]
    .value_counts()
    .head(15)
    .reset_index()
)

artist_counts.columns = ["artist", "appearances"]

artist_counts.columns = [
    "artist",
    "appearances"
]

artist_counts.columns = [
    "artist",
    "appearances"
]

fig_artist = px.bar(
    artist_counts,
    x="appearances",
    y="artist",
    orientation="h",
    title="Top 15 Artists by Playlist Appearances"
)

fig_artist.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig_artist,
    use_container_width=True
)

# =========================================================
# ARTIST DIVERSITY ANALYSIS
# =========================================================

st.subheader("🎤 Artist Diversity Analysis")

# Artist Diversity using individual artists
daily_unique_artists = (
    artist_analysis_df
    .groupby("date")["artist_analysis"]
    .nunique()
    .reset_index(name="unique_artists")
)

daily_total_entries = (
    filtered_df
    .groupby("date")["song"]
    .count()
    .reset_index(name="total_entries")
)

diversity_trend = daily_unique_artists.merge(
    daily_total_entries,
    on="date",
    how="left"
)

# Diversity trend
fig_diversity = px.line(
    diversity_trend,
    x="date",
    y="unique_artists",
    markers=True,
    title="Unique Artists per Playlist Snapshot",
    labels={
        "date": "Date",
        "unique_artists": "Unique Artists"
    }
)

st.plotly_chart(
    fig_diversity,
    use_container_width=True
)


# Top 5 artist concentration using individual artists
top5_df = (
    artist_counts_all
    .head(5)
    .reset_index()
)

top5_df.columns = [
    "artist",
    "appearances"
]

top5_df["share"] = (
    top5_df["appearances"]
    / artist_total_appearances
    * 100
)

fig_top5 = px.bar(
    top5_df,
    x="artist",
    y="share",
    title="Top 5 Artist Concentration",
    labels={
        "artist": "Artist",
        "share": "Share of Playlist Entries (%)"
    },
    text="share"
)

fig_top5.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_top5,
    use_container_width=True
)


# Diversity summary
average_unique_artists = (
    diversity_trend["unique_artists"].mean()
)

st.metric(
    "Average Unique Artists per Snapshot",
    f"{average_unique_artists:.1f}"
)

# --------------------------------------------------
# Album Structure
# --------------------------------------------------

st.subheader("💿 Album Structure")

album_counts = (
    filtered_df["album_type"]
    .value_counts()
    .reset_index()
)

album_counts.columns = [
    "album_type",
    "count"
]

fig_album = px.pie(
    album_counts,
    names="album_type",
    values="count",
    hole=0.45,
    title="Release Format Distribution"
)

st.plotly_chart(
    fig_album,
    use_container_width=True
)

# =========================================================
# RELEASE FORMAT ANALYSIS
# =========================================================

st.subheader("💿 Release Format Analysis")

album_analysis = (
    filtered_df
    .groupby("album_type")
    .agg(
        track_count=("song", "count"),
        average_popularity=("popularity", "mean"),
        average_album_size=("total_tracks", "mean")
    )
    .reset_index()
)

album_analysis["share"] = (
    album_analysis["track_count"]
    / album_analysis["track_count"].sum()
    * 100
)

# Release format share
fig_album_share = px.bar(
    album_analysis,
    x="album_type",
    y="share",
    title="Single vs Album Share",
    labels={
        "album_type": "Release Type",
        "share": "Playlist Share (%)"
    },
    text="share"
)

fig_album_share.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_album_share,
    use_container_width=True
)


# Popularity comparison
fig_album_popularity = px.bar(
    album_analysis,
    x="album_type",
    y="average_popularity",
    title="Average Popularity by Release Type",
    labels={
        "album_type": "Release Type",
        "average_popularity": "Average Popularity"
    },
    text="average_popularity"
)

fig_album_popularity.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_album_popularity,
    use_container_width=True
)


# Album size analysis
fig_album_size = px.bar(
    album_analysis,
    x="album_type",
    y="average_album_size",
    title="Average Number of Tracks per Release Type",
    labels={
        "album_type": "Release Type",
        "average_album_size": "Average Tracks"
    },
    text="average_album_size"
)

fig_album_size.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_album_size,
    use_container_width=True
)


# Detailed table
st.write("### Release Format Metrics")

display_album = album_analysis.copy()

display_album["share"] = display_album["share"].round(2)

display_album["average_popularity"] = (
    display_album["average_popularity"].round(2)
)

display_album["average_album_size"] = (
    display_album["average_album_size"].round(2)
)

st.dataframe(
    display_album,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Explicit Content
# --------------------------------------------------

st.subheader("🔞 Explicit Content")

explicit_rank = (
    filtered_df.groupby(
        pd.cut(
            filtered_df["position"],
            bins=[0, 10, 20, 30, 40, 50],
            labels=[
                "Top 10",
                "11-20",
                "21-30",
                "31-40",
                "41-50"
            ]
        )
    )["is_explicit"]
    .mean()
    .reset_index()
)

explicit_rank["percentage"] = (
    explicit_rank["is_explicit"] * 100
)

fig_explicit = px.bar(
    explicit_rank,
    x="position",
    y="percentage",
    title="Explicit Content Share by Rank Group",
    labels={
        "position": "Rank Group",
        "percentage": "Explicit Share (%)"
    }
)

st.plotly_chart(
    fig_explicit,
    use_container_width=True
)

# --------------------------------------------------
# Duration Analysis
# --------------------------------------------------

st.subheader("⏱️ Track Duration vs Popularity")

fig_duration = px.scatter(
    filtered_df,
    x="duration_minutes",
    y="popularity",
    hover_data=["song", "artist"],
    title="Track Duration vs Popularity",
    labels={
        "duration_minutes": "Duration (minutes)",
        "popularity": "Popularity"
    }
)

st.plotly_chart(
    fig_duration,
    use_container_width=True
)

# =========================================================
# DURATION CATEGORY ANALYSIS
# =========================================================

st.subheader("⏱️ Track Duration Analysis")

duration_df = filtered_df.copy()

duration_df["duration_category"] = pd.cut(
    duration_df["duration_minutes"],
    bins=[0, 2.5, 4, float("inf")],
    labels=[
        "Short (<2.5 min)",
        "Medium (2.5-4 min)",
        "Long (>4 min)"
    ]
)

duration_summary = (
    duration_df
    .groupby("duration_category", observed=False)
    .agg(
        track_count=("song", "count"),
        average_popularity=("popularity", "mean"),
        average_duration=("duration_minutes", "mean")
    )
    .reset_index()
)

duration_summary["share"] = (
    duration_summary["track_count"]
    / duration_summary["track_count"].sum()
    * 100
)

# Duration distribution
fig_duration_distribution = px.bar(
    duration_summary,
    x="duration_category",
    y="share",
    title="Track Duration Distribution",
    labels={
        "duration_category": "Duration Category",
        "share": "Playlist Share (%)"
    },
    text="share"
)

fig_duration_distribution.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_duration_distribution,
    use_container_width=True
)

# Duration vs popularity category comparison
fig_duration_popularity = px.bar(
    duration_summary,
    x="duration_category",
    y="average_popularity",
    title="Average Popularity by Track Duration",
    labels={
        "duration_category": "Duration Category",
        "average_popularity": "Average Popularity"
    },
    text="average_popularity"
)

fig_duration_popularity.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_duration_popularity,
    use_container_width=True
)

# Correlation
duration_correlation = (
    duration_df[
        ["duration_minutes", "popularity"]
    ]
    .corr()
    .iloc[0, 1]
)

st.metric(
    "Duration–Popularity Correlation",
    f"{duration_correlation:.3f}"
)

# Duration metrics table
st.write("### Duration Metrics")

display_duration = duration_summary.copy()

display_duration["share"] = (
    display_duration["share"].round(2)
)

display_duration["average_popularity"] = (
    display_duration["average_popularity"].round(2)
)

display_duration["average_duration"] = (
    display_duration["average_duration"].round(2)
)

st.dataframe(
    display_duration,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# ARTIST COLLABORATION NETWORK
# =========================================================

st.subheader("🤝 Artist Collaboration Network")

import networkx as nx
import re

# Create graph using individual artists
G = nx.Graph()

collab_songs = (
    artist_analysis_df
    .groupby("song")["artist_analysis"]
    .apply(list)
)

for artists_in_song in collab_songs:

    # Remove duplicate artist names within the same song
    artists_in_song = list(set(artists_in_song))

    for artist in artists_in_song:
        G.add_node(artist)

    # Connect artists who appear on the same song
    for i in range(len(artists_in_song)):
        for j in range(i + 1, len(artists_in_song)):

            artist_a = artists_in_song[i]
            artist_b = artists_in_song[j]

            if G.has_edge(artist_a, artist_b):
                G[artist_a][artist_b]["weight"] += 1
            else:
                G.add_edge(
                    artist_a,
                    artist_b,
                    weight=1
                )

# Keep stronger/repeated collaborations
network_edges = [
    (a, b, data)
    for a, b, data in G.edges(data=True)
    if data["weight"] >= 2
]


if network_edges:

    # Create smaller graph for visualization
    network_graph = nx.Graph()

    for artist_a, artist_b, data in network_edges:

        network_graph.add_edge(
            artist_a,
            artist_b,
            weight=data["weight"]
        )


    # Limit to most connected artists
    degree_sorted = sorted(
        network_graph.degree(),
        key=lambda x: x[1],
        reverse=True
    )

    top_network_artists = [
        artist
        for artist, degree in degree_sorted[:30]
    ]

    network_graph = network_graph.subgraph(
        top_network_artists
    ).copy()


    # Network layout
    pos = nx.spring_layout(
        network_graph,
        seed=42,
        k=1.5
    )


    # Edge traces
    edge_x = []
    edge_y = []

    for artist_a, artist_b in network_graph.edges():

        x0, y0 = pos[artist_a]
        x1, y1 = pos[artist_b]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])


    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1),
        hoverinfo="none",
        mode="lines"
    )


    # Node traces
    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for artist in network_graph.nodes():

        x, y = pos[artist]

        node_x.append(x)
        node_y.append(y)

        connections = network_graph.degree(artist)

        node_size.append(
            10 + connections * 3
        )

        node_text.append(
            f"{artist}<br>"
            f"Connections: {connections}"
        )


    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(network_graph.nodes()),
        textposition="top center",
        hovertext=node_text,
        hoverinfo="text",
        marker=dict(
            size=node_size,
            line=dict(width=1)
        )
    )


    fig_network = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )


    fig_network.update_layout(
        title="Artist Collaboration Network",
        showlegend=False,
        hovermode="closest",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        )
    )


    st.plotly_chart(
        fig_network,
        use_container_width=True
    )


    st.caption(
        "Nodes represent artists. Lines represent repeated collaboration links. "
        "Larger nodes indicate artists with more collaboration connections."
    )


else:

    st.info(
        "No repeated collaboration links found for the selected filters."
    )

# =========================================================
# DOWNLOAD DATA
# =========================================================

st.subheader("📥 Download Filtered Data")

download_data = filtered_df.copy()

download_data["date"] = download_data["date"].dt.strftime("%Y-%m-%d")

csv_data = download_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="UK_Top50_Filtered_Data.csv",
    mime="text/csv"
)


# =========================================================
# AUTOMATIC BUSINESS INSIGHTS
# =========================================================

st.subheader("💡 Key Market Insights")

# Calculate filtered metrics
filtered_entries = len(filtered_df)

if filtered_entries > 0:

    unique_artists = filtered_df["artist_normalized"].nunique()

    collaboration_rate = (
        filtered_df["track_type"].eq("Collaboration").mean() * 100
    )

    explicit_rate = (
        filtered_df["is_explicit"].mean() * 100
    )

    average_duration = filtered_df["duration_minutes"].mean()

    average_popularity = filtered_df["popularity"].mean()

    top_artist = (
    filtered_df["artist_normalized"]
    .value_counts()
    .idxmax()
    )

    top_artist_count = (
    filtered_df["artist_normalized"]
    .value_counts()
    .max()
    )

    # Insight cards
    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"🎤 **Artist Dominance:** "
            f"{top_artist} has the highest number of playlist appearances "
            f"with **{top_artist_count:,} entries** in the selected data."
        )

        st.info(
            f"🤝 **Collaboration:** "
            f"**{collaboration_rate:.1f}%** of the selected playlist entries "
            f"are collaborations."
        )

        st.info(
            f"🎵 **Artist Diversity:** "
            f"The selected data contains **{unique_artists:,} unique artists**."
        )

    with col2:
        st.info(
            f"🔞 **Explicit Content:** "
            f"**{explicit_rate:.1f}%** of selected tracks are explicit."
        )

        st.info(
            f"⏱️ **Average Duration:** "
            f"Tracks have an average duration of "
            f"**{average_duration:.2f} minutes**."
        )

        st.info(
            f"⭐ **Average Popularity:** "
            f"The average popularity score is "
            f"**{average_popularity:.1f}/100**."
        )

else:
    st.warning("No data available for the selected filters.")

# =========================================================
# DATA QUALITY & VALIDATION
# =========================================================

st.subheader("🔍 Data Quality & Validation")

st.info(
    "ℹ️ During preprocessing, 12 exact duplicate rows were removed. "
    "The cleaned dataset used by this dashboard contains no remaining "
    "exact duplicate rows."
)

quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

# Missing values
missing_values = filtered_df.isnull().sum().sum()

# Duplicate rows
duplicate_rows = filtered_df.duplicated().sum()

# Invalid positions
invalid_positions = (
    (~filtered_df["position"].between(1, 50))
    .sum()
)

# Invalid popularity
invalid_popularity = (
    (~filtered_df["popularity"].between(0, 100))
    .sum()
)

with quality_col1:
    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

with quality_col2:
    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )

with quality_col3:
    st.metric(
        "Invalid Positions",
        f"{invalid_positions:,}"
    )

with quality_col4:
    st.metric(
        "Invalid Popularity",
        f"{invalid_popularity:,}"
    )


# Validation status
if (
    missing_values == 0
    and duplicate_rows == 0
    and invalid_positions == 0
    and invalid_popularity == 0
):

    st.success(
        "✅ Data quality check passed. "
        "No missing values, duplicates, invalid playlist positions, "
        "or invalid popularity scores were found in the filtered data."
    )

else:

    st.warning(
        "⚠️ Some data quality issues were detected. "
        "Review the validation metrics above."
    )


# Dataset structure
validation_summary = pd.DataFrame({
    "Validation Check": [
        "Missing Values",
        "Duplicate Rows",
        "Invalid Playlist Positions",
        "Invalid Popularity Scores"
    ],
    "Result": [
        missing_values,
        duplicate_rows,
        invalid_positions,
        invalid_popularity
    ]
})

st.write("### Validation Summary")

st.dataframe(
    validation_summary,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# DAILY TOP 50 VALIDATION
# =========================================================

st.subheader("📅 Daily Top 50 Validation")

# Validate the original cleaned dataset
daily_validation = (
    df.groupby("date")
    .agg(
        entries=("position", "count"),
        unique_positions=("position", "nunique"),
        min_position=("position", "min"),
        max_position=("position", "max")
    )
    .reset_index()
)

daily_validation["valid_top50"] = (
    (daily_validation["entries"] == 50)
    & (daily_validation["unique_positions"] == 50)
    & (daily_validation["min_position"] == 1)
    & (daily_validation["max_position"] == 50)
)

valid_snapshots = daily_validation["valid_top50"].sum()
total_snapshots = len(daily_validation)
invalid_snapshots = total_snapshots - valid_snapshots

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Snapshots",
        f"{total_snapshots:,}"
    )

with col2:
    st.metric(
        "Valid Top 50 Snapshots",
        f"{valid_snapshots:,}"
    )

with col3:
    st.metric(
        "Invalid Snapshots",
        f"{invalid_snapshots:,}"
    )

if invalid_snapshots == 0:
    st.success(
        "✅ All playlist snapshots contain a valid Top 50 ranking "
        "with positions 1–50."
    )
else:
    st.warning(
        f"⚠️ {invalid_snapshots} playlist snapshot(s) "
        "require further validation."
    )

st.write("### Daily Validation Details")

st.dataframe(
    daily_validation,
    use_container_width=True,
    hide_index=True
)

# Show only invalid snapshots
invalid_daily_data = daily_validation[
    daily_validation["valid_top50"] == False
]

if len(invalid_daily_data) > 0:

    st.write("### ⚠️ Invalid Playlist Snapshot")

    st.dataframe(
        invalid_daily_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("✅ No invalid playlist snapshots found.")

    # =========================================================
# INVALID SNAPSHOT INVESTIGATION
# =========================================================

st.subheader("🔎 Invalid Snapshot Investigation")

invalid_dates = daily_validation.loc[
    ~daily_validation["valid_top50"],
    "date"
]

if len(invalid_dates) > 0:

    invalid_date = invalid_dates.iloc[0]

    invalid_date_df = df[
        df["date"] == invalid_date
    ].copy()

else:

    invalid_date = None
    invalid_date_df = pd.DataFrame()

position_counts = (
    invalid_date_df["position"]
    .value_counts()
    .sort_index()
    .reset_index()
)

position_counts.columns = [
    "position",
    "record_count"
]

st.write("### Position Frequency")

st.dataframe(
    position_counts,
    use_container_width=True,
    hide_index=True
)

duplicate_positions = position_counts[
    position_counts["record_count"] > 1
]

if len(duplicate_positions) > 0:

    st.warning(
        f"⚠️ {len(duplicate_positions)} playlist positions "
        "have multiple records on this date."
    )

    st.write("### Duplicate Positions")

    st.dataframe(
        duplicate_positions,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No duplicate playlist positions were found."
    )

    # =========================================================
# DUPLICATE POSITION RECORDS
# =========================================================

if len(duplicate_positions) > 0:

    duplicate_position_list = duplicate_positions["position"].tolist()

    duplicate_records = invalid_date_df[
        invalid_date_df["position"].isin(
            duplicate_position_list
        )
    ].sort_values("position")

    st.write("### 🎵 Records Behind Duplicate Positions")

    st.dataframe(
        duplicate_records[
            [
                "position",
                "song",
                "artist",
                "popularity",
                "album_type",
                "is_explicit"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
# EXACT DUPLICATE CHECK FOR INVALID SNAPSHOT
# =========================================================

exact_duplicates = invalid_date_df[
    invalid_date_df.duplicated(keep=False)
].copy()

st.write("### 🔁 Exact Duplicate Records")

st.metric(
    "Exact Duplicate Rows",
    f"{len(exact_duplicates):,}"
)

if len(exact_duplicates) > 0:

    st.warning(
        "⚠️ Exact duplicate records were found in this snapshot."
    )

    st.dataframe(
        exact_duplicates[
            [
                "date",
                "position",
                "song",
                "artist",
                "popularity",
                "album_type",
                "is_explicit"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No exact duplicate rows were found."
    )

    # =========================================================
# DUPLICATE SONG CHECK
# =========================================================

song_counts = (
    invalid_date_df["song"]
    .value_counts()
    .reset_index()
)

song_counts.columns = [
    "song",
    "record_count"
]

duplicate_songs = song_counts[
    song_counts["record_count"] > 1
]

st.write("### 🎵 Duplicate Songs in Invalid Snapshot")

st.metric(
    "Songs Appearing More Than Once",
    f"{len(duplicate_songs):,}"
)

if len(duplicate_songs) > 0:

    st.warning(
        "⚠️ Some songs appear multiple times in this playlist snapshot."
    )

    st.dataframe(
        duplicate_songs,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No duplicate songs were found."
    )

    # =========================================================
# INVALID SNAPSHOT SUMMARY
# =========================================================

st.write("### 📊 Invalid Snapshot Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric(
        "Total Records",
        f"{len(invalid_date_df):,}"
    )

with summary_col2:
    st.metric(
        "Unique Songs",
        f"{invalid_date_df['song'].nunique():,}"
    )

with summary_col3:
    st.metric(
        "Unique Artists",
        f"{invalid_date_df['artist'].nunique():,}"
    )

st.info(
    "These metrics help determine whether the extra records represent "
    "duplicate data or additional distinct playlist records."
)

# =========================================================
# DATA QUALITY CONCLUSION
# =========================================================

st.write("### 📝 Data Quality Conclusion")

if invalid_snapshots == 0:

    st.success(
        "The complete dataset contains valid Top 50 playlist snapshots "
        "for all available dates."
    )

else:

    st.warning(
        f"The dataset contains {invalid_snapshots} snapshot(s) "
        "requiring additional validation. "
        "The identified anomaly is retained for investigation rather "
        "than being removed without evidence."
    )

st.caption(
    "Data-quality anomalies are reported transparently so that "
    "stakeholders can distinguish validated records from records "
    "requiring further review."
)
# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.divider()

st.subheader("📌 Executive Summary")

if len(filtered_df) > 0:

    # Key metrics
    total_tracks = len(filtered_df)

    unique_artists = filtered_df["artist_normalized"].nunique()

    collaboration_pct = (
        filtered_df["track_type"]
        .eq("Collaboration")
        .mean() * 100
    )

    explicit_pct = (
        filtered_df["is_explicit"]
        .mean() * 100
    )

    album_share = (
        filtered_df["album_type"]
        .eq("Album")
        .mean() * 100
    )

    single_share = (
        filtered_df["album_type"]
        .eq("Single")
        .mean() * 100
    )
    compilation_share = (
    filtered_df["album_type"]
    .eq("Compilation")
    .mean() * 100
    )

    avg_duration = filtered_df["duration_minutes"].mean()

    avg_popularity = filtered_df["popularity"].mean()

    # Top artist
    top_artist = (
    filtered_df["artist_normalized"]
    .value_counts()
    .idxmax()
    )

    top_artist_appearances = (
    filtered_df["artist_normalized"]
    .value_counts()
    .max()
    )

    st.markdown(
        f"""
### UK Top 50 Market Overview

The selected UK Top 50 playlist data contains **{total_tracks:,} 
playlist entries** representing **{unique_artists:,} unique artists**.

### Artist Market Structure
- **Top artist:** {top_artist}
- **Top artist appearances:** {top_artist_appearances:,}
- **Artist Concentration Index:** {artist_concentration_index:.4f}
- **Top 5 artist share:** {top5_artist_share * 100:.1f}%
- **Diversity Score:** {diversity_score:.4f}

### Collaboration & Content
- **Collaboration ratio:** {collaboration_pct:.1f}%
- **Explicit content share:** {explicit_pct:.1f}%
- **Average track duration:** {avg_duration:.2f} minutes
- **Average popularity score:** {avg_popularity:.1f}/100

### Release Format
- **Single tracks:** {single_share:.1f}%
- **Album tracks:** {album_share:.1f}%

### Stakeholder Considerations

The dashboard can support decisions related to **artist discovery,
collaboration strategy, release-format planning, UK-focused marketing,
and content positioning**.

The metrics should be interpreted together rather than relying on a
single KPI. Artist concentration indicates how much playlist exposure
is concentrated among frequently appearing artists, while diversity
and collaboration metrics provide additional context about the breadth
and interconnectedness of the playlist.
"""
    )

else:

    st.warning(
        "No data is available for the selected filters."
    )

    # =========================================================
# METHODOLOGY & KPI DEFINITIONS
# =========================================================

st.divider()

st.subheader("📘 Methodology & KPI Definitions")

with st.expander("How this analysis was performed"):

    st.markdown(
        """
### 1. Data Validation
The dataset was checked for:

- Missing values
- Duplicate records
- Invalid playlist positions
- Invalid popularity scores
- Date consistency

### 2. Artist Analysis
Artist appearances were counted across playlist snapshots.

Artist diversity was measured using the number of unique artists
relative to total playlist entries.

    ### 3. Collaboration Analysis
    Artist names containing collaboration indicators such as:

    - `&`
    - `feat.`
    - `featuring`
    - `with`
    - `,`
    - `x`

were treated as collaborative tracks.

### 4. Explicit Content Analysis
Tracks were separated into:

- Explicit
- Non-explicit

The distribution was also compared across playlist rank groups.

### 5. Release Format Analysis
Playlist entries were compared based on:

- Single
- Album
- Compilation

Popularity and average album size were also examined.

### 6. Duration Analysis
Track duration was converted from milliseconds into minutes.

Tracks were grouped into:

- Short: less than 2.5 minutes
- Medium: 2.5–4 minutes
- Long: more than 4 minutes

### 7. Collaboration Network
Artists were represented as nodes and repeated collaborations
were represented as connections between nodes.
"""
    )


with st.expander("📊 KPI Definitions"):

    st.markdown("""
    **Artist Concentration Index (ACI)**  
    Measures how concentrated playlist appearances are among artists.  
    Higher values indicate that appearances are concentrated among fewer artists.

    **Unique Artist Count**  
    Number of distinct individual artists appearing in the selected playlist data.

    **Collaboration Ratio**  
    Percentage of playlist tracks that contain multiple artists.

    **Explicit Content Share**  
    Percentage of tracks marked as explicit.

    **Single vs Album Ratio**  
    Shows the distribution of playlist tracks by release format:
    Single, Album, or Compilation.

    **Content Variety Index**  
    A composite measure based on the variety of songs and artists relative to
    the number of playlist entries.

    **Average Artists per Track**  
    Average number of artists associated with each playlist track.
    """)