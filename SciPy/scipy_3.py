import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d
from scipy.optimize import root_scalar
from scipy.signal import find_peaks

def force(x):
    return 2 * x**2 + 3 * x

x_start = 0.0
x_end = 2.0

work_done, error = integrate.quad(force, x_start, x_end)

print("2. Definite Integral (Work Done) Results")
print(f"Work Done (W):            {work_done:.4f} Joules")
print(f"Numerical Uncertainty:    ±{error:.2e}\n")


time_data = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
velocity_data = np.array([0.0, 3.2, 7.8, 14.1, 22.0])

velocity_interp = interp1d(time_data, velocity_data, kind='linear')

t_unknown = 2.5
predicted_velocity = velocity_interp(t_unknown)

print("3. Interpolation Results")
print(f"Estimated Speed at t = {t_unknown}s: {predicted_velocity:.2f} m/s\n")


def height(t):
    v0 = 20.0
    g = 9.81
    return v0 * t - 0.5 * g * t**2

sol = root_scalar(height, bracket=[1.0, 5.0], method='brentq')

print("4. Root Finding (Impact Time) Results")
print(f"Time of Impact (Ground Hit): {sol.root:.4f} seconds")

t_array = np.linspace(0, 5, 100)
position_signal = np.sin(2 * np.pi * t_array)

peaks, _ = find_peaks(position_signal)

print(" 5. Peak Detection Results ")
print(f"Times of Peak Positions: {t_array[peaks]} seconds")