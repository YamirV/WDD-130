def water_column_height(tower_height, tank_height): 
    """This function will calculate the height of the water column.

    parameters: tower_height, tank_height
    h = t + (3 * w) / 4
    where h is height of the water column
    t is the height of the tower
    w is the height of the walls of the tank that is on top of the tower                                               
    """

    height = tower_height + (3 * tank_height) / 4
    print(f"The height is : {height}")
    return height


def pressure_gain_from_water_height(height):
    """This function calculates the pressure caused by earth's gravity
    parameter: height
    formula: P = (p*g*h) / 1000

    where:
    P is the pressure in kilopascals
    p is the density of water (998.2 kilogram / meter3)
    g is the acceleration from Earths gravity (9.80665 meter / second2)
    h is the height of the water column in meters
    """
    p = 998.2
    g = 9.80665
    h = height
    P = (p * g * h) / 1000
    print(f"The pressure is: {P}")
    return P
 





def pressure_loss_from_pipe(pipe_diameter,
        pipe_length, friction_factor, fluid_velocity):
    """This function calculates the water pressure lost because of friction
    parameters: pipe_diameter, pipe_length, friction_factor, fluid_velocity

    formula: P = -(f * l * p * v**2) / (2000 * d)
    where: 
    P is the lost pressure in kilopascals
    f is the pipe's friction factor
    L is the length of the pipe in meters
    p is the density of water (998.2 kilogram / meter3)
    v is the velocity of the water flowing through the pipe in meters / second
    d is the diameter of the pipe in meters
    """
    d = pipe_diameter
    v = fluid_velocity
    p = 998.2
    l = pipe_length
    f = friction_factor

    P = -(f * l * p * v**2) / (2000 * d)
    print(f"The pressure is: {P}")
    return P
    

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """This function will calculate the pressure loss from pipe fittings
    parameters: fluid_velocity, quantity_fittings

    formula: P = -(0.04 * p * v**2 * n) / 2000
    
    where
    P is the lost pressure in kilopascals
    p is the density of water (998.2 kilogram / meter3)
    v is the velocity of the water flowing through the pipe in meters / second
    n is the quantity of fittings

    """

    p = 998.2
    v = fluid_velocity
    n = quantity_fittings

    P = -(0.04 * p * v**2 * n) / 2000
    print(f"This is the lost pressure: {P}")
    return P


def reynolds_number(hydraulic_diameter, fluid_velocity):
    """This function calculates and returns the reynolds number for a pipe
    parameters: hyraulic_diamter, fluid_velocity
    
    formula: R = (p * d * v) / u
    where
    R is the Reynolds number
    p is the density of water (998.2 kilogram / meter3)
    d is the hydraulic diameter of a pipe in meters. For a round pipe, the hydraulic diameter is the same as the pipe’s inner diameter.
    v is the velocity of the water flowing through the pipe in meters / second
    μ is the dynamic viscosity of water (0.0010016 Pascal seconds)
    """
    p = 998.2
    v = fluid_velocity
    d = hydraulic_diameter
    u = 0.0010016 

    R = (p * d * v) / u
    print(f"This is the Reynolds number: {R}")
    return R


def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """This function calculates the water pressure loss
            parameters: larger_diameter, fluid_velocoity, reynolds_number, smaller_diameter

        formulae: K = (0.1 + (50/R)) * ((D/4)**4 - 1)
        
        P = -(k * p * v) ** 2 / 2000

    where
    k is a constant computed by the first formula and used in the second formula
    R is the Reynolds number that corresponds to the pipe with the larger diameter
    D is the diameter of the larger pipe in meters
    d is the diameter of the smaller pipe in meters
    P is the lost pressure kilopascals
    p is the density of water (998.2 kilogram / meter3)
    v is the velocity of the water flowing through the larger diameter pipe in meters / second
    """
    v = fluid_velocity
    p = 998.2
    D = larger_diameter
    d = smaller_diameter
    R = reynolds_number
  
    # The function must first calculate the value of K in order to find the value of of P.
    K = (0.1 + 50/R) * (((D/d)** 4) - 1)
    P = (-K* p )* (v ** 2) / 2000
     
    print(f"The pressure loss is: {P}")
    return P


PVC_SCHED80_INNER_DIAMETER = 0.28687 # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65               # (meters / second)

HDPE_SDR11_INNER_DIAMETER = 0.048692 # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018   # (unitless)
HOUSEHOLD_VELOCITY = 1.75            # (meters / second)


def main():
    """This is the main function which will clall ther other functions in the order and aassing them as values of parameters for the other
    function in this file,"""
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss

    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss

    loss = pressure_loss_from_pipe_reduction(diameter,
            velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss

    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss

    print(f"Pressure at house: {pressure:.1f} kilopascals")


if __name__ == "__main__":
    main()





