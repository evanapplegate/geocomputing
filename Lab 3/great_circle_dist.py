# this program finds the distance between any two points on Earth's surface given their lat/long coordinates.

import math
import sys

print "This program calculates the great circle distance between any two locations on Earth's surface."

# prompts the user to enter latitude and longitude values.
latitude_input_1 = input("Please enter the decimal latitude of the first location: ")
longitude_input_1 = input("Please enter the decimal longitude of the first location: ")

latitude_input_2 = input("Please enter the decimal latitude of the second location: ")
longitude_input_2 = input("Please enter the decimal longitude of the second location: ")

# Converting the decimal degree inputs to radians.
latitude_1 = math.radians(latitude_input_1)
longitude_1 = math.radians(longitude_input_1)

latitude_2 = math.radians(latitude_input_2)
longitude_2 = math.radians(longitude_input_2)

# I stored the sines and cosines in their own variables to
# make the final equation a little easier to read and write.
latitude_1_sine = math.sin(latitude_1)
latitude_1_cosine = math.cos(latitude_1)

latitude_2_sine = math.sin(latitude_2)
latitude_2_cosine = math.cos(latitude_2)


great_circle_distance_angle = math.acos( (latitude_1_sine * latitude_2_sine) + \
(latitude_1_cosine * latitude_2_cosine) * math.cos(longitude_1 - longitude_2)) 

great_circle_distance_converted = int(great_circle_distance_angle * 6300)

print "The great circle distance between", latitude_input_1, ",", longitude_input_1, "and", latitude_input_2, ",", longitude_input_2,  \
"is about", great_circle_distance_converted, "km."