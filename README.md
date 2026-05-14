# 🌬️ VaayuVigyaan AI — India's Environmental Intelligence Platform

> **वायु Vigyaan** | AI-powered PM2.5 prediction, AQI analysis, health intelligence & pollution forecasting

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat)](https://scikit-learn.org)

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip the project
cd VaayuVigyaan

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run Home.py
```

The app opens at **http://localhost:8501**

---

## 📁 Project Structure

```
VaayuVigyaan/
├── Home.py                    # Landing page — hero, AQI cards, feature showcase
├── pages/
│   ├── 1_Dashboard.py         # Interactive pollution map, trends, comparisons
│   ├── 2_AI_Predictor.py      # XGBoost/GBR PM2.5 prediction engine
│   ├── 3_Health_Impact.py     # Personalised health risk assessment
│   ├── 4_AI_Insights.py       # Explainable AI environmental reasoning
│   ├── 5_Future_Forecast.py   # 6h / 24h / 3-day projections
│   └── 6_WhatIf_Simulator.py  # Policy intervention scenario simulator
├── utils/
│   ├── styles.py              # Global CSS, theming helpers
│   └── model_utils.py         # Model training, loading, prediction
├── models/                    # Saved model artefacts (auto-generated)
├── .streamlit/
│   └── config.toml            # Dark theme configuration
└── requirements.txt
```

---

## 🧠 AI/ML Stack

| Component | Technology |
|-----------|-----------|
| Core model | Gradient Boosting Regressor (scikit-learn) |
| Feature scaling | StandardScaler pipeline |
| Data source | Synthetic CPCB-calibrated training data |
| Explainability | Rule-based + feature contribution scoring |
| Forecasting | Statistical time-series simulation |

**Input features:** Temperature · Humidity · Wind speed · Rainfall · AOD (Aerosol Optical Depth) · Traffic intensity · Industrial activity level

**Outputs:** PM2.5 (µg/m³) · AQI category · Confidence score · Health message · Feature contribution

---

## 🗺 Pages Overview

### 🏠 Home
Hero landing with animated AQI city cards, feature showcase, scrolling alert ticker

### 📊 Dashboard
- Interactive India pollution map (Plotly Mapbox)
- PM2.5 historical trends with season heatmap
- City radar / multi-indicator comparison
- Weather correlation scatter plots

### 🤖 AI Predictor
- 7-input slider interface
- Real-time PM2.5 gauge + AQI badge
- Feature contribution bar chart (XAI)
- 24-hour projection with confidence intervals
- AI explainability reasoning box

### 🏥 Health Impact
- Personal risk profile (age, conditions, outdoor hours)
- 6 health risk cards (respiratory, cardiac, eye, exercise, children, mask)
- Health radar chart
- Prioritised AI recommendations

### 💡 AI Insights
- Rule-based environmental reasoning engine
- Timestamped insight cards with impact levels
- PM2.5 source attribution pie chart
- Insight engine accuracy bar chart

### 📈 Future Forecast
- 6h / 24h / 3-day tabbed forecasts
- Ensemble model comparison (GBR + LSTM + ARIMA simulated)
- Hourly summary grid with AQI colour coding
- Multi-city 72-hour comparison chart

### ⚗️ What-If Simulator
- 7 intervention sliders (traffic, EV, industry, cloud seeding, green cover, dust control)
- Real-time projected PM2.5 reduction
- Intervention breakdown bars
- Policy action scenario comparison
- Environmental impact score + lives-saved estimate

---

## ☁️ Deployment

### Streamlit Community Cloud (Free)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set **Main file path:** `Home.py`
4. Deploy ✅

### Render.com
```
Start command: streamlit run Home.py --server.port $PORT --server.headless true
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "Home.py", "--server.headless", "true"]
```

---

## 📊 Data Sources

| Source | Description |
|--------|-------------|
| CPCB India | Central Pollution Control Board city-level AQI data |
| NASA MERRA-2 | Aerosol optical depth (.nc satellite files) |
| OMI / AERONET | UV aerosol measurements |
| IMD | Indian Meteorological Department weather data |
| OpenAQ | Open air quality measurements API |

---

## Feedback & Refinement

Initial feedback from users highlighted:
- Dashboard felt information-heavy
- AQI meaning was unclear
- Predictor needed more explainability

Improvements implemented:
- Added health interpretation
- Added explainable AI insights
- Improved predictor UI
- Added scenario simulation

## 🏆 Hackathon Highlights

- **< 10 second visual impact** — dark futuristic glassmorphism UI
- **Fully functional AI pipeline** — no placeholder/TODO code
- **7 distinct pages** with unique functionality
- **Real ML model** trained on synthetic CPCB-calibrated data
- **Explainable AI** — feature contributions, insight reasoning
- **Deployment ready** — Streamlit Cloud / Render / Docker

---

*Built with ❤️ for India's clean air future*
