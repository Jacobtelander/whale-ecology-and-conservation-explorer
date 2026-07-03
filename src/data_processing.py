"""Data loading and cleaning functions."""

import pandas as pd
import streamlit as st


SEASON_BY_MONTH = {
    12: "Winter",
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Autumn",
    10: "Autumn",
    11: "Autumn",
}


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load whale observation data from CSV."""
    return pd.read_csv(file_path)


def clean_observation_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean dates, coordinates, and create helper columns."""
    cleaned = data.copy()

    cleaned["date"] = pd.to_datetime(
        cleaned["date"],
        format="mixed",
        errors="coerce",
        utc=True,
    )

    cleaned = cleaned.dropna(
        subset=["date", "latitude", "longitude", "species"]
    )

    cleaned = cleaned[
        cleaned["latitude"].between(-90, 90)
        & cleaned["longitude"].between(-180, 180)
    ].copy()

    cleaned = cleaned.sort_values("date")
    cleaned["year"] = cleaned["date"].dt.year
    cleaned["month"] = cleaned["date"].dt.month
    cleaned["month_name"] = cleaned["date"].dt.month_name()
    cleaned["season"] = cleaned["month"].map(SEASON_BY_MONTH)
    cleaned["date_label"] = cleaned["date"].dt.strftime("%Y-%m-%d")

    return cleaned


def add_color_column(
    data: pd.DataFrame,
    selected_years: tuple[int, int],
) -> pd.DataFrame:
    """Add RGB color values based on observation year."""
    colored = data.copy()

    min_year, max_year = selected_years
    year_span = max(max_year - min_year, 1)

    def year_to_color(year: int) -> list[int]:
        year_position = (year - min_year) / year_span

        if year_position < 0.33:
            return [0, 180, 255, 170]
        if year_position < 0.66:
            return [130, 90, 255, 180]
        return [255, 60, 180, 190]

    colored["color"] = colored["year"].apply(year_to_color)

    return colored
