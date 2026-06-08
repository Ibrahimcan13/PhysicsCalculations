import numpy as np
import matplotlib.pyplot as plt

time_array = np.arange(0, 10.2, 0.2)
g= 9.81
limit_speed = 47
raw_velocity = g*time_array
velocity_array = np.clip(raw_velocity, a_min=0, a_max=limit_speed)

fig, ax = plt.subplots()
ax.plot(time_array, velocity_array, color='red', linestyle='solid', linewidth=3,marker='o' , markersize=2 , markerfacecolor='yellow' , markeredgecolor='yellow', label='velocity')
ax.set(xlabel='Time (s)', ylabel='Velocity (m/s)')
ax.set_title('Velocity vs Time' , color='brown')
ax.grid(True)
ax.legend()
plt.show()
