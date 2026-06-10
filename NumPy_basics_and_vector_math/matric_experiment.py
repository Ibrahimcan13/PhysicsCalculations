import numpy as np
import matplotlib.pyplot as plt
x_input = np.linspace(0, 5.1, 50)
y_output_1 = x_input ** 2
y_output_2 = x_input *2
fig, ax = plt.subplots(2,1)
ax[0].plot(x_input, y_output_1, color='red', linewidth=2,linestyle='solid', marker='o', markersize=2, markerfacecolor='blue', markeredgecolor='blue',label= 'Parabola')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
ax[0].legend()
ax[0].grid(True)
ax[0].set_title('Velocity vs Time', color='black')

ax[1].plot(x_input, y_output_2, color = "brown", linewidth =2, linestyle= 'solid', marker = "s", markersize=2, markerfacecolor="yellow", markeredgecolor='yellow',label= '2x graph')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
ax[1].legend()
ax[1].grid(True)
ax[1].set_title('2x graph')
plt.tight_layout()
plt.show()
