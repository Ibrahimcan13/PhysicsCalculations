from vpython import *

scene = canvas(title="3D Coupled Pendulums & Wave Propagation", width=800, height=600, center=vector(8, 0, 0), background=color.black)
k = float(input("Please enter the k: "))
m = float(input("Please enter the mass of the balls: "))
damping = float(input("Please enter the damping: "))
num_pendulums = 12
spacing = 1.0

balls = []
for i in range(num_pendulums):

    equilibrium_x = i * spacing

    ball = sphere(pos=vector(equilibrium_x, 0, 0), radius=0.2,
                  color=color.cyan if i % 2 == 0 else color.magenta,
                  make_trail=True, retain=50, trail_radius=0.02)

    ball.eq_pos = vector(equilibrium_x, 0, 0)
    ball.velocity = vector(0, 0, 0)
    balls.append(ball)

balls[0].pos.y = 2.0
dt = 0.01

while True:
    rate(100)

    accelerations = [vector(0, 0, 0)] * num_pendulums

    for i in range(num_pendulums):
        displacement = balls[i].pos - balls[i].eq_pos
        restoring_force = -k * displacement
        coupling_force = vector(0, 0, 0)

        if i > 0:
            coupling_force += k * (balls[i - 1].pos - balls[i - 1].eq_pos - displacement)

        if i < num_pendulums - 1:
            coupling_force += k * (balls[i + 1].pos - balls[i + 1].eq_pos - displacement)

        total_force = restoring_force + coupling_force - damping * balls[i].velocity
        accelerations[i] = total_force / m

    for i in range(num_pendulums):
        balls[i].velocity += accelerations[i] * dt
        balls[i].pos += balls[i].velocity * dt