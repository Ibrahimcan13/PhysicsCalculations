from vpython import *
import random

scene = canvas(title="3D Lorentz Force & Magnetic Helix Simulation", width=800, height=600, center=vector(0, 0, 0), background=color.black)

B_field_dir = vector(0, 0, 1)
for x in range(-5, 6, 3):
    for y in range(-5, 6, 3):
        arrow(pos=vector(x, y, -2), axis=B_field_dir * 1.5, color=color.cyan, opacity=0.3, shaftwidth=0.05)

proton = sphere(pos=vector(-5, 0, 0), radius=0.3, color=color.orange, make_trail=True, retain=150)
proton.trail_color = color.magenta

q = 1.0
m = 1.0
B_v = vector(0, 0, 2)
proton.velocity = vector(2, 4, 0.5)
dt = 0.01

label(pos=vector(0, 5, 0), text="Lorentz Force: F = q * (v x B)", box=False, color=color.white)

while True:
    rate(100)

    magnetic_force = q * cross(proton.velocity, B_v)

    acceleration = magnetic_force / m

    proton.velocity = proton.velocity + acceleration * dt

    proton.pos = proton.pos + proton.velocity * dt

    if proton.pos.x > 8 or proton.pos.x < -8 or proton.pos.y > 8 or proton.pos.y < -8:
        proton.pos = vector(-random.uniform(3, 8), random.uniform(-2, 2), 0)
        proton.velocity = vector(random.uniform(1, 3), random.uniform(3, 5), random.uniform(0.2, 1))
        proton.clear_trail()