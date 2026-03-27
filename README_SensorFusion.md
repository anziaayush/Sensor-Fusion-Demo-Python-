# Sensor Fusion — Kalman Filter vs Moving Average

A Python simulation of multi-sensor data fusion, combining noisy ultrasound and radar readings into a single accurate distance estimate. Demonstrates the Kalman filter, moving average filtering, and weighted sensor fusion — core techniques used in robotics, autonomous vehicles, and aerospace systems.

---

## What It Does

Real-world sensors are never perfect. This project simulates two imperfect sensors measuring the same distance, then applies different filtering strategies to recover an accurate signal from the noise.

The simulator generates synthetic sensor data, applies four estimation methods, compares their accuracy using RMSE (Root Mean Square Error), and produces publication-quality plots of the results.

---

## Sensor Models

| Sensor | Noise Model | Characteristics |
|---|---|---|
| Ultrasound | Gaussian noise (σ = 0.08m) | High noise, no outliers |
| Radar | Gaussian noise (σ = 0.03m) + 10% outlier probability | Low noise but occasional wild readings |

The "true" distance follows a sine wave: `2.0 + 0.5 × sin(t)` — simulating a slowly moving target over 10 seconds with 500 samples.

---

## Filtering & Fusion Methods

### 1. Moving Average Filter
Takes the mean of the last N readings. Simple and effective for smoothing out random noise but slow to react to real changes.

```
output = mean(last 5 readings)
```

### 2. Weighted Sensor Fusion
Combines both sensors using fixed weights based on their known reliability.

```
fused = 0.4 × ultrasound + 0.6 × radar
```
Radar is weighted higher because its noise is lower when not producing an outlier.

### 3. Kalman Filter
A mathematically optimal estimator that maintains a belief about the true state and updates it with each new measurement. Unlike moving average, it adapts its trust in new measurements based on uncertainty.

```
Predict:  x = x_prev
          P = P_prev + Q        (uncertainty grows over time)

Update:   K = P / (P + R)       (Kalman gain — how much to trust new data)
          x = x + K × (measurement − x)
          P = (1 − K) × P
```

Where:
- `x` = estimated distance
- `P` = estimation uncertainty
- `Q` = process noise (how much the true value can change)
- `R` = measurement noise (how noisy the sensor is)
- `K` = Kalman gain (balances prediction vs measurement)

The Kalman filter is used in GPS receivers, aircraft navigation, and self-driving cars for exactly this purpose — optimally combining uncertain measurements over time.

---

## Results

The Kalman filter consistently achieves the lowest RMSE across all runs:

| Method | Typical RMSE |
|---|---|
| Raw Ultrasound | ~0.080m |
| Raw Radar | ~0.090m (outliers) |
| Fused Moving Average | ~0.055m |
| Fused Kalman Filter | ~0.030m |

---

## Output Graphs

The program generates a two-panel plot saved to `results/fusion_results.png`:

**Plot 1 — Raw Sensor Measurements**
Shows the true distance (black), noisy ultrasound readings (blue dashed), and radar readings with outlier spikes (red dashed).

**Plot 2 — Filtered and Fused Results**
Shows all four estimation methods overlaid on the true signal — demonstrating how much the Kalman filter improves accuracy over raw and moving-average approaches.

---

## Project Structure

```
sensor-fusion/
├── main.py                  — Entry point, runs simulation and plots results
├── results/
│   └── fusion_results.png   — Output graph (generated on run)
├── data/
│   └── sensor_data.csv      — Raw and fused data (generated on run)
└── requirements.txt
```

---

## How to Run

### Prerequisites
- Python 3.8+
- pip

### Install dependencies

```bash
pip install numpy matplotlib pandas scipy
```

### Run the simulation

```bash
python main.py
```

This will:
1. Simulate 500 timesteps of sensor data
2. Apply all four filtering methods
3. Print RMSE scores to the terminal
4. Save the plot to `results/fusion_results.png`
5. Save all data to `data/sensor_data.csv`

### Example terminal output

```
Simulating sensor data...
Applying sensor fusion...
RMSE - Ultrasound: 0.081m
RMSE - Radar:      0.089m
RMSE - Fused MA:   0.054m
RMSE - Fused KF:   0.031m
Results saved to data/sensor_data.csv
```

---

## Key Concepts Demonstrated

- **Sensor fusion** — combining multiple imperfect sensors into one reliable estimate
- **Kalman filtering** — recursive Bayesian estimation under Gaussian noise
- **Moving average filtering** — sliding window smoothing
- **RMSE evaluation** — quantifying estimation accuracy
- **Outlier handling** — robustness of fusion vs single-sensor approaches

---

## Technologies

- **Language:** Python 3
- **Libraries:** NumPy, Matplotlib, Pandas, SciPy

---

## Author

**Aayush Anzi**
[github.com/anziaayush](https://github.com/anziaayush)
