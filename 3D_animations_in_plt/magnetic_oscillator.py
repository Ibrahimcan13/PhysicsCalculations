import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dt = 0.03
k_gravity = float(input("Enter gravity constant: "))
k_magnet = float(input("Enter the coefficient of the magnet: "))
damp = float(input("Enter the damping constant between 0 and 0.1 : "))

if damp < 0.1:
    mag_R = np.array([1.5, 0.0, -1.0])
    mag_G = np.array([-0.75, 1.3, -1.0])
    mag_B = np.array([-0.75, -1.3, -1.0])

    pos = np.array([1.0, 1.0, 2.0])
    vel = np.array([0.0, 0.0, 0.0])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.xaxis.set_pane_color((0, 0, 0, 0))
    ax.yaxis.set_pane_color((0, 0, 0, 0))
    ax.zaxis.set_pane_color((0, 0, 0, 0))
    ax.tick_params(colors='lime')

    ax.set_xlim3d([-7, 7])
    ax.set_ylim3d([-7, 7])
    ax.set_zlim3d([-7, 7])


    trail, = ax.plot([], [], [], '-', lw=1.5, color='cyan', alpha=0.5)
    ball, = ax.plot([], [], [], 'o', ms=25, color='red')
    x_history, y_history, z_history = [], [], []

    def update(frame):
        global pos, vel, x_history, y_history, z_history


        acc = -k_gravity * pos

        r_R = mag_R - pos
        dist_R = np.linalg.norm(r_R)
        acc += (k_magnet / (dist_R ** 3)) * r_R

        r_G = mag_G - pos
        dist_G = np.linalg.norm(r_G)
        acc += (k_magnet / (dist_G ** 3)) * r_G


        r_B = mag_B - pos
        dist_B = np.linalg.norm(r_B)
        acc += (k_magnet / (dist_B ** 3)) * r_B

        acc -= damp * vel


        vel += acc * dt
        pos += vel * dt


        x_history.append(pos[0])
        y_history.append(pos[1])
        z_history.append(pos[2])

        trail.set_data(x_history, y_history)
        trail.set_3d_properties(z_history)

        ball.set_data([pos[0]], [pos[1]])
        ball.set_3d_properties([pos[2]])

        return trail, ball


    ani = FuncAnimation(fig, update, interval=4, blit=True, cache_frame_data=False)
    plt.show()

else:
    print("please enter the damp coefficient between 0 and 0.1")