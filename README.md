# Whale Migration Tracker

An interactive geospatial dashboard for exploring whale observation records over time.

This project is designed as a portfolio project for **data science in conservation**, combining geospatial visualization, ecological interpretation, and careful communication of data limitations.

## Features

- Interactive whale observation map
- Species filtering
- Year range filtering
- Observation heatmap
- Chronological observation timeline
- Observations per year
- Observations per month
- Observations by season
- Latitude distribution by month
- Automated conservation insights
- Data quality and bias notes

## Why this matters

Whale observation records can help reveal seasonal and spatial patterns, but they are not the same as true migration tracks or population abundance estimates. This project therefore emphasizes both visualization and responsible interpretation.

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly
- PyDeck
- OBIS-style biodiversity observation data

## Project structure

```text
whale-migration-tracker/
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
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
pytest
```

## Current limitations

- Observation density may reflect research effort and reporting bias.
- Connected timeline paths are not confirmed tracks of individual whales.
- Seasonal patterns can reflect both whale behavior and human sampling effort.
- The project currently focuses on exploratory analysis, not causal ecological modeling.

## Future improvements

- Add multiple whale species profiles
- Add animated time slider
- Add marine protected area overlays
- Add sea-surface temperature data
- Add habitat clustering analysis
- Deploy the app online
