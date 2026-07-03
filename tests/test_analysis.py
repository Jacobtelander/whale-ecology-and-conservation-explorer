import pandas as pd

from src.analysis import (
    calculate_chronological_observation_distance,
    get_latitude_range,
    get_peak_observation_month,
    haversine_distance,
)


def test_haversine_distance_zero_for_same_point():
    assert haversine_distance(0, 0, 0, 0) == 0


def test_chronological_observation_distance_empty_data():
    data = pd.DataFrame(columns=["latitude", "longitude"])
    assert calculate_chronological_observation_distance(data) == 0


def test_peak_observation_month():
    data = pd.DataFrame({"month_name": ["June", "June", "July"]})
    assert get_peak_observation_month(data) == "June"


def test_latitude_range():
    data = pd.DataFrame({"latitude": [10, 20, -5]})
    assert get_latitude_range(data) == 25
