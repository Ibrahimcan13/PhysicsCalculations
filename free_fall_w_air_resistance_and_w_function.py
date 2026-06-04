print("Calculator of Free Fall Resistance With a Function")

def calculation_of_terminal_velocity(mass , area):
    g=9.81
    drag_coef = 0.47
    rho = 1.225
    terminal_velocity = ((2*mass*g)/(drag_coef*area*rho))**0.5
    return terminal_velocity

mass_input = float(input("Please enter the mass of the object in kg: "))
area_input = float(input("Please enter the area of the object in m2: "))

calculated_terminal_velocity = calculation_of_terminal_velocity(mass_input , area_input)

print(f"Terminal Velocity is: {calculated_terminal_velocity:.3f}")