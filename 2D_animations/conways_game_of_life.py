import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

print("Second object's speed is 0 m/s")
m1= float(input("enter the value of m1: "))
m2= float(input("enter the value of m2: "))
v1= float(input("enter the value of v1: "))
v2=0
x1 = float(input("enter the value of x1: "))
x2 = float(input("enter the value of x2: "))

fig, ax = plt.subplots()

ax.set_xlim(-30,30)
ax.set_ylim(-5,5)
fig.set_facecolor('white')
ax.set_facecolor('white')
ax.grid(True, linestyle='-', color='gray', alpha=0.7)

ball1, = ax.plot([], [], 'o', ms=20, color='cyan')
ball2, = ax.plot([], [], 'o', ms=20, color='red')


def update(frame):
    global x1, x2, v1, v2

    dt = 0.01

    x1 += v1 * dt
    x2 += v2 * dt

    if x1 >= x2:
        v1, v2 = v2, v1

    elif x2 >= 20:
        v2 = -v2

    elif x1 <= -20:
        v1 = -v1

    ball1.set_data([x1], [0])
    ball2.set_data([x2], [0])

    return ball1, ball2,

ani = FuncAnimation(fig, update, interval=6, frames=20000, blit=True)
plt.show()