import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1 = L2 =  float(input("Enter the length of the pendulums: "))
m1 = float(input("Enter the mass of the first object: "))
m2 = float(input("Enter the mass of the second object: "))

theta1_deg = float(input("Enter the angle of the first object: "))
theta2_deg = float(input("Enter the angle of the second object: "))

theta1 = np.radians(theta1_deg)
theta2 = np.radians(theta2_deg)

omega1 = float(input("Enter the omega of the first object: "))
omega2 = float(input("Enter the omega of the second object: "))

fig, ax = plt.subplots()
ax.set_xlim(-25,25)
ax.set_ylim(-25,25)
line, = ax.plot([], [], lw=2, color = "cyan")

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
ax.set_title('Double Pendulum')
ax.set_xlabel('x')
ax.set_ylabel('y')

def update(frame):
    global theta1, theta2, omega1, omega2

    dt = 0.02
    g = 9.81

    delta = theta1 - theta2

    den1 = L1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))
    num1 = -g * (2 * m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2) - 2 * np.sin(delta) * m2 * (omega2**2 * L2 + omega1**2 * L1 * np.cos(delta))
    alpha1 = num1 / den1

    den2 = L2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))
    num2 = 2 * np.sin(delta) * (omega1**2 * L1 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1) + omega2**2 * L2 * m2 * np.cos(delta))
    alpha2 = num2 / den2

    omega1 += alpha1 * dt
    omega2 += alpha2 * dt
    theta1 += omega1 * dt
    theta2 += omega2 * dt

    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)

    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)

    line.set_data([0, x1, x2], [0, y1, y2])
    return line,

ani = FuncAnimation(fig, update, interval=5,frames=40000,  blit=True, repeat=True)
plt.show()
