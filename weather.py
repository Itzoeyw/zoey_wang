import requests
import datetime
import json

# 1. Setup - Coordinates (e.g., Dublin)
LATITUDE = 53.3498
LONGITUDE = -6.2603
FILE_NAME = "weather_cache.json"

# 2. Get the date from the user
date_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

if not date_input:
    # If no date, calculate tomorrow's date
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    searched_date = tomorrow.strftime('%Y-%m-%d')
else:
    searched_date = date_input

# 3. Check the file first (the "Cache")
# We try to open the file to see if we already checked this date before
try:
    with open(FILE_NAME, "r") as file:
        cache = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    # If file doesn't exist yet, start with an empty dictionary
    cache = {}

# 4. Logic: Decide whether to call the API or use the file
if searched_date in cache:
    print(f"(Using saved data for {searched_date})")
    precipitation = cache[searched_date]
else:
    # Build the URL with the parameters
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

    try:
        response = requests.get(url)
        data = response.json()

        # Extract the precipitation value from the API response
        # The API returns a list, so we take the first item [0]
        precipitation = data.get('daily', {}).get('precipitation_sum', [None])[0]

        # Save this new result into our cache dictionary
        cache[searched_date] = precipitation

        # Write the updated cache back to the file
        with open(FILE_NAME, "w") as file:
            json.dump(cache, file)

    except Exception as e:
        print(f"Error connecting to API: {e}")
        precipitation = -1  # Mark as error

# 5. Check the result and print for the user
if precipitation is None or precipitation < 0:
    print("I don't know.")
elif precipitation > 0.0:
    print(f"It will rain! Precipitation: {precipitation}mm")
else:
    print("It will not rain.")