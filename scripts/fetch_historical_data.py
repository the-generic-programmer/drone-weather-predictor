# fetch_historical_data.py
import requests
import pandas as pd

latitude = 10.8505
longitude = 76.2711
start_date = "2023-06-01"
end_date = "2025-06-01"
timezone = "auto"

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": ",".join([
        "temperature_2m", "relative_humidity_2m", "rain",
        "cloudcover", "windspeed_10m"
    ]),
    "daily": "sunrise,sunset",
    "timezone": timezone
}

response = requests.get(url, params=params)
data = response.json()

hourly_df = pd.DataFrame(data["hourly"])
hourly_df.to_csv("historical_hourly_data.csv", index=False)

print("✅ Saved as historical_hourly_data.csv")
