from vpython import *
import math

scene = canvas(title="3D Fourier Series Epicycles Simulation", width=800, height=600, center=vector(2, 0, 0), background=color.black)

time = 0
dt = 0.02
num_circles = 5
num_circles = 5
base_pos = vector(0, 0, 0)
rods = []
visual_circles = []
current_center = base_pos
custom_gray = vector(0.5, 0.5, 0.5)

for i in range(num_circles):
    n = i * 2 + 1
    radius = 1.5 * (4 / (n * math.pi))

    rod = cylinder(pos=current_center, axis=vector(radius, 0, 0), radius=0.02, color=color.cyan, opacity=0.6)
    rods.append(rod)
    vis_circle = ring(pos=current_center, axis=vector(0,0,1), radius=radius, thickness=0.01, opacity=0.2)
    visual_circles.append(vis_circle)
    current_center = current_center + rod.axis

drawing_tip = sphere(pos=current_center, radius=0.08, color=color.magenta, make_trail=True, retain=300, trail_radius=0.015)

wave_x_start = 5.0
wave_points = []

while True:
    rate(120)

    current_center = base_pos

    for i in range(num_circles):
        n = i * 2 + 1
        radius = 1.5 * (4 / (n * math.pi))

        theta = n * time

        dx = radius * math.cos(theta)
        dy = radius * math.sin(theta)

        rods[i].pos = current_center
        rods[i].axis = vector(dx, dy, 0)
        visual_circles[i].pos = current_center

        current_center = current_center + rods[i].axis

    drawing_tip.pos = current_center
    time += dt