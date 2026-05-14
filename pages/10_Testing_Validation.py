"""VaayuVigyaan AI — Testing & Validation

Hackathon checklist page.
Adds scenario testing + model validation metrics (UI only).
"""

import streamlit as st
import sys
import os
from math import isfinite

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import inject_css, page_header, aqi_badge
from utils.model_utils import load_or_train_model, predict_pm25, CITY_META
from utils.styles import pm25_to_aqi

st.set_page_config(
    page_title="Testing & Validation | VaayuVigyaan",
    page_icon="🧪",
    layout="wide",
)
inject_css()

st.markdown(
    page_header(
        "Testing & Validation",
        "Scenario testing · explainable validation · prototype summary",
        "🧪",
    ),
    unsafe_allow_html=True,
)

# Load model once (no logic changes)
with st.spinner("Running model validation pipeline..."):
    model, meta = load_or_train_model()

# Model Validation card
st.markdown("""
<div style="background:rgba(2,15,35,0.7); border:1px solid rgba(0,212,255,0.15); border-radius:18px; padding:20px 22px;">
  <div style="font-family:'Orbitron',monospace; font-size:1.05rem; font-weight:900; color:#e8f4ff; margin-bottom:8px;">Model Validation</div>
  <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px;">
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:
    st.metric("R²", f"{meta.get('r2_test', 0):.3f}", "Test split")
with c2:
    st.metric("RMSE", f"{meta.get('rmse', 0):.2f} µg/m³", "Test split")
with c3:
    st.metric("MAE", f"{meta.get('mae', 0):.2f} µg/m³", "Test split")
with c4:
    st.metric(
        "Dataset Size",
        f"{meta.get('n_train', 0):,} train",
        f"Cities: {len(meta.get('cities', []))}",
    )

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Scenario testing
st.markdown(
    """
    <div style="font-family:'Orbitron',monospace; font-size:1.05rem; font-weight:900; color:#e8f4ff; margin-bottom:10px;">
        Scenario Examples (Realistic validation)
    </div>
    """,
    unsafe_allow_html=True,
)

# Each scenario: inputs tuned for realistic conditions
SCENARIOS = [
    {
        "name": "1) Delhi winter pollution",
        "city": "Delhi",
        "inputs": {
            "temperature": 9.0,
            "humidity": 60.0,
            "pm10": 260.0,
            "no2": 75.0,
            "so2": 25.0,
            "co": 1.6,
            "o3": 18.0,
            "no": 28.0,
        },
        "expected": "Higher PM2.5 due to inversion + high coarse dust + combustion precursors.",
    },
    {
        "name": "2) Rainfall pollution reduction",
        "city": "Delhi",
        "inputs": {
            "temperature": 20.0,
            "humidity": 85.0,
            "pm10": 120.0,
            "no2": 45.0,
            "so2": 14.0,
            "co": 0.9,
            "o3": 35.0,
            "no": 18.0,
        },
        "expected": "Lower PM2.5 as wet scavenging reduces particle mass.",
    },
    {
        "name": "3) High traffic scenario",
        "city": "Mumbai",
        "inputs": {
            "temperature": 30.0,
            "humidity": 70.0,
            "pm10": 170.0,
            "no2": 90.0,
            "so2": 18.0,
            "co": 2.6,
            "o3": 45.0,
            "no": 55.0,
        },
        "expected": "PM2.5 rises due to vehicle emissions (NOx/CO) and increased dust resuspension.",
    },
    {
        "name": "4) High humidity condition",
        "city": "Kolkata",
        "inputs": {
            "temperature": 28.0,
            "humidity": 92.0,
            "pm10": 140.0,
            "no2": 55.0,
            "so2": 16.0,
            "co": 1.4,
            "o3": 38.0,
            "no": 22.0,
        },
        "expected": "PM2.5 increases from hygroscopic particle growth at high RH.",
    },
    {
        "name": "5) Low wind urban trapping",
        "city": "Bengaluru",
        "inputs": {
            "temperature": 25.0,
            "humidity": 65.0,
            "pm10": 150.0,
            "no2": 60.0,
            "so2": 12.0,
            "co": 1.1,
            "o3": 25.0,
            "no": 20.0,
        },
        "expected": "PM2.5 moderately elevated due to reduced dispersion (stagnant conditions).",
    },
]


def safe_float(x):
    try:
        xf = float(x)
        return xf if isfinite(xf) else None
    except Exception:
        return None


for s in SCENARIOS:
    city = s["city"]
    if city not in CITY_META:
        # fallback: use approximate lat/lon
        lat, lon = 28.6, 77.2
    else:
        lat, lon = CITY_META[city]["lat"], CITY_META[city]["lon"]

    with st.expander(s["name"], expanded=True):
        st.markdown(f"""
    ### 🌍 Scenario City: {city}

    **Expected Behaviour:**  
    {s["expected"]}
    """)