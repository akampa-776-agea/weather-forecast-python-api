# Plot temperatures and precipitation.

"""Visualization functions for daily weather forecasts."""

import matplotlib.pyplot as plt
import pandas as pd


def plot_forecast(df: pd.DataFrame) -> None:
    """Plot maximum/minimum temperatures and daily precipitation."""

    if df.empty:
        raise ValueError("Cannot plot an empty forecast.")

    required_columns = [ "Date", "Max Temperature (°C)", "Min Temperature (°C)", "Precipitation (mm)",]

    missing = [column for column in required_columns if column not in df.columns ]

    if missing:
        raise ValueError( f"Forecast DataFrame is missing columns: {missing}")

    dates = pd.to_datetime(df["Date"])

    fig, ax1 = plt.subplots(figsize=(11, 6))

    ax1.plot( dates, df["Max Temperature (°C)"], marker="o", label="Maximum temperature (°C)",)

    ax1.plot(dates, df["Min Temperature (°C)"],  marker="o", label="Minimum temperature (°C)",)

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("Daily Weather Forecast")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.bar( dates, df["Precipitation (mm)"],  alpha=0.25, label="Precipitation (mm)", width=0.5, )
    ax2.set_ylabel("Precipitation (mm)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend( lines1 + lines2,  labels1 + labels2, loc="upper left",)

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
# Test: python -c "from src.weather_forecast.forecast import get_forecast, forecast_to_dataframe; from src.weather_forecast.visualization import plot_forecast; data = get_forecast(51.05089, 13.73832, days=3); df = forecast_to_dataframe(data); plot_forecast(df); print('Visualization test completed.')"