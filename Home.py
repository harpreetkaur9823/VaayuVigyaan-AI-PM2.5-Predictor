"""VaayuVigyaan AI — Home

Streamlit-native SaaS-style homepage.

Requirements implemented:
- Single hero block (3 lines only)
- Two CTA buttons only: AI Predictor, Dashboard
- Live snapshot section: Top polluted city, Cleanest city, Average AQI, Risk level
- Risk level is color-coded (Green=Moderate, Orange=High, Red=Severe)
- AI Predictor logic unchanged; layout improved
- City dashboard clean grid (max 3 columns per row)
- Health panel logic unchanged; spacing improved
- Trust section clean cards

Notes:
- Uses custom HTML/CSS only where it improves layout/visual consistency.
"""

import os
import sys
from typing import Dict, Any, Optional


import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import inject_css, aqi_badge, pm25_to_aqi, get_city_data
from utils.live_api import get_live_air_data
from utils.model_utils import load_or_train_model, predict_pm25


st.set_page_config(
    page_title="VaayuVigyaan AI | AI Air Intelligence",
    page_icon="🌦️",
    layout="wide",
)

inject_css()


# Optional background video (kept behind content)
import base64

video_path = os.path.join("video", "1851190-uhd_3840_2160_25fps.mp4")
if os.path.exists(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(
        f"""
        <style>
        .video-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
            opacity: 0.18;
            pointer-events: none;
        }}
        .stApp {{ background: transparent !important; }}
        </style>
        <video autoplay loop muted playsinline class="video-bg">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True,
    )


def _risk_category_from_aqi(aqi_value: int) -> str:
    if aqi_value <= 150:
        return "Moderate"
    if aqi_value <= 200:
        return "High"
    return "Severe"


def _risk_color(cat: str) -> str:
    return {
        "Moderate": "#22c55e",  # Green
        "High": "#f97316",      # Orange
        "Severe": "#ef4444",    # Red
    }.get(cat, "#22c55e")


@st.cache_data(ttl=600, show_spinner=False)
def _fetch_snapshot_all_cities() -> Dict[str, Dict[str, Any]]:
    static = get_city_data()
    out: Dict[str, Dict[str, Any]] = {}
    for city in static.keys():
        d = get_live_air_data(city)
        pm25 = float(d.get("pm25") or static[city].get("pm25", 80))
        out[city] = {
            "pm25": pm25,
            "aqi": int(pm25_to_aqi(pm25)),
            "is_live": bool(d.get("is_live", False)),
        }
    return out


def _card(title: str, value: str, subtitle: str, accent: Optional[str] = None) -> str:
    c = accent or "#00d4ff"
    return f"""
    <div style="
        padding:16px 14px;
        border-radius:14px;
        background:rgba(255,255,255,0.06);
        border:1px solid rgba(255,255,255,0.08);
        box-shadow: 0 0 0 rgba(0,0,0,0);
    ">
        <div style="font-size:12px; color:#aab4c5; letter-spacing:0.02em;">{title}</div>
        <div style="margin-top:8px; font-size:22px; font-weight:800; color:{c}; line-height:1;">{value}</div>
        <div style="margin-top:8px; font-size:12px; color:#7a8599;">{subtitle}</div>
    </div>
    """


# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("**VaayuVigyaan**\nDECISION INTELLIGENCE · INDIA")
    st.page_link("pages/1_Dashboard.py", label="Live Air Map")
    st.page_link("pages/2_AI_Predictor.py", label="AI Predictor")
    st.page_link("pages/3_Health_Impact.py", label="Health Impact")
    st.page_link("pages/7_Model_Details.py", label="Model Details")

    city_list = list(get_city_data().keys())
    city_sel = st.selectbox(
        "📍 City context",
        city_list,
        index=min(4, len(city_list) - 1) if city_list else 0,
    )


# ---------------- Section 1: HERO (ONLY 3 lines) ----------------
st.markdown(
    """
    <div style="padding-top: 0.35rem; text-align:left;">
      <div style="font-family: 'Orbitron', monospace; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.03em; line-height: 1.12;">
        VaayuVigyaan AI
      </div>
      <div style="margin-top: 0.35rem; font-family: 'Inter', sans-serif; font-size: 1.08rem; color: #94a3b8; line-height: 1.45;">
        Breathe Smarter with AI Air Intelligence — see the air, act with clarity
      </div>
      <div style="margin-top: 0.55rem; font-family: 'Inter', sans-serif; font-size: 0.92rem; color: #7db8d8; line-height: 1.35;">
        Real-time AQI · Predictive PM2.5 · Health guidance for India
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ---------------- Section 2: CTA BUTTONS (exactly 2) ----------------
cta1, cta2 = st.columns(2, gap="large")
with cta1:
    if st.button("AI Predictor", use_container_width=True, type="primary"):
        st.switch_page("pages/2_AI_Predictor.py")
with cta2:
    if st.button("Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Dashboard.py")

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)


# ---------------- Section 3: LIVE SNAPSHOT ----------------
snapshot = _fetch_snapshot_all_cities()

if snapshot:
    worst_city = max(snapshot.items(), key=lambda kv: kv[1]["aqi"])[0]
    clean_city = min(snapshot.items(), key=lambda kv: kv[1]["aqi"])[0]
    avg_aqi = sum(v["aqi"] for v in snapshot.values()) / max(1, len(snapshot))
    avg_aqi_int = int(round(avg_aqi))
    risk_cat = _risk_category_from_aqi(avg_aqi_int)
else:
    worst_city = "-"
    clean_city = "-"
    avg_aqi_int = 0
    risk_cat = "Moderate"

risk_color = _risk_color(risk_cat)

# Use a single style system (custom cards)
c1, c2, c3, c4 = st.columns(4, gap="large")
with c1:
    st.markdown(
        _card(
            "Top polluted city",
            str(snapshot[worst_city]["aqi"]) if worst_city in snapshot else "—",
            f"{worst_city}" if worst_city in snapshot else "AQI snapshot",
            accent="#ef4444",
        ),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        _card(
            "Cleanest city",
            str(snapshot[clean_city]["aqi"]) if clean_city in snapshot else "—",
            f"{clean_city}" if clean_city in snapshot else "AQI snapshot",
            accent="#22c55e",
        ),
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        _card(
            "Average AQI",
            str(avg_aqi_int),
            "Across sample cities",
            accent="#38bdf8",
        ),
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        _card(
            "Risk level",
            risk_cat,
            "Color-coded health view",
            accent=risk_color,
        ),
        unsafe_allow_html=True,
    )

st.divider()


# ---------------- Section 4: AI PREDICTOR (logic unchanged; layout improved) ----------------
st.subheader("🤖 AI Predictor")

with st.spinner("Loading AI engine (GBR model)…"):
    model, meta = load_or_train_model()

# Defaults from current city (fallback-safe)
static_city = get_city_data().get(city_sel, {})
live_city = get_live_air_data(city_sel)

_default_temp = float(live_city.get("temperature") or static_city.get("temp") or 28)
_default_hum = float(live_city.get("humidity") or static_city.get("humidity") or 60)
_default_pm10 = float(live_city.get("pm10") or static_city.get("pm10") or 120)
_default_no2 = float(live_city.get("no2") or static_city.get("no2") or 35)
_default_so2 = float(live_city.get("so2") or static_city.get("so2") or 12)
_default_co_ppm = (
    float((live_city.get("co") or static_city.get("co") or 1200) / 1145.0)
    if live_city.get("co") is not None
    else 0.8
)
_default_o3 = float(live_city.get("o3") or static_city.get("o3") or 40)

col_inputs, col_result = st.columns([1, 1.08], gap="large")

with col_inputs:
    st.markdown("**Inputs (what’s in the air)**")

    temperature = st.slider("🌡️ Temperature", 5.0, 48.0, _default_temp, 0.5)
    humidity = st.slider("💧 Humidity", 10, 100, int(round(_default_hum)), 1)
    pm10 = st.slider("PM₁₀", 0.0, 400.0, _default_pm10, 1.0)
    no2 = st.slider("NO₂", 0.0, 200.0, _default_no2, 1.0)
    so2 = st.slider("SO₂", 0.0, 100.0, _default_so2, 0.5)
    co = st.slider("CO", 0.0, 5.0, _default_co_ppm, 0.05)
    o3 = st.slider("O₃", 0.0, 150.0, _default_o3, 1.0)

    predict_clicked = st.button(
        "Get Guidance", use_container_width=True, type="primary"
    )

with col_result:
    if "home_prediction" not in st.session_state:
        st.session_state.home_prediction = None

    if predict_clicked:
        lat = meta.get("city_lat", {}).get(
            city_sel, get_city_data()[city_sel]["lat"]
        )
        lon = meta.get("city_lon", {}).get(
            city_sel, get_city_data()[city_sel]["lon"]
        )

        inputs = {
            "temperature": float(temperature),
            "humidity": float(humidity),
            "pm10": float(pm10),
            "no2": float(no2),
            "so2": float(so2),
            "co": float(co),
            "o3": float(o3),
            "no": 18.0,
        }

        # Keep ML model logic unchanged
        res = predict_pm25(model, inputs, lat=lat, lon=lon)
        aqi_v = pm25_to_aqi(res["pm25"])

        # Action suggestion (same as original approach)
        if aqi_v <= 50:
            action = "Go out — normal precautions"
            mask_hint = "Mask usually not needed."
        elif aqi_v <= 100:
            action = "Go out carefully — sensitive groups take it easy"
            mask_hint = "Consider a mask for longer outdoor time."
        elif aqi_v <= 150:
            action = "Limit outdoor exertion — consider a mask"
            mask_hint = "N95 recommended for sensitive groups."
        elif aqi_v <= 200:
            action = "Avoid outdoors if possible"
            mask_hint = "Use a high-filtration mask if you must step out."
        else:
            action = "Avoid outdoor exposure"
            mask_hint = "Only essential travel. Use N95/N99 if unavoidable."

        st.session_state.home_prediction = {
            "aqi": int(aqi_v),
            "category": res.get("category"),
            "risk_level": "Moderate" if aqi_v <= 150 else "High",
            "action": action,
            "mask_hint": mask_hint,
            "res": res,
        }

    pred = st.session_state.home_prediction

    if pred is None:
        st.info("Adjust the sliders and press Get Guidance.")
    else:
        aqi_v = int(pred["aqi"])
        res = pred["res"]

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        cA, cB = st.columns(2, gap="large")
        with cA:
            st.markdown(
                _card(
                    "AQI",
                    str(aqi_v),
                    "AQI band",
                    accent="#38bdf8" if aqi_v <= 150 else "#f97316",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(aqi_badge(aqi_v), unsafe_allow_html=True)
            st.caption(pred.get("category") or "")

        with cB:
            # Risk stays in the same logic from existing app (Moderate vs High label)
            st.markdown(
                _card(
                    "Risk level",
                    str(pred["risk_level"]),
                    "Model-based guidance",
                    accent=_risk_color(
                        "Moderate" if aqi_v <= 150 else "High"
                    ),
                ),
                unsafe_allow_html=True,
            )
            st.caption(f"Confidence: {res.get('confidence','—')}%")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.success(pred["action"])
        st.caption(pred["mask_hint"])

        cP1, cP2 = st.columns(2, gap="large")
        with cP1:
            st.metric(
                "Predicted PM₂.₅",
                f"{res.get('pm25','—')} µg/m³",
            )
        with cP2:
            st.metric(
                "Model confidence",
                f"{res.get('confidence','—')}%",
            )

st.divider()


# ---------------- Section 5: CITY DASHBOARD ----------------
st.subheader("🌆 City Air Dashboard")

ordered = sorted(snapshot.items(), key=lambda kv: kv[1]["aqi"], reverse=True)
city_cards = ordered[:12]

rows = (len(city_cards) + 2) // 3  # max 3 columns
for r in range(rows):
    row_cities = city_cards[r * 3 : r * 3 + 3]
    cols = st.columns(len(row_cities), gap="large")
    for col, (city, d) in zip(cols, row_cities):
        with col:
            st.caption(city)
            st.metric("AQI", str(int(d["aqi"])))
            st.caption(f"PM₂.₅ {float(d['pm25']):.0f} µg/m³")
            st.markdown(aqi_badge(int(d["aqi"])), unsafe_allow_html=True)
            st.caption("LIVE" if d.get("is_live") else "OFFLINE")

st.divider()


# ---------------- Section 6: HEALTH PANEL (logic unchanged) ----------------
st.subheader("🧠 AI Health Decision Panel")

live_selected = get_live_air_data(city_sel)
pm25_now = float(
    live_selected.get("pm25")
    or get_city_data()[city_sel].get("pm25", 80)
)
aqi_now = int(pm25_to_aqi(pm25_now))

# Convert to actionable text (logic preserved style)
if aqi_now <= 50:
    go_out = "Yes — it’s relatively safe"
    mask_needed = "Mask usually not needed"
    sensitive_risk = "Low risk for most people"
    best_time = "Anytime — normal precautions"
elif aqi_now <= 100:
    go_out = "Mostly safe"
    mask_needed = "Consider mask for longer outings"
    sensitive_risk = "Sensitive groups: take it easy"
    best_time = "Short outings; mid-morning feels better"
elif aqi_now <= 150:
    go_out = "Limit outdoor exertion"
    mask_needed = "Wear a mask for sensitive groups"
    sensitive_risk = "Elevated risk: children/elderly benefit from precautions"
    best_time = "Later hours when conditions stabilize"
elif aqi_now <= 200:
    go_out = "Avoid outdoors if possible"
    mask_needed = "High-filtration mask recommended"
    sensitive_risk = "High risk: sensitive groups should stay indoors"
    best_time = "Prefer indoors; essential travel only"
else:
    go_out = "Avoid outdoor exposure"
    mask_needed = "N95/N99 if unavoidable"
    sensitive_risk = "Severe risk: stay indoors, reduce exertion"
    best_time = "Only essential movement"

st.caption(
    f"Current for **{city_sel}**: AQI {aqi_now} · PM₂.₅ {pm25_now:.0f} µg/m³"
)

col_h1, col_h2, col_h3, col_h4 = st.columns(4, gap="large")
with col_h1:
    st.info(go_out)
with col_h2:
    st.warning(mask_needed)
with col_h3:
    st.warning(sensitive_risk)
with col_h4:
    st.success(best_time)

st.divider()


# ---------------- Section 7: TRUST ----------------
st.subheader("Why VaayuVigyaan AI")

trust_cards = [
    ("⚡", "AI-based forecasting", "Predictive PM2.5 → decision-ready AQI guidance."),
    ("🌎", "India-focused datasets", "Trained on CPCB 2025 data across multiple Indian cities."),
    ("🫀", "Health-first insights", "Recommendations designed for action."),
    ("🔄", "Real-time + predictive intelligence", "Live AQI snapshots with model reasoning."),
]

cols_t = st.columns(4, gap="large")
for col, (icon, title, desc) in zip(cols_t, trust_cards):
    with col:
        st.markdown(
            _card(
                f"{icon} {title}",
                " ",
                desc,
                accent="#38bdf8",
            ),
            unsafe_allow_html=True,
        )


