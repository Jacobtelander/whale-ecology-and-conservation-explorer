# Whale Ecology and Conservation Explorer

An interactive geospatial dashboard for exploring and analysing whale observation records using open biodiversity data.

The project combines geospatial visualisation, ecological analysis, and interactive data exploration to investigate seasonal movement patterns, species differences, observation bias, and conservation-relevant insights.

Built with **Python**, **Streamlit**, **Pandas**, **Plotly**, and **PyDeck**, using occurrence data from the **Ocean Biodiversity Information System (OBIS)**.

---

## 🚀 Live Demo

https://whale-ecology-explorer.streamlit.app

---

## Dashboard Preview

![Dashboard overview.png](images/Dashboard%20overview.png)

### Interactive Observation Map

![Interactive observation map.png](images/Interactive%20observation%20map.png)

### Comparative Ecology

![Comparative ecology.png](images/Comparative%20ecology.png)

---

# Why this project?

Marine biodiversity datasets are becoming increasingly available through open data initiatives such as OBIS. However, many existing visualisation tools focus primarily on displaying observations rather than helping users interpret ecological patterns.

This project was developed to demonstrate how modern data science techniques can support marine conservation through interactive exploration of whale observation data.

The dashboard encourages users to investigate questions such as:

- How do different whale species vary throughout the year?
- Which months have the highest observation density?
- How does latitude change seasonally?
- What potential observation biases exist?
- What ecological patterns emerge from the available data?

---

# Features

### Interactive Observation Map

- Interactive world map
- Multiple basemap styles
- Observation timeline
- Heatmap layer
- Time animation
- Species colouring
- Seasonal colouring
- Monthly colouring
- Year gradient colouring

---

### Ecological Analysis

- Monthly observation patterns
- Seasonal distributions
- Latitude by month
- Long-term observation trends
- Chronological observation timeline
- Conservation insights
- Automatic ecological findings
- Observation bias assessment

---

### Comparative Ecology

Compare multiple whale species simultaneously.

Includes:

- Observation counts
- Peak observation month
- Mean latitude
- Latitude range
- Observation period
- Scientific names
- Monthly comparison charts
- Seasonal movement comparison

---

### Migration Timeline

Interactive cumulative timeline allowing users to explore how whale observations accumulate through time.

Features:

- Play
- Pause
- Reset
- Progress indicator
- Timeline statistics

---

# Skills Demonstrated

This project demonstrates practical skills in:

- Geospatial data visualisation
- Interactive dashboard development
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Ecological data interpretation
- Comparative statistical analysis
- Scientific communication
- Software engineering for data science
- Python application development

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Plotly | Statistical visualisations |
| PyDeck | Interactive mapping |
| Requests | OBIS API integration |
| Pytest | Unit testing |

---

# Data Source

All whale observations are obtained from the

**Ocean Biodiversity Information System (OBIS)**

https://obis.org/

Species currently included:

- Humpback Whale
- Blue Whale
- Fin Whale
- Gray Whale
- Minke Whale
- Sperm Whale

---

# Project Structure

```
Whale Ecology and Conservation Explorer
│
├── app.py
├── data/
│   └── whales.csv
├── src/
│   ├── analysis.py
│   ├── config.py
│   ├── data_processing.py
│   ├── mapping.py
│   └── species.py
├── tests/
│   └── test_analysis.py
├── fetch_obis_data.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/whale-ecology-and-conservation-explorer.git
```

Navigate into the project

```bash
cd whale-ecology-and-conservation-explorer
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# Project Roadmap

Future improvements include:

- Marine Protected Areas overlay
- Sea Surface Temperature integration
- Species distribution modelling
- Environmental variable analysis
- Interactive GIS layers
- Exportable reports
- Advanced ecological metrics
- Machine learning based migration clustering

---

# Limitations

This project uses **observation records**, not GPS tracks of individual whales.

Observed spatial and temporal patterns should therefore be interpreted with caution, as they may reflect:

- research effort
- coastal accessibility
- whale-watching activity
- reporting infrastructure

rather than true whale abundance.

---

# Author

**Jacob Telander**
