from vpython import *
import math

scene = canvas(title="3D Double Pendulum & Chaos Theory Simulation", width=800, height=600, center=vector(0, -1, 0), background=color.black)

g = 9.81
dt = 0.005
L1 = 2.0
L2 = 1.5
m1 = 2.0
m2 = 1.5

theta1_A = math.pi / 2
theta2_A = math.pi / 2
omega1_A = 0.0
omega2_A = 0.0

theta1_B = (math.pi / 2) + 0.001
theta2_B = (math.pi / 2) + 0.001
omega1_B = 0.0
omega2_B = 0.0

base = sphere(pos=vector(0, 0, 0), radius=0.1, color=color.white)

rod1_A = cylinder(pos=base.pos, axis=vector(0, -L1, 0), radius=0.03, color=color.cyan, opacity=0.5)
ball1_A = sphere(pos=rod1_A.pos + rod1_A.axis, radius=0.15, color=color.cyan)
rod2_A = cylinder(pos=ball1_A.pos, axis=vector(0, -L2, 0), radius=0.03, color=color.cyan, opacity=0.5)
ball2_A = sphere(pos=rod2_A.pos + rod2_A.axis, radius=0.12, color=color.blue, make_trail=True, retain=100)

rod1_B = cylinder(pos=base.pos + vector(0,0,-0.2), axis=vector(0, -L1, 0), radius=0.03, color=color.magenta, opacity=0.5)
ball1_B = sphere(pos=rod1_B.pos + rod1_B.axis, radius=0.15, color=color.magenta)
rod2_B = cylinder(pos=ball1_B.pos, axis=vector(0, -L2, 0), radius=0.03, color=color.magenta, opacity=0.5)
ball2_B = sphere(pos=rod2_B.pos + rod2_B.axis, radius=0.12, color=color.red, make_trail=True, retain=100)


def get_derivatives(theta1, theta2, omega1, omega2):
    dtheta1 = omega1
    dtheta2 = omega2
    delta = theta1 - theta2

    num1 = -g * (2 * m1 + m2) * math.sin(theta1) - m2 * g * math.sin(theta1 - 2 * theta2) - 2 * math.sin(delta) * m2 * (
                omega2 ** 2 * L2 + omega1 ** 2 * L1 * math.cos(delta))
    den1 = L1 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
    alpha1 = num1 / den1

    num2 = 2 * math.sin(delta) * (
                omega1 ** 2 * L1 * (m1 + m2) + g * (m1 + m2) * math.cos(theta1) + omega2 ** 2 * L2 * m2 * math.cos(
            delta))
    den2 = L2 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
    alpha2 = num2 / den2

    return dtheta1, dtheta2, alpha1, alpha2


while True:
    rate(180)

    dth1_A, dth2_A, alp1_A, alp2_A = get_derivatives(theta1_A, theta2_A, omega1_A, omega2_A)
    omega1_A += alp1_A * dt
    omega2_A += alp2_A * dt
    theta1_A += dth1_A * dt
    theta2_A += dth2_A * dt

    dth1_B, dth2_B, alp1_B, alp2_B = get_derivatives(theta1_B, theta2_B, omega1_B, omega2_B)
    omega1_B += alp1_B * dt
    omega2_B += alp2_B * dt
    theta1_B += dth1_B * dt
    theta2_B += dth2_B * dt

    x1_A = L1 * math.sin(theta1_A)
    y1_A = -L1 * math.cos(theta1_A)
    ball1_A.pos = vector(x1_A, y1_A, 0)
    rod1_A.axis = ball1_A.pos - rod1_A.pos

    x2_A = x1_A + L2 * math.sin(theta2_A)
    y2_A = y1_A - L2 * math.cos(theta2_A)
    ball2_A.pos = vector(x2_A, y2_A, 0)
    rod2_A.pos = ball1_A.pos
    rod2_A.axis = ball2_A.pos - ball1_A.pos

    x1_B = L1 * math.sin(theta1_B)
    y1_B = -L1 * math.cos(theta1_B)
    ball1_B.pos = vector(x1_B, y1_B, -0.2)
    rod1_B.axis = ball1_B.pos - rod1_B.pos

    x2_B = x1_B + L2 * math.sin(theta2_B)
    y2_B = y1_B - L2 * math.cos(theta2_B)
    ball2_B.pos = vector(x2_B, y2_B, -0.2)
    rod2_B.pos = ball1_B.pos
    rod2_B.axis = ball2_B.pos - ball1_B.pos