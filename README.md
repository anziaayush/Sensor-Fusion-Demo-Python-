# Sensor Fusion Demo (Python)

Simulation environment with two virtual distance sensors (ultrasound + radar) and simple filter fusion for improved distance estimation. Demonstrates data analysis and estimation skills.

## Goal

- Simulate noisy ultrasound and radar distance measurements
- Apply moving average + lightweight Kalman filter fusion
- Visualize raw vs fused sensor data in plots
- Export results for analysis

## Techniques Used

- Virtual sensor simulation (ultrasound: high noise, radar: outliers)
- Moving average filter
- Simple Kalman filter implementation
- Data fusion strategies
- Matplotlib visualization + CSV export

## Installation

```bash
git clone https://github.com/<your-username>/sensor-fusion-demo.git
cd sensor-fusion-demo
pip install -r requirements.txt
