import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

y = float(input("Please enter a number that is bigger than 0 meter: "))
g=9.81
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

    dt = 0.01
    v -= g * dt
    y += v * dt

    if y <= 0:
        y = 0
        v = -v

    ball.set_data([0], [y])

    return ball,
ani = FuncAnimation(fig, update, interval=6, frames=10000,blit=True)
plt.show()
