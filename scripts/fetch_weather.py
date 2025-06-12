import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../.env")

LAT = float(os.getenv("LAT", 28.6139))
LON = float(os.getenv("LON", 77.2090))
DAYS_BACK = int(os.getenv("DAYS_BACK", 1))
TIMEZONE = os.getenv("TIMEZONE", "UTC")
OUTPUT_PATH = "../data/weather_history.csv"

# Construct API request
print("[INFO] Fetching weather data from Open-Meteo...")
end = datetime.utcnow()
start = end - timedelta(days=DAYS_BACK)

url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={LAT}&longitude={LON}"
    f"&start_date={start.date()}&end_date={end.date()}"
    f"&hourly=temperature_2m,humidity_2m,wind_speed_10m,wind_direction_10m"
    f"&timezone={TIMEZONE}"
)

response = requests.get(url)
response.raise_for_status()
data = response.json()

df = pd.DataFrame(data["hourly"])
df["timestamp"] = pd.to_datetime(df["time"])
df.drop(columns=["time"], inplace=True)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)
print(f"[INFO] Weather history saved to {OUTPUT_PATH}")