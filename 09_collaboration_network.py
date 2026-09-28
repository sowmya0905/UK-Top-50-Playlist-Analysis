import pandas as pd
import re
import networkx as nx

# Load cleaned dataset
df = pd.read_csv("data/UK_Top50_Cleaned.csv")

# Function to split collaborating artists
def split_artists(artist_text):
    artists = re.split(
        r"&|\bfeat\.?\b|\bfeaturing\b|\bwith\b|,|\bx\b",
        str(artist_text),
        flags=re.IGNORECASE
    )

    return [
        artist.strip()
        for artist in artists
        if artist.strip()
    ]


# Create graph
G = nx.Graph()

# Process every playlist entry
for artist_text in df["artist"]:
    artists = split_artists(artist_text)

    # Add individual artists
    for artist in artists:
        G.add_node(artist)

    # Create connections between collaborators
    if len(artists) > 1:
        for i in range(len(artists)):
            for j in range(i + 1, len(artists)):
                artist_a = artists[i]
                artist_b = artists[j]

                if G.has_edge(artist_a, artist_b):
                    G[artist_a][artist_b]["weight"] += 1
                else:
                    G.add_edge(
                        artist_a,
                        artist_b,
                        weight=1
                    )

# --------------------------------
# Network statistics
# --------------------------------

print("\n===== COLLABORATION NETWORK =====")

print("Number of Artists:", G.number_of_nodes())
print("Number of Collaboration Links:", G.number_of_edges())

# Most connected artists
degree_data = sorted(
    G.degree(),
    key=lambda x: x[1],
    reverse=True
)

print("\n===== MOST CONNECTED ARTISTS =====")

for artist, connections in degree_data[:20]:
    print(
        f"{artist}: {connections} connections"
    )

# --------------------------------
# Save network data
# --------------------------------

network_edges = nx.to_pandas_edgelist(G)

network_edges.to_csv(
    "reports/collaboration_network_edges.csv",
    index=False
)

network_nodes = pd.DataFrame(
    degree_data,
    columns=["artist", "connections"]
)

network_nodes.to_csv(
    "reports/collaboration_network_nodes.csv",
    index=False
)

print("\nCollaboration network files saved successfully!")