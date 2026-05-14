"""
Synthetic Indian environmental data generator for VaayuVigyaan AI
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Major Indian cities with coordinates and base pollution levels
CITY_DATA = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "base_pm25": 180, "state": "Delhi"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "base_pm25": 85, "state": "Maharashtra"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "base_pm25": 70, "state": "Maharashtra"},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "base_pm25": 55, "state": "Karnataka"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "base_pm25": 130, "state": "West Bengal"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "base_pm25": 60, "state": "Tamil Nadu"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "base_pm25": 75, "state": "Telangana"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "base_pm25": 110, "state": "Gujarat"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "base_pm25": 155, "state": "Uttar Pradesh"},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "base_pm25": 165, "state": "Bihar"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "base_pm25": 120, "state": "Rajasthan"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "base_pm25": 95, "state": "Chandigarh"},
}


def get_seasonal_factor(month):
    """Return pollution multiplier based on season (higher in winter)."""
    factors = {1: 1.6, 2: 1.5, 3: 1.2, 4: 1.0, 5: 0.9, 6: 0.7,
               7: 0.6, 8: 0.65, 9: 0.75, 10: 1.1, 11: 1.4, 12: 1.6}
    return factors.get(month, 1.0)


def generate_historical_data(days=365):
    """Generate 365 days of historical PM2.5 data for all cities."""
    np.random.seed(42)
    records = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    for city, info in CITY_DATA.items():
        for i in range(days):
            date = start_date + timedelta(days=i)
            seasonal = get_seasonal_factor(date.month)
            # Add day-of-week effect (weekdays slightly higher due to traffic)
            dow_factor = 1.05 if date.weekday() < 5 else 0.92
            base = info["base_pm25"] * seasonal * dow_factor
            # Add realistic noise
            pm25 = max(5, base + np.random.normal(0, base * 0.2))
            aqi = pm25_to_aqi(pm25)
            records.append({
                "date": date.date(),
                "city": city,
                "state": info["state"],
                "lat": info["lat"],
                "lon": info["lon"],
                "pm25": round(pm25, 1),
                "aqi": round(aqi, 0),
                "temperature": round(25 + 10 * np.sin((date.month - 4) * np.pi / 6) + np.random.normal(0, 2), 1),
                "humidity": round(60 - 20 * np.sin((date.month - 6) * np.pi / 6) + np.random.normal(0, 8), 1),
                "wind_speed": round(max(0.5, np.random.exponential(3)), 1),
                "rainfall": round(max(0, np.random.exponential(2) if date.month in [6,7,8,9] else np.random.exponential(0.3)), 1),
            })
    return pd.DataFrame(records)


def generate_training_data(n=5000):
    """Generate synthetic training data for XGBoost model."""
    np.random.seed(42)
    temp = np.random.uniform(15, 45, n)
    humidity = np.random.uniform(20, 95, n)
    wind_speed = np.random.exponential(3, n)
    wind_speed = np.clip(wind_speed, 0.5, 15)
    rainfall = np.random.exponential(1, n)
    rainfall = np.clip(rainfall, 0, 50)
    aod = np.random.uniform(0.05, 1.2, n)
    traffic = np.random.uniform(0, 100, n)
    industrial = np.random.uniform(0, 100, n)
    season = np.random.choice([0.7, 1.0, 1.3, 1.6], n)  # summer, monsoon, post-monsoon, winter

    # Realistic PM2.5 formula
    pm25 = (
        aod * 180
        + (100 - humidity) * 0.4
        + traffic * 0.8
        + industrial * 1.1
        - wind_speed * 8
        - rainfall * 5
        + temp * 0.5
        + (season - 1) * 40
        + np.random.normal(0, 15, n)
    )
    pm25 = np.clip(pm25, 5, 500)

    return pd.DataFrame({
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rainfall": rainfall,
        "aod": aod,
        "traffic_intensity": traffic,
        "industrial_activity": industrial,
        "pm25": pm25,
    })


def pm25_to_aqi(pm25):
    """Convert PM2.5 to India AQI (NAQI)."""
    breakpoints = [
        (0, 30, 0, 50),
        (30, 60, 51, 100),
        (60, 90, 101, 200),
        (90, 120, 201, 300),
        (120, 250, 301, 400),
        (250, 500, 401, 500),
    ]
    for low_c, high_c, low_i, high_i in breakpoints:
        if low_c <= pm25 <= high_c:
            return ((high_i - low_i) / (high_c - low_c)) * (pm25 - low_c) + low_i
    return 500


def get_current_city_data():
    """Get current-day simulated data for all cities."""
    np.random.seed(int(datetime.now().strftime("%j")))  # seed by day of year
    today = datetime.now()
    seasonal = get_seasonal_factor(today.month)
    result = {}
    for city, info in CITY_DATA.items():
        base = info["base_pm25"] * seasonal
        pm25 = max(8, base + np.random.normal(0, base * 0.18))
        result[city] = {
            "pm25": round(pm25, 1),
            "aqi": round(pm25_to_aqi(pm25)),
            "lat": info["lat"],
            "lon": info["lon"],
            "state": info["state"],
        }
    return result
