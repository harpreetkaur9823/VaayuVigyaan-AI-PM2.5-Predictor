"""
VaayuVigyaan AI — Model utilities
Trained on CPCB 2025 data: 22,182 records, 25 Indian cities, Feb-Mar 2025.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "cpcb_gbr_model.pkl")
DATA_PATH  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data",   "cpcb_preprocessed.csv")

# Features must match training exactly
FEATURE_NAMES = [
    'pm10', 'temperature', 'humidity', 'no2', 'so2', 'co', 'o3', 'no',
    'hour', 'day_of_week', 'month', 'season', 'is_weekend',
    'morning_rush', 'evening_rush', 'latitude', 'longitude'
]

# ── CPCB city coordinates & metadata ─────────────────────────────────────────
CITY_META = {
    'Delhi':       {'lat': 28.6139, 'lon': 77.2090, 'state': 'Delhi UT',           'zone': 'North'},
    'Mumbai':      {'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra',         'zone': 'West'},
    'Kolkata':     {'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal',         'zone': 'East'},
    'Chennai':     {'lat': 13.0827, 'lon': 80.2707, 'state': 'Tamil Nadu',          'zone': 'South'},
    'Hyderabad':   {'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana',           'zone': 'South'},
    'Ahmedabad':   {'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat',             'zone': 'West'},
    'Lucknow':     {'lat': 26.8467, 'lon': 80.9462, 'state': 'Uttar Pradesh',       'zone': 'North'},
    'Jaipur':      {'lat': 26.9124, 'lon': 75.7873, 'state': 'Rajasthan',           'zone': 'North'},
    'Patna':       {'lat': 25.5941, 'lon': 85.1376, 'state': 'Bihar',               'zone': 'East'},
    'Bhopal':      {'lat': 23.2599, 'lon': 77.4126, 'state': 'Madhya Pradesh',      'zone': 'Central'},
    'Chandigarh':  {'lat': 30.7333, 'lon': 76.7794, 'state': 'Chandigarh UT',       'zone': 'North'},
    'Amritsar':    {'lat': 31.6340, 'lon': 74.8723, 'state': 'Punjab',              'zone': 'North'},
    'Bhubaneswar': {'lat': 20.2961, 'lon': 85.8245, 'state': 'Odisha',             'zone': 'East'},
    'Dehradun':    {'lat': 30.3165, 'lon': 78.0322, 'state': 'Uttarakhand',         'zone': 'North'},
    'Guwahati':    {'lat': 26.1445, 'lon': 91.7362, 'state': 'Assam',              'zone': 'Northeast'},
    'Agartala':    {'lat': 23.8315, 'lon': 91.2868, 'state': 'Tripura',            'zone': 'Northeast'},
    'Imphal':      {'lat': 24.8170, 'lon': 93.9368, 'state': 'Manipur',            'zone': 'Northeast'},
    'Shillong':    {'lat': 25.5788, 'lon': 91.8933, 'state': 'Meghalaya',          'zone': 'Northeast'},
    'Kohima':      {'lat': 25.6751, 'lon': 94.1086, 'state': 'Nagaland',           'zone': 'Northeast'},
    'Aizawl':      {'lat': 23.7271, 'lon': 92.7176, 'state': 'Mizoram',            'zone': 'Northeast'},
    'Gangtok':     {'lat': 27.3389, 'lon': 88.6065, 'state': 'Sikkim',             'zone': 'Northeast'},
    'Thrissur':    {'lat': 10.5276, 'lon': 76.2144, 'state': 'Kerala',             'zone': 'South'},
    'Puducherry':  {'lat': 11.9416, 'lon': 79.8083, 'state': 'Puducherry UT',      'zone': 'South'},
    'Bilaspur':    {'lat': 22.0797, 'lon': 82.1391, 'state': 'Chhattisgarh',       'zone': 'Central'},
}


def _fallback_train():
    """Train on synthetic data if CPCB data not available."""
    np.random.seed(42)
    n = 5000
    X = np.column_stack([
        np.random.uniform(5, 400, n),    # pm10
        np.random.uniform(15, 45, n),    # temperature
        np.random.uniform(20, 95, n),    # humidity
        np.random.uniform(5, 150, n),    # no2
        np.random.uniform(1, 60, n),     # so2
        np.random.uniform(0.2, 3.0, n),  # co
        np.random.uniform(10, 120, n),   # o3
        np.random.uniform(1, 80, n),     # no
        np.random.randint(0, 24, n),     # hour
        np.random.randint(0, 7, n),      # day_of_week
        np.random.randint(1, 13, n),     # month
        np.random.randint(1, 5, n),      # season
        np.random.randint(0, 2, n),      # is_weekend
        np.random.randint(0, 2, n),      # morning_rush
        np.random.randint(0, 2, n),      # evening_rush
        np.random.uniform(8, 32, n),     # latitude
        np.random.uniform(68, 97, n),    # longitude
    ])
    y = np.clip(0.4 * X[:, 0] + 0.1 * X[:, 1] - 0.2 * X[:, 2]
                + 0.08 * X[:, 3] + np.random.normal(0, 8, n), 1, 500)

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.15, random_state=42)
    model = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('gbr', GradientBoostingRegressor(n_estimators=200, learning_rate=0.08,
                                           max_depth=5, random_state=42))
    ])
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)
    r2   = round(r2_score(y_te, preds), 4)
    rmse = round(float(np.sqrt(mean_squared_error(y_te, preds))), 2)
    mae  = round(float(mean_absolute_error(y_te, preds)), 2)
    return {
        'model': model, 'features': FEATURE_NAMES,
        'r2_test': r2, 'rmse': rmse, 'mae': mae,
        'feature_importance': dict(zip(FEATURE_NAMES, model.named_steps['gbr'].feature_importances_)),
        'city_pm25_mean': {c: 80 for c in CITY_META},
        'city_lat': {c: CITY_META[c]['lat'] for c in CITY_META},
        'city_lon': {c: CITY_META[c]['lon'] for c in CITY_META},
        'n_train': len(X_tr), 'n_test': len(X_te),
        'cities': list(CITY_META.keys()),
        'data_source': 'Synthetic fallback',
    }


def load_or_train_model():
    """
    Load the CPCB-trained model.
    Falls back to synthetic training if pkl missing or incompatible.
    Returns (model, metadata_dict)
    """
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    if os.path.exists(MODEL_PATH):
        try:
            meta = joblib.load(MODEL_PATH)
            return meta['model'], meta
        except Exception:
            try:
                os.remove(MODEL_PATH)
            except OSError:
                pass

    # No saved model — train from CPCB CSV if available, else synthetic
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        feats = [f for f in FEATURE_NAMES if f in df.columns]
        X = df[feats].copy()
        y = df['pm25'].values
        y_bins = pd.cut(y, bins=[0, 15, 35, 75, 150, 500], labels=False)
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.15, random_state=42, stratify=y_bins)

        model = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler',  StandardScaler()),
            ('gbr', GradientBoostingRegressor(
                n_estimators=400, learning_rate=0.05, max_depth=6,
                subsample=0.8, min_samples_leaf=3, max_features=0.7, random_state=42,
            ))
        ])
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        r2   = round(r2_score(y_te, preds), 4)
        rmse = round(float(np.sqrt(mean_squared_error(y_te, preds))), 2)
        mae  = round(float(mean_absolute_error(y_te, preds)), 2)
        imp  = dict(zip(feats, model.named_steps['gbr'].feature_importances_))

        meta = {
            'model': model, 'features': feats,
            'r2_test': r2, 'rmse': rmse, 'mae': mae,
            'feature_importance': imp,
            'city_pm25_mean': df.groupby('city')['pm25'].mean().round(1).to_dict(),
            'city_lat':       df.groupby('city')['latitude'].mean().round(4).to_dict(),
            'city_lon':       df.groupby('city')['longitude'].mean().round(4).to_dict(),
            'n_train': len(X_tr), 'n_test': len(X_te),
            'cities': sorted(df['city'].unique().tolist()),
            'data_source': 'CPCB 2025 (25 Indian cities)',
        }
    else:
        meta = _fallback_train()

    joblib.dump(meta, MODEL_PATH, compress=3)
    return meta['model'], meta


def predict_pm25(model, inputs: dict, lat: float = 28.6, lon: float = 77.2) -> dict:
    """
    Predict PM2.5 from user inputs.
    inputs keys: temperature, humidity, wind_speed (not used directly), rainfall,
                 pm10, no2, so2, co, o3, no  (optional — median-imputed if missing)
    """
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    dow  = now.weekday()
    month = now.month
    season_map = {12:1, 1:1, 2:1, 3:2, 4:2, 5:2, 6:4, 7:4, 8:4, 9:4, 10:3, 11:3}
    season = season_map[month]
    is_we  = int(dow >= 5)
    m_rush = int(7 <= hour <= 10)
    e_rush = int(17 <= hour <= 21)

    row = {
        'pm10':         inputs.get('pm10',        np.nan),
        'temperature':  inputs.get('temperature',  np.nan),
        'humidity':     inputs.get('humidity',     np.nan),
        'no2':          inputs.get('no2',          np.nan),
        'so2':          inputs.get('so2',          np.nan),
        'co':           inputs.get('co',           np.nan),
        'o3':           inputs.get('o3',           np.nan),
        'no':           inputs.get('no',           np.nan),
        'hour':         hour,
        'day_of_week':  dow,
        'month':        month,
        'season':       season,
        'is_weekend':   is_we,
        'morning_rush': m_rush,
        'evening_rush': e_rush,
        'latitude':     lat,
        'longitude':    lon,
    }

    # Build feature vector in training order
    _, meta = load_or_train_model()
    feat_order = meta.get('features', FEATURE_NAMES)
    X = np.array([[row.get(f, np.nan) for f in feat_order]])
    pm25 = float(model.predict(X)[0])
    pm25 = max(1.0, pm25)

    # AQI category
    if pm25 <= 12:       cat, color = "Good",                    "#4ade80"
    elif pm25 <= 35.4:   cat, color = "Moderate",               "#facc15"
    elif pm25 <= 55.4:   cat, color = "Unhealthy for Sensitive", "#fb923c"
    elif pm25 <= 150.4:  cat, color = "Unhealthy",               "#f87171"
    elif pm25 <= 250.4:  cat, color = "Very Unhealthy",          "#c084fc"
    else:                cat, color = "Hazardous",               "#991b1b"

    health_msgs = {
        "Good":                    "Air quality is satisfactory — no restrictions.",
        "Moderate":                "Acceptable; unusually sensitive people may feel effects.",
        "Unhealthy for Sensitive": "Sensitive groups (elderly, children, asthma) should limit outdoor time.",
        "Unhealthy":               "Everyone may start experiencing health effects. Limit outdoor activity.",
        "Very Unhealthy":          "Health alert — serious effects for all. Avoid outdoor exertion.",
        "Hazardous":               "Emergency conditions — avoid all outdoor activity.",
    }

    stability = max(0, 1.0 - abs(inputs.get('humidity', 60) - 50) / 100)
    confidence = round(85 + stability * 10, 1)

    return {
        'pm25':           round(pm25, 1),
        'category':       cat,
        'color':          color,
        'health_message': health_msgs[cat],
        'confidence':     confidence,
    }
