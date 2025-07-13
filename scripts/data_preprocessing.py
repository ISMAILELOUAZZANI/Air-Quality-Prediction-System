import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_path="data/air_quality_data.csv", output_path="data/preprocessed_data.csv"):
    # Load data and validate
    try:
        df = pd.read_csv(input_path)
        if df.empty:
            raise ValueError("Input data is empty")
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

    # Validate required columns
    required_columns = ["timestamp", "city", "temperature", "humidity", "pressure", "wind_speed", "pm2.5", "aqi"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Handle timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Handle missing values more effectively
    # First fill with median for numerical columns
    numerical_cols = ["temperature", "humidity", "pressure", "wind_speed", "pm2.5", "aqi"]
    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
    
    # Then drop any remaining rows with missing values
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(subset=["city", "timestamp"], inplace=True)

    # Encode categorical features
    df = pd.get_dummies(df, columns=["city"], prefix="city")

    # Normalize numerical features
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Select target variables
    # For regression: PM2.5
    # For classification: AQI class using EPA standards
    def classify_aqi(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Moderate"
        elif aqi <= 150: return "Unhealthy for Sensitive Groups"
        elif aqi <= 200: return "Unhealthy"
        elif aqi <= 300: return "Very Unhealthy"
        else: return "Hazardous"
    
    df["aqi_class"] = df["aqi"].apply(classify_aqi)
    df["pm2.5"] = df["pm2.5"]  # Keep PM2.5 for regression tasks

    # Save preprocessed data
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")
    return df

if __name__ == "__main__":
    preprocess_data()