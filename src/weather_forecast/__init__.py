# Expose the package functions cleanly.


"""Weather Forecast application package."""

from .api_client import WeatherAPIError, request_json
from .forecast import (
    WeatherForecaster,
    decode_weather_code,
    forecast_to_dataframe,
    get_forecast,
    summarize_forecast,
)
from .geocoding import choose_location, geocode
from .visualization import plot_forecast

__all__ = [
    "WeatherAPIError",
    "request_json",
    "WeatherForecaster",
    "geocode",
    "choose_location",
    "get_forecast",
    "decode_weather_code",
    "forecast_to_dataframe",
    "summarize_forecast",
    "plot_forecast",
]

# test: python -c "from src.weather_forecast import geocode, get_forecast, forecast_to_dataframe, summarize_forecast, plot_forecast, WeatherAPIError; print('All package imports passed.')"