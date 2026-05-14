"""
VaayuVigyaan AI — Shared CSS styles and theme utilities
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #020b18;
    --bg-secondary: #041428;
    --bg-card: rgba(4, 30, 60, 0.7);
    --accent-cyan: #00d4ff;
    --accent-teal: #00ffd4;
    --accent-blue: #0088ff;
    --accent-green: #00ff88;
    --accent-red: #ff4444;
    --accent-orange: #ff8800;
    --text-primary: #e8f4ff;
    --text-secondary: #7db8d8;
    --border-glow: rgba(0, 212, 255, 0.3);
    --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.15);
    --radius: 16px;
}

html, body, .stApp {
    background: #020b18 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e8f4ff !important;
}
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 50% -20%, rgba(0,100,200,0.15) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,212,255,0.08) 0%, transparent 60%),
        linear-gradient(180deg, #020b18 0%, #020a15 100%) !important;
    background-attachment: fixed !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
div[data-testid="stToolbar"] {visibility: hidden;}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020e1e 0%, #010a16 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.2) !important;
}

[data-testid="stSidebarNav"] a {
    color: #7db8d8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
}
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #00d4ff !important;
    background: rgba(0,212,255,0.1) !important;
}

h1 { font-family: 'Orbitron', monospace !important; color: #e8f4ff !important; }
h2 { font-family: 'Inter', sans-serif !important; color: #e8f4ff !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
h3 { font-family: 'Inter', sans-serif !important; color: #cbd5e1 !important; font-weight: 600 !important; }
p, .stMarkdown p { color: #94a3b8 !important; font-family: 'Inter', sans-serif !important; font-size: 0.975rem !important; line-height: 1.65 !important; }

.stButton > button {
    background: linear-gradient(135deg, rgba(0,136,255,0.2), rgba(0,212,255,0.1)) !important;
    border: 1px solid #00d4ff !important;
    color: #00d4ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.3), rgba(0,255,212,0.1)) !important;
    box-shadow: 0 0 25px rgba(0,212,255,0.4) !important;
    transform: translateY(-2px) !important;
}

[data-testid="metric-container"] {
    background: rgba(4,30,60,0.7) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 30px rgba(0,212,255,0.1) !important;
    transition: all 0.3s !important;
}
[data-testid="metric-container"]:hover {
    border-color: #00d4ff !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 40px rgba(0,212,255,0.25) !important;
    transform: translateY(-3px) !important;
}
[data-testid="stMetricValue"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.8rem !important;
}
[data-testid="stMetricLabel"] {
    color: #7db8d8 !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-size: 0.85rem !important;
}

.stSlider [data-testid="stSliderThumb"] { background: #00d4ff !important; }
.stSlider [data-testid="stSliderTrackFill"] { background: linear-gradient(90deg, #0088ff, #00d4ff) !important; }

.stSelectbox div[data-baseweb="select"] > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(0,20,50,0.8) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
    border-radius: 8px !important;
    color: #e8f4ff !important;
}

hr { border: none !important; height: 1px !important; background: linear-gradient(90deg, transparent, #00d4ff, transparent) !important; opacity: 0.3 !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #020b18; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #0088ff, #00d4ff); border-radius: 3px; }

@keyframes fadeInUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse-glow { 0%,100% { box-shadow: 0 0 20px rgba(0,212,255,0.2); } 50% { box-shadow: 0 0 40px rgba(0,212,255,0.5); } }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes scanline { from { transform: translateY(-100%); } to { transform: translateY(200vh); } }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,20,50,0.5) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    gap: 4px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7db8d8 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,136,255,0.3), rgba(0,212,255,0.15)) !important;
    color: #00d4ff !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #0088ff, #00d4ff, #00ffd4) !important;
    box-shadow: 0 0 10px rgba(0,212,255,0.5) !important;
}
.stProgress > div { background: rgba(0,20,50,0.5) !important; }

.stExpander {
    background: rgba(4,30,60,0.7) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 12px !important;
}

/* ── PREMIUM UPGRADES ─────────────────────────────── */
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebarNav"] a {
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
}
label, .stSelectbox label, .stSlider label, .stMultiSelect label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
/* Metric value — keep mono feel with Inter numeric */
[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}
/* Code/mono spans use JetBrains Mono */
code, pre, .stCode, [data-testid="stCode"] {
    font-family: 'JetBrains Mono', monospace !important;
}
/* Smooth focus ring */
*:focus-visible {
    outline: 2px solid rgba(56,189,248,0.5) !important;
    outline-offset: 2px !important;
}
/* Expander header */
.streamlit-expanderHeader p {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #e2e8f0 !important;
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title, subtitle="", icon=""):
    return f"""
    <div style="padding:1.75rem 0 1.25rem 0; animation: fadeInUp 0.5s ease-out;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:0.6rem;">
            <div style="width:3px; height:18px; background:linear-gradient(180deg,#38bdf8,#0ea5e9); border-radius:2px;"></div>
            <span style="font-family:'Inter',sans-serif; font-size:0.7rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#38bdf8; opacity:0.8;">VaayuVigyaan AI · India</span>
        </div>
        <h1 style="font-family:'Inter',sans-serif; font-size:1.85rem; font-weight:800;
            background: linear-gradient(135deg,#f1f5f9 0%,#38bdf8 55%,#67e8f9 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text; margin:0 0 0.4rem 0; line-height:1.15;
            letter-spacing:-0.03em;">{icon} {title}</h1>
        <p style="font-family:'Inter',sans-serif; color:#64748b; font-size:0.925rem;
            margin:0; font-weight:400; line-height:1.5;">{subtitle}</p>
        <div style="height:1px; background:linear-gradient(90deg,#38bdf8,#0ea5e9,transparent); margin-top:1.1rem; opacity:0.4;"></div>
    </div>"""


def aqi_badge(value):
    if value <= 50:
        cat, color, bg = "GOOD", "#00ff88", "rgba(0,255,136,0.1)"
    elif value <= 100:
        cat, color, bg = "MODERATE", "#ffdd00", "rgba(255,221,0,0.1)"
    elif value <= 150:
        cat, color, bg = "SENSITIVE", "#ff8800", "rgba(255,136,0,0.1)"
    elif value <= 200:
        cat, color, bg = "UNHEALTHY", "#ff4444", "rgba(255,68,68,0.1)"
    elif value <= 300:
        cat, color, bg = "V.UNHEALTHY", "#cc00ff", "rgba(204,0,255,0.1)"
    else:
        cat, color, bg = "HAZARDOUS", "#990000", "rgba(153,0,0,0.2)"
    return f'<span style="background:{bg};border:1px solid {color};color:{color};font-family:Orbitron,monospace;font-size:0.6rem;font-weight:700;letter-spacing:0.15em;padding:3px 10px;border-radius:20px;text-shadow:0 0 8px {color};">{cat}</span>'


def pm25_to_aqi(pm25):
    breakpoints = [
        (0,12,0,50),(12.1,35.4,51,100),(35.5,55.4,101,150),
        (55.5,150.4,151,200),(150.5,250.4,201,300),(250.5,350.4,301,400),(350.5,500,401,500)
    ]
    for lo_c,hi_c,lo_i,hi_i in breakpoints:
        if lo_c <= pm25 <= hi_c:
            return round(lo_i + (pm25 - lo_c)*(hi_i - lo_i)/(hi_c - lo_c))
    return 500


def get_city_data():
    """Returns realistic sample data for Indian cities."""
    import numpy as np
    cities = {
        "Delhi": {"lat":28.6139,"lon":77.2090,"pm25":145,"pm10":220,"aod":0.82,"temp":35,"humidity":55,"wind":2.1,"industry":0.9,"traffic":0.95},
        "Mumbai": {"lat":19.0760,"lon":72.8777,"pm25":82,"pm10":130,"aod":0.55,"temp":31,"humidity":78,"wind":4.2,"industry":0.65,"traffic":0.80},
        "Kolkata": {"lat":22.5726,"lon":88.3639,"pm25":118,"pm10":178,"aod":0.71,"temp":33,"humidity":72,"wind":1.8,"industry":0.75,"traffic":0.85},
        "Chennai": {"lat":13.0827,"lon":80.2707,"pm25":58,"pm10":92,"aod":0.38,"temp":34,"humidity":70,"wind":5.5,"industry":0.55,"traffic":0.65},
        "Bengaluru": {"lat":12.9716,"lon":77.5946,"pm25":72,"pm10":115,"aod":0.44,"temp":28,"humidity":60,"wind":3.2,"industry":0.60,"traffic":0.75},
        "Hyderabad": {"lat":17.3850,"lon":78.4867,"pm25":88,"pm10":142,"aod":0.58,"temp":32,"humidity":52,"wind":3.8,"industry":0.65,"traffic":0.70},
        "Pune": {"lat":18.5204,"lon":73.8567,"pm25":95,"pm10":150,"aod":0.61,"temp":30,"humidity":58,"wind":3.0,"industry":0.70,"traffic":0.72},
        "Ahmedabad": {"lat":23.0225,"lon":72.5714,"pm25":110,"pm10":175,"aod":0.68,"temp":36,"humidity":45,"wind":2.5,"industry":0.80,"traffic":0.75},
        "Lucknow": {"lat":26.8467,"lon":80.9462,"pm25":132,"pm10":198,"aod":0.76,"temp":34,"humidity":60,"wind":2.0,"industry":0.72,"traffic":0.80},
        "Jaipur": {"lat":26.9124,"lon":75.7873,"pm25":105,"pm10":165,"aod":0.65,"temp":38,"humidity":40,"wind":2.8,"industry":0.68,"traffic":0.70},
    }
    return cities
