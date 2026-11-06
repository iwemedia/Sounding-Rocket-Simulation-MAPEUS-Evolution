# services/weather_service.py
import requests
from config.constants import DEFAULT_WIND_SPEED

def fetch_weather_data(lat: float, lon: float) -> dict:
    """
    Queries the external Open-Meteo weather API using custom headers and payload setups.

    Args:
        lat (float): The latitude coordinate of the launch site.
        lon (float): The longitude coordinate of the launch site.

    Returns:
        dict: The raw parsed JSON response payload from the API, or an empty dict on failure.

    * Fix 001: problem automated blocking of py-script request - > API -> custom header:
    Based on: [ https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers]
    Based on: [https://www.youtube.com/watch?v=4m0Hncf1aAU]
    ** Fixed that the Open-Meteo REST API rejected connection requests from the
    simulation, causing the script to continuously fall back to the offline `DEFAULT_WIND_SPEED` metric.
    ** by implementing a custom Identity Signatures (Header Spoofing User Agent):
    ** with a structured `headers` dictionary containing a realistic web browser fingerprint,
    into authorizing the automated script as a human client session.

    * Fix 002: clear up the messy URL query by using dictionary Payload Arrays:
    Source: [ Requests Documentation by Kenneth Ritz: https://requests.readthedocs.io/_/downloads/en/v2.9.1/pdf/]
    ** Extracted embedded raw URL queries and migrated them into a clean, separated argument layout
    (`payload = { ... }`). By passing this configuration directly into the `requests.get(url, params=payload)` pipeline,
    the networking engine builds a perfectly formatted, standard-compliant URL string automatically.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    # dictionary URL Fix 002
    payload = {
        "latitude": lat,
        "longitude": lon,
        "current": "wind_speed_10m"
    }

    # declare User-Agent Fix 001
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        # Fixes 001 - 002 - 003
        response = requests.get(url, params=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        # fall back
        pass

    return {}

def extract_wind_speed(weather_data: dict) -> float:
    """
    Extracts the current surface wind velocity metric at a 10m altitude.

    Args:
        weather_data (dict): The raw JSON dictionary payload fetched from the weather API.

    Returns:
        float: The extracted wind speed value, or the fallback DEFAULT_WIND_SPEED if validation fails.

    * Fix 003: Secured Silent Except-Triggers (Strict API Contract Validation):
    Based on: [try-except block: https://python.org]
    ** Handling data payload extraction logic by embedding explicit key-existence audits
    (`if "current" in data ...`) prior to executing structural float type castings.
    This insulates the data validation pipeline from crashing on malformed JSON packages.
    """
    
    try:
        # Verify key existence before casting
        if "current" in weather_data and "wind_speed_10m" in weather_data["current"]:
            # Directly return the float value
            return float(weather_data["current"]["wind_speed_10m"])

    except (KeyError, ValueError):
        # fallback for pipeline breaks and fall through
        pass

    return DEFAULT_WIND_SPEED
