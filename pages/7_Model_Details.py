"""VaayuVigyaan AI — Model Details (for technical users)

This page is intentionally tucked away from the homepage.
It provides model/training metrics and data lineage for technical reviewers.
"""

import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import inject_css, page_header
from utils.model_utils import load_or_train_model

st.set_page_config(page_title="Model Details | VaayuVigyaan", page_icon="🧩", layout="wide")
inject_css()

st.markdown(page_header("Model Details (technical)", "Training & evaluation metrics behind the PM2.5 predictor", "🧩"), unsafe_allow_html=True)

with st.spinner("Loading model metadata..."):
    model, meta = load_or_train_model()

st.markdown(
    """
    <div style="background:rgba(2,15,35,0.6); border:1px solid rgba(0,212,255,0.2); border-radius:16px; padding:1rem;">
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("R²", f"{meta.get('r2_test', 0):.3f}", "Test split")
c2.metric("RMSE", f"{meta.get('rmse', 0)} µg/m³", "Test split")
c3.metric("MAE", f"{meta.get('mae', 0)} µg/m³", "Test split")
c4.metric("Training records", f"{meta.get('n_train', 0):,}", f"Cities: {len(meta.get('cities', []))}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <br>
    <div style="display:flex; gap:10px; align-items:center;">
      <div style="width:10px; height:10px; border-radius:50%; background:#00d4ff; box-shadow:0 0 18px rgba(0,212,255,0.35);"></div>
      <div style="font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:950; letter-spacing:0.14em; text-transform:uppercase; color:#00d4ff; opacity:0.85;">
        Data lineage
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(f"Data source: {meta.get('data_source', 'Unknown')}")

with st.expander("Feature columns used (technical)", expanded=False):
    st.code("\n".join(meta.get("features", [])))

with st.expander("Feature importance (model-specific)", expanded=False):
    fi = meta.get("feature_importance", {})
    if not fi:
        st.info("No feature importance available in metadata.")
    else:
        # Sort top 12
        top = sorted(fi.items(), key=lambda x: x[1], reverse=True)[:12]
        st.dataframe({"Feature": [k for k, _ in top], "Importance": [v for _, v in top]})

