"""Map creation functions."""

import pandas as pd
import pydeck as pdk

from src.config import MAP_STYLES


def add_map_color_column(data: pd.DataFrame, color_mode: str) -> pd.DataFrame:
    """Add map color values based on selected color mode."""
    colored = data.copy()

    if color_mode == "Season":
        season_colors = {
            "Winter": [70, 130, 255, 180],
            "Spring": [80, 220, 120, 180],
            "Summer": [255, 190, 60, 180],
            "Autumn": [220, 100, 255, 180],
        }
        colored["map_color"] = colored["season"].map(season_colors)

    elif color_mode == "Month":
        colored["map_color"] = colored["month"].apply(
            lambda month: [
                int(255 * month / 12),
                int(180 * (1 - month / 12)),
                220,
                180,
            ]
        )

    elif color_mode == "Species":
        species_colors = {
            "Humpback Whale": [0, 180, 255, 180],
            "Blue Whale": [60, 100, 255, 180],
            "Fin Whale": [255, 160, 60, 180],
            "Gray Whale": [160, 160, 160, 180],
            "Sperm Whale": [180, 80, 255, 180],
            "Minke Whale": [80, 220, 120, 180],
        }
        colored["map_color"] = colored["common_name"].map(species_colors)

    else:
        colored["map_color"] = colored["color"]

    return colored


def create_pydeck_map(
    data: pd.DataFrame,
    show_heatmap: bool,
    show_path: bool,
    point_radius: int,
    map_style: str,
    color_mode: str = "Year",
) -> pdk.Deck:
    """Create the main PyDeck map."""
    data = add_map_color_column(data, color_mode)

    midpoint = {
        "latitude": data["latitude"].mean(),
        "longitude": data["longitude"].mean(),
    }

    layers = []

    if show_heatmap:
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=data,
            get_position="[longitude, latitude]",
            get_weight=1,
            radius_pixels=60,
        )
        layers.append(heatmap_layer)

    if show_path and len(data) > 1:
        path_data = pd.DataFrame(
            {"path": [data[["longitude", "latitude"]].values.tolist()]}
        )

        path_layer = pdk.Layer(
            "PathLayer",
            data=path_data,
            get_path="path",
            get_width=3,
            get_color=[255, 230, 0, 220],
            width_min_pixels=2,
            pickable=False,
        )
        layers.append(path_layer)

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[longitude, latitude]",
        get_radius=point_radius,
        get_fill_color="map_color",
        get_line_color=[255, 255, 255, 80],
        line_width_min_pixels=0.5,
        opacity=0.85,
        pickable=True,
    )
    layers.append(point_layer)

    view_state = pdk.ViewState(
        latitude=midpoint["latitude"],
        longitude=midpoint["longitude"],
        zoom=2,
        min_zoom=0.5,
        max_zoom=10,
        pitch=0,
    )

    return pdk.Deck(
        map_style=MAP_STYLES[map_style],
        layers=layers,
        initial_view_state=view_state,
        tooltip={
            "html": """
            <b>Species:</b> {common_name}<br>
            <b>Scientific name:</b> {species}<br>
            <b>Date:</b> {date_label}<br>
            <b>Year:</b> {year}<br>
            <b>Month:</b> {month}<br>
            <b>Season:</b> {season}<br>
            <b>Lat:</b> {latitude}<br>
            <b>Lon:</b> {longitude}
            """,
            "style": {"color": "white"},
        },
    )