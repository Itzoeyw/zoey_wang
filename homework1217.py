import json
import requests
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, cache_file="forecasts.json"):
        self.cache_file = cache_file
        self.data = self._load_cache()

    def _load_cache(self):
        """Loads the saved forecasts from a JSON file."""
        try:
            with open(self.cache_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_cache(self):
        """Saves the current data dictionary to a JSON file."""
        with open(self.cache_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def _fetch_from_api(self, date):
        """Fetches precipitation data from Open-Meteo API."""
        # Default coordinates (e.g., London), can be adjusted
        latitude = 51.5074
        longitude = -0.1278

        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
            f"&daily=precipitation_sum&timezone=Europe%2FLondon"
            f"&start_date={date}&end_date={date}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            return "Unknown (API Error)"

        data = response.json()
        precipitation = data.get("daily", {}).get("precipitation_sum", [0])[0]

        if precipitation > 0:
            return "It will rain"
        elif precipitation == 0:
            return "It will not rain"
        else:
            return "Unknown"

    def __setitem__(self, date, forecast):
        """Allows weather_forecast[date] = forecast"""
        self.data[date] = forecast
        self._save_cache()

    def __getitem__(self, date):
        """Allows forecast = weather_forecast[date]"""
        # If date is not in our dictionary, fetch it from API
        if date not in self.data:
            print(f"Fetching data for {date} from the internet...")
            forecast = self._fetch_from_api(date)
            self.__setitem__(date, forecast)  # Save via __setitem__ logic

        return self.data[date]

    def __iter__(self):
        """Allows iterating over the dates: for date in weather_forecast"""
        return iter(self.data)

    def items(self):
        """Returns a generator of (date, weather) tuples."""
        for date, weather in self.data.items():
            yield date, weather


# --- Usage Example ---

if __name__ == "__main__":
    weather_forecast = WeatherForecast()

    # Get a date from the user (Defaulting to tomorrow for testing)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_input = input(f"Enter a date (YYYY-MM-DD) [Default {tomorrow}]: ") or tomorrow

    # 1. Use [date] to trigger __getitem__
    # This will check the file first, then the API if missing.
    result = weather_forecast[date_input]
    print(f"Forecast for {date_input}: {result}")

    # 2. Use __iter__ to list all known dates
    print("\nAll dates currently in history:")
    for date in weather_forecast:
        print(f"- {date}")

    # 3. Use .items() to show saved results
    print("\nFull breakdown (Date: Result):")
    for date, forecast in weather_forecast.items():
        print(f"{date}: {forecast}")