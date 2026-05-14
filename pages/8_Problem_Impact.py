"""VaayuVigyaan AI — Problem Statement & Real-world Impact

Hackathon checklist page.
Design: cyber dark + glassmorphism consistent with existing pages.
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import inject_css
from utils.styles import page_header


st.set_page_config(page_title="Problem & Impact | VaayuVigyaan", page_icon="🌍", layout="wide")
inject_css()

st.markdown(
    page_header(
        "Problem Statement & Real-world Impact",
        "Why PM2.5 intelligence matters for India",
        "🌍",
    ),
    unsafe_allow_html=True,
)

# Premium section helper (pure presentation)
def premium_card(title: str, body: str, glow: str, border: str, icon: str = "✨"):
    return f"""
    <div style="background:rgba(2,15,35,0.85);
                border:1px solid {border};
                border-top:2px solid {glow};
                border-radius:18px;
                padding:18px 20px;
                box-shadow:0 0 45px {glow}12;
                transition:transform 0.2s ease, box-shadow 0.2s ease;">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:10px;">
            <div style="width:34px; height:34px; border-radius:12px;
                        background:linear-gradient(135deg, rgba(0,212,255,0.18), rgba(0,255,212,0.08));
                        border:1px solid rgba(0,212,255,0.25);
                        display:flex; align-items:center; justify-content:center;
                        box-shadow: 0 0 25px rgba(0,212,255,0.12); font-size:1.1rem;">{icon}</div>
            <div>
                <div style="font-family:'Orbitron',monospace; color:#e8f4ff; font-weight:900; letter-spacing:-0.02em; font-size:1.05rem;">
                    {title}
                </div>
                <div style="font-family:'Inter',sans-serif; color:#7db8d8; font-size:0.88rem; line-height:1.6; margin-top:4px;">
                    {body}
                </div>
            </div>
        </div>
    </div>
    """

# Animated premium metric card

def metric_card(label: str, value: str, hint: str, color: str):
    return f"""
    <div style="background:rgba(4,20,45,0.7);
                border:1px solid {color}33;
                border-radius:18px;
                padding:18px 18px;
                box-shadow: 0 0 55px {color}12;
                min-height:112px;
                position:relative; overflow:hidden;">
        <div style="position:absolute; inset:-2px;
                    background:radial-gradient(circle at 20% 20%, {color}22, transparent 55%),
                               radial-gradient(circle at 80% 10%, #00ffd422, transparent 55%),
                               radial-gradient(circle at 70% 90%, rgba(56,189,248,0.14), transparent 52%);
                    opacity:1; pointer-events:none;"></div>
        <div style="position:relative; z-index:1;">
            <div style="font-family:'Inter',sans-serif; font-size:0.72rem; font-weight:800;
                        letter-spacing:0.14em; text-transform:uppercase; color:#7db8d8;">
                {label}
            </div>
            <div style="font-family:'Orbitron',monospace; font-size:2.15rem; font-weight:900;
                        color:{color}; letter-spacing:-0.03em; margin-top:10px; line-height:1.1;">
                {value}
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:0.88rem; color:#94a3b8; margin-top:6px; line-height:1.45;">
                {hint}
            </div>
        </div>
    </div>
    """

# Layout
st.markdown(
    """
    <div style="margin: 0 0 1.1rem 0; display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div style="width:10px; height:10px; border-radius:50%; background:#00d4ff;
                    box-shadow:0 0 18px rgba(0,212,255,0.35);"></div>
        <div style="font-family:'Inter',sans-serif; font-size:0.8rem; font-weight:950;
                    letter-spacing:0.14em; text-transform:uppercase; color:#38bdf8; opacity:0.86;">
            India needs predictive, health-aware AQI intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

colA, colB = st.columns(2, gap="large")

with colA:
    st.markdown("""<div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:900; color:#e8f4ff;">A) Problem Statement</div>""", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "PM2.5 & AQI crisis",
            "India faces persistent PM2.5-driven AQI spikes. Fine particles penetrate deep into lungs, staying airborne longer than coarse dust.",
            "#00d4ff",
            "rgba(0,212,255,0.25)",
            "🧫",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "Why PM2.5 is dangerous",
            "PM2.5 travels deep into the respiratory tract. It amplifies inflammation and increases risk for asthma attacks, cardiovascular stress, and reduced lung function—especially for children and seniors.",
            "#00ffd4",
            "rgba(0,255,212,0.22)",
            "🫁",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "Lack of predictive intelligence",
            "Most tools react to today’s AQI. VaayuVigyaan focuses on tomorrow’s PM2.5 trajectory using AI + explainable reasoning so decisions can be made before exposure happens.",
            "#0088ff",
            "rgba(0,136,255,0.22)",
            "🛰️",
        ),
        unsafe_allow_html=True,
    )

with colB:
    st.markdown("""<div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:900; color:#e8f4ff;">B) Why Existing Solutions Are Not Enough</div>""", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "Current-only AQI",
            "Many apps show only today’s AQI—useful, but not enough for planning outdoor activities, school events, or interventions.",
            "#facc15",
            "rgba(250,204,21,0.22)",
            "📍",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "Little/no XAI",
            "Few solutions explain *why* pollution is high (driver-level reasoning). Without explainability, users can’t trust or act confidently.",
            "#ff8800",
            "rgba(255,136,0,0.22)",
            "🧠",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        premium_card(
            "Weak personalized health reasoning",
            "Generic health alerts often ignore who is most vulnerable (asthma patients, elderly, children) and what actions reduce risk.",
            "#fb923c",
            "rgba(251,146,60,0.22)",
            "🧬",
        ),
        unsafe_allow_html=True,
    )

# Real-world impact + premium metrics
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """<div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:900; color:#e8f4ff; margin-bottom:0.7rem;">C) Real-world Impact</div>""",
    unsafe_allow_html=True,
)

impact_cols = st.columns(2, gap="large")

with impact_cols[0]:
    st.markdown(
        """
        <div style="background:rgba(2,15,35,0.7); border:1px solid rgba(0,212,255,0.15); border-radius:16px; padding:18px 20px;">
          <div style="font-family:'Inter',sans-serif; font-weight:900; letter-spacing:0.12em; text-transform:uppercase; color:#38bdf8; font-size:0.78rem;">Who benefits</div>
          <ul style="margin:10px 0 0 18px; color:#7db8d8; font-family:'Inter',sans-serif; line-height:1.85; font-size:0.95rem;">
            <li>Citizens planning day-to-day exposure</li>
            <li>Asthma patients and respiratory-care communities</li>
            <li>Children and elderly caregivers</li>
            <li>Hospitals & public health teams</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with impact_cols[1]:
    st.markdown(
        """
        <div style="background:rgba(2,15,35,0.7); border:1px solid rgba(0,212,255,0.15); border-radius:16px; padding:18px 20px;">
          <div style="font-family:'Inter',sans-serif; font-weight:900; letter-spacing:0.12em; text-transform:uppercase; color:#00ffd4; font-size:0.78rem;">Extended stakeholders</div>
          <ul style="margin:10px 0 0 18px; color:#94a3b8; font-family:'Inter',sans-serif; line-height:1.85; font-size:0.95rem;">
            <li>Schools (safety for outdoor learning)</li>
            <li>City planners & transport agencies</li>
            <li>Government agencies for targeted interventions</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """<div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:900; color:#e8f4ff; margin-bottom:0.7rem;">D) Premium Impact Metrics</div>""",
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4, gap="large")

with m1:
    st.markdown(metric_card("Annual air pollution deaths", "~1.0L+", "Illustrative estimate used for hackathon narrative", "#ff4444"), unsafe_allow_html=True)
with m2:
    st.markdown(metric_card("Vulnerable population", "Millions", "Asthma, elderly, children—highest exposure risk", "#fb923c"), unsafe_allow_html=True)
with m3:
    st.markdown(metric_card("Cities affected", "~100+", "Across NCR + tier-1/2 Indian metros", "#00d4ff"), unsafe_allow_html=True)
with m4:
    st.markdown(metric_card("Estimated economic impact", "₹ Trillions", "Healthcare, lost productivity & logistics costs", "#00ffd4"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """<div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:900; color:#e8f4ff; margin-bottom:0.7rem;">E) How VaayuVigyaan Helps</div>""",
    unsafe_allow_html=True,
)

# Animated premium cards (UI only)
help_flow = [
    ("🔮 Predict PM2.5", "Forecast risk before you step out" , "#38bdf8"),
    ("🧠 Explainable AI", "Understand drivers behind pollution" , "#00ffd4"),
    ("🏥 Health Intelligence", "Personalized guidance for vulnerable groups" , "#ff8800"),
    ("🛠️ Smart Decisions", "What-if scenarios for smarter interventions" , "#a78bfa"),
]

fc1, fc2, fc3, fc4 = st.columns(4, gap="large")
for (col, (t, b, c)) in zip([fc1, fc2, fc3, fc4], help_flow):
    with col:
        st.markdown(
            f"""
            <div style="background:rgba(2,15,35,0.85); border:1px solid {c}2A;
                        border-radius:18px; padding:18px 18px; position:relative; overflow:hidden;
                        box-shadow:0 0 50px {c}12;">
                <div style="position:absolute; inset:-60px -60px auto auto; width:160px; height:160px;
                            background:radial-gradient(circle, {c}33, transparent 60%); opacity:0.9;"></div>
                <div style="position:relative;">
                    <div style="font-family:'Orbitron',monospace; font-size:0.78rem; font-weight:900;
                                letter-spacing:0.25em; text-transform:uppercase; color:{c}; opacity:0.95;">
                        PREMIUM MODULE
                    </div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.2rem; font-weight:950;
                                color:#e8f4ff; margin-top:10px; line-height:1.2;">{t}</div>
                    <div style="font-family:'Inter',sans-serif; color:#7db8d8; font-size:0.95rem; margin-top:8px; line-height:1.6;">{b}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("""<div style="height:18px"></div>""", unsafe_allow_html=True)

