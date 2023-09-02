# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_motor.ipynb.

# %% auto 0
__all__ = ['tire_radius', 'Torque_to_Force', 'Acceleration', 'zero_to_sixty', 'top_speed', 'rpm_at_mph', 'evaluate']

# %% ../nbs/00_motor.ipynb 3
import math
from .utilities import *

# %% ../nbs/00_motor.ipynb 5
def tire_radius(tire:str="165/80R15" # tire size in the format of "165/80R15"
                )->float:  # tire radius in inches
    """Calculate the tire radius in inches
    """
    wheel_diameter_inches = int(tire[-2:]) 
    sidewall_height = int(tire[0:3]) # sidewall height in mm
    aspect_ratio = int(tire.split("/")[1][0:2]) # aspect ratio
    sidewall_height_inches = sidewall_height * (aspect_ratio / 100) / 25.4 # sidewall height in inches
    radius = wheel_diameter_inches / 2 + sidewall_height_inches
    return radius


# %% ../nbs/00_motor.ipynb 7
def Torque_to_Force(torque:float, # torque in Nm
                    gear_ratio:float, # gear ratio
                    radius: float # radius of the wheel in m
                    )->float:   # Force acting on the pavement to push the car (N)
    """ Convert engine torque to force acting on pavement to push the car """
    return torque * gear_ratio / radius

# %% ../nbs/00_motor.ipynb 11
def Acceleration(F:float, # Force in N
                 mass:float, # mass of the car in kg
                 )->float: # acceleration in m/s^2
    """ Calculate the acceleration of the car """
    return F / mass

def zero_to_sixty(A:float # acceleration in m/s^2
                  )->float: # time in seconds
    """ Calculate the time it takes to go from 0 to 60 mph """
    # convert A from m/s^2 to mph/s
    A = A * 2.23693629 
    return 60 / A


# %% ../nbs/00_motor.ipynb 15
def top_speed(rpm_max:float, # max rpm
              gear_ratio:float, # gear ratio
              radius:float # radius of the wheel in m
              )->float: # top speed in mph
    """ Calculate the top speed of the car """
    return rpm_max * 60 * meters_to_inches(radius) * math.pi / (gear_ratio * 63360)

# %% ../nbs/00_motor.ipynb 19
def rpm_at_mph(gear_ratio:float, # gear ratio
                 tire:str, # tire size in the format of "165/80R15"
                 mph:float=60 # speed in mph (default is 60 mph)
                 )->float: # rpm
    """ Calculate the rpm at a given speed """
    radius = tire_radius(tire) # tire radius in inches
    tire_circumference = 2 * math.pi * radius # tire circumference in inches
    tire_rpm = mph * 5280 * 12 / (tire_circumference * 60) # tire rpm 
    return round(tire_rpm * gear_ratio)

# %% ../nbs/00_motor.ipynb 22
def evaluate(gear_ratio:float, # gear ratio
             GVWR:float, # gross vehicle weight rating in kg
             tire:str, # tire size in the format of "165/80R15"
             rpm_max:int, # max rpm
             torque:float # torque in Nm
             ):
    """ Evaluate the car """
    radius = tire_radius(tire)/12 # tire radius in feet
    radius = feet_to_meters(radius)
    F = Torque_to_Force(torque, gear_ratio, radius)
    A = Acceleration(F, GVWR)
    to60 = zero_to_sixty(A)
    mph_max = top_speed(rpm_max, gear_ratio, radius)
    return {"zero to sixty (sec)":round(to60,1), "Top speed (mph)":round(mph_max)}
