import numpy as np
import matplotlib.pyplot as plt

amplitude = float(input('Enter amplitude: '))
omega = float(input('Enter omega: '))

time = np.linspace(0,10,500)
position = amplitude * np.cos(omega * time)
velocity = amplitude * omega * np.sin(omega * time) * (-1)
acceleration = (-1) * (omega **2) * position

fig, ax = plt.subplots(2,1, sharex=True)
ax[0].plot(time, position, color='red')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Position')
ax[0].set_title('Position and Velocity')
ax[0].grid(True, alpha=0.5, linestyle='--')

ax[1].plot(time, velocity, color='blue', label='Velocity', linewidth=2, linestyle='--')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
ax[1].plot(time, acceleration, color='green', label='Acceleration', linewidth=2, linestyle='solid')
ax[1].legend(loc='upper left')
ax[1].grid(True, alpha=0.5, linestyle='--')

plt.tight_layout()
plt.show()


