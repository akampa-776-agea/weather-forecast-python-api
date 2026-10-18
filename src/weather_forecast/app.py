# The application will connect the modules we have already tested: geocoding, forecast retrieval, summaries, and visualization.

"""Command-line application for weather forecasting."""

from .api_client import WeatherAPIError
from .forecast import ( get_forecast, forecast_to_dataframe,summarize_forecast,)
from .geocoding import geocode, choose_location
from .visualization import plot_forecast


def main():
    """Run the interactive weather forecasting application."""

    print("=" * 50)
    print("       WEATHER FORECAST APPLICATION")
    print("=" * 50)

    city = input("\nEnter a city or place name: ").strip()

    if not city:
        print("Error: City name cannot be empty.")
        return

    try:
        # Step 1: Search for the location.
        locations = geocode(city)
        location = choose_location(locations)

        if location is None:
            print("Location selection cancelled. Exiting.")
            return

        latitude = location["latitude"]
        longitude = location["longitude"]

        print( f"\nSelected location: {location['name']}, "  f"{location.get('country', 'Unknown')}" )
        print(f"Coordinates: {latitude}, {longitude}")

        # Step 2: Get the forecast duration.
        while True:
            days_input = input( "\nHow many forecast days? (1-16): " ).strip()

            try:
                days = int(days_input)
            except ValueError:
                print("Please enter a whole number.")
                continue

            if 1 <= days <= 16:
                break

            print("Enter a number between 1 and 16.")

        # Step 3: Retrieve and process the forecast.
        forecast_data = get_forecast( latitude,  longitude,  days=days, )

        forecast_df = forecast_to_dataframe(forecast_data)

        print("\nDAILY FORECAST")
        print("-" * 50)
        print(forecast_df.to_string(index=False))

        # Step 4: Display summary statistics.
        summary = summarize_forecast(forecast_df)

        print("\nFORECAST SUMMARY")
        print("-" * 50)
        print( f"Forecast period: {summary['forecast_start']} " f"to {summary['forecast_end']}" )
        print( f"Warmest day: {summary['warmest_day']} " f"({summary['warmest_temperature_c']:.1f} °C)" )
        print( f"Coldest night: {summary['coldest_night']} " f"({summary['coldest_temperature_c']:.1f} °C)" )
        print( f"Wettest day: {summary['wettest_day']} " f"({summary['wettest_precipitation_mm']:.1f} mm)")
        print( f"Total forecast precipitation: " f"{summary['total_precipitation_mm']:.1f} mm" )
        print( f"Average daily maximum temperature: " f"{summary['average_max_temperature_c']:.1f} °C" )

        # Step 5: Plot the forecast.
        show_chart = input( "\nDisplay the forecast chart? (y/n): ").strip().lower()
        if show_chart == "y": plot_forecast(forecast_df)

        print("\nWeather forecast completed successfully.")

    except WeatherAPIError as error:
        print(f"\nWeather API error: {error}")

    except (KeyError, TypeError, ValueError) as error:
        print(f"\nUnable to process the forecast: {error}")


if __name__ == "__main__":
    main()
# Test:python -m src.weather_forecast.app
# results
# 