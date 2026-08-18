import sympy as sp

x, y, a, b, c = sp.symbols('x y a b c')

print("1. Algebraic Equation Solving ")

eq1 = x**2 - 5*x + 6
solutions1 = sp.solve(eq1, x)

print(f"Equation: {eq1} = 0")
print(f"Roots:    {solutions1}\n")

eq2 = sp.Eq(2*x + 3, 11)
solutions2 = sp.solve(eq2, x)

print(f"Equation: {eq2}")
print(f"Solution: {solutions2}\n")

eq3 = a*x**2 + b*x + c
quadratic_formula = sp.solve(eq3, x)

print(f"Quadratic Formula for {eq3} = 0:")
print(f"x1,2 = {quadratic_formula}\n")

sys_eq1 = sp.Eq(x + y, 5)
sys_eq2 = sp.Eq(x - y, 1)

system_solutions = sp.solve((sys_eq1, sys_eq2), (x, y))

print("Linear System Solutions (x + y = 5, x - y = 1):")
print(f"Solutions: {system_solutions}")


print("\n 2. Differential Equations")

t = sp.symbols('t')
y = sp.Function('y')

diffeq = sp.Eq(y(t).diff(t) + y(t), 0)
sol1 = sp.dsolve(diffeq, y(t))

print(f"Differential Eq 1: {diffeq}")
print(f"General Solution:  {sol1}\n")

