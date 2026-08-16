import sympy as sp

x, y = sp.symbols('x y')

expr1 = (x + 2)**3
expanded_expr = sp.expand(expr1)

print("1. Algebraic Operations")
print(f"Original Expression: {expr1}")
print(f"Expanded Expression: {expanded_expr}\n")


expr2 = x**2 - 4
factored_expr = sp.factor(expr2)

print(f"Original Expression: {expr2}")
print(f"Factored Expression: {factored_expr}\n")


expr3 = sp.sin(x)**2 + sp.cos(x)**2
simplified_expr = sp.simplify(expr3)

print(f"Trigonometric Expression: {expr3}")
print(f"Simplified Result:       {simplified_expr}")


limit_expr1 = sp.sin(x) / x
limit_result1 = sp.limit(limit_expr1, x, 0)

print("\n 2. Limit Calculations")
print(f"Lim (x -> 0) of sin(x)/x: {limit_result1}")


limit_expr2 = (2*x**2 + 3) / (x**2 - 5)
limit_result2 = sp.limit(limit_expr2, x, sp.oo)

print(f"Lim (x -> oo) of (2x^2 + 3)/(x^2 - 5): {limit_result2}")


limit_expr3 = 1 / x
limit_result3_right = sp.limit(limit_expr3, x, 0, dir='+')

print(f"Lim (x -> 0+) of 1/x: {limit_result3_right}")


f = sp.exp(x) * sp.sin(x)

df_dx = sp.diff(f, x)

d2f_dx2 = sp.diff(f, x, 2)

print("\n 3. Analytical Derivatives")
print(f"Function f(x):       {f}")
print(f"First Derivative  f'(x):  {df_dx}")
print(f"Second Derivative f''(x): {d2f_dx2}")


df_at_0 = df_dx.subs(x, 0)
print(f"f'(0) value: {df_at_0}")

expr_int = 3*x**2 + 2*x
indefinite_int = sp.integrate(expr_int, x)

print("\n-4. Symbolic Integration")
print(f"Original Function:         {expr_int}")
print(f"Indefinite Integral (int): {indefinite_int} + C")

definite_int = sp.integrate(sp.sin(x), (x, 0, sp.pi))

print(f"Definite Integral sin(x) from 0 to pi: {definite_int}")