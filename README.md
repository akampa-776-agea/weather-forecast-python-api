
# Weather Forecast with Python Web APIs

## 1. Project Overview

The Weather Forecast application is a Python-based project that retrieves weather forecasts from public web APIs, processes the data, calculates summary statistics, and visualizes daily weather conditions.

Users can search for a city, select a matching location, choose the forecast duration, and view the forecast and its summary.

## 2. Objectives

- Integrate Python with public web APIs.
- Retrieve geographic coordinates using a geocoding API.
- Fetch daily weather forecasts for selected locations.
- Process API responses using Pandas.
- Calculate descriptive weather statistics.
- Visualize temperature and precipitation patterns.
- Apply Object-Oriented Programming project organization and modular Python development.
- Validate inputs and handle API errors.
- Test application functions using Pytest.

## 3. Technologies Used

- Python
- Requests
- Pandas
- Matplotlib
- Pytest
- Open-Meteo Geocoding API
- Open-Meteo Forecast API

## 4. Project Structure

```text
Mini-Project 1 Weather Forecast with Python Web APIs/
│
├── src/
│   └── weather_forecast/
│       ├── __init__.py
│       ├── api_client.py
│       ├── app.py
│       ├── forecast.py
│       ├── geocoding.py
│       └── visualization.py
│
├── tests/
│   └── test_weather.py
│
├── sample_data/
│   ├── forecast_sample.json
│   └── geocoding_sample.json
│
├── notebooks/
├── README.md
└── requirements.txt
```

## 5. Features

### Location Search
Search for a city or place and select a matching location using its geographic details.

### Weather Forecast Retrieval
Retrieve daily maximum and minimum temperatures, precipitation, maximum wind speed, and weather codes.

### Data Processing
Transform API responses into a Pandas DataFrame and convert weather codes into readable descriptions.

### Summary Statistics
Identify the warmest day, coldest night, wettest day, total forecast precipitation, and average daily maximum temperature.

### Visualization
Plot maximum and minimum temperatures alongside daily precipitation.

### Error Handling
Validate user inputs and handle common API request failures using a shared HTTP client.

### Automated Testing
Use Pytest to check data processing, input validation, weather-code decoding, and other core functions.

## 6. Installation

Ensure Python is installed on your computer.

Clone or download the project repository and navigate to its root directory.

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## 7. Running the Application

From the project root, run:

```bash
python -m src.weather_forecast.app
```

Follow the prompts to:

1. Enter a city or place name.
2. Select the correct location.
3. Choose a forecast duration between 1 and 16 days.
4. Review the daily forecast and summary.
5. Choose whether to display the chart.

An internet connection is required to retrieve live weather data.

## 8. Running the Tests

Run the automated tests from the project root:

```bash
python -m pytest tests/test_weather.py -v
```

The test suite uses saved JSON samples for offline testing of core data-processing functionality.

## 9. Data Sources

- Geocoding API: https://geocoding-api.open-meteo.com/v1/search
- Weather Forecast API: https://api.open-meteo.com/v1/forecast

Weather data availability and forecasts are subject to the API provider's service and data coverage.

## 10. Limitations

- Forecast accuracy depends on the underlying weather model and forecast horizon.
- Internet access is required for live API requests.
- Location search can return multiple places with similar names, so users must select the intended location.
- Offline tests use saved sample responses and do not guarantee that live API services are available.

## 11. Future Improvements

- Improve location ranking and matching.
- Add weather alerts and recommendations.
- Include historical weather comparisons.
- Add more extensive automated tests for API failures and application workflows.
- Develop a graphical or web-based user interface.

## 12. Author

Developed as a Python mini-project to practise web API integration, data processing, visualization, modular programming, and automated testing.

verified: Get-Content .\README.md -TotalCount 20