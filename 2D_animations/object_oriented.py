import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

NUM_PARTICLES = int(input("Enter the number of particles between 1 and 3: "))
RADIUS = float(input("Enter the radius of the particles: "))

if NUM_PARTICLES >3 or NUM_PARTICLES  <=0 :
    print("The number of particles between 1 and 3 cannot be less than or equal to 0 or be more than 3.")
else:

    fig, ax = plt.subplots()
    ax.set_xlim(-15,15)
    ax.set_ylim(-15,15)

    positions = np.array([[-5.0, 5.0],
                          [5.0, -5.0],
                          [0.0, -8.0]])

    velocities = np.array([[3.0, 2.0],
                           [-2.0, 4.0],
                           [1.0, -3.0]])

    balls, = ax.plot(positions[:, 0], positions[:, 1], 'o', ms=15, color='blue')

    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('red')
    ax.spines['left'].set_color('red')
    ax.spines['top'].set_color('red')
    ax.spines['right'].set_color('red')
    ax.tick_params(axis='both', colors='red')
    ax.grid(color='gray', linestyle='solid', linewidth=0.5, alpha=0.8)
    ax.set_title('This Thing')
    ax.set_xlabel('x')
    ax.set_ylabel('y')


    def update(frame):
        global positions, velocities

        dt = 0.02

        positions += velocities * dt

        for i in range(NUM_PARTICLES):
            if positions[i, 0] > 15 - RADIUS or positions[i, 0] < -15 + RADIUS:
                velocities[i, 0] *= -1
            if positions[i, 1] > 15 - RADIUS or positions[i, 1] < -15 + RADIUS:
                velocities[i, 1] *= -1

        for i in range(NUM_PARTICLES):
            for j in range(i + 1, NUM_PARTICLES):

                delta = positions[i] - positions[j]
                dist = np.linalg.norm(delta)

                if dist < 2 * RADIUS:
                    normal = delta / dist

                    rel_vel = velocities[i] - velocities[j]
                    vel_along_normal = np.dot(rel_vel, normal)

                    if vel_along_normal < 0:

                        impulse = vel_along_normal * normal
                        velocities[i] -= impulse
                        velocities[j] += impulse

        balls.set_data(positions[:, 0], positions[:, 1])
        return balls,

    ani = FuncAnimation(fig, update, interval=5, frames=40000, blit=True, repeat=True)
    plt.show()