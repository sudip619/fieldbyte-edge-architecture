#!/bin/bash
echo "Starting Fieldbyte Edge Infrastructure..."

# 1. Boot the Database
cd /home/pi/fieldbyte-edge
npx supabase start &

# Wait 10 seconds for DB containers to initialize
sleep 10 

# 2. Start the Hardware Listener (Currently Simulator)
python3 simulator.py &

# 3. Launch the Control Room Kiosk
python3 -m streamlit run control_room.py --server.headless true &