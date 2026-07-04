import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

c = float(input("Enter the damped force which is between 0 and 1: "))
F0 = float(input("Enter the initial force: "))
m = float(input("Enter the mass: "))
w = float(input("Enter the omega of system: "))
k = float(input("Enter the damping rate: "))
v= float(input("Enter the initial velocity: "))
x = float(input("Enter the initial y position: "))
x_eq = 0
t = 0

fig, ax = plt.subplots()
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ball, = ax.plot([],[], 'o' ,ms=10, color='cyan')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
ax.set_title('Realistic Oscillator')
ax.set_xlabel('x')
ax.set_ylabel('y')

def update(frame):
    global x, v, t

    dt = 0.02

    f_spring = -k * (x - x_eq)
    f_damping = -c * v
    f_driving = F0 * np.sin(w * t)

    total_force = f_spring + f_damping + f_driving
    acceleration = total_force / m

    v += acceleration * dt
    x += v * dt
    t += dt

    ball.set_data([x], [0])
    return ball,
ani = FuncAnimation(fig, update, interval=5,frames=30000,  blit=True)
plt.show()