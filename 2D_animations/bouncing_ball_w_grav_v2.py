import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

y = float(input("Please enter a number that is bigger than 0 meter: "))
g = 9.81
cor = float(input("Please enter the coefficient of restitution between 0 and 1: "))
v = 0.000

fig, ax = plt.subplots()

ax.set_xlim(-5,5)
ax.set_ylim(0,y+5)
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('lime')
ax.spines['left'].set_color('lime')
ax.tick_params(axis='both', colors='lime')
ax.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ball, = ax.plot([], [], 'o', ms=22, color='cyan')

def update(frame):
    global y, v

    dt = 0.0001
    sub_steps = 300

    for _ in range(sub_steps):
        v -= g * dt
        y += v * dt

        if y <= 0:
            y = 0
            v = -v * cor

    ball.set_data([0], [y])
    return ball,

ani = FuncAnimation(fig, update, interval=6, frames=10000,blit=True)
plt.show()