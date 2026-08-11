import numpy as np
from scipy import integrate
from scipy import constants
from scipy import optimize

def integrand(x):
    return np.sin(x)

result, error = integrate.quad(integrand, 0, np.pi)

print(f"Result: {result}")
print(f"Estimated Absolute Error: {error}")

def polynomial(x, a, b):
    return a * x**2 + b

a_val = 2.0
b_val = 5.0

result, error = integrate.quad(polynomial, 0, 3, args=(a_val, b_val))

print(f"Integral Result: {result:.4f}")

lambda_green = 500 * constants.nano

E_joule = (constants.h * constants.c) / lambda_green

E_eV = E_joule / constants.eV

print(f"Photon Energy (Joule) : {E_joule:.4e} J")
print(f"Photon Energy (eV)    : {E_eV:.2f} eV")

def spring_force(x, k):
    return k * x

k_spring = 50.0
x_start = 0.0
x_end = 0.2
work_done, error = integrate.quad(spring_force, x_start, x_end, args=(k_spring,))

print(f"Work done to stretch the spring: {work_done:.4f} Joules")
print(f"Estimated error: {error:.4e}")

time = np.array([0, 1, 2, 3, 4, 5])

velocity = np.array([0, 2, 8, 18, 32, 50])

displacement_simpson = integrate.simpson(velocity, x=time)
displacement_trap = integrate.trapezoid(velocity, x=time)

print(f"Displacement (Simpson): {displacement_simpson:.2f} meters")
print(f"Displacement (Trapezoid): {displacement_trap:.2f} meters")

def f(x):
    return x**3 + np.cos(x) - 3

sol = optimize.root_scalar(f, bracket=[1, 2], method='brentq')

print("Is optimization successful?", sol.converged)
print("Root value (x):", sol.root)

def net_force(v, m, g, c):
    return m * g - c * v**2

m_val = 80.0
g_val = 9.81
c_val = 0.25

sol1 = optimize.root_scalar(
    net_force,
    args=(m_val, g_val, c_val),
    bracket=[0, 100],
    method='brentq'
)

print(f"Terminal Velocity: {sol1.root:.2f} m/s")


def potential_energy(r, A, B):
    return (A / r**12) - (B / r**6)

A_const = 1.0
B_const = 2.0

sol_min = optimize.minimize_scalar(
    potential_energy,
    args=(A_const, B_const),
    bounds=(0.5, 3.0),
    method='bounded'
)

print(f"Is optimization successful? {sol_min.success}")
print(f"Equilibrium distance (r): {sol_min.x:.4f}")
print(f"Minimum Potential Energy: {sol_min.fun:.4f}")