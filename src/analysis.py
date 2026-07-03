"""Analysis functions for whale observation data."""

from math import atan2, cos, radians, sin, sqrt

import pandas as pd
import plotly.express as px

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

SEASON_ORDER = ["Winter", "Spring", "Summer", "Autumn"]


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Calculate distance in kilometers between two coordinates."""
    earth_radius_km = 6371

    lat1, lon1, lat2, lon2 = map(
        radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


def calculate_chronological_observation_distance(data: pd.DataFrame) -> float:
    """
    Calculate distance between observations in chronological order.

    This is not the real distance travelled by a whale.
    It is the distance between observation records.
    """
    if len(data) <= 1:
        return 0

    coordinates = data[["latitude", "longitude"]].values.tolist()
    total_distance_km = 0

    for i in range(1, len(coordinates)):
        lat1, lon1 = coordinates[i - 1]
        lat2, lon2 = coordinates[i]

        total_distance_km += haversine_distance(
            lat1,
            lon1,
            lat2,
            lon2,
        )

    return total_distance_km


def create_observations_per_year_chart(data: pd.DataFrame, species_label: str):
    """Create a bar chart with observation counts per year."""
    observations_per_year = (
        data
        .groupby("year")
        .size()
        .reset_index(name="observations")
    )

    fig = px.bar(
        observations_per_year,
        x="year",
        y="observations",
        title=f"{species_label} observations per year",
        labels={"year": "Year", "observations": "Number of observations"},
    )

    fig.update_layout(template="plotly_white", height=350)
    return fig


def create_observations_per_month_chart(data: pd.DataFrame, species_label: str):
    """Create a bar chart showing seasonal observation patterns."""
    observations_per_month = (
        data
        .groupby(["month", "month_name"])
        .size()
        .reset_index(name="observations")
        .sort_values("month")
    )

    fig = px.bar(
        observations_per_month,
        x="month_name",
        y="observations",
        title=f"{species_label} observations per month",
        labels={"month_name": "Month", "observations": "Number of observations"},
    )

    fig.update_xaxes(categoryorder="array", categoryarray=MONTH_ORDER)
    fig.update_layout(template="plotly_white", height=380)
    return fig


def create_latitude_by_month_chart(data: pd.DataFrame, species_label: str):
    """Create a box plot of latitude by month to show seasonal movement patterns."""
    fig = px.box(
        data,
        x="month_name",
        y="latitude",
        points="outliers",
        title=f"{species_label} latitude distribution by month",
        labels={"month_name": "Month", "latitude": "Latitude"},
    )

    fig.update_xaxes(categoryorder="array", categoryarray=MONTH_ORDER)
    fig.update_layout(template="plotly_white", height=420)
    return fig


def create_season_chart(data: pd.DataFrame, species_label: str):
    """Create a bar chart with observations by season."""
    observations_per_season = (
        data
        .groupby("season")
        .size()
        .reset_index(name="observations")
    )

    fig = px.bar(
        observations_per_season,
        x="season",
        y="observations",
        title=f"{species_label} observations by season",
        labels={"season": "Season", "observations": "Number of observations"},
    )

    fig.update_xaxes(categoryorder="array", categoryarray=SEASON_ORDER)
    fig.update_layout(template="plotly_white", height=350)
    return fig


def get_peak_observation_month(data: pd.DataFrame) -> str:
    """Return the month with the most observations."""
    if data.empty:
        return "No data"

    monthly_counts = data.groupby("month_name").size()
    return str(monthly_counts.idxmax())


def get_latitude_range(data: pd.DataFrame) -> float:
    """Return latitude range in degrees."""
    if data.empty:
        return 0
    return float(data["latitude"].max() - data["latitude"].min())


def build_conservation_insights(data: pd.DataFrame) -> list[str]:
    """Generate simple interpretation bullets for the filtered dataset."""
    if data.empty:
        return ["No observations match the selected filters."]

    peak_month = get_peak_observation_month(data)
    latitude_range = get_latitude_range(data)
    first_year = int(data["year"].min())
    last_year = int(data["year"].max())
    most_common_season = str(data.groupby("season").size().idxmax())

    insights = [
        f"The highest number of observations in the current filter occurs in {peak_month}.",
        f"The most represented season is {most_common_season}.",
        f"The filtered records cover {first_year}–{last_year} and span about {latitude_range:.1f} degrees of latitude.",
        "Observation density should not be interpreted as true whale abundance; it can reflect research effort, reporting bias, and coastal accessibility.",
        "Connected timelines show chronological observation order, not confirmed tracks of individual whales.",
    ]

    return insights


def calculate_data_quality_summary(raw_data: pd.DataFrame, cleaned_data: pd.DataFrame) -> dict[str, float]:
    """Summarize how much data was removed during cleaning."""
    raw_count = len(raw_data)
    cleaned_count = len(cleaned_data)
    removed_count = raw_count - cleaned_count
    removed_percent = (removed_count / raw_count * 100) if raw_count else 0

    return {
        "raw_count": raw_count,
        "cleaned_count": cleaned_count,
        "removed_count": removed_count,
        "removed_percent": removed_percent,
    }
