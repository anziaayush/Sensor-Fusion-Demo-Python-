# Sensor Fusion Demo (Python)

Simulation environment with two virtual distance sensors (ultrasound + radar) and simple filter fusion for improved distance estimation. Demonstrates data analysis and estimation skills. the main.py simulates a robot or car trying to measure its distance from an object using two different sensors, then tries to get a more accurate reading by combining them.

## Goal

Imagine a self-driving car trying to measure how far away a wall is. It has two sensors, but both are imperfect:

Ultrasound sensor — like a bat's echolocation. It works well but is quite noisy/shaky in its readings
Radar sensor — more precise, but occasionally gives completely wrong readings (outliers)

Since neither sensor is perfect alone, the code fuses them together to get a better estimate.

## Techniques Used

1. Sensors — Two classes (UltrasoundSensor, RadarSensor) that simulate real-world imperfect sensors by adding random errors to the "true" distance.
2. Filters — Two ways to smooth out noisy data:

Moving Average — takes the last 5 readings and averages them, smoothing out spikes
Kalman Filter — a smarter mathematical filter used in GPS, aerospace, and robotics. It "predicts" where the value should be, then corrects itself with new data

3. Fusion — Combining both sensors into one better estimate, either by weighted average (60% radar, 40% ultrasound) or through the Kalman filter
4. Results — It calculates RMSE (Root Mean Square Error — how wrong each method is on average) and saves plots + a CSV file

## What does it gives as output?
The sensor readings are then faked by taking that true value and adding random errors to it in Python — ultrasound gets random shaking, radar gets occasional wild spikes. Those are the dashed colored lines in Plot 1.
The "true distance" is created by a math formula: 2.0 + 0.5 × sin(t). This just makes a gentle wave that goes up and down between roughly 1.5m and 2.5m over time. That's the black line.
Plot 2 shows what happens after the code tries to clean up those messy readings using the filters. The purple Kalman line should end up closest to the black "true" line, which is the whole point of the demo.

## Installation

```bash
git clone https://github.com/<your-username>/sensor-fusion-demo.git
cd sensor-fusion-demo
pip install -r requirements.txt
