import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

# Load and preprocess the dataset
DATA_PATH = "../data/merged_data.csv"
MODEL_PATH = "../models/weather_predictor.pkl"

print("[INFO] Loading dataset...")
data = pd.read_csv(DATA_PATH)

# Check for missing values
data.dropna(inplace=True)

# Separate features and targets
y_columns = [col for col in data.columns if col.startswith("target_")]
X = data.drop(columns=y_columns)
y = data[y_columns]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
print("[INFO] Training model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
print("[INFO] Evaluating model...")
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"MAE: {mae:.3f}, RMSE: {rmse:.3f}")

# Save the model and scaler
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump({"model": model, "scaler": scaler, "features": list(X.columns)}, MODEL_PATH)
print(f"[INFO] Model saved to {MODEL_PATH}")
