-- 1. Create the Equipment Table
CREATE TABLE equipment (
  equipment_id SERIAL PRIMARY KEY,
  serial_number VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(100),
  model VARCHAR(100),
  location VARCHAR(200),
  commissioned_at TIMESTAMPTZ,
  status VARCHAR(20) DEFAULT 'active'
);

-- 2. Create the Sensor Readings Table
CREATE TABLE sensor_readings (
  sl_no BIGSERIAL PRIMARY KEY,
  recorded_at TIMESTAMPTZ NOT NULL,
  serial_number VARCHAR(50) NOT NULL REFERENCES equipment(serial_number),
  
  -- Vibration Data (Drive End)
  vibration_de_x_rms FLOAT4,
  vibration_de_y_rms FLOAT4,
  vibration_de_z_rms FLOAT4,
  vibration_de_overall_rms FLOAT4,
  vibration_de_peak FLOAT4,
  
  -- Vibration Data (Non-Drive End)
  vibration_nde_x_rms FLOAT4,
  vibration_nde_y_rms FLOAT4,
  vibration_nde_z_rms FLOAT4,
  vibration_nde_overall_rms FLOAT4,
  vibration_nde_peak FLOAT4,
  
  -- Temperature Data
  bearing_temp_de FLOAT4,
  bearing_temp_nde FLOAT4,
  
  -- Process Parameters
  rpm FLOAT4,
  flow_rate FLOAT4,
  suction_pressure FLOAT4,
  discharge_pressure FLOAT4,
  
  -- The Generated Column (Automated Math)
  differential_pressure FLOAT4 GENERATED ALWAYS AS (discharge_pressure - suction_pressure) STORED,
  
  -- Alarm Flags
  alarm_vibration_de SMALLINT DEFAULT 0,
  alarm_vibration_nde SMALLINT DEFAULT 0,
  alarm_bearing_temp_de SMALLINT DEFAULT 0,
  alarm_bearing_temp_nde SMALLINT DEFAULT 0,
  alarm_process SMALLINT DEFAULT 0,
  overall_status SMALLINT DEFAULT 0
);

-- 3. Create Indexes for Performance
CREATE INDEX idx_sensor_readings_recorded_at ON sensor_readings (serial_number, recorded_at DESC);
CREATE INDEX idx_sensor_readings_status ON sensor_readings (overall_status, recorded_at DESC);

-- 4. Insert a Dummy Pump
INSERT INTO equipment (serial_number, name, model, location)
VALUES ('PUMP-001', 'Main Cooling Water Pump', 'Centrifugal-X100', 'Factory Floor Section A');