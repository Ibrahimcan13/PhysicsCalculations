from vpython import *
import random

scene = canvas(title="3D Kinetic Gas & Elastic Collision Simulation", width=800, height=600, center=vector(0, 0, 0), background=color.black)
length = random.randint(3,8)
box_frame = box(pos=vector(0,0,0), size=vector(length, length, length), color=color.white, opacity=0.1, linecolor=color.gray)

ball_colors = [color.cyan, color.magenta, color.yellow, color.green, color.orange, color.red]
balls = []
num_balls = random.randint(4,7)

for i in range(num_balls):

    random_pos = vector(random.uniform(-length / 2 + 0.5, length / 2 - 0.5),
                        random.uniform(-length / 2 + 0.5, length / 2 - 0.5),
                        random.uniform(-length / 2 + 0.5, length / 2 - 0.5))

    b = sphere(pos=random_pos, radius=0.25, color=random.choice(ball_colors),
               make_trail=True, retain=30, trail_radius=0.05)

    b.velocity = vector(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-3, 3))
    b.mass = 1.0
    balls.append(b)

dt = 0.01

while True:
    rate(100)

    for b in balls:

        b.pos = b.pos + b.velocity * dt

        if abs(b.pos.x) >= (length / 2 - b.radius):
            b.velocity.x = -b.velocity.x

            b.pos.x = (length / 2 - b.radius) if b.pos.x > 0 else -(length / 2 - b.radius)

        if abs(b.pos.y) >= (length / 2 - b.radius):
            b.velocity.y = -b.velocity.y
            b.pos.y = (length / 2 - b.radius) if b.pos.y > 0 else -(length / 2 - b.radius)

        if abs(b.pos.z) >= (length / 2 - b.radius):
            b.velocity.z = -b.velocity.z
            b.pos.z = (length / 2 - b.radius) if b.pos.z > 0 else -(length / 2 - b.radius)

    for i in range(num_balls):
        for j in range(i + 1, num_balls):
            ball1 = balls[i]
            ball2 = balls[j]

            distance_vector = ball1.pos - ball2.pos
            distance = distance_vector.mag

            if distance <= (ball1.radius + ball2.radius):

                v_rel = ball1.velocity - ball2.velocity

                normal_dir = distance_vector.norm()

                v_rel_normal = dot(v_rel, normal_dir)

                if v_rel_normal < 0:
                    impulse = normal_dir * v_rel_normal
                    ball1.velocity = ball1.velocity - impulse
                    ball2.velocity = ball2.velocity + impulse

