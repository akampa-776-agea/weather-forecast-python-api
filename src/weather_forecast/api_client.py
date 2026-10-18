#HTTP requests, timeouts, retries and custom exceptions.

"""Shared HTTP client for weather API requests."""

import time
from typing import Any

import requests


class WeatherAPIError(Exception):
    """Raised when a weather API request fails."""


def request_json(url: str, params: dict[str, Any],  timeout: float = 15, max_retries: int = 3,) -> dict[str, Any]:
    """Request JSON with bounded retries for transient failures."""

    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    if max_retries < 0:
        raise ValueError("max_retries cannot be negative.")

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout,)

            # Retry rate-limit and server errors.
            if response.status_code == 429 or response.status_code >= 500:
                response.raise_for_status()

            response.raise_for_status()
            return response.json()

        except (requests.ConnectionError, requests.Timeout) as exc:
            error = exc

        except requests.HTTPError as exc:
            status = ( exc.response.status_code if exc.response is not None else None )

            # Do not retry ordinary client errors.
            if status != 429 and (status is None or status < 500):
                raise WeatherAPIError( f"Weather API returned HTTP error: {status}") from exc

            error = exc

        except requests.RequestException as exc:
            raise WeatherAPIError(  f"Weather API request failed: {exc}"  ) from exc

        except ValueError as exc:
            raise WeatherAPIError(  "Weather API returned invalid JSON."  ) from exc

        if attempt < max_retries:
            delay = 2 ** attempt
            print(  f"Request failed ({error}). " f"Retrying in {delay} second(s)..." )
            time.sleep(delay)

    raise WeatherAPIError(f"Weather API request failed after "f"{max_retries + 1} attempts: {error}" ) from error
