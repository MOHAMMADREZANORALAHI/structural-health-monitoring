import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def generate_vibration_data(duration=5.0, sampling_rate=100.0):
    """
    Simulates structural vibration data with structural frequencies and noise.
    """
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    
    # Simulating two natural frequencies of a structure (e.g., 5 Hz and 12 Hz)
    freq1, freq2 = 5.0, 12.0
    signal = 2.0 * np.sin(2 * np.pi * freq1 * t) + 1.5 * np.sin(2 * np.pi * freq2 * t)
    
    # Adding random environmental noise
    noise = np.random.normal(0, 0.5, size=t.shape)
    acceleration = signal + noise
    
    return pd.DataFrame({"Time": t, "Acceleration": acceleration})

def analyze_frequency_domain(df, sampling_rate=100.0):
    """
    Performs Fast Fourier Transform (FFT) to analyze structural frequencies.
    """
    acc = df["Acceleration"].to_numpy()
    n = len(acc)
    
    # Compute FFT
    yf = fft(acc)
    xf = fftfreq(n, 1 / sampling_rate)
    
    # Keep only positive frequencies
    positive_indices = xf >= 0
    frequencies = xf[positive_indices]
    amplitudes = (2.0 / n) * np.abs(yf[positive_indices])
    
    return frequencies, amplitudes

if __name__ == "__main__":
    print("="*50)
    print("Structural Health Monitoring - Vibration Analysis Tool")
    print("="*50)
    
    # 1. Generate data
    fs = 100.0  # Sampling frequency (Hz)
    print("[INFO] Simulating structural vibration data...")
    vibration_df = generate_vibration_data(duration=10.0, sampling_rate=fs)
    
    # 2. Perform frequency analysis
    print("[INFO] Performing Fast Fourier Transform (FFT)...")
    freqs, amps = analyze_frequency_domain(vibration_df, sampling_rate=fs)
    
    # 3. Identify dominant frequencies
    peak_indices = np.argsort(amps)[-2:][::-1]
    print(f"\n[RESULTS] Detected Primary Structural Frequencies:")
    for idx in peak_indices:
        print(f" - Frequency: {freqs[idx]:.2f} Hz | Amplitude: {amps[idx]:.2f}")
    
    print("\n[INFO] Analysis completed successfully.")
    print("="*50)
