import numpy as np
import matplotlib.pyplot as plt

g=9.81
time_array = np.arange(0, 10.5, 0.5)
velocity_array = time_array * g

fig, ax = plt.subplots()
ax.plot(time_array, velocity_array , color = 'blue', linestyle = 'solid', marker = 'o' , linewidth = 2 , label = 'velocity', markerfacecolor='brown', markeredgecolor='brown')
ax.set(xlabel = 'Time (s)', ylabel = 'Velocity (m/s)')
ax.set_title("Time vs Velocity", color = 'red' , fontsize = 20)
ax.grid(True)
ax.legend()
plt.show()