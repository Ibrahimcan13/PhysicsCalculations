from vpython import *
import random

scene = canvas(title="3D Keplerian Gravity & Orbit Simulator", width=800, height=600, center=vector(0, 0, 0), background=color.black)

G = 1

sun = sphere(pos=vector(0,0,0), radius=0.6, color=color.yellow, emissive=True)
sun.mass = 1000.0

planets = []
num_planets = random.randint(2, 4)
planet_colors = [color.cyan, color.magenta, color.green, color.orange]

for i in range(num_planets):

    orbital_radius = random.uniform(2.5, 5.5)

    random_pos = vector(orbital_radius, 0, 0)
    p_radius = random.uniform(0.1,0.3)
    p = sphere(pos=random_pos, radius = p_radius, color=random.choice(planet_colors),
               make_trail=True, retain=150, trail_radius= p_radius / 3)

    p.mass = 1

    perfect_speed = sqrt(G * sun.mass / orbital_radius)
    p.velocity = vector(0, perfect_speed * random.uniform(0.8, 1.2), random.uniform(-0.2, 0.2))

    planets.append(p)

dt = 0.005


while True:
    rate(150)

    for p in planets:

        r_vector = sun.pos - p.pos
        distance = r_vector.mag

        if distance <= (sun.radius + p.radius):
            p.visible = False
            p.clear_trail()
            planets.remove(p)
            continue

        r_hat = r_vector.norm()

        force_magnitude = (G * sun.mass * p.mass) / (distance ** 2)
        gravity_force = r_hat * force_magnitude

        acceleration = gravity_force / p.mass

        p.velocity = p.velocity + acceleration * dt
        p.pos = p.pos + p.velocity * dt