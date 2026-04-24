import requests
import datetime
import time
import random

# Your local Supabase REST API URL
API_URL = "http://127.0.0.1:54321/rest/v1/sensor_readings"
ANON_KEY = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH "


HEADERS = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

print("Starting Virtual Pump Simulator (PUMP-001)...")
print("Press Ctrl+C to stop.")

def send_reading():
    # Generating slightly randomized dummy data to make the dashboard look "alive"
    rpm_val = round(random.uniform(2950, 2980), 1)
    temp_val = round(random.uniform(55.0, 60.0), 1)
    suction = 1.2
    discharge = round(random.uniform(4.5, 5.0), 1)
    
    payload = {
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "serial_number": "PUMP-001",
        "vibration_de_x_rms": round(random.uniform(1.0, 2.5), 2),
        "bearing_temp_de": temp_val,
        "rpm": rpm_val,
        "suction_pressure": suction,
        "discharge_pressure": discharge,
        "overall_status": 0
    }
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 201:
            print(f"[SUCCESS] Sent -> RPM: {rpm_val} | Temp: {temp_val}°C")
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[CONNECTION FAILED] {e}")

# Run an infinite loop, sending data every 3 seconds
while True:
    send_reading()
    time.sleep(3)