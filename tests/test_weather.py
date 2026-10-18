# Automated tests using saved JSON samples, including offline tests.

"""Offline tests for the weather forecast application."""

import json
from pathlib import Path

import pandas as pd
import pytest

from src.weather_forecast import (
    WeatherAPIError,
    decode_weather_code,
    forecast_to_dataframe,
    geocode,
    get_forecast,
    request_json,
    summarize_forecast,
)


SAMPLE_DIR = Path("sample_data")


@pytest.fixture
def forecast_sample():
    """Load the saved forecast response."""
    with open(
        SAMPLE_DIR / "forecast_sample.json",
        encoding="utf-8",
    ) as file:
        return json.load(file)


@pytest.fixture
def geocoding_sample():
    """Load the saved geocoding response."""
    with open(
        SAMPLE_DIR / "geocoding_sample.json",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_geocoding_sample_contains_coordinates(geocoding_sample):
    locations = geocoding_sample["results"]

    assert locations
    assert "latitude" in locations[0]
    assert "longitude" in locations[0]


def test_forecast_sample_has_three_days(forecast_sample):
    assert len(forecast_sample["daily"]["time"]) == 3


def test_forecast_fields_have_matching_lengths(forecast_sample):
    daily = forecast_sample["daily"]
    expected_length = len(daily["time"])

    for field in [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
        "weather_code",
    ]:
        assert len(daily[field]) == expected_length


def test_forecast_parses_into_dataframe(forecast_sample):
    df = forecast_to_dataframe(forecast_sample)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "Weather Description" in df.columns


def test_weather_code_decoding():
    assert decode_weather_code(0) == "Clear sky"
    assert decode_weather_code(3) == "Overcast"
    assert decode_weather_code(61) == "Slight rain"
    assert decode_weather_code(999) == "Unknown weather condition"


def test_forecast_summary_values(forecast_sample):
    df = forecast_to_dataframe(forecast_sample)
    summary = summarize_forecast(df)

    assert summary["forecast_start"] == df["Date"].iloc[0]
    assert summary["forecast_end"] == df["Date"].iloc[-1]
    assert summary["total_precipitation_mm"] == pytest.approx(
        df["Precipitation (mm)"].sum()
    )


def test_empty_city_name_is_rejected():
    with pytest.raises(ValueError, match="City name cannot be empty"):
        geocode("   ")


@pytest.mark.parametrize(
    ("latitude", "longitude", "days"),
    [
        (100, 13.7, 3),
        (51.05, 200, 3),
        (51.05, 13.7, 0),
    ],
)
def test_invalid_forecast_inputs_are_rejected(
    latitude,
    longitude,
    days,
):
    with pytest.raises(ValueError):
        get_forecast(latitude, longitude, days)


def test_request_timeout_validation():
    with pytest.raises(ValueError, match="Timeout must be greater than zero"):
        request_json("https://example.com", {}, timeout=0)


def test_negative_retry_count_is_rejected():
    with pytest.raises(ValueError, match="max_retries cannot be negative"):
        request_json("https://example.com", {}, max_retries=-1)


def test_custom_api_exception_exists():
    error = WeatherAPIError("Test error")
    assert str(error) == "Test error"
