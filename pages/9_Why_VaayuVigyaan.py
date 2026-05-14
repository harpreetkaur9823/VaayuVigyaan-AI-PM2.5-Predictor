"""VaayuVigyaan AI — USP / Competitor Comparison

Hackathon checklist page.
Theme: consistent cyber dark + glassmorphism.
"""

import streamlit as st

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import inject_css
from utils.styles import page_header


st.set_page_config(
    page_title="Why VaayuVigyaan | VaayuVigyaan",
    page_icon="🧩",
    layout="wide",
)
inject_css()

st.markdown(
    page_header(
        "USP / Competitor Comparison",
        "India-focused explainable intelligence across the full AQI + health workflow",
        "🧩",
    ),
    unsafe_allow_html=True,
)


def premium_table(compare_title: str) -> str:
    header_names = ["IQAir", "CPCB Dashboard", "Google AQI", "VaayuVigyaan AI"]
    headers_html = "".join(
        f"""<th style="background:rgba(4,30,60,0.85); color:#e8f4ff; font-family:'Orbitron',monospace;
                      font-size:0.7rem; letter-spacing:0.16em; text-transform:uppercase;
                      padding:12px 10px; border-bottom:1px solid rgba(0,212,255,0.14);">{n}</th>"""
        for n in header_names
    )

    return f"""
    <div style="background:rgba(2,15,35,0.85); border:1px solid rgba(0,212,255,0.18);
                border-radius:18px; padding:18px 18px;
                box-shadow:0 0 55px rgba(0,212,255,0.08);">
        <div style="font-family:'Inter',sans-serif; font-weight:900; letter-spacing:0.14em;
                    text-transform:uppercase; color:#38bdf8; font-size:0.78rem;
                    margin-bottom:14px;">
            {compare_title}
        </div>
        <div style="overflow:auto;">
            <table style="width:100%; border-collapse:separate; border-spacing:0;">
                <thead>
                    <tr>
                        <th style="position:sticky; top:0; background:rgba(4,30,60,0.85);
                                   color:#7db8d8; font-family:'Inter',sans-serif; font-size:0.85rem;
                                   text-align:left; padding:12px 10px;
                                   border-bottom:1px solid rgba(0,212,255,0.14);">
                            Feature
                        </th>
                        {headers_html}
                    </tr>
                </thead>
                <tbody>
    """


def row(feature: str, v1: str, v2: str, v3: str, v4: str) -> str:
    c_ok = "#00ff88"
    c_mid = "#facc15"
    c_no = "#94a3b8"

    def color_for(sym: str) -> str:
        if sym == "YES":
            return c_ok
        if sym == "PART":
            return c_mid
        return c_no

    def cell(txt: str, color: str) -> str:
        return f"""<td style="padding:10px 10px; border-bottom:1px solid rgba(0,212,255,0.08);">
            <span style="font-family:'Space Mono',monospace; font-size:0.7rem; color:{color};
                         border:1px solid rgba(255,255,255,0.08);
                         background:rgba(0,0,0,0.15);
                         padding:4px 10px; border-radius:999px;
                         display:inline-block;">{txt}</span>
        </td>"""

    return f"""
    <tr>
        <td style="padding:10px 10px; border-bottom:1px solid rgba(0,212,255,0.08);">
            <div style="font-family:'Inter',sans-serif; color:#94a3b8; font-size:0.95rem; line-height:1.5;">
                {feature}
            </div>
        </td>
        {cell(v1, color_for(v1))}
        {cell(v2, color_for(v2))}
        {cell(v3, color_for(v3))}
        {cell(v4, color_for(v4))}
    </tr>
    """


def premium_table_close() -> str:
    return "</tbody></table></div></div>"


st.markdown(
    """
    <div style="margin: 0 0 1.2rem 0; display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div style="width:10px; height:10px; border-radius:50%; background:#00ffd4;
                    box-shadow:0 0 18px rgba(0,255,212,0.25);"></div>
        <div style="font-family:'Inter',sans-serif; font-size:0.8rem; font-weight:950;
                    letter-spacing:0.14em; text-transform:uppercase; color:#00ffd4; opacity:0.86;">
            India’s Explainable AI-powered PM2.5 Environmental Intelligence Platform
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    premium_table("Competitor landscape (hackathon comparison)"),
    unsafe_allow_html=True,
)

st.markdown(row("Live AQI (near real-time)", "YES", "PART", "YES", "YES"), unsafe_allow_html=True)
st.markdown(
    row("PM2.5 Prediction", "PART", "PART", "NO", "YES"),
    unsafe_allow_html=True,
)
st.markdown(
    row("Explainable AI (XAI)", "NO", "NO", "NO", "YES"),
    unsafe_allow_html=True,
)
st.markdown(
    row("Health Intelligence", "PART", "NO", "PART", "YES"),
    unsafe_allow_html=True,
)
st.markdown(
    row("What-if Simulation", "NO", "NO", "NO", "YES"),
    unsafe_allow_html=True,
)
st.markdown(
    row("Future Forecast", "PART", "NO", "PART", "YES"),
    unsafe_allow_html=True,
)
st.markdown(
    row("India-focused intelligence", "PART", "YES", "PART", "YES"),
    unsafe_allow_html=True,
)

st.markdown(premium_table_close(), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

usp_c1, usp_c2 = st.columns([1.2, 1], gap="large")

with usp_c1:
    st.markdown(
        """
        <div style="background:rgba(2,15,35,0.8); border:1px solid rgba(0,212,255,0.16);
                    border-radius:18px; padding:18px 20px;
                    box-shadow:0 0 45px rgba(0,212,255,0.08);">
            <div style="font-family:'Orbitron',monospace; font-size:1.05rem; font-weight:900; color:#e8f4ff;">
                Why VaayuVigyaan wins
            </div>
            <div style="font-family:'Inter',sans-serif; color:#7db8d8; font-size:0.98rem; line-height:1.7; margin-top:8px;">
                We combine <b>PM2.5 prediction</b>, <b>explainable drivers</b>,
                <b>personalized health guidance</b>, and <b>what-if decision support</b>
                into one India-first platform.
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px;">
                <span style="font-family:'Space Mono',monospace; border:1px solid rgba(0,212,255,0.22); background:rgba(0,212,255,0.06);
                             color:#00d4ff; padding:6px 12px; border-radius:999px;">AI XAI</span>
                <span style="font-family:'Space Mono',monospace; border:1px solid rgba(0,255,212,0.22); background:rgba(0,255,212,0.06);
                             color:#00ffd4; padding:6px 12px; border-radius:999px;">Health Intelligence</span>
                <span style="font-family:'Space Mono',monospace; border:1px solid rgba(250,204,21,0.22); background:rgba(250,204,21,0.06);
                             color:#facc15; padding:6px 12px; border-radius:999px;">What-if Simulation</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with usp_c2:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg, rgba(56,189,248,0.10), rgba(0,255,212,0.04));
                    border:1px solid rgba(0,212,255,0.16); border-radius:18px; padding:18px 20px;
                    box-shadow: 0 0 55px rgba(56,189,248,0.08);">
            <div style="font-family:'Inter',sans-serif; font-weight:900; letter-spacing:0.14em;
                        text-transform:uppercase; color:#38bdf8; font-size:0.78rem;">
                Why This Matters
            </div>
            <ul style="margin:10px 0 0 18px; color:#94a3b8; font-family:'Inter',sans-serif;
                       line-height:1.85; font-size:0.95rem;">
                <li>Turning AQI into <b>action</b></li>
                <li>Explaining <b>pollution drivers</b> for trust</li>
                <li>Preventing exposure for <b>vulnerable groups</b></li>
                <li>Enabling policy decisions with <b>simulation</b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="background:rgba(2,15,35,0.85); border:1px solid rgba(0,212,255,0.18);
                border-radius:18px; padding:18px 20px;
                box-shadow:0 0 50px rgba(0,212,255,0.08);">
        <div style="display:flex; gap:14px; align-items:center; flex-wrap:wrap;">
            <div style="font-size:1.3rem; width:42px; height:42px; border-radius:16px;
                        background:rgba(56,189,248,0.10); border:1px solid rgba(0,212,255,0.2);
                        display:flex; align-items:center; justify-content:center;">🏆</div>
            <div>
                <div style="font-family:'Orbitron',monospace; color:#e8f4ff; font-weight:950; font-size:1.15rem;">
                    India’s Explainable AI-powered PM2.5 Intelligence
                </div>
                <div style="font-family:'Inter',sans-serif; color:#7db8d8; font-size:0.98rem; line-height:1.7; margin-top:6px;">
                    VaayuVigyaan is strongest where users need it most: <b>prediction</b>,
                    <b>XAI trust</b>, <b>health readiness</b>, and <b>what-if decision support</b>—
                    not just a dashboard.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

