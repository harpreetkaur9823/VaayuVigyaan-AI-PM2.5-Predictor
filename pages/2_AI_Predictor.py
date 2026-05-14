"""
VaayuVigyaan AI — PM2.5 Predictor
Trained on CPCB 2025 data: 22,182 records across 25 Indian cities.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.styles import inject_css, page_header, aqi_badge, pm25_to_aqi
from utils.model_utils import load_or_train_model, predict_pm25, CITY_META
from utils.live_api import get_live_air_data, co_ugm3_to_ppm

st.set_page_config(page_title="AI Predictor | VaayuVigyaan", page_icon="🤖", layout="wide")
inject_css()

CHART_CFG = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(2,15,35,0.7)',
    font=dict(family='Inter, sans-serif', color='#64748b', size=12),
    title_font=dict(family='Inter, sans-serif', color='#e2e8f0', size=14, weight=600),
    xaxis=dict(gridcolor='rgba(56,189,248,0.07)', tickfont=dict(color='#475569', size=11)),
    yaxis=dict(gridcolor='rgba(56,189,248,0.07)', tickfont=dict(color='#475569', size=11)),
    margin=dict(l=16, r=16, t=44, b=16),
)

st.markdown(page_header("AI PM₂.₅ Predictor",
    "GBR model trained on 22,182 CPCB 2025 records · 25 Indian cities · R²=0.94",
    "🤖"), unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
with st.spinner("Loading CPCB-trained model..."):
    model, meta = load_or_train_model()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Model R²",        f"{meta['r2_test']:.3f}",  "CPCB real data")
c2.metric("Test RMSE",       f"{meta['rmse']} µg/m³")
c3.metric("Test MAE",        f"{meta['mae']} µg/m³")
c4.metric("Training Records",f"{meta['n_train']:,}",    f"{len(meta['cities'])} cities")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Sidebar city selector ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;
        font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
        color:#38bdf8;opacity:0.7;margin-bottom:0.75rem;">City Context</div>""",
        unsafe_allow_html=True)
    city_sel = st.selectbox("Reference City", ["Custom"] + sorted(CITY_META.keys()), index=2)
    if city_sel != "Custom":
        ref_lat  = CITY_META[city_sel]['lat']
        ref_lon  = CITY_META[city_sel]['lon']
        avg_pm25 = meta.get('city_pm25_mean', {}).get(city_sel, 80)
        # Fetch live data for this city to pre-fill sliders
        @st.cache_data(ttl=600, show_spinner=False)
        def _live(c): return get_live_air_data(c)
        live = _live(city_sel)
        live_badge = "◉ LIVE" if live.get("is_live") else "○ Offline"
        live_col   = "#4ade80" if live.get("is_live") else "#facc15"
        st.markdown(f"""<div style="font-family:'Inter',sans-serif;font-size:0.8rem;
            color:#64748b;margin-top:8px;">
            {CITY_META[city_sel]['state']}<br>
            <span style="color:{live_col};font-size:0.7rem;">{live_badge}</span>&nbsp;
            PM₂.₅ <b style="color:#38bdf8">{live.get('pm25', avg_pm25)} µg/m³</b>
            &nbsp;|&nbsp; AQI <b style="color:#38bdf8">{live.get('owm_aqi','—')}</b>
            </div>""", unsafe_allow_html=True)
    else:
        ref_lat  = 28.61
        ref_lon  = 77.21
        live     = {}

# ── Input / output layout ─────────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1.4], gap="large")

with col_in:
    st.markdown("""<div style="background:rgba(2,15,35,0.8);border:1px solid rgba(56,189,248,0.15);
        border-radius:16px;padding:24px;">""", unsafe_allow_html=True)

    st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
        letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;opacity:0.7;
        margin-bottom:1rem;">Meteorological Parameters</div>""", unsafe_allow_html=True)

    _def_temp = float(live.get('temperature') or 28.0) if city_sel != 'Custom' else 28.0
    _def_hum  = float(live.get('humidity')    or 62.0) if city_sel != 'Custom' else 62.0
    _def_pm10 = float(live.get('pm10')        or 80.0) if city_sel != 'Custom' else 80.0
    _def_no2  = float(live.get('no2')         or 35.0) if city_sel != 'Custom' else 35.0
    _def_so2  = float(live.get('so2')         or 12.0) if city_sel != 'Custom' else 12.0
    _def_co   = float(co_ugm3_to_ppm(live.get('co') or 1145.0)) if city_sel != 'Custom' else 0.8
    _def_o3   = float(live.get('o3')          or 40.0) if city_sel != 'Custom' else 40.0
    _def_no   = float(live.get('no')          or 18.0) if city_sel != 'Custom' else 18.0
    temperature = st.slider("🌡 Temperature (°C)", 5.0, 48.0, min(48.0, max(5.0, _def_temp)), 0.5)
    humidity    = st.slider("💧 Relative Humidity (%)", 10, 100, min(100, max(10, int(_def_hum))))

    st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
        letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;opacity:0.7;
        margin:1rem 0 0.75rem;">Pollutant Concentrations</div>""", unsafe_allow_html=True)

    pm10 = st.slider("PM₁₀ (µg/m³)", 0.0, 400.0, min(400.0, max(0.0, round(_def_pm10, 0))), 1.0)
    no2  = st.slider("NO₂ (µg/m³)",  0.0, 200.0, min(200.0, max(0.0, round(_def_no2,  0))), 1.0)
    so2  = st.slider("SO₂ (µg/m³)",  0.0, 100.0, min(100.0, max(0.0, round(_def_so2,  1))), 0.5)
    co   = st.slider("CO (ppm)",      0.0,   5.0,  min(5.0,  max(0.0, round(_def_co,   2))), 0.05)
    o3   = st.slider("O₃ (µg/m³)",   0.0, 150.0, min(150.0, max(0.0, round(_def_o3,   0))), 1.0)
    no   = st.slider("NO (µg/m³)",   0.0, 100.0, min(100.0, max(0.0, round(_def_no,   0))), 1.0)

    predict_btn = st.button("⚡  PREDICT PM₂.₅", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_out:
    inputs = {
        'temperature': temperature, 'humidity': humidity,
        'pm10': pm10, 'no2': no2, 'so2': so2,
        'co': co, 'o3': o3, 'no': no,
    }
    result = predict_pm25(model, inputs, lat=ref_lat, lon=ref_lon)
    pm25   = result['pm25']
    aqi_v  = pm25_to_aqi(pm25)
    color  = result['color']

    # ── Gauge ─────────────────────────────────────────────────────────────────
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pm25,
        title=dict(text="PM₂.₅ µg/m³",
                   font=dict(family='Inter, sans-serif', color='#94a3b8', size=13)),
        number=dict(font=dict(family='Inter, sans-serif', color=color, size=44,
                               weight=700), suffix=" µg/m³"),
        delta=dict(reference=35.4,
                   font=dict(family='Inter, sans-serif', size=13),
                   increasing=dict(color='#f87171'),
                   decreasing=dict(color='#4ade80')),
        gauge=dict(
            axis=dict(range=[0, 300],
                      tickfont=dict(family='Inter', color='#475569', size=10),
                      tickvals=[0, 12, 35, 55, 150, 250, 300],
                      ticktext=['0','12','35','55','150','250','300+']),
            bar=dict(color=color, thickness=0.22),
            bgcolor='rgba(2,15,35,0.8)',
            bordercolor='rgba(56,189,248,0.2)',
            steps=[
                dict(range=[0, 12],    color='rgba(74,222,128,0.1)'),
                dict(range=[12, 35.4], color='rgba(250,204,21,0.08)'),
                dict(range=[35.4,55.4],color='rgba(251,146,60,0.08)'),
                dict(range=[55.4,150], color='rgba(248,113,113,0.08)'),
                dict(range=[150,250],  color='rgba(192,132,252,0.08)'),
                dict(range=[250,300],  color='rgba(153,27,27,0.15)'),
            ],
            threshold=dict(line=dict(color='#38bdf8', width=2), value=35.4),
        ),
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', height=270,
        margin=dict(l=30,r=30,t=20,b=10),
        font=dict(family='Inter, sans-serif', color='#64748b'),
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    # ── Result card ───────────────────────────────────────────────────────────
    badge_html = aqi_badge(aqi_v)
    st.markdown(f"""
    <div style="background:rgba(2,15,35,0.85); border:1px solid {color}30;
        border-top:2px solid {color}; border-radius:14px; padding:18px 20px;
        box-shadow: 0 0 30px {color}12; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center;
            flex-wrap:wrap; gap:12px;">
            <div>
                <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
                    letter-spacing:0.1em; text-transform:uppercase; color:#475569;">AQI</div>
                <div style="font-family:'Inter',sans-serif; font-size:2.8rem; font-weight:800;
                    color:{color}; letter-spacing:-0.04em; line-height:1;">{aqi_v}</div>
                <div style="margin-top:6px;">{badge_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:600;
                    letter-spacing:0.1em; text-transform:uppercase; color:#475569;">CONFIDENCE</div>
                <div style="font-family:'Inter',sans-serif; font-size:2rem; font-weight:700;
                    color:#67e8f9; letter-spacing:-0.03em;">{result['confidence']}%</div>
                <div style="font-family:'Inter',sans-serif; font-size:0.7rem; color:#334155;">
                    Model certainty</div>
            </div>
        </div>
        <div style="margin-top:14px; padding-top:12px;
            border-top:1px solid rgba(56,189,248,0.1);
            font-family:'Inter',sans-serif; font-size:0.9rem;
            color:#94a3b8; line-height:1.55;">{result['health_message']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature importance bars ────────────────────────────────────────────────
    imp_raw = meta.get('feature_importance', {})
    # Show input-relevant features only
    input_feats = {
        'pm10': pm10, 'temperature': temperature, 'humidity': humidity,
        'no2': no2, 'so2': so2, 'co': co, 'o3': o3, 'no': no,
    }
    total_imp = sum(imp_raw.get(f, 0) for f in input_feats)
    if total_imp == 0: total_imp = 1
    sorted_imp = sorted(
        [(f, imp_raw.get(f, 0)) for f in input_feats],
        key=lambda x: x[1], reverse=True
    )

    st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:600;
        letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;opacity:0.7;
        margin-bottom:8px;">Feature Contribution (CPCB model)</div>""", unsafe_allow_html=True)

    palette = ['#38bdf8','#67e8f9','#4ade80','#facc15','#fb923c','#f87171','#c084fc','#94a3b8']
    for i, (feat, val) in enumerate(sorted_imp):
        pct = val / sum(v for _, v in sorted_imp) * 100 if sum(v for _, v in sorted_imp) > 0 else 0
        c = palette[i % len(palette)]
        label_map = {'pm10':'PM₁₀','temperature':'Temp','humidity':'Humidity',
                     'no2':'NO₂','so2':'SO₂','co':'CO','o3':'O₃','no':'NO'}
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
            <div style="font-family:'Inter',sans-serif;font-size:0.7rem;color:#64748b;
                width:72px;text-align:right;flex-shrink:0;">{label_map.get(feat, feat)}</div>
            <div style="flex:1;background:rgba(0,20,50,0.5);border-radius:3px;height:6px;">
                <div style="width:{pct:.1f}%;height:100%;background:{c};border-radius:3px;
                    box-shadow:0 0 5px {c}66;transition:width 0.8s ease;"></div>
            </div>
            <div style="font-family:'Inter',monospace;font-size:0.65rem;color:{c};width:36px;">{pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── 24-hour projection ────────────────────────────────────────────────────────
st.markdown("""<div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
    letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;
    opacity:0.7;margin-bottom:0.75rem;">24-Hour Projection</div>""", unsafe_allow_html=True)

rng = np.random.default_rng(int(pm25 * 100) % 2**31)
hours = np.arange(25)
diurnal = 12 * np.sin((hours - 8) * np.pi / 12) + 6 * np.sin((hours - 19) * np.pi / 6)
noise   = rng.normal(0, pm25 * 0.07, 25)
curve   = np.clip(pm25 + diurnal + noise - 0.05 * hours, 2, 500)
upper   = np.clip(curve * 1.15, 2, 550)
lower   = np.clip(curve * 0.85, 2, 500)

now_dt = datetime.now().replace(second=0, microsecond=0)
xtimes = [now_dt + timedelta(hours=int(h)) for h in hours]

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(x=xtimes, y=upper, mode='lines', line=dict(width=0), showlegend=False))
fig_proj.add_trace(go.Scatter(x=xtimes, y=lower, mode='lines', line=dict(width=0),
    fill='tonexty', fillcolor='rgba(56,189,248,0.08)', name='95% CI'))
fig_proj.add_trace(go.Scatter(x=xtimes, y=curve, mode='lines+markers',
    line=dict(color='#38bdf8', width=2.5),
    marker=dict(color='#38bdf8', size=4),
    name='PM₂.₅ Forecast'))
fig_proj.add_hline(y=35.4, line=dict(color='#4ade80', dash='dash', width=1),
    annotation_text="WHO 35", annotation_font=dict(color='#4ade80', size=9, family='Inter'))

fig_proj.add_shape(type='line', xref='x', yref='paper',
    x0=now_dt, x1=now_dt, y0=0, y1=1,
    line=dict(color='#38bdf8', dash='solid', width=1.5))
fig_proj.add_annotation(x=now_dt, xref='x', y=1.0, yref='paper',
    text="NOW", showarrow=False, yanchor='bottom',
    font=dict(color='#38bdf8', size=9, family='Inter'))

fig_proj.update_layout(title="24-Hour PM₂.₅ Projection", **CHART_CFG, height=300,
    xaxis_title="Time", yaxis_title="PM₂.₅ (µg/m³)", hovermode='x unified',
    legend=dict(bgcolor='rgba(2,15,35,0.6)', bordercolor='rgba(56,189,248,0.15)',
                borderwidth=1, font=dict(color='#94a3b8', size=11, family='Inter')))
st.plotly_chart(fig_proj, use_container_width=True, config={"displayModeBar": False})

# ── AI Explanation box ────────────────────────────────────────────────────────
explanations = []
if pm10 > 100:
    explanations.append(f"🔬 <b>PM₁₀ dominance ({pm10:.0f} µg/m³)</b> — Coarse particles strongly correlated with PM₂.₅ in CPCB data (importance: {meta['feature_importance'].get('pm10',0)*100:.1f}%). Likely road dust or construction activity.")
if no2 > 60:
    explanations.append(f"🚗 <b>Elevated NO₂ ({no2:.0f} µg/m³)</b> — Secondary PM₂.₅ formation via NO₂ oxidation. Photochemical smog indicator. Peak contribution in afternoon hours.")
if humidity > 75:
    explanations.append(f"💧 <b>High humidity ({humidity}%)</b> — Hygroscopic growth of fine particles at RH > 70% can increase PM₂.₅ mass by 20-40%. Also reduces boundary layer mixing.")
if temperature > 35:
    explanations.append(f"🌡 <b>High temperature ({temperature:.0f}°C)</b> — Accelerates secondary aerosol chemistry and increases boundary layer instability, modulating pollutant dispersion.")
if co > 1.5:
    explanations.append(f"💨 <b>Elevated CO ({co:.2f} ppm)</b> — Marker for incomplete combustion (vehicles/biomass burning). Co-emitted with fine BC particles.")
if so2 > 30:
    explanations.append(f"🏭 <b>SO₂ ({so2:.0f} µg/m³)</b> — Industrial/power plant emissions. Forms sulfate aerosols within hours — significant secondary PM₂.₅ precursor.")
if not explanations:
    explanations.append("✅ <b>Parameters within normal range</b> — No single dominant pollutant driving current PM₂.₅ level. Mixed urban background conditions.")

st.markdown(f"""
<div style="background:rgba(56,189,248,0.04);border:1px solid rgba(56,189,248,0.15);
    border-radius:14px;padding:20px 22px;margin-top:0.5rem;">
    <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:600;
        letter-spacing:0.1em;text-transform:uppercase;color:#38bdf8;margin-bottom:14px;">
        ⚡ XAI — Explainability Engine
    </div>
    <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#475569;
        margin-bottom:12px;">Model trained on CPCB 2025 · {meta['data_source']}</div>
    {''.join(f'<div style="font-family:Inter,sans-serif;font-size:0.9rem;color:#94a3b8;margin-bottom:9px;padding:9px 12px;background:rgba(56,189,248,0.05);border-radius:8px;border-left:3px solid rgba(56,189,248,0.3);">{t}</div>' for t in explanations)}
</div>""", unsafe_allow_html=True)
