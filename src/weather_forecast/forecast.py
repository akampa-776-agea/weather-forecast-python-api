# Fetch forecasts, create tables, decode weather codes and calculate summaries.

"""Weather forecast retrieval, parsing, and summary functions."""

from typing import Any

import pandas as pd

from .api_client import request_json


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

DAILY_FIELDS = [ "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max", "weather_code",]

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_forecast( lat: float, lon: float, days: int = 7,) -> dict[str, Any]:
    """Retrieve daily weather forecasts for a geographic location."""

    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180.")

    if isinstance(days, bool) or not isinstance(days, int) or not 1 <= days <= 16:
        raise ValueError("Days must be an integer between 1 and 16.")

    params = { "latitude": lat, "longitude": lon, "daily": ",".join(DAILY_FIELDS), "timezone": "auto", "forecast_days": days,}

    return request_json( FORECAST_URL, params=params, timeout=15, max_retries=3,)


def decode_weather_code(code: int) -> str:
    """Convert a WMO weather code into a readable description."""

    return WEATHER_CODES.get(code, "Unknown weather condition")


def forecast_to_dataframe( forecast_data: dict[str, Any],) -> pd.DataFrame:
    """Convert the API daily forecast response into a DataFrame."""

    if "daily" not in forecast_data:
        raise ValueError("Forecast data is missing the daily section.")

    daily = forecast_data["daily"]
    required_fields = ["time", *DAILY_FIELDS]

    missing = [field for field in required_fields if field not in daily]
    if missing:
        raise ValueError(f"Forecast data is missing fields: {missing}")

    lengths = {field: len(daily[field]) for field in required_fields}
    if len(set(lengths.values())) != 1:
        raise ValueError("Forecast daily fields have inconsistent lengths.")

    df = pd.DataFrame({
        "Date": daily["time"],
        "Max Temperature (°C)": daily["temperature_2m_max"],
        "Min Temperature (°C)": daily["temperature_2m_min"],
        "Precipitation (mm)": daily["precipitation_sum"],
        "Max Wind Speed (km/h)": daily["wind_speed_10m_max"],
        "Weather Code": daily["weather_code"],
    })

    df["Weather Description"] = df["Weather Code"].apply(decode_weather_code)

    return df


def summarize_forecast(df: pd.DataFrame) -> dict[str, Any]:
    """Calculate key statistics from a forecast DataFrame."""

    if df.empty:
        raise ValueError("Cannot summarize an empty forecast.")

    warmest_index = df["Max Temperature (°C)"].idxmax()
    coldest_index = df["Min Temperature (°C)"].idxmin()
    wettest_index = df["Precipitation (mm)"].idxmax()

    return {
        "forecast_start": df["Date"].iloc[0],
        "forecast_end": df["Date"].iloc[-1],
        "warmest_day": df.loc[warmest_index, "Date"],
        "warmest_temperature_c": df.loc[
            warmest_index, "Max Temperature (°C)"
        ],
        "coldest_night": df.loc[coldest_index, "Date"],
        "coldest_temperature_c": df.loc[
            coldest_index, "Min Temperature (°C)"
        ],
        "wettest_day": df.loc[wettest_index, "Date"],
        "wettest_precipitation_mm": df.loc[
            wettest_index, "Precipitation (mm)"
        ],
        "total_precipitation_mm": df["Precipitation (mm)"].sum(),
        "average_max_temperature_c": df["Max Temperature (°C)"].mean(),
    }

# test python -c "from src.weather_forecast.forecast import get_forecast, forecast_to_dataframe, summarize_forecast; data = get_forecast(51.05089, 13.73832, days=3); df = forecast_to_dataframe(data); print(df.to_string(index=False)); print('\nSummary:', summarize_forecast(df))"
# results
# 1. Forecast table
# function successfully retrieved three days of weather data for Dresden, Germany.
# - 18 October: Maximum 12.5°C, minimum 9.3°C, overcast.
# - 19 October: Maximum 12.1°C, minimum 5.8°C, overcast.
# - 20 October: Warmest day at 14.0°C, with fog reported.


# 2. Summary statistics
# The wettest day is reported as 18 October because all three days have zero precipitation. When values tie, pandas returns the first matching row; this is expected.


class WeatherForecaster:
    """Manage weather forecast retrieval and analysis for one location."""

    def __init__( self, latitude: float, longitude: float, days: int = 7, ) -> None:
        """Initialize a forecaster with validated location and forecast settings."""
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")

        if (  isinstance(days, bool) or not isinstance(days, int)or not 1 <= days <= 16):
            raise ValueError("Days must be an integer between 1 and 16.")

        self.latitude: float = latitude
        self.longitude: float = longitude
        self.days: int = days
        self.forecast_data: dict[str, Any] | None = None

    def fetch_forecast(self) -> dict[str, Any]:
        """Retrieve and store forecast data for this location."""
        self.forecast_data = get_forecast( lat=self.latitude,  lon=self.longitude, days=self.days,)
        return self.forecast_data

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the stored forecast into a DataFrame."""
        if self.forecast_data is None:
            raise RuntimeError( "No forecast data available. Call fetch_forecast() first.")

        return forecast_to_dataframe(self.forecast_data)

    def summarize(self) -> dict[str, Any]:
        """Return summary statistics for the stored forecast."""
        forecast_df = self.to_dataframe()
        return summarize_forecast(forecast_df)
# class WeatherForecaster adds:
# 1. Attributes: location, forecast duration, and stored forecast data.
# 2. Methods: fetch, transform, and summarize.
# Encapsulation: forecast configuration and retrieved data are managed together in one object.
# Composition/reuse: the class delegates work to your existing tested functions instead of duplicating their logic.
# Type hints and docstrings: included throughout.
# python -c "import json; from pathlib import Path; from src.weather_forecast.forecast import WeatherForecaster; data = json.loads(Path('sample_data/forecast_sample.json').read_text(encoding='utf-8')); w = WeatherForecaster(0.31628, 32.58219, 3); w.forecast_data = data; print('Location:', w.latitude, w.longitude); print('Forecast days:', len(w.to_dataframe())); print('Summary:', w.summarize())"
# these results come from the sample dataset, not a live forecast for Kampala.