import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


k = float(input("Enter k : "))
m = float(input("please enter the mass:"))
y_eq =0
y = float(input("Enter y : "))
v = float(input("Enter v : "))


fig, ax = plt.subplots()
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ball, = ax.plot([],[], 'o' ,ms=10, color='cyan')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.spines['bottom'].set_color('lime')
ax.spines['left'].set_color('lime')
ax.tick_params(axis='both', colors='lime')
ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
ax.set_title('Simple Harmonic Motion')
ax.set_xlabel('x')
ax.set_ylabel('y')

def update(frame):
    global y, v

    dt = 0.02

    displacement = y - y_eq
    force = -k * displacement

    acceleration = force / m

    v += acceleration * dt
    y += v * dt

    ball.set_data([0], [y])

    return ball,

ani = FuncAnimation(fig, update, interval=2,frames=10000, blit=True, repeat=True)
plt.show()