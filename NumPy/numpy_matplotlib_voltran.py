import numpy as np
import matplotlib.pyplot as plt

time_array = np.linspace(0, 2, 11)
g=9.81
velocity_array = g*time_array

fig, ax = plt.subplots()
ax.plot(time_array, velocity_array, color='red', linestyle='solid', linewidth=3)
ax.set(xlabel='Time (s)', ylabel='Velocity (m/s)')
ax.set_title('Velocity vs Time', color='blue', fontweight='bold')
ax.grid(True)
plt.show()