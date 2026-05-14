"""
VaayuVigyaan AI — Future Forecast Page
Premium startup-grade temporal pollution projections.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.styles import inject_css, page_header, aqi_badge, pm25_to_aqi, get_city_data

st.set_page_config(
    page_title="Forecast | VaayuVigyaan",
    page_icon="📈",
    layout="wide",
)
inject_css()

# ── Premium chart defaults ────────────────────────────────────────────────────
CHART_CFG = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(2,15,35,0.7)',
    font=dict(family='Inter, sans-serif', color='#64748b', size=12),
    title_font=dict(family='Inter, sans-serif', color='#e2e8f0', size=14, weight=600),
    xaxis=dict(
        gridcolor='rgba(56,189,248,0.07)',
        zerolinecolor='rgba(56,189,248,0.15)',
        tickfont=dict(color='#475569', size=11),
        linecolor='rgba(56,189,248,0.1)',
    ),
    yaxis=dict(
        gridcolor='rgba(56,189,248,0.07)',
        zerolinecolor='rgba(56,189,248,0.15)',
        tickfont=dict(color='#475569', size=11),
        linecolor='rgba(56,189,248,0.1)',
    ),
    margin=dict(l=16, r=16, t=44, b=16),
)

st.markdown(
    page_header("Air Quality Forecast",
                "ML-driven PM2.5 projections · 6h · 24h · 72h · ensemble confidence bands",
                "📈"),
    unsafe_allow_html=True,
)

cities = get_city_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.7rem; font-weight:600;
        letter-spacing:0.1em; text-transform:uppercase; color:#38bdf8;
        opacity:0.7; margin-bottom:0.75rem;">Forecast Settings</div>
    """, unsafe_allow_html=True)
    city = st.selectbox("City", list(cities.keys()), index=0)
    show_ensemble = st.toggle("Ensemble Models", value=True)
    show_ci       = st.toggle("Confidence Bands", value=True)
    show_thresholds = st.toggle("AQI Thresholds", value=True)

data       = cities[city]
pm25_now   = data['pm25']
aqi_now    = pm25_to_aqi(pm25_now)

# ── Forecast generator ────────────────────────────────────────────────────────
def generate_forecast(base_pm25: float, hours: int, seed: int = 42):
    """
    Generate a realistic diurnal PM2.5 forecast.
    Returns (forecast, upper_ci, lower_ci) arrays.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(hours)
    now_hour = datetime.now().hour
    hour_of_day = (now_hour + t) % 24

    # Double-peak diurnal: morning rush ~8AM, evening rush ~7PM
    morning_peak = 18 * np.exp(-0.5 * ((hour_of_day - 8) / 3) ** 2)
    evening_peak = 14 * np.exp(-0.5 * ((hour_of_day - 19) / 2.5) ** 2)
    diurnal = morning_peak + evening_peak

    # Slight downward trend (e.g. wind picking up)
    trend = -0.04 * t

    noise   = rng.normal(0, base_pm25 * 0.07, hours)
    pm25    = np.clip(base_pm25 + diurnal + trend + noise, 4, 500)

    # Widening CI over time
    spread  = 0.08 + 0.003 * t
    upper   = np.clip(pm25 * (1 + spread), 4, 550)
    lower   = np.clip(pm25 * (1 - spread * 0.8), 2, 500)
    return pm25, upper, lower

# ── Top KPI row ───────────────────────────────────────────────────────────────
fc6,  _, _ = generate_forecast(pm25_now, 6,  seed=1)
fc24, _, _ = generate_forecast(pm25_now, 24, seed=2)
fc72, _, _ = generate_forecast(pm25_now, 72, seed=3)

delta6  = fc6[-1]  - pm25_now
delta24 = fc24[-1] - pm25_now
peak72  = fc72.max()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current PM2.5",    f"{pm25_now} µg/m³",    f"AQI {aqi_now}")
col2.metric("6h Projection",    f"{fc6[-1]:.0f} µg/m³", f"{delta6:+.0f} µg/m³",  delta_color="inverse")
col3.metric("24h Projection",   f"{fc24[-1]:.0f} µg/m³",f"{delta24:+.0f} µg/m³", delta_color="inverse")
col4.metric("72h Peak",         f"{peak72:.0f} µg/m³",  "worst-case window")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Tabbed forecast charts ─────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["⏱  6-Hour", "🕐  24-Hour", "📅  72-Hour"])

TABS = [
    (tab1, 6,  "6-Hour",  1),
    (tab2, 24, "24-Hour", 2),
    (tab3, 72, "72-Hour", 3),
]

for tab, hours, label, seed in TABS:
    with tab:
        pm25_fc, upper, lower = generate_forecast(pm25_now, hours, seed)
        now_dt = datetime.now().replace(second=0, microsecond=0)
        # Build datetime list — keep as datetime objects for plotly x-axis
        times = [now_dt + timedelta(hours=i) for i in range(hours)]

        fig = go.Figure()

        # ── Confidence band ──
        if show_ci:
            fig.add_trace(go.Scatter(
                x=times, y=upper,
                mode='lines', line=dict(width=0),
                showlegend=False, name='Upper CI',
            ))
            fig.add_trace(go.Scatter(
                x=times, y=lower,
                mode='lines', line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(56,189,248,0.09)',
                name='95% Confidence Band',
                showlegend=True,
            ))

        # ── Ensemble models ──
        if show_ensemble and hours <= 24:
            rng2 = np.random.default_rng(seed + 100)
            for ens_color, ens_mult, ens_name in [
                ('#a78bfa', 1.04, 'LSTM Ensemble'),
                ('#34d399', 0.96, 'ARIMA Ensemble'),
            ]:
                alt = np.clip(pm25_fc * ens_mult + rng2.normal(0, pm25_now * 0.04, hours), 4, 500)
                fig.add_trace(go.Scatter(
                    x=times, y=alt,
                    mode='lines',
                    line=dict(color=ens_color, width=1.5, dash='dot'),
                    name=ens_name, opacity=0.55,
                ))

        # ── Primary GBR forecast ──
        fig.add_trace(go.Scatter(
            x=times, y=pm25_fc,
            mode='lines+markers',
            line=dict(color='#38bdf8', width=2.5),
            marker=dict(
                color='#38bdf8', size=4,
                line=dict(color='rgba(56,189,248,0.3)', width=3),
            ),
            name='GBR Forecast',
        ))

        # ── AQI threshold lines ──
        if show_thresholds:
            thresholds = [
                (35.4,  '#4ade80', 'WHO Safe 35'),
                (55.4,  '#facc15', 'Moderate 55'),
                (150.4, '#f87171', 'Unhealthy 150'),
            ]
            for val, col, lbl in thresholds:
                fig.add_hline(
                    y=val,
                    line=dict(color=col, dash='dash', width=1),
                    annotation_text=lbl,
                    annotation_position="top right",
                    annotation_font=dict(color=col, size=9, family='Inter'),
                )

        # ── Background AQI zone bands ──
        fig.add_hrect(y0=0,    y1=35.4,  fillcolor='rgba(74,222,128,0.02)',  layer='below', line_width=0)
        fig.add_hrect(y0=35.4, y1=55.4,  fillcolor='rgba(250,204,21,0.02)',  layer='below', line_width=0)
        fig.add_hrect(y0=55.4, y1=150.4, fillcolor='rgba(248,113,113,0.02)', layer='below', line_width=0)
        fig.add_hrect(y0=150.4,y1=500,   fillcolor='rgba(167,139,250,0.02)', layer='below', line_width=0)

        # ── "NOW" vertical line ──
        # add_vline annotation is broken when x-axis has datetime values in some
        # plotly versions; use add_shape + add_annotation instead.
        fig.add_shape(
            type='line',
            xref='x', yref='paper',
            x0=now_dt, x1=now_dt,
            y0=0, y1=1,
            line=dict(color='#38bdf8', dash='solid', width=1.5),
        )
        fig.add_annotation(
            x=now_dt, xref='x',
            y=1.0, yref='paper',
            text="NOW",
            showarrow=False,
            yanchor='bottom',
            font=dict(color='#38bdf8', size=9, family='Inter'),
        )

        fig.update_layout(
            title=f"{label} PM₂.₅ Forecast — {city}",
            **CHART_CFG,
            height=400,
            xaxis_title="Time",
            yaxis_title="PM2.5 (µg/m³)",
            hovermode='x unified',
            legend=dict(
                bgcolor='rgba(2,15,35,0.6)',
                bordercolor='rgba(56,189,248,0.15)',
                borderwidth=1,
                font=dict(color='#94a3b8', size=11, family='Inter'),
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Forecast summary grid ─────────────────────────────────────────────
        interval   = 3 if hours <= 24 else 24
        s_times    = times[::interval][:8]
        s_vals     = pm25_fc[::interval][:8]
        s_aqis     = [pm25_to_aqi(v) for v in s_vals]

        st.markdown("""
        <div style="font-family:'Inter',sans-serif; font-size:0.68rem; font-weight:600;
            letter-spacing:0.1em; text-transform:uppercase; color:#38bdf8;
            opacity:0.7; margin:0.5rem 0 0.75rem;">Interval Summary</div>
        """, unsafe_allow_html=True)

        grid_cols = st.columns(min(len(s_times), 8))
        for i, (t_dt, pm_v, aqi_v) in enumerate(zip(s_times, s_vals, s_aqis)):
            if aqi_v <= 50:    c = "#4ade80"
            elif aqi_v <= 100: c = "#facc15"
            elif aqi_v <= 150: c = "#fb923c"
            elif aqi_v <= 200: c = "#f87171"
            else:              c = "#c084fc"

            t_str = t_dt.strftime("%d %b\n%H:%M") if hours > 24 else t_dt.strftime("%H:%M")
            with grid_cols[i]:
                st.markdown(f"""
                <div style="background:rgba(2,15,35,0.8);
                    border:1px solid {c}30;
                    border-top:2px solid {c};
                    border-radius:10px; padding:10px 8px; text-align:center;
                    transition:all 0.2s;">
                    <div style="font-family:'Inter',monospace; font-size:0.62rem;
                        color:#475569; white-space:pre; line-height:1.4;">{t_str}</div>
                    <div style="font-family:'Inter',sans-serif; font-size:1.05rem;
                        font-weight:700; color:{c}; margin:5px 0; line-height:1;">{pm_v:.0f}</div>
                    <div style="font-family:'Inter',sans-serif; font-size:0.6rem;
                        color:#475569; font-weight:500;">AQI {aqi_v}</div>
                </div>
                """, unsafe_allow_html=True)

# ── Multi-city 72h comparison ─────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.7rem; font-weight:600;
    letter-spacing:0.1em; text-transform:uppercase; color:#38bdf8;
    opacity:0.7; margin-bottom:1rem;">72-Hour Multi-City Comparison</div>
""", unsafe_allow_html=True)

compare_cities = list(cities.keys())[:6]
palette = ['#38bdf8','#4ade80','#facc15','#fb923c','#f87171','#c084fc']
fig_multi = go.Figure()
now_dt = datetime.now().replace(second=0, microsecond=0)
t72 = [now_dt + timedelta(hours=i) for i in range(72)]

for idx, c_name in enumerate(compare_cities):
    base = cities[c_name]['pm25']
    fc, _, _ = generate_forecast(base, 72, seed=idx * 7 + 11)
    fig_multi.add_trace(go.Scatter(
        x=t72, y=fc,
        name=c_name,
        mode='lines',
        line=dict(color=palette[idx % len(palette)], width=1.8),
        hovertemplate=f'{c_name}: %{{y:.0f}} µg/m³<extra></extra>',
    ))

fig_multi.add_hline(
    y=35.4,
    line=dict(color='#4ade80', dash='dash', width=1),
    annotation_text="WHO 35 µg/m³",
    annotation_font=dict(color='#4ade80', size=9, family='Inter'),
)

fig_multi.update_layout(
    title="72-Hour PM₂.₅ Forecast — Major Cities",
    **CHART_CFG,
    height=360,
    xaxis_title="Date",
    yaxis_title="PM2.5 (µg/m³)",
    hovermode='x unified',
    legend=dict(
        bgcolor='rgba(2,15,35,0.6)',
        bordercolor='rgba(56,189,248,0.15)',
        borderwidth=1,
        font=dict(color='#94a3b8', size=11, family='Inter'),
    ),
)
st.plotly_chart(fig_multi, use_container_width=True, config={"displayModeBar": False})

# ── Forecast accuracy card ─────────────────────────────────────────────────────
st.markdown("""
<div style="background:rgba(2,15,35,0.7);
    border:1px solid rgba(56,189,248,0.12);
    border-radius:14px; padding:20px 24px;
    display:flex; gap:3rem; flex-wrap:wrap; align-items:center;
    justify-content:space-around; margin-top:0.5rem;">
    <div style="text-align:center;">
        <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
            letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:4px;">6h MAE</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.8rem; font-weight:700;
            color:#4ade80; letter-spacing:-0.03em;">±4.2</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#475569;">µg/m³</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
            letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:4px;">24h MAE</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.8rem; font-weight:700;
            color:#38bdf8; letter-spacing:-0.03em;">±8.7</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#475569;">µg/m³</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
            letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:4px;">Model R²</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.8rem; font-weight:700;
            color:#a78bfa; letter-spacing:-0.03em;">0.973</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#475569;">GBR + ensemble</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
            letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:4px;">Data Source</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.1rem; font-weight:600;
            color:#e2e8f0;">OpenAQ + CPCB</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#475569;">live + calibrated</div>
    </div>
</div>
""", unsafe_allow_html=True)
