from pathlib import Path
import re

p = Path("Home.py")
text = p.read_text(encoding="utf-8")

pattern = r"(# --------------- Section 1: HERO ---------------[\s\S]*?)(?=# --------------- Section 2)"

new_hero = """
# --------------- Section 1: HERO ---------------
st.markdown(
    \"\"\"
    <div style="padding-top: 0.25rem;">
      <div style="font-family: 'Orbitron', monospace; font-size: 2.2rem; font-weight: 900; color: white;">
        VaayuVigyaan AI
      </div>

      <div style="margin-top: 0.4rem; font-size: 1.05rem; color: #b0bcd4;">
        Breathe Smarter with AI Air Intelligence — see the air, act with clarity
      </div>

      <div style="margin-top: 0.5rem; font-size: 0.92rem; color: #7db8d8;">
        Real-time AQI · Predictive PM2.5 · Health guidance for India
      </div>
    </div>
    \"\"\",
    unsafe_allow_html=True,
)
"""

new_text = re.sub(pattern, new_hero, text, flags=re.DOTALL)

if new_text == text:
    print("❌ NO MATCH FOUND — PATCH FAILED")
else:
    print("✅ HERO PATCH APPLIED SUCCESSFULLY")

p.write_text(new_text, encoding="utf-8")