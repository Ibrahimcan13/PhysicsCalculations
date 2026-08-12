import numpy as np
from scipy import optimize
from scipy.optimize import curve_fit
from scipy import linalg

def cost_function(variables):
    x, y = variables
    return (x - 3)**2 + (y + 2)**2 + 5

initial_guess = [0.0, 0.0]

sol_2d = optimize.minimize(cost_function, initial_guess)

print("Multivariable Optimization")
print("Success:", sol_2d.success)
print(f"Optimal Point (x, y): ({sol_2d.x[0]:.2f}, {sol_2d.x[1]:.2f})")
print(f"Minimum Value f(x, y): {sol_2d.fun:.2f}\n")


def damped_oscillation(t, A, gamma, omega):
    return A * np.exp(-gamma * t) * np.cos(omega * t)

t_data = np.linspace(0, 10, 100)
y_exact = damped_oscillation(t_data, 5.0, 0.3, 2.5)

np.random.seed(42)
y_noise = 0.2 * np.random.normal(size=len(t_data))
y_data = y_exact + y_noise

popt, pcov = curve_fit(damped_oscillation, t_data, y_data)

A_fit, gamma_fit, omega_fit = popt

perr = np.sqrt(np.diag(pcov))

print("Curve Fitting Results")
print(f"Fitted Amplitude (A):       {A_fit:.3f} ± {perr[0]:.3f}")
print(f"Fitted Damping (gamma):    {gamma_fit:.3f} ± {perr[1]:.3f}")
print(f"Fitted Frequency (omega):  {omega_fit:.3f} ± {perr[2]:.3f}")


A = np.array([
    [3.0,  2.0, -1.0],
    [2.0, -2.0,  4.0],
    [-1.0, 0.5, -1.0]
])

b = np.array([1.0, -2.0, 0.0])

x_sol = linalg.solve(A, b)

print("Linear System Solution ")
print(f"Solution vector (x, y, z): {x_sol}\n")

M = np.array([
    [2.0, -1.0],
    [-1.0, 2.0]
])

eigenvalues, eigenvectors = linalg.eig(M)

print(" Eigenvalues & Eigenvectors")
print("Eigenvalues (lambda):", eigenvalues.real)
print("Eigenvectors matrix (columns are eigenvectors):\n", eigenvectors)
