"""
VaayuVigyaan AI — CPCB 2025 Data Pipeline
Loads all 30 city CSVs/XLSXs, pivots to wide format,
engineers features, and returns an ML-ready DataFrame.
"""

import os
import pandas as pd
import numpy as np

CPCB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cpcb")

# Parameters we care about as features
FEATURE_PARAMS = ['pm25', 'pm10', 'no2', 'o3', 'so2', 'co',
                  'temperature', 'relativehumidity']

# City → metadata (state, lat, lon, zone)
CITY_META = {
    "Delhi (UT)":                    {"state": "Delhi",          "lat": 28.614,  "lon": 77.209,  "zone": "north"},
    "Lucknow Uttar Pradesh":         {"state": "Uttar Pradesh",  "lat": 26.847,  "lon": 80.947,  "zone": "north"},
    "Patna Bihar":                   {"state": "Bihar",          "lat": 25.594,  "lon": 85.138,  "zone": "north"},
    "Chandigarh Haryana":            {"state": "Haryana",        "lat": 30.733,  "lon": 76.779,  "zone": "north"},
    "Jaipur Rajasthan":              {"state": "Rajasthan",      "lat": 26.912,  "lon": 75.787,  "zone": "north"},
    "Amritsar Punjab":               {"state": "Punjab",         "lat": 31.634,  "lon": 74.872,  "zone": "north"},
    "Dehradun Uttra_khand":          {"state": "Uttarakhand",    "lat": 30.316,  "lon": 78.032,  "zone": "north"},
    "Kolkata West Bengal":           {"state": "West Bengal",    "lat": 22.573,  "lon": 88.364,  "zone": "east"},
    "Bhubaneswar Odisha":            {"state": "Odisha",         "lat": 20.296,  "lon": 85.824,  "zone": "east"},
    "Dhanbad Jharkhand":             {"state": "Jharkhand",      "lat": 23.799,  "lon": 86.430,  "zone": "east"},
    "Guwahati Assam":                {"state": "Assam",          "lat": 26.144,  "lon": 91.736,  "zone": "northeast"},
    "Imphal Manipur":                {"state": "Manipur",        "lat": 24.817,  "lon": 93.937,  "zone": "northeast"},
    "Aizawl Mizoram":                {"state": "Mizoram",        "lat": 23.727,  "lon": 92.717,  "zone": "northeast"},
    "Shillong Meghalaya":            {"state": "Meghalaya",      "lat": 25.567,  "lon": 91.883,  "zone": "northeast"},
    "Kohima Nagaland":               {"state": "Nagaland",       "lat": 25.674,  "lon": 94.111,  "zone": "northeast"},
    "Agartala Tripura":              {"state": "Tripura",        "lat": 23.831,  "lon": 91.280,  "zone": "northeast"},
    "Naharlagun Arunachal Pradesh":  {"state": "Arunachal Pradesh","lat": 27.105, "lon": 93.694, "zone": "northeast"},
    "Gangtok Sikkim":                {"state": "Sikkim",         "lat": 27.339,  "lon": 88.612,  "zone": "northeast"},
    "Chennai Tamil Nadu":            {"state": "Tamil Nadu",     "lat": 13.083,  "lon": 80.271,  "zone": "south"},
    "Bengaluru Karnataka":           {"state": "Karnataka",      "lat": 12.972,  "lon": 77.595,  "zone": "south"},
    "Hyderabad Telegana":            {"state": "Telangana",      "lat": 17.385,  "lon": 78.487,  "zone": "south"},
    "Thrissur Kerala":               {"state": "Kerala",         "lat": 10.527,  "lon": 76.214,  "zone": "south"},
    "Visakhapatnam AndraPradesh":    {"state": "Andhra Pradesh", "lat": 17.686,  "lon": 83.218,  "zone": "south"},
    "Puducherry (UT)":               {"state": "Puducherry",     "lat": 11.934,  "lon": 79.830,  "zone": "south"},
    "Ahmedabad Gujarat":             {"state": "Gujarat",        "lat": 23.023,  "lon": 72.571,  "zone": "west"},
    "Chh.SambhajiNagar Maharashtra": {"state": "Maharashtra",    "lat": 19.877,  "lon": 75.343,  "zone": "west"},
    "Bhopal Madhya Pradesh":         {"state": "Madhya Pradesh", "lat": 23.259,  "lon": 77.413,  "zone": "central"},
    "Bilaspur Chhattisgarh":         {"state": "Chhattisgarh",   "lat": 22.088,  "lon": 82.137,  "zone": "central"},
    "Baddi Himachal Pradesh":        {"state": "Himachal Pradesh","lat": 30.958,  "lon": 76.792,  "zone": "north"},
    "Srinagar Jammu and Kashmir":    {"state": "J&K",            "lat": 34.080,  "lon": 74.797,  "zone": "north"},
}


def load_file(filepath: str) -> pd.DataFrame:
    """Read a CSV or XLSX file into a DataFrame."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.xlsx':
            return pd.read_excel(filepath)
        else:
            try:
                return pd.read_csv(filepath, encoding='utf-8')
            except UnicodeDecodeError:
                return pd.read_csv(filepath, encoding='latin-1')
    except Exception as e:
        print(f"  [WARN] Could not load {os.path.basename(filepath)}: {e}")
        return pd.DataFrame()


def pivot_city(df: pd.DataFrame, city_name: str) -> pd.DataFrame:
    """
    Long → wide: one row per (location, 15-min timestamp),
    columns = each parameter value.
    """
    if df.empty or 'parameter' not in df.columns:
        return pd.DataFrame()

    # Parse timestamp
    df = df.copy()
    df['ts'] = pd.to_datetime(df['datetimeLocal'], errors='coerce', utc=False)
    df = df.dropna(subset=['ts', 'value', 'parameter'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df[df['value'] >= 0]

    # Keep only feature parameters
    df = df[df['parameter'].isin(FEATURE_PARAMS)]

    # Pivot: mean per (location, timestamp bucket) to handle duplicates
    df['ts_bucket'] = df['ts'].dt.floor('15min')
    pivot = (
        df.groupby(['location_name', 'ts_bucket', 'parameter'])['value']
        .mean()
        .unstack('parameter')
        .reset_index()
    )
    pivot.columns.name = None
    pivot['city'] = city_name

    # Add lat/lon from first row of original df
    meta = CITY_META.get(city_name, {})
    pivot['lat'] = meta.get('lat', df['latitude'].iloc[0] if 'latitude' in df.columns else np.nan)
    pivot['lon'] = meta.get('lon', df['longitude'].iloc[0] if 'longitude' in df.columns else np.nan)
    pivot['state'] = meta.get('state', city_name)
    pivot['zone'] = meta.get('zone', 'unknown')

    return pivot


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based and derived features."""
    df = df.copy()

    # Time features
    df['hour']       = df['ts_bucket'].dt.hour
    df['month']      = df['ts_bucket'].dt.month
    df['dayofweek']  = df['ts_bucket'].dt.dayofweek
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)

    # Cyclical encoding of hour and month (avoids 23→0 discontinuity)
    df['hour_sin']   = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos']   = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin']  = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos']  = np.cos(2 * np.pi * df['month'] / 12)

    # Derived pollutant ratios
    if 'pm10' in df.columns and 'pm25' in df.columns:
        df['pm_ratio'] = (df['pm25'] / df['pm10'].replace(0, np.nan)).fillna(0.5)

    if 'no2' in df.columns and 'o3' in df.columns:
        df['no2_o3_ratio'] = (df['no2'] / (df['o3'].replace(0, np.nan) + 1)).fillna(1)

    # Zone one-hot (lightweight)
    for z in ['north', 'south', 'east', 'west', 'northeast', 'central']:
        df[f'zone_{z}'] = (df['zone'] == z).astype(int)

    return df


def load_all_cpcb(cpcb_dir: str = None) -> pd.DataFrame:
    """
    Load, clean, pivot, and engineer features for all CPCB city files.
    Returns an ML-ready DataFrame with pm25 as target column.
    """
    if cpcb_dir is None:
        cpcb_dir = CPCB_DIR

    all_frames = []
    files = sorted(os.listdir(cpcb_dir))

    for fname in files:
        if not (fname.endswith('.csv') or fname.endswith('.xlsx')):
            continue
        city_name = os.path.splitext(fname)[0]
        fpath = os.path.join(cpcb_dir, fname)
        print(f"  Loading: {city_name}...", end=' ')

        raw = load_file(fpath)
        if raw.empty:
            print("EMPTY")
            continue

        wide = pivot_city(raw, city_name)
        if wide.empty or 'pm25' not in wide.columns:
            print("NO PM2.5")
            continue

        n_valid = wide['pm25'].notna().sum()
        print(f"{n_valid} PM2.5 rows")
        all_frames.append(wide)

    if not all_frames:
        raise ValueError("No valid data loaded from CPCB files.")

    combined = pd.concat(all_frames, ignore_index=True)
    combined = engineer_features(combined)

    # Drop rows without target
    combined = combined.dropna(subset=['pm25'])
    combined = combined[combined['pm25'].between(1, 999)]  # sanity filter

    print(f"\n✓ Total ML-ready rows: {len(combined):,} | Cities: {combined['city'].nunique()}")
    return combined


def get_feature_cols() -> list:
    """Return the ordered list of feature columns used in training."""
    base = ['temperature', 'relativehumidity', 'pm10', 'no2', 'o3', 'so2', 'co',
            'hour_sin', 'hour_cos', 'month_sin', 'month_cos',
            'is_weekend', 'lat', 'lon',
            'zone_north', 'zone_south', 'zone_east',
            'zone_west', 'zone_northeast', 'zone_central']
    return base
