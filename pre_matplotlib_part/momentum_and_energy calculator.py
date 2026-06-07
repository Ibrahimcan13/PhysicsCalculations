print("Energy and Momentum Calculator")

def physics_calculator():
    counter = 0
    while True:
        counter += 1
        print(f"Experiment number: {counter}")
        print('Type "q" for quiting the calculation')

        mass_input = input("Please enter the mass (kg): ")
        if mass_input == "q":
            print("Goodbye!")
            break

        velocity_input = input("Please enter the velocity (m/s): ")
        if velocity_input == "q":
            print("Goodbye!")
            break

        try:
            mass_float = float(mass_input)
            velocity_float = float(velocity_input)
            if mass_float<0 or velocity_float<0:
                print("Mass or velocity must be positive")
                continue

            kinetic_energy = (mass_float/2)* (velocity_float**2)
            momentum = mass_float * velocity_float
            print(f"RESULTS: \n Kinetic Energy: {kinetic_energy} \n Momentum: {momentum} ")

        except ValueError:
            print("Please enter a valid value")

physics_calculator()
