# 🌫️ Air Quality Prediction System

## 📌 Overview
This project uses real-time weather data from OpenWeatherMap API and a trained machine learning model (Random Forest) to predict PM2.5 air pollution levels.

## 🔧 Tech Stack
- Python
- RandomForestRegressor
- OpenWeatherMap API
- scikit-learn, pandas, joblib, requests

## 📁 Project Structure
- `train_model.py`: Train and save model from historical weather data
- `main.py`: Fetch current weather and predict PM2.5
- `model.pkl`: Trained model file
- `data.csv`: Input dataset
- `requirements.txt`: Dependencies

## ▶️ How to Use
```bash
pip install -r requirements.txt
python train_model.py   # To train and save model
python main.py          # To predict PM2.5 using live data
```

## 📘 Notes
- Replace `data.csv` with your own dataset
- You need an API key from https://openweathermap.org/api

## 📜 License
MIT
"""

# -------------------------------------------------------------
# Sample data.csv (not full dataset)
# temp,humidity,wind_speed,pm25
# 25.3,45,2.3,55.2
# 19.6,60,1.0,40.1
# ...
