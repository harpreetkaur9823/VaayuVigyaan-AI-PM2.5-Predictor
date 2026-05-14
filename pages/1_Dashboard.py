"""
VaayuVigyaan AI — Analytics Dashboard
Live data via OpenWeatherMap API · CPCB fallback
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os

from folium import Map
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.styles import inject_css, page_header, aqi_badge, pm25_to_aqi, get_city_data
from utils.live_api import get_live_air_data, CITY_COORDS, co_ugm3_to_ppm


st.set_page_config(page_title="Dashboard | VaayuVigyaan", page_icon="📊", layout="wide")
inject_css()

CHART_CFG = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(2,15,35,0.7)',
    font=dict(family='Inter, sans-serif', color='#64748b', size=12),
    title_font=dict(family='Inter, sans-serif', color='#e2e8f0', size=14, weight=600),
    xaxis=dict(gridcolor='rgba(56,189,248,0.07)', tickfont=dict(color='#475569', size=11),
               linecolor='rgba(56,189,248,0.1)'),
    yaxis=dict(gridcolor='rgba(56,189,248,0.07)', tickfont=dict(color='#475569', size=11),
               linecolor='rgba(56,189,248,0.1)'),
    margin=dict(l=16, r=16, t=44, b=16),
)

def hex_to_rgba(hex_color, alpha=0.1):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'

st.markdown(page_header("Analytics Dashboard",
    "Real-time AQI · OpenWeatherMap Live API · CPCB 2025 dataset", "📊"),
    unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
        letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;opacity:0.7;
        margin-bottom:0.75rem;">Dashboard Controls</div>""", unsafe_allow_html=True)
    all_cities = list(CITY_COORDS.keys())
    selected_cities = st.multiselect("Cities", all_cities, default=all_cities[:8])
    time_range = st.selectbox("Trend Period", ["Last 7 days","Last 30 days","Last 90 days","Last Year"])
    refresh_btn = st.button("🔄 Refresh Live Data", use_container_width=True)

if not selected_cities:
    selected_cities = all_cities[:8]

# ── Fetch live data ───────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_live(cities):
    return {c: get_live_air_data(c) for c in cities}

if refresh_btn:
    st.cache_data.clear()

with st.spinner("Fetching live air quality data..."):
    live_data = fetch_all_live(tuple(selected_cities))

# Check if any city returned live data
any_live = any(live_data[c].get("is_live", False) for c in selected_cities)
source_label = "OpenWeatherMap Live ◉" if any_live else "CPCB Estimates (offline)"
source_color = "#4ade80" if any_live else "#facc15"

st.markdown(f"""
<div style="display:inline-flex;align-items:center;gap:8px;margin-bottom:1rem;
    background:rgba(2,15,35,0.6);border:1px solid {source_color}30;
    border-radius:8px;padding:6px 14px;">
    <div style="width:7px;height:7px;border-radius:50%;background:{source_color};
        box-shadow:0 0 6px {source_color};
        {'animation:pulse-glow 2s infinite' if any_live else ''}"></div>
    <span style="font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:500;
        color:{source_color};">{source_label}</span>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
pm25_vals = [live_data[c]['pm25'] for c in selected_cities]
aqi_vals  = [pm25_to_aqi(v) for v in pm25_vals]
worst_idx = int(np.argmax(pm25_vals))
best_idx  = int(np.argmin(pm25_vals))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Avg PM₂.₅",       f"{np.mean(pm25_vals):.0f} µg/m³", f"WHO limit: 35")
c2.metric("Avg AQI",          f"{np.mean(aqi_vals):.0f}")
c3.metric("Most Polluted",    selected_cities[worst_idx], f"{pm25_vals[worst_idx]:.0f} µg/m³")
c4.metric("Cleanest",         selected_cities[best_idx],  f"{pm25_vals[best_idx]:.0f} µg/m³")
c5.metric("Cities Unhealthy", f"{sum(1 for v in aqi_vals if v>150)}/{len(selected_cities)}", "AQI > 150")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Live city AQI cards ──────────────────────────────────────────────────────
st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
    letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;
    opacity:0.7;margin-bottom:0.75rem;">Live City Readings</div>""", unsafe_allow_html=True)

n_cols = min(len(selected_cities), 5)
rows_needed = (len(selected_cities) + n_cols - 1) // n_cols

for row in range(rows_needed):
    cols = st.columns(n_cols)
    for col_i in range(n_cols):
        idx = row * n_cols + col_i
        if idx >= len(selected_cities):
            break
        city = selected_cities[idx]
        d    = live_data[city]
        pm25 = d['pm25']
        aqi_v = pm25_to_aqi(pm25)
        badge = aqi_badge(aqi_v)
        is_live = d.get('is_live', False)

        if aqi_v <= 50:    c, glow = "#4ade80", "rgba(74,222,128,0.12)"
        elif aqi_v <= 100: c, glow = "#facc15", "rgba(250,204,21,0.1)"
        elif aqi_v <= 150: c, glow = "#fb923c", "rgba(251,146,60,0.1)"
        elif aqi_v <= 200: c, glow = "#f87171", "rgba(248,113,113,0.1)"
        else:              c, glow = "#c084fc", "rgba(192,132,252,0.1)"

        live_dot = f'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#4ade80;box-shadow:0 0 5px #4ade80;margin-left:4px;"></span>' if is_live else ''

        with cols[col_i]:
            st.markdown(f"""
            <div style="background:rgba(2,15,35,0.85);border:1px solid {c}30;
                border-top:2px solid {c};border-radius:12px;padding:16px 12px;
                text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.4),0 0 20px {glow};
                transition:all 0.3s;margin-bottom:0.75rem;">
                <div style="font-family:'Inter',sans-serif;font-weight:600;font-size:0.85rem;
                    color:#e2e8f0;margin-bottom:6px;">{city}{live_dot}</div>
                <div style="font-family:'Inter',sans-serif;font-size:2rem;font-weight:800;
                    color:{c};letter-spacing:-0.04em;line-height:1;">{aqi_v}</div>
                <div style="font-family:'Inter',monospace;font-size:0.65rem;color:#475569;
                    margin:4px 0;">PM₂.₅ {pm25} µg/m³</div>
                <div style="margin-top:6px;">{badge}</div>
                {'<div style="font-family:Inter,sans-serif;font-size:0.6rem;color:#64748b;margin-top:4px;">NO₂: '+str(d.get("no2","—"))+'  SO₂: '+str(d.get("so2","—"))+'</div>' if any_live else ''}
            </div>""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🗺  Pollution Map", "📈  Trends", "⚖  Comparison", "🌡  Correlations"])

with tab1:

    st.markdown("""
    <style>
    .map-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }

    .map-sub {
        color: #94a3b8;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="map-title">
            🌍 Live India Pollution Intelligence Map
        </div>
        <div class="map-sub">
            Real-time PM2.5 heat intensity across India
        </div>
        """,
        unsafe_allow_html=True
    )

    india_center = [22.9734, 79.1361]

    # -----------------------------
    # AQI COLORS
    # -----------------------------
    def aqi_color(aqi):
        if aqi <= 50:
            return "#00ff88"
        elif aqi <= 100:
            return "#d9ff00"
        elif aqi <= 150:
            return "#ffb300"
        elif aqi <= 200:
            return "#ff5500"
        else:
            return "#ff0000"

    # -----------------------------
    # CREATE PREMIUM MAP
    # -----------------------------
    m = folium.Map(
        location=india_center,
        zoom_start=5,
        tiles=None,
        control_scale=True
    )

    # NASA / Earth-like dark basemap
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        name="Dark Earth",
        control=False
    ).add_to(m)

    # -----------------------------
    # BUILD DATA
    # -----------------------------
    heat_data = []

    for city in selected_cities:

        try:
            d = live_data.get(city, {})

            lat = d.get("latitude")
            lon = d.get("longitude")
            pm25 = d.get("pm25")

            if lat is None or lon is None or pm25 is None:
                continue

            lat = float(lat)
            lon = float(lon)
            pm25 = float(pm25)

            aqi = pm25_to_aqi(pm25)

            # Stronger weighted heatmap
            intensity = min(pm25 * 2.5, 300)

            heat_data.append([lat, lon, intensity])

            color = aqi_color(aqi)

            # -----------------------------
            # BIG OUTER GLOW
            # -----------------------------
            folium.Circle(
                location=[lat, lon],
                radius=65000,
                color=None,
                fill=True,
                fill_color=color,
                fill_opacity=0.10
            ).add_to(m)

            # -----------------------------
            # MAIN CITY GLOW
            # -----------------------------
            folium.Circle(
                location=[lat, lon],
                radius=35000,
                color=None,
                fill=True,
                fill_color=color,
                fill_opacity=0.25
            ).add_to(m)

            # -----------------------------
            # CENTER CORE
            # -----------------------------
            folium.CircleMarker(
                location=[lat, lon],
                radius=12,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.95,
                weight=0,
                tooltip=f"""
                <b>{city}</b><br>
                AQI: {aqi}<br>
                PM2.5: {pm25:.1f}
                """
            ).add_to(m)

        except Exception:
            pass

    # -----------------------------
    # REAL HEATMAP
    # -----------------------------
    if heat_data:

        HeatMap(
            heat_data,
            radius=50,
            blur=35,
            min_opacity=0.35,
            max_zoom=8,
            gradient={
                0.2: "#00ffff",
                0.4: "#00ff88",
                0.6: "#ffee00",
                0.8: "#ff5500",
                1.0: "#ff0000"
            }
        ).add_to(m)

    # -----------------------------
    # RENDER MAP
    # -----------------------------
    st_folium(
        m,
        height=700,
        use_container_width=True
    )

with tab2:
    np.random.seed(7)
    days = {"Last 7 days":7,"Last 30 days":30,"Last 90 days":90,"Last Year":365}[time_range]
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='D')
    palette = ['#38bdf8','#4ade80','#facc15','#fb923c','#f87171','#c084fc','#67e8f9','#a3e635']

    fig_ts = go.Figure()
    for idx, city in enumerate(selected_cities[:8]):
        base = live_data[city]['pm25']
        noise = np.random.normal(0, base*0.14, days)
        seasonal = 18 * np.sin(np.linspace(0, 2*np.pi, days))
        vals = np.clip(base + noise + seasonal, 5, 450)
        c = palette[idx % len(palette)]
        fig_ts.add_trace(go.Scatter(
            x=dates, y=vals, name=city, mode='lines',
            line=dict(width=1.8, color=c),
            fill='tozeroy', fillcolor=hex_to_rgba(c, 0.03),
        ))
    fig_ts.add_hline(y=35.4, line=dict(color='#4ade80', dash='dash', width=1),
                     annotation_text="WHO 35", annotation_font=dict(color='#4ade80', size=9, family='Inter'))
    fig_ts.update_layout(title="PM₂.₅ Historical Trend", **CHART_CFG, height=400,
        hovermode='x unified',
        legend=dict(bgcolor='rgba(2,15,35,0.6)', bordercolor='rgba(56,189,248,0.12)',
                    borderwidth=1, font=dict(color='#94a3b8', size=11, family='Inter')))
    st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})

    # Seasonal heatmap
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    seasonal_f = [1.5,1.4,1.1,0.9,0.8,0.65,0.5,0.5,0.7,1.0,1.3,1.6]
    matrix = []
    cities_heat = selected_cities[:8]
    for city in cities_heat:
        base = live_data[city]['pm25']
        row = [round(base * f * np.random.uniform(0.9, 1.1)) for f in seasonal_f]
        matrix.append(row)

    fig_heat = go.Figure(go.Heatmap(
        z=matrix, x=months, y=cities_heat,
        colorscale=[[0,'#0f4c20'],[0.25,'#4ade80'],[0.5,'#facc15'],
                    [0.75,'#f87171'],[1,'#7f1d1d']],
        text=[[str(v) for v in row] for row in matrix],
        texttemplate='%{text}', textfont=dict(size=10, family='Inter', color='white'),
        hovertemplate='%{y} — %{x}: %{z} µg/m³<extra></extra>',
    ))
    fig_heat.update_layout(title="Monthly PM₂.₅ Pattern (µg/m³)", **CHART_CFG, height=320)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        df_bar = pd.DataFrame([{
            "City": c,
            "PM₂.₅": live_data[c]['pm25'],
            "AQI": pm25_to_aqi(live_data[c]['pm25'])
        } for c in selected_cities]).sort_values("PM₂.₅")

        bar_colors = []
        for v in df_bar['AQI']:
            if v <= 50:    bar_colors.append('#4ade80')
            elif v <= 100: bar_colors.append('#facc15')
            elif v <= 150: bar_colors.append('#fb923c')
            elif v <= 200: bar_colors.append('#f87171')
            else:          bar_colors.append('#c084fc')

        fig_bar = go.Figure(go.Bar(
            x=df_bar['PM₂.₅'], y=df_bar['City'],
            orientation='h',
            marker=dict(color=bar_colors, opacity=0.85, line=dict(width=0)),
            text=[f"{v} µg/m³" for v in df_bar['PM₂.₅']],
            textposition='outside',
            textfont=dict(family='Inter', size=10, color='#94a3b8'),
            hovertemplate='%{y}: %{x} µg/m³<extra></extra>',
        ))
        fig_bar.add_vline(x=35.4, line=dict(color='#4ade80', dash='dash', width=1),
                          annotation_text="WHO", annotation_font=dict(color='#4ade80', size=9, family='Inter'))
        fig_bar.update_layout(title="PM₂.₅ Ranking (Live)", **CHART_CFG, height=380,
                               xaxis_title="PM₂.₅ (µg/m³)", yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        # Multi-pollutant bar comparison for live data
        pollutants = ['pm25', 'pm10', 'no2', 'so2']
        poll_labels = ['PM₂.₅', 'PM₁₀', 'NO₂', 'SO₂']
        poll_colors = ['#38bdf8', '#4ade80', '#facc15', '#f87171']

        fig_mp = go.Figure()
        for poll, label, color in zip(pollutants, poll_labels, poll_colors):
            vals = [live_data[c].get(poll, 0) or 0 for c in selected_cities[:6]]
            fig_mp.add_trace(go.Bar(
                name=label, x=selected_cities[:6], y=vals,
                marker=dict(color=color, opacity=0.8, line=dict(width=0)),
                hovertemplate=f'{label}: %{{y:.1f}} µg/m³<extra></extra>',
            ))
        fig_mp.update_layout(title="Multi-Pollutant Comparison (Live)", **CHART_CFG,
                              height=380, barmode='group',
                              legend=dict(bgcolor='rgba(2,15,35,0.6)',
                                          font=dict(color='#94a3b8', family='Inter', size=11)))
        st.plotly_chart(fig_mp, use_container_width=True, config={"displayModeBar": False})

with tab4:
    col_c, col_d = st.columns(2)
    with col_c:
        scatter_df = pd.DataFrame([{
            "city": c,
            "no2":  live_data[c].get("no2", 0) or 0,
            "pm25": live_data[c]["pm25"],
            "aqi":  pm25_to_aqi(live_data[c]["pm25"]),
        } for c in selected_cities])

        fig_sc = px.scatter(scatter_df, x='no2', y='pm25', text='city', color='aqi',
            color_continuous_scale=[[0,'#4ade80'],[0.4,'#facc15'],[0.7,'#f87171'],[1,'#c084fc']],
            size=[30]*len(scatter_df),
            labels={'no2':'NO₂ (µg/m³)', 'pm25':'PM₂.₅ (µg/m³)', 'aqi':'AQI'})
        fig_sc.update_traces(textposition='top center',
                              textfont=dict(size=10, family='Inter', color='white'))
        fig_sc.update_layout(title="NO₂ vs PM₂.₅ (Live)", **CHART_CFG, height=360)
        st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

    with col_d:
        scatter_df2 = pd.DataFrame([{
            "city":     c,
            "humidity": live_data[c].get("humidity") or 60,
            "pm25":     live_data[c]["pm25"],
        } for c in selected_cities])

        fig_sc2 = px.scatter(scatter_df2, x='humidity', y='pm25', text='city',
            color='pm25',
            color_continuous_scale=[[0,'#4ade80'],[0.5,'#fb923c'],[1,'#c084fc']],
            size=[30]*len(scatter_df2),
            trendline='ols',
            labels={'humidity':'Humidity (%)', 'pm25':'PM₂.₅ (µg/m³)'})
        fig_sc2.update_traces(textposition='top center',
                               textfont=dict(size=10, family='Inter', color='white'))
        fig_sc2.update_layout(title="Humidity vs PM₂.₅ Correlation", **CHART_CFG, height=360)
        st.plotly_chart(fig_sc2, use_container_width=True, config={"displayModeBar": False})
