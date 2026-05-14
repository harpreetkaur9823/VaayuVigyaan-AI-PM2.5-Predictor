"""
VaayuVigyaan AI — What-If Scenario Simulator
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.styles import inject_css, page_header, aqi_badge, pm25_to_aqi, get_city_data

st.set_page_config(page_title="What-If Simulator | VaayuVigyaan", page_icon="⚗️", layout="wide")
inject_css()

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,10,25,0.6)',
    font=dict(family='Rajdhani', color='#7db8d8'),
    title_font=dict(family='Orbitron', color='#e8f4ff', size=13),
    xaxis=dict(gridcolor='rgba(0,212,255,0.1)', tickfont=dict(color='#7db8d8')),
    yaxis=dict(gridcolor='rgba(0,212,255,0.1)', tickfont=dict(color='#7db8d8')),
    margin=dict(l=20,r=20,t=50,b=20),
)

st.markdown(page_header("What-If Simulator", "Simulate policy interventions and measure projected PM2.5 impact", "⚗️"), unsafe_allow_html=True)

cities = get_city_data()
with st.sidebar:
    city = st.selectbox("📍 Simulate City", list(cities.keys()), index=0)

data = cities[city]
pm25_base = data['pm25']
aqi_base  = pm25_to_aqi(pm25_base)

# ─── Info header ──────────────────────────────────────────────────────────────
badge = aqi_badge(aqi_base)
st.markdown(f"""
<div style="background:rgba(4,20,45,0.7); border:1px solid rgba(0,212,255,0.2);
    border-radius:16px; padding:20px 24px; margin-bottom:1.5rem;
    display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
    <div>
        <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:0.2em; color:#7db8d8;">
            BASELINE SCENARIO — {city.upper()}
        </div>
        <div style="display:flex; align-items:center; gap:16px; margin-top:8px; flex-wrap:wrap;">
            <span style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:800; color:#ff8800;">
                {pm25_base} µg/m³
            </span>
            {badge}
        </div>
    </div>
    <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#7db8d8; text-align:right;">
        Adjust intervention sliders →<br>
        See projected improvement in real-time
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Intervention sliders ─────────────────────────────────────────────────────
col_sliders, col_results = st.columns([1.1, 1], gap="large")

with col_sliders:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:0.25em;
        color:#00d4ff; opacity:0.8; margin-bottom:1rem;">▸ POLICY INTERVENTION CONTROLS</div>
    """, unsafe_allow_html=True)

    # Traffic intervention
    st.markdown("""<div style="background:rgba(4,20,45,0.6); border:1px solid rgba(0,212,255,0.15);
        border-radius:12px; padding:16px; margin-bottom:12px;">""", unsafe_allow_html=True)
    traffic_cut = st.slider("🚗 Traffic Reduction (%)", 0, 80, 0, 5,
                            help="Odd-even scheme, metro expansion, WFH policies")
    ev_adoption = st.slider("⚡ EV Fleet Adoption (%)", 0, 100, 0, 5,
                            help="% of vehicles converted to electric")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(4,20,45,0.6); border:1px solid rgba(0,212,255,0.15);
        border-radius:12px; padding:16px; margin-bottom:12px;">""", unsafe_allow_html=True)
    industry_cut = st.slider("🏭 Industrial Emission Cut (%)", 0, 70, 0, 5,
                              help="Cleaner tech adoption, shift to gas from coal")
    factory_close = st.slider("🔒 Factory Closure Days/Month", 0, 30, 0, 1,
                               help="Scheduled shutdowns during high-AQI events")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(4,20,45,0.6); border:1px solid rgba(0,212,255,0.15);
        border-radius:12px; padding:16px; margin-bottom:12px;">""", unsafe_allow_html=True)
    rainfall_boost = st.slider("🌧 Artificial Rainfall (Cloud Seeding mm)", 0, 30, 0, 1,
                                help="Simulate cloud-seeding intervention")
    green_cover    = st.slider("🌳 Green Cover Increase (%)", 0, 40, 0, 2,
                                help="Urban forestry, rooftop gardens, parks")
    dust_control   = st.slider("🛣 Road Dust Control (%)", 0, 80, 0, 5,
                                help="Water spraying, paved roads, dust barriers")
    st.markdown("</div>", unsafe_allow_html=True)

    # Source contribution factors (from city data)
    TRAFFIC_SHARE  = data['traffic'] * 0.35
    INDUSTRY_SHARE = data['industry'] * 0.30
    DUST_SHARE     = 0.12
    BIOMASS_SHARE  = 0.10
    OTHER_SHARE    = 1 - TRAFFIC_SHARE - INDUSTRY_SHARE - DUST_SHARE - BIOMASS_SHARE

    # Calculate PM2.5 reduction
    traffic_reduction  = pm25_base * TRAFFIC_SHARE * (traffic_cut / 100) * (1 + ev_adoption * 0.005)
    industry_reduction = pm25_base * INDUSTRY_SHARE * (industry_cut / 100) * (1 + factory_close * 0.01)
    rain_reduction     = rainfall_boost * 0.8
    green_reduction    = pm25_base * (green_cover / 100) * 0.15
    dust_reduction     = pm25_base * DUST_SHARE * (dust_control / 100)

    total_reduction = traffic_reduction + industry_reduction + rain_reduction + green_reduction + dust_reduction
    pm25_projected  = max(3, pm25_base - total_reduction)
    aqi_projected   = pm25_to_aqi(pm25_projected)
    pct_improvement = (total_reduction / pm25_base * 100) if pm25_base > 0 else 0

with col_results:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:0.25em;
        color:#00ffd4; opacity:0.8; margin-bottom:1rem;">▸ PROJECTED OUTCOME</div>
    """, unsafe_allow_html=True)

    # Big reduction display
    if pct_improvement < 15:   proj_color = "#ff8800"
    elif pct_improvement < 35: proj_color = "#ffdd00"
    else:                      proj_color = "#00ff88"

    badge_proj = aqi_badge(aqi_projected)

    st.markdown(f"""
    <div style="background:rgba(4,20,45,0.85); border:1px solid {proj_color}44;
        border-radius:20px; padding:28px; text-align:center; margin-bottom:1rem;
        box-shadow:0 0 40px {proj_color}15;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-bottom:1.5rem;">
            <div>
                <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.15em;
                    color:#7db8d8;">CURRENT PM2.5</div>
                <div style="font-family:'Orbitron',monospace; font-size:2.5rem; font-weight:800;
                    color:#ff8800; text-shadow:0 0 25px #ff880066;">{pm25_base}</div>
            </div>
            <div>
                <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.15em;
                    color:#7db8d8;">PROJECTED PM2.5</div>
                <div style="font-family:'Orbitron',monospace; font-size:2.5rem; font-weight:800;
                    color:{proj_color}; text-shadow:0 0 25px {proj_color}66;">{pm25_projected:.1f}</div>
            </div>
        </div>
        <div style="font-family:'Orbitron',monospace; font-size:4rem; font-weight:900;
            color:{proj_color}; text-shadow:0 0 50px {proj_color}; line-height:1;">
            ↓ {pct_improvement:.1f}%
        </div>
        <div style="font-family:'Rajdhani',sans-serif; color:#7db8d8; margin:8px 0;">
            Total PM2.5 Reduction: <b style="color:{proj_color};">{total_reduction:.1f} µg/m³</b>
        </div>
        <div style="margin-top:12px;">{badge_proj}</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a6b8a; margin-top:6px;">
            AQI: {aqi_base} → {aqi_projected}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Breakdown of reductions
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.2em;
        color:#00d4ff; opacity:0.7; margin-bottom:10px;">▸ INTERVENTION BREAKDOWN</div>
    """, unsafe_allow_html=True)

    breakdown = [
        ("🚗 Traffic + EV", traffic_reduction, "#00d4ff"),
        ("🏭 Industrial", industry_reduction, "#ff8800"),
        ("🌧 Rainfall", rain_reduction, "#0088ff"),
        ("🌳 Green Cover", green_reduction, "#00ff88"),
        ("🛣 Dust Control", dust_reduction, "#ffdd00"),
    ]
    for label, val, color in breakdown:
        pct = (val / total_reduction * 100) if total_reduction > 0 else 0
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div style="font-family:'Space Mono',monospace; font-size:0.7rem; color:#7db8d8;
                width:140px; flex-shrink:0;">{label}</div>
            <div style="flex:1; background:rgba(0,20,50,0.5); border-radius:4px; height:8px;">
                <div style="width:{pct:.1f}%; height:100%; background:{color};
                    border-radius:4px; box-shadow:0 0 6px {color}66; min-width:2px;"></div>
            </div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:{color};
                width:55px; text-align:right;">−{val:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Scenario comparison chart ────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:0.25em;
    color:#00d4ff; opacity:0.8; margin-bottom:1rem;">▸ SCENARIO MODELLING ACROSS INTERVENTION LEVELS</div>
""", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Traffic reduction sensitivity
    traffic_levels = np.arange(0, 81, 10)
    pm25_traf = [max(3, pm25_base - pm25_base * TRAFFIC_SHARE * (t/100)) for t in traffic_levels]
    fig_traf = go.Figure()
    fig_traf.add_trace(go.Scatter(
        x=traffic_levels, y=pm25_traf, mode='lines+markers',
        line=dict(color='#00d4ff', width=2.5),
        marker=dict(color='#00d4ff', size=7),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.06)',
        hovertemplate='%{x}% reduction → PM2.5: %{y:.1f}<extra></extra>',
    ))
    fig_traf.add_hline(y=35.4, line=dict(color='#00ff88', dash='dash', width=1),
                       annotation_text="WHO Safe 35",
                       annotation_font=dict(color='#00ff88', size=9))
    fig_traf.update_layout(
        title="Traffic Reduction Sensitivity",
        **CHART_LAYOUT, height=300,
        xaxis_title="Traffic Reduction (%)",
        yaxis_title="Projected PM2.5",
    )
    st.plotly_chart(fig_traf, use_container_width=True)

with col_chart2:
    # Combined scenario waterfall
    scenarios = ["Baseline", "Low Action\n(20%)", "Medium Action\n(40%)", "High Action\n(60%)", "Maximum\n(80%)"]
    scenario_pm25 = [pm25_base]
    for factor in [0.2, 0.4, 0.6, 0.8]:
        r = pm25_base * (TRAFFIC_SHARE*factor + INDUSTRY_SHARE*factor + DUST_SHARE*factor*0.5)
        scenario_pm25.append(max(3, pm25_base - r))

    bar_colors_s = []
    for v in scenario_pm25:
        aqi_v = pm25_to_aqi(v)
        if aqi_v <= 50:    bar_colors_s.append('#00ff88')
        elif aqi_v <= 100: bar_colors_s.append('#ffdd00')
        elif aqi_v <= 150: bar_colors_s.append('#ff8800')
        elif aqi_v <= 200: bar_colors_s.append('#ff4444')
        else:              bar_colors_s.append('#cc00ff')

    fig_scen = go.Figure(go.Bar(
        x=scenarios, y=scenario_pm25,
        marker=dict(color=bar_colors_s, opacity=0.85, line=dict(width=0)),
        text=[f"{v:.0f}" for v in scenario_pm25],
        textposition='outside',
        textfont=dict(family='Space Mono', size=11, color='white'),
        hovertemplate='%{x}: PM2.5 %{y:.1f} µg/m³<extra></extra>',
    ))
    fig_scen.add_hline(y=35.4, line=dict(color='#00ff88', dash='dash', width=1),
                       annotation_text="WHO target", annotation_font=dict(color='#00ff88', size=9))
    fig_scen.update_layout(
        title="Policy Action Scenarios",
        **CHART_LAYOUT, height=300,
        xaxis_title="Intervention Level",
        yaxis_title="PM2.5 (µg/m³)",
    )
    st.plotly_chart(fig_scen, use_container_width=True)

# ─── Environmental impact score ───────────────────────────────────────────────
env_score = min(100, pct_improvement * 1.5)
lives_saved_per_yr = int(pct_improvement * 3.2)  # rough proxy

st.markdown(f"""
<div style="background:linear-gradient(135deg, rgba(0,40,15,0.4), rgba(0,30,50,0.4));
    border:1px solid rgba(0,255,136,0.25); border-radius:16px; padding:24px;
    display:flex; gap:3rem; flex-wrap:wrap; align-items:center; justify-content:space-around;">
    <div style="text-align:center;">
        <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.2em; color:#7db8d8;">ENV. IMPACT SCORE</div>
        <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900; color:#00ff88;
            text-shadow:0 0 40px #00ff88;">{env_score:.0f}/100</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.2em; color:#7db8d8;">PM2.5 SAVED</div>
        <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900; color:#00d4ff;
            text-shadow:0 0 30px #00d4ff;">{total_reduction:.1f}</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a6b8a;">µg/m³ REDUCTION</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.2em; color:#7db8d8;">LIVES PROTECTED</div>
        <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900; color:#ffdd00;
            text-shadow:0 0 30px #ffdd00;">{lives_saved_per_yr:,}</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a6b8a;">EST. PER YEAR</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:0.2em; color:#7db8d8;">AQI IMPROVEMENT</div>
        <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900; color:#ff8800;
            text-shadow:0 0 30px #ff8800;">{aqi_base - aqi_projected}</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a6b8a;">AQI POINTS</div>
    </div>
</div>
""", unsafe_allow_html=True)
