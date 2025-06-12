Drone-Based Microclimate Weather Predictor
This project leverages drone flight data and weather APIs to predict microclimatic conditions and drone flying suitability using machine learning. It includes a full pipeline from data collection to prediction and visualization.

Features
ROS2-based drone telemetry logger

Real-time weather data integration (Open-Meteo API)

Historical weather data collection for model training

Data preprocessing with timestamp alignment

Machine learning model for weather condition predictions

CLI pipeline automation

Forecast API integration for flight planning

Dashboard-ready output formats

Directory Structure
bash
drone-weather-predictor/
│
├── data/                   # Data storage
├── models/                 # Trained models
├── scripts/
│   ├── drone_listener.py   # ROS2 node
│   ├── fetch_weather.py    # Weather data fetcher
│   ├── forecast_pipeline.py# Forecast integration
│   ├── preprocess_data.py  # Data merger
│   ├── train_model.py      # Model trainer 
│   ├── predict.py          # Prediction script
│   └── run_pipeline.py     # Automation script (planned)
│
├── .env                    # Configuration
├── README.md               # Documentation
└── requirements.txt        # Dependencies
Requirements
Python 3.8+

ROS2 Humble (installation guide)

Required packages: pip install -r requirements.txt

Getting Started
Clone repository

Configure location in .env:

bash
LAT=28.6139
LON=77.2090
DAYS_BACK=1
TIMEZONE=UTC
Install ROS2 dependencies

Run drone_listener.py for telemetry collection

Workflow Pipeline
Collect drone logs via ROS2 node → data/drone_logs.csv

Fetch historical weather data → data/weather_history.csv

Retrieve weather forecast → data/forecast_weather.csv

Preprocess and merge datasets → data/merged_data.csv

Train prediction model → models/ (one-time setup)

Generate predictions using predict.py

Visualization
Connect BI tools like Metabase to the data/ directory for:

Predicted vs actual weather comparisons

Drone performance metrics

Microclimate trend analysis

Roadmap
 Core data pipeline implementation

 Machine learning integration

 CLI automation (run_pipeline.py)

 Battery life prediction module

 Dashboard deployment guide

Contributing
We welcome contributions through pull requests. Please read our CONTRIBUTING.md before submitting changes.

License
Apache License 2.0

Author
Aaditya Singh – 2025
Built with Open-Meteo, ROS2, Scikit-Learn, and pandas