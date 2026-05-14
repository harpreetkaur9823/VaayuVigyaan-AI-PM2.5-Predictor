# Dashboard upgrade plan (pages/1_Dashboard.py)

## Current info gathered
- `pages/1_Dashboard.py` already exists and uses Streamlit + Plotly and fetches live data via `utils.live_api.get_live_air_data`.
- `utils/live_api.py` defines `CITY_COORDS` and live city polling utilities.
- Project requirements do **not** mention folium/streamlit-folium, but local environment already has `folium==0.20.0` and `streamlit_folium` installed.

## Implementation goals
1. Replace/upgrade the map section to use **folium**:
   - Center on India (lat ~22.97, lon ~79.86).
   - Add HeatMap of PM2.5 points (from city PM2.5).
   - Add CircleMarkers for major cities with category-based colors.
   - Tooltips show: City, PM2.5, AQI category.
   - Use a dark map tile style (e.g., CartoDB Dark Matter / Stamen Toner Dark fallback).
2. Add KPI cards:
   - Average AQI in India (over selected cities).
   - Most polluted city.
   - Cleanest city.
   - National risk level (derived from % of cities by AQI bucket or max AQI).
3. City comparison section:
   - Bar chart: PM2.5 vs cities (Plotly or native Streamlit).
   - Optional AQI trend line: if no historical data is available, show a simulated/placeholder trend based on live snapshot seasonal factor (must be clearly labeled as “modelled”). If strict, omit trend.
4. AI insights panel:
   - Generate 3–5 bullet insights using city ranking and bucket distribution.

## Dependent files to edit
- `pages/1_Dashboard.py`

## Followup steps after edit
- Run: `python -m py_compile pages/1_Dashboard.py`
- Run: `streamlit run Home.py` and click “View Live Dashboard”
- Verify map renders and tooltips work; ensure no exceptions from folium/streamlit-folium.

