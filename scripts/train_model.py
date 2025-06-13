import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv("historical_hourly_data.csv", parse_dates=["time"])
df = df.dropna()

# Time-based target shift (forecast 3 hours ahead)
forecast_horizon = 3  # in hours
for target in ["temperature_2m", "relative_humidity_2m", "rain", "cloudcover", "windspeed_10m"]:
    df[f"{target}_future"] = df[target].shift(-forecast_horizon)

# Drop final rows with NaNs after shift
df = df.dropna()

# Optional: Extract time features (hour, day)
df["hour"] = df["time"].dt.hour
df["dayofweek"] = df["time"].dt.dayofweek

# Feature columns (current values + time features)
features = [
    "temperature_2m", "relative_humidity_2m", "rain",
    "cloudcover", "windspeed_10m", "hour", "dayofweek"
]
X = df[features]

# Target columns: 3-hour future values
targets = [
    "temperature_2m_future", "relative_humidity_2m_future",
    "rain_future", "cloudcover_future", "windspeed_10m_future"
]
y = df[targets]

# Split for validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# XGBoost multi-output regression
model = MultiOutputRegressor(xgb.XGBRegressor(n_estimators=100, max_depth=5, random_state=42))
model.fit(X_train, y_train)

# Evaluation
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
print(f"Model trained — MSE: {mse:.4f}")

# Save model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
