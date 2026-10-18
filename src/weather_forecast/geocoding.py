# Find a location and retrieve its coordinates.

"""Location lookup using the Open-Meteo Geocoding API."""

from typing import Any

from .api_client import request_json


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode(name: str) -> list[dict[str, Any]]:
    """Return matching locations for a city or place name.

    Args:
        name: City or place to search for.

    Returns:
        A list of matching location dictionaries.

    Raises:
        ValueError: If the supplied city name is empty.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("City name cannot be empty.")

    params = { "name": name.strip(), "count": 10,"language": "en","format": "json", }

    data = request_json( GEOCODING_URL, params=params, timeout=15, max_retries=3,)

    return data.get("results", [])


def choose_location( locations: list[dict[str, Any]],) -> dict[str, Any] | None:
    """Let the user select one location from the search results."""

    if not locations:
        print("No matching locations found.")
        return None

    for index, location in enumerate(locations, start=1):
        name = location.get("name", "Unknown")
        admin = location.get("admin1", "")
        country = location.get("country", "Unknown")

        description = ", ".join( part for part in [name, admin, country] if part)

        print(f"{index}. {description}")

    while True:
        choice = input( "Select a location number, or enter 0 to cancel: " ).strip()

        try:
            number = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if number == 0:
            return None

        if 1 <= number <= len(locations):
            return locations[number - 1]

        print("Selection is out of range.")

# test: python -c "from src.weather_forecast.geocoding import geocode; results = geocode('Dresden'); print('Matches found:', len(results)); print('First match:', results[0]['name'], results[0]['country'])"
# The Open-Meteo Geocoding API returned 10 matching locations.
# The first result was Dresden, Germany.