"""
VaayuVigyaan AI — Live Air Quality via OpenWeatherMap Air Pollution API
"""

import urllib.request
import json
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/air_pollution/forecast"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

CITY_COORDS = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Amritsar": (31.6340, 74.8723),
    "Chandigarh": (30.7333, 76.7794),
    "Patna": (25.5941, 85.1376),
    "Bhopal": (23.2599, 77.4126),
    "Bhubaneswar": (20.2961, 85.8245),
    "Dehradun": (30.3165, 78.0322),
    "Agartala": (23.8315, 91.2868),
    "Guwahati": (26.1445, 91.7362),
    "Thrissur": (10.5276, 76.2144),
    "Shillong": (25.5788, 91.8933),
}

# OpenWeather AQI Labels
OWM_AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}

# Thread-safe cache
_cache = {}
_cache_lock = threading.Lock()
CACHE_TTL = 600  # 10 minutes


def _fetch(url: str, timeout: int = 8):
    """
    Fetch JSON data from API.
    Tries requests first, then urllib.
    """

    try:
        import requests as _req

        response = _req.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "VaayuVigyaan/2.0"},
        )

        if response.status_code == 200:
            return response.json()

        print(f"API Error {response.status_code}: {url}")
        return None

    except ImportError:
        pass

    except Exception as e:
        print(f"Requests Error: {e}")

    # Fallback → urllib
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "VaayuVigyaan/2.0"},
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode())

    except Exception as e:
        print(f"URLLib Error: {e}")
        return None


def get_live_air_data(city_name: str = "Pune") -> dict:
    """
    Fetch live air pollution + weather data.
    Falls back to CPCB sample data if API fails.
    """

    now = time.time()

    # Check cache
    with _cache_lock:
        cached = _cache.get(city_name)

        if cached and (now - cached["ts"]) < CACHE_TTL:
            return cached["data"]

    coords = CITY_COORDS.get(city_name)

    if coords is None:
        return _fallback(city_name)

    lat, lon = coords

    if not API_KEY:
        print("Missing OPENWEATHER_API_KEY")
        return _fallback(city_name, lat, lon)

    # Air Pollution API
    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
    raw = _fetch(url)

    # Fallback if API fails
    if not raw or "list" not in raw or not raw["list"]:

        fallback_data = _fallback(city_name, lat, lon)

        with _cache_lock:
            _cache[city_name] = {
                "ts": now,
                "data": fallback_data,
            }

        return fallback_data

    entry = raw["list"][0]
    comp = entry.get("components", {})
    owm_aqi = entry.get("main", {}).get("aqi", 3)

    # Weather API
    weather_url = (
        f"{WEATHER_URL}"
        f"?lat={lat}&lon={lon}"
        f"&appid={API_KEY}&units=metric"
    )

    weather = _fetch(weather_url)

    temp = None
    humidity = None
    wind_speed = None
    weather_desc = "N/A"

    if weather:
        temp = weather.get("main", {}).get("temp")
        humidity = weather.get("main", {}).get("humidity")
        wind_speed = weather.get("wind", {}).get("speed")

        weather_list = weather.get("weather", [])

        if weather_list:
            weather_desc = (
                weather_list[0]
                .get("description", "N/A")
                .title()
            )

    result = {
        "city": city_name,
        "owm_aqi": owm_aqi,
        "owm_label": OWM_AQI_LABELS.get(
            owm_aqi,
            "Unknown"
        ),
        "pm25": round(comp.get("pm2_5", 0), 1),
        "pm10": round(comp.get("pm10", 0), 1),
        "co": round(comp.get("co", 0), 2),
        "no2": round(comp.get("no2", 0), 1),
        "so2": round(comp.get("so2", 0), 1),
        "o3": round(comp.get("o3", 0), 1),
        "no": round(comp.get("no", 0), 1),
        "nh3": round(comp.get("nh3", 0), 1),
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "weather_desc": weather_desc,
        "latitude": lat,
        "longitude": lon,
        "is_live": True,
        "source": "OpenWeatherMap Live",
    }

    # Save cache
    with _cache_lock:
        _cache[city_name] = {
            "ts": now,
            "data": result,
        }

    return result


def get_all_cities_live(cities: list = None) -> dict:
    """
    Get live data for multiple cities.
    """

    if cities is None:
        cities = list(CITY_COORDS.keys())

    return {
        city: get_live_air_data(city)
        for city in cities
    }


def get_forecast_data(city_name: str = "Pune") -> list:
    """
    Get air pollution forecast.
    Returns next ~96 hours.
    """

    coords = CITY_COORDS.get(city_name)

    if coords is None:
        return []

    lat, lon = coords

    url = (
        f"{FORECAST_URL}"
        f"?lat={lat}&lon={lon}"
        f"&appid={API_KEY}"
    )

    raw = _fetch(url)

    if not raw or "list" not in raw:
        return []

    from datetime import datetime

    records = []

    for entry in raw["list"]:
        comp = entry.get("components", {})

        records.append({
            "dt": datetime.utcfromtimestamp(entry["dt"]),
            "pm25": comp.get("pm2_5", 0),
            "pm10": comp.get("pm10", 0),
            "no2": comp.get("no2", 0),
            "o3": comp.get("o3", 0),
            "aqi": entry.get("main", {}).get("aqi", 1),
        })

    return records


def _fallback(
    city_name: str,
    lat: float = 0.0,
    lon: float = 0.0
) -> dict:
    """
    CPCB-calibrated fallback data.
    """

    from utils.styles import get_city_data

    cities = get_city_data()
    d = cities.get(city_name, {})

    coords = CITY_COORDS.get(
        city_name,
        (lat, lon)
    )

    return {
        "city": city_name,
        "owm_aqi": 3,
        "owm_label": "Moderate",
        "pm25": d.get("pm25", 80),
        "pm10": d.get(
            "pm10",
            d.get("pm25", 80) * 1.5
        ),
        "co": 1200.0,
        "no2": 35.0,
        "so2": 12.0,
        "o3": 50.0,
        "no": 15.0,
        "nh3": 5.0,
        "temperature": d.get("temp", 30),
        "humidity": d.get("humidity", 60),
        "wind_speed": d.get("wind", 3.0),
        "weather_desc": "Offline Mode",
        "latitude": coords[0],
        "longitude": coords[1],
        "is_live": False,
        "source": "CPCB Fallback",
    }


def co_ugm3_to_ppm(co_ugm3: float) -> float:
    """
    Convert CO from µg/m³ → ppm
    """
    return round(co_ugm3 / 1145.0, 3)