import streamlit as st

from streamlit_autorefresh import st_autorefresh

from src.analysis import (
    build_conservation_insights,
    calculate_chronological_observation_distance,
    calculate_data_quality_summary,
    create_latitude_by_month_chart,
    create_observations_per_month_chart,
    create_observations_per_year_chart,
    create_season_chart,
)
from src.config import DATA_PATH, MAP_STYLES
from src.data_processing import add_color_column, clean_observation_data, load_data
from src.mapping import create_pydeck_map
from src.species import show_species_info


st.set_page_config(
    page_title="Whale Migration Tracker",
    layout="wide"
)

st.title("🐋 Whale Migration Tracker")

st.markdown(
    """
    Explore real whale observation records through an interactive geospatial dashboard.

    This app focuses on ecological interpretation: seasonal patterns, latitudinal movement,
    observation bias, and conservation-relevant data limitations.
    """
)

st.info(
    "Note: Observation timelines connect records in chronological order. "
    "They should not be interpreted as exact movement paths of individual whales."
)

raw_df = load_data(DATA_PATH)
df = clean_observation_data(raw_df)
data_quality = calculate_data_quality_summary(raw_df, df)

st.sidebar.header("Controls")

species_options = sorted(df["species"].dropna().unique())

selected_species = st.sidebar.multiselect(
    "Choose whale species",
    species_options,
    default=[species_options[0]],
)

show_species_info(selected_species)

show_heatmap = st.sidebar.checkbox("Show observation heatmap", value=False)
show_path = st.sidebar.checkbox("Show observation timeline", value=False)

map_style = st.sidebar.selectbox("Choose map style", list(MAP_STYLES.keys()))

color_mode = st.sidebar.selectbox(
    "Color observations by",
    [
        "Year",
        "Season",
        "Month",
    ],
    help="Change how observations are coloured on the map.",
)

point_radius = st.sidebar.slider(
    "Point size",
    min_value=5_000,
    max_value=100_000,
    value=25_000,
    step=5_000,
)

max_points = st.sidebar.slider(
    "Max observations shown on map",
    min_value=100,
    max_value=5_000,
    value=1_000,
    step=100,
)

if not selected_species:
    st.warning("Please select at least one whale species from the sidebar.")
    st.stop()

filtered_df = df[df["species"].isin(selected_species)].copy()

min_year = int(filtered_df["year"].min())
max_year = int(filtered_df["year"].max())

if "selected_years" not in st.session_state:
    st.session_state.selected_years = (min_year, max_year)

selected_years = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=st.session_state.selected_years,
)

st.session_state.selected_years = selected_years

st.sidebar.markdown("### Timeline animation")

if "is_animating" not in st.session_state:
    st.session_state.is_animating = False

play_col, pause_col, reset_col = st.sidebar.columns(3)

if play_col.button("▶ Play"):
    st.session_state.is_animating = True
    st.session_state.selected_years = (
        selected_years[0],
        selected_years[0],
    )

if pause_col.button("⏸ Pause"):
    st.session_state.is_animating = False

if reset_col.button("↺ Reset"):
    st.session_state.is_animating = False
    st.session_state.selected_years = (min_year, max_year)

if st.session_state.is_animating:
    st_autorefresh(interval=900, key="migration_animation")

    start_year, end_year = st.session_state.selected_years

    if end_year < max_year:
        end_year += 1
        st.session_state.selected_years = (start_year, end_year)
    else:
        st.session_state.is_animating = False

selected_years = st.session_state.selected_years
current_map_year = selected_years[1]



filtered_df = filtered_df[
    (filtered_df["year"] >= selected_years[0])
    & (filtered_df["year"] <= selected_years[1])
].copy()

if filtered_df.empty:
    st.warning("No observations match the selected filters.")
    st.stop()

filtered_df = add_color_column(filtered_df, selected_years)
analysis_df = filtered_df.copy()


map_df = filtered_df[
    filtered_df["year"] <= current_map_year
].copy()


if len(map_df) > max_points:
    map_df = map_df.sample(n=max_points, random_state=42).sort_values("date")

species_label = ", ".join(selected_species)
total_distance_km = calculate_chronological_observation_distance(analysis_df)

st.write(f"Showing observations for: {species_label}")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Filtered observations", len(analysis_df))
col2.metric("Shown on map", len(map_df))
col3.metric("First observation", str(analysis_df["date"].min().date()))
col4.metric("Last observation", str(analysis_df["date"].max().date()))
col5.metric("Observation distance", f"{total_distance_km:,.0f} km")

st.subheader("Conservation insights")
for insight in build_conservation_insights(analysis_df):
    st.markdown(f"- {insight}")

st.divider()

st.subheader("Seasonal analysis")
left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(
        create_observations_per_month_chart(analysis_df, species_label),
        use_container_width=True,
    )

with right_col:
    st.plotly_chart(
        create_season_chart(analysis_df, species_label),
        use_container_width=True,
    )

st.plotly_chart(
    create_latitude_by_month_chart(analysis_df, species_label),
    use_container_width=True,
)

st.caption(
    "Latitude by month can reveal seasonal movement patterns, but it is still based on observation records, "
    "not confirmed individual migration tracks."
)

st.divider()
st.subheader("Long-term observation trend")
st.plotly_chart(
    create_observations_per_year_chart(analysis_df, species_label),
    use_container_width=True,
)

st.divider()
st.subheader("Observation map")
deck = create_pydeck_map(
    data=map_df,
    show_heatmap=show_heatmap,
    show_path=show_path,
    point_radius=point_radius,
    map_style=map_style,
    color_mode=color_mode,
)




st.subheader("Migration Timeline")

timeline_col1, timeline_col2, timeline_col3 = st.columns(3)

timeline_col1.metric(
    "Timeline year",
    current_map_year,
)

timeline_col2.metric(
    "Observations displayed",
    f"{len(map_df):,}",
)

timeline_col3.metric(
    "Selected period",
    f"{selected_years[0]}–{selected_years[1]}",
)

st.caption(
    f"Displaying cumulative whale observations from "
    f"**{selected_years[0]}** to **{current_map_year}**."
)

progress = (
    (current_map_year - selected_years[0])
    / max(selected_years[1] - selected_years[0], 1)
)

st.progress(progress)





st.pydeck_chart(deck, use_container_width=True, height=750)

if color_mode == "Season":
    st.markdown(
        """
        **Map color legend**

        🔵 **Winter** &nbsp;&nbsp;
        🟢 **Spring** &nbsp;&nbsp;
        🟡 **Summer** &nbsp;&nbsp;
        🟣 **Autumn**
        """
    )

elif color_mode == "Month":
    st.markdown(
        """
        **Observation month**

        <div style="
            height: 18px;
            border-radius: 8px;
            background: linear-gradient(
                to right,
                rgb(21,165,220),
                rgb(128,90,220),
                rgb(255,0,220)
            );
        "></div>

        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span>January</span>
            <span>December</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif color_mode == "Year":
    st.markdown(
        f"""
        **Observation year**

        <div style="
            height: 18px;
            border-radius: 8px;
            background: linear-gradient(
                to right,
                rgb(0,180,255),
                rgb(130,90,255),
                rgb(255,60,180)
            );
        "></div>

        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span>{selected_years[0]}</span>
            <span>{selected_years[1]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("Data quality and limitations"):
    st.write(
        f"The raw dataset contains **{data_quality['raw_count']:,}** records. "
        f"After cleaning dates, coordinates, and species names, **{data_quality['cleaned_count']:,}** records remain."
    )
    st.write(
        f"Removed records: **{data_quality['removed_count']:,}** "
        f"({data_quality['removed_percent']:.1f}% of the raw dataset)."
    )
    st.markdown(
        """
        Important limitations:
        - These are observation records, not GPS tracks of individual whales.
        - Areas with more researchers, whale-watching activity, or reporting infrastructure may have more records.
        - A dense cluster of observations does not automatically mean higher whale abundance.
        - Seasonal patterns can reflect both whale ecology and human observation effort.
        """
    )

with st.expander("Show filtered whale observation data"):
    st.dataframe(analysis_df)
