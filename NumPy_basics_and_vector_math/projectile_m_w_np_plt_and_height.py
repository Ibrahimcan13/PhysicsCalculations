import numpy as np
import matplotlib.pyplot as plt

g= 9.81
velocity_initial = float(input("Please enter the initial velocity:"))
degree = float(input("Please enter the initial degree:"))
radians = np.radians(degree)

time_flight = (2*velocity_initial*np.sin(radians)) / g
input_time = np.linspace(0, time_flight, 300)

x_position = velocity_initial*np.cos(radians) * input_time
y_position = velocity_initial*np.sin(radians) * input_time - (0.5*g)*(input_time**2)

fig, ax = plt.subplots(3,1)

ax[0].plot(input_time, x_position, color='red', linewidth=2)
ax[0].grid(True, alpha=0.3)
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('X Position (m)')
ax[0].set_title('X position and time', color='darkblue')
ax[1].plot(input_time, y_position, color='purple', linewidth=2)
ax[1].grid(True, alpha=0.3)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Y Position (m)')
ax[1].set_title('Y position and time', color='darkblue')

ax[2].plot(x_position, y_position, color='green', linewidth=2)
ax[2].grid(True, alpha=0.3)
ax[2].set_xlabel('X Position (m)')
ax[2].set_ylabel('Y Position (m)')
ax[2].set_title('X position and Y Position', color='darkblue')

plt.tight_layout()
plt.show()
