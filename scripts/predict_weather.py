import pandas as pd
import joblib
import time
from datetime import datetime

# Load trained model
model = joblib.load("model.pkl")

# Define thresholds for alerts
THRESHOLDS = {
    "rain": 5.0,            # mm
    "cloudcover": 80.0,     # %
    "windspeed": 30.0       # km/h
}

def load_latest_drone_log(filepath="drone_log.csv"):
    """
    Load the latest drone log entry (assumes time-sorted CSV).
    """
    df = pd.read_csv(filepath, parse_dates=["time"])
    df = df.dropna()
    latest = df.iloc[-1]

    # Extract input features matching training
    features = pd.DataFrame([{
        "temperature_2m": latest["temperature_2m"],
        "relative_humidity_2m": latest["relative_humidity_2m"],
        "rain": latest["rain"],
        "cloudcover": latest["cloudcover"],
        "windspeed_10m": latest["windspeed_10m"],
        "hour": latest["time"].hour,
        "dayofweek": latest["time"].dayofweek
    }])
    
    return features, latest["time"]

def issue_warnings(predictions):
    rain, _, _, cloud, wind = predictions[0]
    messages = []
    if rain > THRESHOLDS["rain"]:
        messages.append(f"⚠️ Heavy Rainfall Predicted: {rain:.1f} mm")
    if cloud > THRESHOLDS["cloudcover"]:
        messages.append(f"☁️ High Cloud Cover: {cloud:.0f}%")
    if wind > THRESHOLDS["windspeed"]:
        messages.append(f"💨 Strong Winds: {wind:.1f} km/h")

    if messages:
        print("\n🚨 WEATHER ALERT FOR NEXT 3 HOURS:")
        for msg in messages:
            print(" -", msg)
    else:
        print("✅ Weather looks good for next 3 hours.")

def main_loop():
    while True:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running weather prediction...")
        
        try:
            features, log_time = load_latest_drone_log()
            predictions = model.predict(features)

            # Print predictions
            print(f"\n📡 Forecast for {log_time + pd.Timedelta(hours=3)}:")
            print(f"🌡️ Temp: {predictions[0][0]:.1f}°C")
            print(f"💧 Humidity: {predictions[0][1]:.1f}%")
            print(f"🌧️ Rainfall: {predictions[0][2]:.1f} mm")
            print(f"☁️ Cloud Cover: {predictions[0][3]:.1f}%")
            print(f"💨 Wind Speed: {predictions[0][4]:.1f} km/h")

            # Check for alerts
            issue_warnings(predictions)

        except Exception as e:
            print("❌ Error during prediction:", e)

        print("\n⏳ Waiting 5 minutes before next prediction...")
        time.sleep(300)  # 5 minutes

# Start the loop
if __name__ == "__main__":
    main_loop()