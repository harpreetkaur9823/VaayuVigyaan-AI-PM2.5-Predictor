"""
VaayuVigyaan AI — Health Impact Dashboard
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.styles import inject_css, page_header, aqi_badge, pm25_to_aqi, get_city_data

def hex_to_rgba(hex_color, alpha=0.1):
    """Convert a #rrggbb hex color to rgba() string safe for Plotly."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'


st.set_page_config(page_title="Health Impact | VaayuVigyaan", page_icon="🏥", layout="wide")
inject_css()

st.markdown(page_header("Health Intelligence", "AI-powered personal health risk assessment", "🏥"), unsafe_allow_html=True)

cities = get_city_data()

with st.sidebar:
    st.markdown("### ⚙️ Health Profile")
    city = st.selectbox("📍 Your City", list(cities.keys()), index=2)  # Pune default
    age_group = st.selectbox("👤 Age Group", ["Child (0-12)", "Teen (13-17)", "Adult (18-59)", "Senior (60+)"])
    health_conditions = st.multiselect("🩺 Pre-existing Conditions",
        ["Asthma", "COPD", "Heart Disease", "Diabetes", "Allergies", "Pregnancy"],
        default=[]
    )
    outdoor_hours = st.slider("🌿 Daily Outdoor Hours", 0, 12, 3)

pm25_val = cities[city]['pm25']
aqi_val  = pm25_to_aqi(pm25_val)
badge    = aqi_badge(aqi_val)

# Risk multipliers
age_mult = {"Child (0-12)": 1.6, "Teen (13-17)": 1.2, "Adult (18-59)": 1.0, "Senior (60+)": 1.5}[age_group]
condition_mult = 1.0 + 0.2 * len(health_conditions)
outdoor_mult = 1.0 + outdoor_hours * 0.06
total_mult = age_mult * condition_mult * outdoor_mult

# ─── Hero card ────────────────────────────────────────────────────────────────
if aqi_val <= 50:   overall_color, overall_text = "#00ff88", "LOW RISK"
elif aqi_val <= 100: overall_color, overall_text = "#ffdd00", "MODERATE RISK"
elif aqi_val <= 150: overall_color, overall_text = "#ff8800", "ELEVATED RISK"
elif aqi_val <= 200: overall_color, overall_text = "#ff4444", "HIGH RISK"
else:               overall_color, overall_text = "#cc00ff", "SEVERE RISK"

personal_score = min(100, aqi_val * total_mult / 4)
st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(4,20,45,0.9),rgba(0,20,50,0.7));
    border:1px solid {overall_color}44; border-radius:20px; padding:28px;
    box-shadow: 0 0 40px {overall_color}18; margin-bottom:1.5rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div>
            <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.25em;
                color:#7db8d8;">YOUR PERSONAL RISK PROFILE</div>
            <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:800;
                color:{overall_color}; text-shadow:0 0 25px {overall_color}; margin:8px 0;">{overall_text}</div>
            <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                <span style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#aad4ee;">
                    {city} — PM2.5: {pm25_val} µg/m³
                </span>
                {badge}
            </div>
        </div>
        <div style="text-align:center;">
            <div style="font-family:'Orbitron',monospace; font-size:3.5rem; font-weight:900;
                color:{overall_color}; text-shadow:0 0 40px {overall_color}; line-height:1;">
                {personal_score:.0f}
            </div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#7db8d8;">
                PERSONAL RISK SCORE /100
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Health indicators ─────────────────────────────────────────────────────────
def risk_card(title, icon, score, description, rec, color):
    score = min(100, max(0, score))
    bar_color = '#00ff88' if score < 30 else '#ffdd00' if score < 55 else '#ff8800' if score < 75 else '#ff4444'
    label = "LOW" if score < 30 else "MODERATE" if score < 55 else "HIGH" if score < 75 else "CRITICAL"
    return f"""
    <div style="background:rgba(4,20,45,0.75); border:1px solid rgba(0,212,255,0.2);
        border-radius:16px; padding:20px; height:100%;
        transition:all 0.3s; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
            <span style="font-size:1.5rem;">{icon}</span>
            <div style="font-family:'Orbitron',monospace; font-size:0.8rem; font-weight:700;
                color:#e8f4ff;">{title}</div>
        </div>
        <div style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:'Orbitron',monospace; font-size:0.65rem; color:{bar_color};
                background:rgba(0,0,0,0.3); border:1px solid {bar_color}44;
                padding:2px 8px; border-radius:20px;">{label}</span>
            <span style="font-family:'Space Mono',monospace; font-size:0.9rem; color:{bar_color};
                font-weight:700;">{score:.0f}%</span>
        </div>
        <div style="background:rgba(0,20,50,0.6); border-radius:6px; height:6px; overflow:hidden; margin-bottom:12px;">
            <div style="width:{score}%; height:100%; background:linear-gradient(90deg,{bar_color},{bar_color}88);
                border-radius:6px; box-shadow:0 0 8px {bar_color}66;"></div>
        </div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#7db8d8;
            margin-bottom:10px; line-height:1.4;">{description}</div>
        <div style="background:rgba(0,136,255,0.08); border-left:3px solid #00d4ff;
            border-radius:4px; padding:8px 10px;
            font-family:'Rajdhani',sans-serif; font-size:0.85rem; color:#aad4ee;">
            💡 {rec}
        </div>
    </div>
    """

# compute risks
base_risk = min(100, aqi_val / 3)
asthma_risk = min(100, base_risk * total_mult * (1.8 if "Asthma" in health_conditions else 1.0))
elderly_risk = min(100, base_risk * (1.7 if "Senior" in age_group else 1.0) * condition_mult)
child_risk = min(100, base_risk * (1.6 if "Child" in age_group else 1.0) * (1 + 0.15 * len(health_conditions)))
outdoor_risk = min(100, base_risk * outdoor_mult)
mask_need = min(100, base_risk * total_mult * 0.9)
exercise_safe = max(0, 100 - mask_need)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(risk_card(
        "Respiratory Risk", "🫁", asthma_risk,
        f"Based on PM2.5={pm25_val}µg/m³ + {'Asthma detected' if 'Asthma' in health_conditions else 'no asthma'}",
        "Use N95 mask; avoid peak traffic hours 8-10AM and 6-9PM",
        overall_color
    ), unsafe_allow_html=True)

with col2:
    st.markdown(risk_card(
        "Cardiovascular Risk", "❤️", min(100, base_risk * (1.5 if "Heart Disease" in health_conditions else 1.0) * age_mult),
        f"Fine particles penetrate bloodstream; {'Heart disease flag active' if 'Heart Disease' in health_conditions else 'no cardiac flag'}",
        "Consult cardiologist if AQI > 150; take medication before going out",
        overall_color
    ), unsafe_allow_html=True)

with col3:
    st.markdown(risk_card(
        "Eye & Skin Irritation", "👁", min(100, base_risk * 0.7 * total_mult),
        "Particulate matter causes conjunctivitis and skin inflammation",
        "Wear protective glasses; use moisturizer; avoid rubbing eyes",
        overall_color
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(risk_card(
        "Outdoor Exercise Safety", "🏃", outdoor_risk,
        f"Running/cycling for {outdoor_hours}h/day at current AQI level",
        "Morning 5-7AM is safest. Avoid evenings. Indoor workouts preferred.",
        overall_color
    ), unsafe_allow_html=True)

with col5:
    st.markdown(risk_card(
        "Children Safety Index", "🧒", child_risk,
        "Children breathe ~50% more air per body weight than adults",
        "Keep indoors during school hours if AQI>100. Use air purifiers.",
        overall_color
    ), unsafe_allow_html=True)

with col6:
    st.markdown(risk_card(
        "Mask Requirement", "😷", mask_need,
        f"{'N95 respirator' if mask_need>60 else 'Surgical mask'} recommended at this exposure level",
        "N95 filters 95% of PM2.5. Replace every 8 hours of outdoor use.",
        overall_color
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Pollution exposure gauge (spider / radial) ─────────────────────────────
col_g, col_r = st.columns([1, 1])

with col_g:
    categories = ["Respiratory", "Cardiovascular", "Eye/Skin", "Exercise", "Children", "General"]
    vals_radar = [asthma_risk, min(100,base_risk*1.3), min(100,base_risk*0.7), outdoor_risk, child_risk, base_risk]
    vals_radar.append(vals_radar[0])
    cats_r = categories + [categories[0]]
    fig_radar = go.Figure(go.Scatterpolar(
        r=vals_radar, theta=cats_r, fill='toself',
        line=dict(color=overall_color, width=2),
        fillcolor=hex_to_rgba(overall_color, 0.09),
        name='Your Risk Profile',
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='rgba(0,10,25,0.6)',
            radialaxis=dict(visible=True, range=[0,100],
                tickfont=dict(color='#7db8d8', size=9),
                gridcolor='rgba(0,212,255,0.15)'),
            angularaxis=dict(tickfont=dict(color='#e8f4ff', family='Rajdhani', size=11),
                gridcolor='rgba(0,212,255,0.1)'),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(text="Health Risk Radar", font=dict(family='Orbitron', color='#e8f4ff', size=13)),
        height=380,
        margin=dict(l=40,r=40,t=50,b=20),
        font=dict(color='#7db8d8'),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_r:
    # Recommendations panel
    recs = [
        ("🏠", "Stay Indoor", "Seal windows; use air purifiers with HEPA filters at home", aqi_val > 100),
        ("😷", "Wear N95 Mask", "N95/N99 respirator required when going out", aqi_val > 150),
        ("💊", "Take Medication", "Pre-dose bronchodilators before outdoor exposure (consult doctor)", "Asthma" in health_conditions or "COPD" in health_conditions),
        ("🏃", "Limit Outdoor Activity", f"Reduce outdoor hours to <{max(1,outdoor_hours-2)}h/day", aqi_val > 120),
        ("🌿", "Use Air Purifier", "CADR ≥ 200 cfm for room <400 sq ft", aqi_val > 100),
        ("💧", "Stay Hydrated", "Water helps flush particulates that enter bloodstream", True),
        ("📱", "Monitor AQI", "Check AQI every 2 hours; set alerts at 150", True),
        ("🩺", "Consult Doctor", "Seek medical advice if experiencing breathlessness or chest pain", aqi_val > 200),
    ]
    active_recs = [(i, d, r) for i, d, r, active in recs if active]

    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:0.2em;
        color:#00d4ff; margin-bottom:12px;">▸ AI HEALTH RECOMMENDATIONS</div>
    """, unsafe_allow_html=True)

    for icon, title, rec in active_recs[:6]:
        st.markdown(f"""
        <div style="background:rgba(0,20,50,0.5); border:1px solid rgba(0,212,255,0.15);
            border-radius:10px; padding:12px 16px; margin-bottom:8px;
            display:flex; align-items:flex-start; gap:12px;">
            <span style="font-size:1.2rem; flex-shrink:0;">{icon}</span>
            <div>
                <div style="font-family:'Orbitron',monospace; font-size:0.7rem; color:#00d4ff;
                    margin-bottom:4px;">{title}</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#7db8d8;">{rec}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
