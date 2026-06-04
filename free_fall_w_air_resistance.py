g = 9.81
drag_coef = 0.47
rho = 1.225
mass = float(input("Please enter the mass of the object in kg: "))
area =  float(input("Please enter the area of the object in m2: "))
terminal_velocity = ((2*mass*g)/(drag_coef*area*rho))**0.5
print(f"terminal velocity is: {terminal_velocity:.3f}m/s")