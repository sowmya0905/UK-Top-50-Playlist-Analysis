# 🎵 UK Top 50 Playlist Analysis

## Market Structure, Artist Diversity & Content Localization Analysis

An end-to-end **Data Analytics and Business Intelligence project** analyzing the United Kingdom Top 50 playlist to understand **artist dominance, market concentration, collaboration patterns, content diversity, explicit content, release formats, track duration, and playlist trends**.

The project includes data validation and cleaning, exploratory data analysis, artist-level analysis, collaboration network analysis, market metrics, and an interactive **Streamlit dashboard**.

---

## 📌 Project Overview

Music playlists provide useful signals about artist visibility, content characteristics, and market structure.

This project analyzes daily **UK Top 50 playlist data** to answer questions such as:

* Which artists appear most frequently?
* How concentrated is playlist exposure among leading artists?
* How diverse is the artist pool?
* How frequently do artists collaborate?
* Are collaborations more common in certain rank groups?
* What proportion of playlist content is explicit?
* How are explicit tracks distributed across rankings?
* Are Albums, Singles, or Compilations more represented?
* What is the distribution of track durations?
* Is track duration associated with popularity?
* How does playlist composition change over time?

The final result is an interactive dashboard designed to make these insights easy to explore.

---

## 🎯 Objectives

The main objectives of this project are:

1. Validate and standardize the UK Top 50 playlist dataset.
2. Identify and remove duplicate records.
3. Normalize artist names.
4. Separate multi-artist collaborations into individual artists.
5. Analyze artist dominance and diversity.
6. Measure artist concentration.
7. Analyze solo and collaborative tracks.
8. Study collaboration frequency across ranking groups.
9. Build a collaboration network.
10. Analyze explicit and non-explicit content.
11. Analyze Album, Single, and Compilation representation.
12. Study track-duration patterns.
13. Compare track duration with popularity.
14. Calculate market-level KPIs.
15. Build an interactive Streamlit dashboard.
16. Provide stakeholder-oriented insights and recommendations.

---

## 📊 Dataset

The project uses United Kingdom Top 50 playlist data.

### Dataset Summary

| Metric                       |                          Value |
| ---------------------------- | -----------------------------: |
| Raw records                  |                         27,800 |
| Cleaned records              |                         27,788 |
| Unique dates                 |                            555 |
| Date range                   | 18 May 2024 – 27 November 2025 |
| Expected daily positions     |                           1–50 |
| Unique raw artist names      |                            343 |
| Unique songs                 |                            803 |
| Collaboration-indicator rows |                          5,306 |
| Album entries                |                         16,669 |
| Single entries               |                         11,053 |
| Compilation entries          |                             78 |
| Non-explicit entries         |                         18,888 |
| Explicit entries             |                          8,912 |

### Data Cleaning

The preprocessing stage includes:

* Duplicate detection and removal
* Date standardization
* Artist-name normalization
* Collaboration splitting
* Track-duration conversion
* Explicit-content standardization
* Position validation
* Popularity validation
* Daily Top 50 snapshot validation

After cleaning, **12 exact duplicate records were removed**, resulting in **27,788 analytical records**.

---

## 🔍 Analysis Performed

### 1. Data Validation

The project validates:

* Missing values
* Duplicate records
* Playlist positions
* Popularity values
* Daily Top 50 completeness
* Minimum and maximum positions
* Unique positions per date

A daily snapshot is considered structurally valid when it contains the expected 50 entries with unique positions from 1 to 50.

---

### 2. Artist Dominance & Diversity

Artist analysis is performed using an **individual-artist representation**.

Multi-artist entries are separated using collaboration indicators such as:

```text
&
feat.
featuring
with
,
x
```

This prevents a collaboration such as:

```text
Artist A & Artist B
```

from being treated as one combined artist.

The dashboard provides:

* Artist dominance leaderboard
* Artist appearance counts
* Unique artist count
* Daily artist diversity
* Artist Concentration Index
* Top 5 Artist Share
* Diversity Score

---

### 3. Collaboration Analysis

Tracks are classified as:

* **Solo**
* **Collaboration**

The project analyzes:

* Collaboration Ratio
* Average Artists per Track
* Collaboration frequency
* Collaboration by rank group
* Artist-to-artist relationships

### Rank Groups

The Top 50 is divided into:

| Rank Group | Positions |
| ---------- | --------- |
| Top 10     | 1–10      |
| 11–20      | 11–20     |
| 21–30      | 21–30     |
| 31–40      | 31–40     |
| 41–50      | 41–50     |

---

## 🕸️ Collaboration Network

A collaboration network is created using **NetworkX**.

* Artists are represented as nodes.
* Collaborative relationships are represented as edges.
* Repeated collaborations increase edge weight.

The network visualization helps identify:

* Frequently connected artists
* Repeated collaboration patterns
* Artist relationship clusters
* Highly connected participants

The network represents relationships observed within the analyzed playlist data and should not be interpreted as a complete map of the music industry.

---

## 🔞 Explicit Content Analysis

The project compares:

* Explicit tracks
* Non-explicit tracks

The dashboard provides:

* Explicit Content Share
* Explicit vs Non-explicit distribution
* Explicit content by rank group
* Explicit-content trends

This analysis provides descriptive information about the content composition of the playlist.

---

## 💿 Release Format Analysis

The dataset contains three release-format categories:

* **Album**
* **Single**
* **Compilation**

The dashboard analyzes:

* Release Format Distribution
* Release Format Share
* Track count by release type
* Average popularity by release type
* Average album size
* Album size vs playlist inclusion

---

## ⏱️ Track Duration Analysis

Track duration is converted from milliseconds into minutes.

The project analyzes:

* Duration distribution
* Short tracks
* Medium-duration tracks
* Long tracks
* Average popularity by duration group
* Duration vs popularity
* Duration-popularity correlation

The duration analysis is descriptive and does not imply that track duration causes popularity.

---

## 📈 Market Metrics

The dashboard includes the following KPIs.

### Artist Concentration Index

The Artist Concentration Index is calculated using the squared shares of individual artist appearances:

```text
ACI = Σ (Artist Share²)
```

A higher value mathematically represents a more concentrated distribution of artist appearances.

---

### Unique Artist Count

Number of distinct individual artists represented after collaboration splitting.

```text
Unique Artist Count =
Number of distinct individual artists
```

---

### Collaboration Ratio

Percentage of playlist entries classified as collaborations.

```text
Collaboration Ratio =
Collaborative Tracks / Total Tracks
```

---

### Explicit Content Share

Percentage of playlist entries marked explicit.

```text
Explicit Content Share =
Explicit Tracks / Total Tracks
```

---

### Diversity Score

A project-defined metric:

```text
Diversity Score =
Unique Individual Artists / Total Playlist Entries
```

---

### Content Variety Index

A project-defined composite metric:

```text
Content Variety Index =
(Unique Songs + Unique Individual Artists)
/
Total Playlist Entries
```

---

### Average Artists per Track

Measures the average number of individual artists associated with each track.

---

## 📊 Dashboard Features

The Streamlit dashboard provides interactive analysis through:

### Filters

* 📅 Date Range
* 🎤 Artist
* 🤝 Solo / Collaboration
* 💿 Album Type

### Dashboard Sections

* KPI Overview
* Artist Dominance
* Artist Diversity
* Collaboration Analysis
* Collaboration Network
* Explicit Content Analysis
* Album Structure
* Track Duration Analysis
* Market Metrics
* Market Trends
* Rank Group Analysis
* Data Quality & Validation
* Executive Summary

---

## 🖥️ Dashboard Preview

Add your dashboard screenshots here after taking them from Streamlit.

```markdown
![Dashboard Overview](images/dashboard_overview.png)
```

```markdown
![Artist Analysis](images/artist_analysis.png)
```

```markdown
![Collaboration Network](images/collaboration_network.png)
```

```markdown
![Market Metrics](images/market_metrics.png)
```

> Create an `images` folder in the repository and place your screenshots inside it.

---

## 🛠️ Technologies Used

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Visualization

* Plotly
* Matplotlib

### Network Analysis

* NetworkX

### Dashboard

* Streamlit

### Development

* Visual Studio Code
* Git
* GitHub

---

## 📁 Project Structure

```text
UK-Top-50-Playlist-Analysis/
│
├── data/
│   ├── Atlantic_United_Kingdom.csv
│   └── UK_Top50_Cleaned.csv
│
├── notebooks/
│   ├── 01_data_analysis.py
│   └── 02_data_cleaning.py
│
├── 03_artist_analysis.py
├── 04_collaboration_analysis.py
├── 05_explicit_analysis.py
├── 06_album_analysis.py
├── 07_duration_analysis.py
├── 08_market_metrics.py
├── 09_collaboration_network.py
│
├── app.py
├── README.md
└── UK_Top_50_Playlist_Analysis_Research_Paper.pdf
```

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sowmya0905/UK-Top-50-Playlist-Analysis.git
```

### Step 2: Open the Project

```bash
cd UK-Top-50-Playlist-Analysis
```

### Step 3: Install Required Libraries

```bash
pip install pandas numpy streamlit plotly networkx matplotlib
```

### Step 4: Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The application will open in your browser, normally at:

```text
http://localhost:8501
```

---

## 🚀 How to Use the Dashboard

1. Start the Streamlit application.
2. Open the dashboard in your browser.
3. Use the sidebar filters.
4. Select a date range.
5. Select an artist if required.
6. Select Solo or Collaboration.
7. Select Album, Single, or Compilation.
8. Explore the KPI cards.
9. Analyze artist dominance.
10. Explore collaboration patterns.
11. Review explicit-content distribution.
12. Analyze release formats.
13. Study track duration.
14. Review market trends.
15. Use the Executive Summary for stakeholder-level interpretation.

---

## 💡 Key Insights

The dataset provides several important structural observations:

* The project contains **27,800 raw playlist records** across **555 dates**.
* After duplicate removal, **27,788 records** remain for analysis.
* The dataset contains **803 unique songs**.
* There are **343 unique raw artist names** before individual collaboration splitting.
* **5,306 records contain collaboration indicators**, making collaboration an important analytical dimension.
* Album and Single tracks represent the large majority of release-format entries, while Compilation entries form a smaller category.
* Both explicit and non-explicit tracks have substantial representation, allowing meaningful comparison.
* Artist-level analysis requires collaboration splitting to avoid treating multiple artists as a single combined entity.
* Rank-group analysis provides an additional view of how collaboration, popularity, explicitness, and artist diversity vary across the Top 50.

---

## 📌 Business / Stakeholder Recommendations

Based on the analytical framework, stakeholders can:

1. Monitor individual artist visibility instead of relying only on combined artist strings.
2. Track Top 5 Artist Share and Artist Concentration Index together.
3. Monitor collaboration patterns across different ranking groups.
4. Use explicit-content metrics for descriptive audience and localization analysis.
5. Keep Album, Single, and Compilation categories separate in reporting.
6. Monitor track-duration and popularity relationships as descriptive patterns.
7. Use date-based trends to identify changes in playlist composition.
8. Use the collaboration network to explore repeated artist relationships.
9. Automate data-quality checks when new playlist snapshots become available.
10. Maintain consistent definitions for custom KPIs across future reporting periods.

---

## 📚 Research Paper

The complete research paper for this project includes:

* Abstract
* Introduction
* Problem Statement
* Objectives
* Dataset Description
* Data Validation
* Data Cleaning
* Methodology
* KPI Definitions
* Artist Analysis
* Collaboration Analysis
* Explicit Content Analysis
* Release Format Analysis
* Track Duration Analysis
* Market Structure
* Dashboard Description
* Key Findings
* Recommendations
* Limitations
* Future Scope
* Conclusion

The research paper is available in the repository as:

```text
UK_Top_50_Playlist_Analysis_Research_Paper.pdf
```

---

## ⚠️ Limitations

* The dataset does not directly contain complete streaming, revenue, or audience-demographic information.
* Some KPIs such as Diversity Score and Content Variety Index are project-defined metrics.
* Artist splitting depends on text-based collaboration delimiters.
* Playlist presence does not establish causal relationships with popularity.
* The collaboration network represents relationships observed in the analyzed playlist.
* Results represent the specified analysis period and should not automatically be generalized to all UK music consumption.

---

## 🔮 Future Scope

Future improvements could include:

* Streaming-data integration
* Audience segmentation
* Time-series forecasting
* Artist popularity prediction
* Playlist movement prediction
* Automated daily data ingestion
* Automated validation pipeline
* Advanced NLP on track metadata
* Temporal collaboration networks
* Community detection
* Cross-country playlist comparison
* Explainable machine-learning models

---

## 👩‍💻 Author

**Sowmya Gandikota**

B.Tech – Computer Science & Engineering
Specialization: Data Science

### Areas of Interest

* Data Analytics
* Data Visualization
* Python
* Tableau
* Excel
* Machine Learning
* Business Intelligence

---

## ⭐ Project Highlights

```text
✔ End-to-end Data Analytics Project
✔ Real-world Playlist Dataset
✔ Data Cleaning & Validation
✔ Artist-Level Analysis
✔ Collaboration Network Analysis
✔ Market Concentration Metrics
✔ Explicit Content Analysis
✔ Release Format Analysis
✔ Track Duration Analysis
✔ Interactive Streamlit Dashboard
✔ Executive Stakeholder Insights
✔ Research Paper
```

---

## 📄 Project Status

**Status: Completed ✅**

The project includes a cleaned dataset, analytical Python scripts, an interactive Streamlit dashboard, market KPIs, collaboration-network analysis, and a complete research paper.

---

## ⭐ If you found this project useful

Feel free to explore the repository, review the dashboard, and connect with me for feedback or collaboration.
