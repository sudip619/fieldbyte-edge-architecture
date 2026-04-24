import requests
import datetime
import time
import random
import struct
import json

# Your local Supabase REST API URL
API_URL = "http://127.0.0.1:54321/rest/v1/sensor_readings"
ANON_KEY = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"

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
    vib_val = round(random.uniform(1.0, 2.5), 2)
    suction = 1.2
    discharge = round(random.uniform(4.5, 5.0), 1)
    status_val = 0
    
    payload = {
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "serial_number": "PUMP-001",
        "vibration_de_x_rms": vib_val,
        "bearing_temp_de": temp_val,
        "rpm": rpm_val,
        "suction_pressure": suction,
        "discharge_pressure": discharge,
        "overall_status": status_val
    }
    
    # --- PHASE 2 HARDWARE OPTIMIZATION DEMO ---
    # We pack the data into C-style bytes: 
    # 'i' (integer 4-bytes for RPM), 'f' (float 4-bytes for Temp), 
    # 'f' (float 4-bytes for Vib), 'f' (float 4-bytes for Press), 'B' (1-byte unsigned char for Status)
    # Total size: 4 + 4 + 4 + 4 + 1 = 17 Bytes
    
    packed_bytes = struct.pack('!ifffB', 
                               int(rpm_val), 
                               float(temp_val), 
                               float(vib_val), 
                               float(discharge), 
                               int(status_val))
    
    # Calculate sizes to prove the bandwidth savings
    json_payload = json.dumps(payload).encode('utf-8')
    json_size = len(json_payload)
    byte_size = len(packed_bytes)
    savings = ((json_size - byte_size) / json_size) * 100
    
    print(f"\n[HARDWARE POC] Payload Size Comparison:")
    print(f"  -> Standard JSON Size : {json_size} bytes")
    print(f"  -> Packed Byte Size   : {byte_size} bytes")
    print(f"  -> Bandwidth Saved    : {savings:.1f}%")
    # ------------------------------------------
    
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