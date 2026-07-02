import matplotlib.pyplot as plt
import matplotlib.animation as animation
g = 9.81
cor = float(input("Please enter the coefficient of restitution between 0 and 1: "))
x = float(input("Please enter the x position of the ball: "))
y = float(input("Please enter the y position of the ball: "))
vx = float(input("Please enter the x velocity of the ball: "))
vy = float(input("Please enter the y velocity of the ball: "))

fig, ax = plt.subplots()
ax.set_xlim(-15,15)
ax.set_ylim(0,y+5)
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='both', colors='white')
ax.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ball, = ax.plot([], [], 'o', ms=22, color='red')

def update(frame):
    global x, y, vx, vy

    dt = 0.0005
    sub_steps = 100

    for _ in range(sub_steps):
        vy -= g * dt
        x += vx * dt
        y += vy * dt
        if y <= 0:
            y = 0
            vy = -vy * cor
            vx = vx * 0.98

        if x >= 15:
            x = 15
            vx = -vx * cor

        if x <= -15:
            x = -15
            vx = -vx * cor

    ball.set_data([x], [y])
    return ball,
ani = animation.FuncAnimation(fig, update, interval=5,frames=30000, blit=True)
plt.show()