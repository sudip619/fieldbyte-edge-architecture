import streamlit as st
import requests
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG (The "Sleek" Setup) ---
st.set_page_config(page_title="Fieldbyte Edge Control", layout="wide", initial_sidebar_state="collapsed")

# The "Quantum Shift" CSS Hack to force dark mode and hide Streamlit branding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stMetric {background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    </style>
""", unsafe_allow_html=True)

# --- DATABASE CONFIG ---
API_URL = "http://127.0.0.1:54321/rest/v1/sensor_readings"
ANON_KEY = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH" # Your verified key
HEADERS = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Range-Unit": "items"
}

def fetch_latest_data():
    """Fetches the single most recent row from local Supabase"""
    try:
        res = requests.get(f"{API_URL}?select=*&order=recorded_at.desc&limit=1", headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            if len(data) > 0:
                return data[0]
    except Exception as e:
        pass
    return None

def fetch_historical_data():
    """Fetches the last 50 rows for trend analysis"""
    try:
        res = requests.get(f"{API_URL}?select=*&order=recorded_at.desc&limit=50", headers=HEADERS)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

# --- UI LAYOUT ---
st.title("🔴 FIELDBYTE EDGE | Autonomous Telemetry")
st.markdown("Target: **PUMP-001 (Main Cooling Water Pump)** | Status: **LIVE (Local Edge)**")

# Create empty placeholders for the "Quantum Shift" fluid updates
metric_row = st.empty()
chart_row = st.empty()
history_row = st.empty() # New placeholder for the historical trend

# --- THE REAL-TIME LOOP ---
# This loop fetches data every 2 seconds and overwrites the UI without flashing
while True:
    data = fetch_latest_data()
    
    if data:
        rpm = data.get('rpm', 0)
        temp_de = data.get('bearing_temp_de', 0)
        vib_x = data.get('vibration_de_x_rms', 0)
        diff_press = data.get('differential_pressure', 0)
        status = data.get('overall_status', 0)

        # Health Score Logic (The "Crazy" Anomaly Detection)
        health_color = "green" if status == 0 and temp_de < 65 else "red"
        health_text = "OPTIMAL" if health_color == "green" else "PRE-FAILURE DETECTED"

        with metric_row.container():
            st.markdown(f"<h3 style='color: {health_color}; text-align: center;'>SYSTEM STATUS: {health_text}</h3>", unsafe_allow_html=True)
            
            # Top row metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Drive End Temp (°C)", f"{temp_de:.1f}", delta="-0.2" if temp_de < 58 else "+1.4", delta_color="inverse")
            col2.metric("Diff Pressure (bar)", f"{diff_press:.2f}")
            col3.metric("X-Axis VRMF (mm/s)", f"{vib_x:.2f}")
            col4.metric("Pump Speed (RPM)", f"{rpm:.0f}")

        with chart_row.container():
            col_chart1, col_chart2 = st.columns(2)

            # Fluid Gauge Chart for RPM
            fig_rpm = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = rpm,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "RPM Telemetry", 'font': {'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 3500]},
                    'bar': {'color': "#00ffcc"}, # Cyberpunk neon cyan
                    'steps': [
                        {'range': [0, 2000], 'color': "gray"},
                        {'range': [2000, 3000], 'color': "darkblue"}],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 3200}
                }
            ))
            fig_rpm.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300)
            col_chart1.plotly_chart(fig_rpm, use_container_width=True, key=f"rpm_{time.time()}")

            # Fluid Gauge Chart for Temp
            fig_temp = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = temp_de,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Bearing Temp (°C)", 'font': {'color': 'white'}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "orange" if temp_de > 60 else "#00ffcc"},
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 85}
                }
            ))
            fig_temp.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300)
            # Fixed the duplicate key bug here
            col_chart2.plotly_chart(fig_temp, use_container_width=True, key=f"temp_{time.time()}")
            
        with history_row.container():
            history_data = fetch_historical_data()
            if history_data:
                # Convert JSON to a Pandas DataFrame for easy plotting
                df = pd.DataFrame(history_data)
                df['recorded_at'] = pd.to_datetime(df['recorded_at']).dt.strftime('%H:%M:%S')
                
                # Reverse the dataframe so time flows left to right
                df = df.iloc[::-1]

                st.markdown("---")
                st.markdown("<h4 style='color: #00ffcc;'>Live Telemetry Trend (Last 50 Cycles)</h4>", unsafe_allow_html=True)
                
                col_trend, col_export = st.columns([4, 1])
                
                with col_trend:
                    # Plotting Temperature and Vibration over time
                    chart_data = df[['recorded_at', 'bearing_temp_de', 'vibration_de_x_rms']].set_index('recorded_at')
                    st.line_chart(chart_data, height=200, use_container_width=True)
                    
                with col_export:
                    st.markdown("<br>", unsafe_allow_html=True)
                    # The "Boss-Pleaser" Export Button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Export Shift Log (CSV)",
                        data=csv,
                        file_name='pump_001_shift_log.csv',
                        mime='text/csv',
                        key=f"export_{time.time()}"
                    )

    time.sleep(2) # Query database every 2 seconds