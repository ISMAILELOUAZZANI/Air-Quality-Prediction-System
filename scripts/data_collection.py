import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

# API key and cities
API_KEY = "d1e0a3311c8efb56b7308be90f3d8d27"  #  API key
CITIES = ["Casablanca", "Rabat", "Marrakech"]
BASE_URL_AIR = "http://api.openweathermap.org/data/2.5/air_pollution"
BASE_URL_WEATHER = "http://api.openweathermap.org/data/2.5/weather"
OUTPUT_FILE = "data/air_quality_data.csv"

def collect_data():
    data = []
    current_time = datetime.now()
    for city in CITIES:
        print(f"Processing data for {city} at {current_time}")
        coords = {
            "Casablanca": {"lat": 33.5731, "lon": -7.5898},
            "Rabat": {"lat": 34.0209, "lon": -6.8416},
            "Marrakech": {"lat": 31.6295, "lon": -7.9811}
        }
        lat, lon = coords[city]["lat"], coords[city]["lon"]

        air_params = {"lat": lat, "lon": lon, "appid": API_KEY}
        air_response = requests.get(BASE_URL_AIR, params=air_params)
        print(f"API response for {city}: Status code {air_response.status_code}")
        if air_response.status_code == 200:
            air_data = air_response.json()
            for entry in air_data.get("list", []):
                timestamp = datetime.fromtimestamp(entry["dt"])
                weather_params = {"lat": lat, "lon": lon, "appid": API_KEY}
                weather_response = requests.get(BASE_URL_WEATHER, params=weather_params)
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    data.append({
                        "city": city,
                        "timestamp": timestamp,
                        "pm2.5": entry["components"]["pm2_5"],
                        "aqi": entry["main"]["aqi"],
                        "temperature": weather_data["main"]["temp"] - 273.15,  # Kelvin to Celsius
                        "humidity": weather_data["main"]["humidity"],
                        "pressure": weather_data["main"]["pressure"],
                        "wind_speed": weather_data["wind"]["speed"]
                    })
        else:
            print(f"Failed to get data for {city}: {air_response.text}")

    # Append to existing data
    if os.path.exists(OUTPUT_FILE):
        existing_df = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([existing_df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)
    df.drop_duplicates(subset=["city", "timestamp"], inplace=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data appended to {OUTPUT_FILE} at {current_time}")

if __name__ == "__main__":
    while True:  # Run indefinitely until stopped with Ctrl+C
        collect_data()
        time.sleep(1800)  # Wait 30 minutes (1800 seconds)