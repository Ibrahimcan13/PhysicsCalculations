import vpython as vp
import math

mag = float(input("Magnitude: "))
speed = float(input("Speed: "))
dt = 0.02
time = 0

vp.canvas(title='3D bouncing pendulum', width=800, height=600, background=vp.color.black)

ceiling = vp.box(pos=vp.vector(0, 10, 0), size=vp.vector(2, 0.5, 2), color=vp.color.orange)
ball = vp.sphere(pos=vp.vector(0, 2, 0), radius=0.8, color=vp.color.green)
rope = vp.cylinder(pos=ceiling.pos, axis=ball.pos - ceiling.pos, radius=0.05, color=vp.color.green)

while True:
    vp.rate(90)

    time += dt

    ball.pos.y = 10 - abs(mag * math.cos(time * speed))
    ball.pos.x = mag * math.sin(time * speed)
    rope.axis = ball.pos - ceiling.pos