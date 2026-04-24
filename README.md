# Fieldbyte Edge | Autonomous Telemetry Architecture

## Overview
This repository contains the Phase 1 Edge Computing architecture for Fieldbyte's industrial telemetry platform. It is designed to run 100% offline on a Raspberry Pi, bypassing factory Wi-Fi limitations, while calculating live differential pressure and predicting machine failure.

## 🛠️ Tech Stack
* **Database Engine:** PostgreSQL (via Local Supabase Docker Containers)
* **Frontend UI:** Streamlit & Plotly (Kiosk-mode ready)
* **Hardware Simulation:** Python 

## 🚀 Production Migration Guide (Pi Deployment)
To migrate this prototype to a physical factory Raspberry Pi, follow these steps:
1. Install Docker and Python 3 on the Raspberry Pi OS.
2. Clone this repository.
3. Run `pip install -r requirements.txt`.
4. Configure the Pi to run `edge_boot.sh` on startup via `systemd`. 

## 📡 Phase 2 Hardware Optimization (MQTT & Byte-Packing)
As discussed, for the production hardware rollout, the following optimizations are recommended for the wireless sensor-to-Pi transmission:
* **Protocol:** Transition from HTTP REST to **MQTT**. Run a lightweight Mosquitto broker on the Pi to handle high-frequency accelerometer data with near-zero latency.
* **Payload Optimization:** Instead of transmitting JSON, the edge microcontrollers (e.g., ESP32) should pack the sensor readings into raw byte arrays. 
* **Database Handling:** Once the Pi's MQTT subscriber receives the byte array, it unpacks the data and inserts it into the Supabase PostgreSQL database, where it is natively stored as highly compressed binary on the disk.

## 🗄️ Database Schema & Autonomous Logic
The database utilizes PostgreSQL `GENERATED ALWAYS AS` columns to save Pi CPU cycles. 
* Differential pressure is calculated natively during the SQL `INSERT` operation.
* A rolling 30-day data retention policy is recommended via pg_cron to ensure the Pi's SD card never runs out of memory.