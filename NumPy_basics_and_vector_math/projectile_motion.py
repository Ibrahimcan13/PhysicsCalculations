import numpy as np
import matplotlib.pyplot as plt

g=9.81
velocity_initial = float(input("Please enter the initial velocity:"))
degree = float(input("Please enter the degree of motion:"))
radian = np.radians(degree)
input_time = np.linspace(0,10.1,100)
output_1 =  velocity_initial*np.cos(radian)*input_time
output_2 = velocity_initial*np.sin(radian)*input_time - (0.5*g*(input_time**2))

fig, ax = plt.subplots(2,1)
ax[0].plot(input_time,output_1, linewidth=4, color='red', linestyle='solid', marker='s', markersize=1, markerfacecolor='yellow', markeredgecolor='yellow')
ax[0].set_ylabel('Velocity (m/s)')
ax[0].set_xlabel('Time (s)')
ax[0].set_title('Time vs Horizontal Displacement', color='red')
ax[0].grid(True)

ax[1].plot(input_time, output_2, linewidth=2,color='black', linestyle = 'solid', marker='x', markersize=2, markerfacecolor='green', markeredgecolor='green')
ax[1].set_ylabel('displacement (m)')
ax[1].set_xlabel('Time (s)')
ax[1].set_title('Time vs Vertical Displacement', color='red')
ax[1].grid(True)
plt.tight_layout()
plt.show()