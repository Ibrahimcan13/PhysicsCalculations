import matplotlib.pyplot as plt
from matplotlib import animation

m1 = float(input('Enter m1: '))
m2 = float(input('Enter m2: '))
x1 = float(input('Enter x1: '))
x2 = float(input('Enter x2: '))
v1 = float(input('Enter v1: '))
v2 = float(input('Enter v2: '))

fig, ax = plt.subplots()

ax.set_xlim(-20,20)
ax.set_ylim(-2,2)
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)

ball1, = ax.plot([], [], 'o', ms=20, color='lime')
ball2, = ax.plot([], [], 'o', ms=20, color='magenta')


def update(frame):
    global x1, x2, v1, v2

    dt = 0.01

    x1 += v1 * dt
    x2 += v2 * dt

    if x1 >= x2:

        v1, v2 = v2, v1

    ball1.set_data([x1], [0])
    ball2.set_data([x2], [0])

    return ball1, ball2,

ani = animation.FuncAnimation(fig, update, interval=6,frames=10000, blit=True)
plt.show()