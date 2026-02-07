import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os

class UltrasoundSensor:
    """Noisy ultrasound sensor simulation"""
    def __init__(self):
        self.noise_std = 0.08  # High noise
    
    def measure(self, true_distance):
        noise = np.random.normal(0, self.noise_std)
        return true_distance + noise

class RadarSensor:
    """Radar sensor with outliers"""
    def __init__(self):
        self.outlier_prob = 0.1
        self.noise_std = 0.03
    
    def measure(self, true_distance):
        if np.random.random() < self.outlier_prob:
            # Outlier: completely wrong reading
            return true_distance + np.random.uniform(-2, 2)
        noise = np.random.normal(0, self.noise_std)
        return true_distance + noise

class MovingAverageFilter:
    """Simple moving average filter"""
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.buffer = []
    
    def update(self, measurement):
        self.buffer.append(measurement)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
        return np.mean(self.buffer)

class SimpleKalmanFilter:
    """Lightweight 1D Kalman filter for distance estimation"""
    def __init__(self, process_noise=0.01, measurement_noise=0.05):
        self.x = 2.0  # Initial state estimate (distance)
        self.P = 1.0  # Initial uncertainty
        self.Q = process_noise  # Process noise
        self.R = measurement_noise  # Measurement noise
    
    def predict(self):
        # State prediction (constant velocity model, v=0)
        self.x = self.x
        self.P = self.P + self.Q
    
    def update(self, z):
        # Measurement update
        K = self.P / (self.P + self.R)  # Kalman gain
        self.x = self.x + K * (z - self.x)
        self.P = (1 - K) * self.P

def simulate_sensors(n_samples=500, true_distance_func=lambda t: 2.0 + 0.5*np.sin(t/50)):
    """Generate simulated sensor data"""
    ultrasound = UltrasoundSensor()
    radar = RadarSensor()
    
    time = np.linspace(0, 10, n_samples)
    true_distance = true_distance_func(time)
    
    ultrasound_data = np.array([ultrasound.measure(d) for d in true_distance])
    radar_data = np.array([radar.measure(d) for d in true_distance])
    
    return time, true_distance, ultrasound_data, radar_data

def fuse_sensors(ultrasound_data, radar_data):
    """Apply different fusion strategies"""
    # Moving average filters
    ultrasound_ma = MovingAverageFilter(5)
    radar_ma = MovingAverageFilter(5)
    
    ultrasound_filtered = []
    radar_filtered = []
    
    # Kalman filter
    kf = SimpleKalmanFilter()
    
    fused_ma = []
    fused_kf = []
    
    for u, r in zip(ultrasound_data, radar_data):
        # Moving average
        ultrasound_filtered.append(ultrasound_ma.update(u))
        radar_filtered.append(radar_ma.update(r))
        
        # Weighted average (radar more reliable when not outlier)
        fused_ma.append(0.4*u + 0.6*r)
        
        # Kalman fusion
        kf.predict()
        kf.update(0.5*u + 0.5*r)  # Pre-fuse measurements
        fused_kf.append(kf.x)
    
    return (np.array(ultrasound_filtered), np.array(radar_filtered),
            np.array(fused_ma), np.array(fused_kf))

def main():
    # Simulate data
    print("Simulating sensor data...")
    time, true_distance, ultrasound_data, radar_data = simulate_sensors()
    
    # Apply fusion
    print("Applying sensor fusion...")
    u_filtered, r_filtered, fused_ma, fused_kf = fuse_sensors(ultrasound_data, radar_data)
    
    # Calculate RMSE
    rmse_true = lambda x: np.sqrt(np.mean((x - true_distance)**2))
    print(f"RMSE - Ultrasound: {rmse_true(ultrasound_data):.3f}m")
    print(f"RMSE - Radar: {rmse_true(radar_data):.3f}m") 
    print(f"RMSE - Fused MA: {rmse_true(fused_ma):.3f}m")
    print(f"RMSE - Fused KF: {rmse_true(fused_kf):.3f}m")
    
    # Create plots
    os.makedirs("results", exist_ok=True)
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time, true_distance, 'k-', linewidth=2, label='True Distance')
    plt.plot(time, ultrasound_data, 'b--', alpha=0.7, label='Ultrasound')
    plt.plot(time, radar_data, 'r--', alpha=0.7, label='Radar')
    plt.ylabel('Distance [m]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title('Raw Sensor Measurements')
    
    plt.subplot(2, 1, 2)
    plt.plot(time, true_distance, 'k-', linewidth=2, label='True Distance')
    plt.plot(time, u_filtered, 'b-', alpha=0.8, label='Ultrasound (MA)')
    plt.plot(time, r_filtered, 'r-', alpha=0.8, label='Radar (MA)')
    plt.plot(time, fused_ma, 'g-', linewidth=2, label='Fused (MA)')
    plt.plot(time, fused_kf, 'm-', linewidth=2, label='Fused (Kalman)')
    plt.xlabel('Time [s]')
    plt.ylabel('Distance [m]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title('Filtered & Fused Measurements')
    
    plt.tight_layout()
    plt.savefig('results/fusion_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Save data
    df = pd.DataFrame({
        'time': time,
        'true_distance': true_distance,
        'ultrasound': ultrasound_data,
        'radar': radar_data,
        'fused_ma': fused_ma,
        'fused_kf': fused_kf
    })
    df.to_csv('data/sensor_data.csv', index=False)
    print("Results saved to data/sensor_data.csv")

if __name__ == "__main__":
    main()
