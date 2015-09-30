# this program finds the distance between any two points on Earth's surface given their lat/long coordinates.

import math

print "This program calculates the great circle distance between any two locations on Earth's surface."

# prompts the user to enter latitude and longitude values. This is stored as a list.

while True:
    try: 
        coordinate_1 = input("Enter the first location in decimal degrees using the format [latitude], [longitude]: ")
        coordinate_2 = input("Enter the second location in decimal degrees using the format [latitude], [longitude]: ")
    except SyntaxError:
        print "Whoops, looks like you tried to enter coordinates with N, W, S or E, or something else entirely; please enter decimal degrees."
        bad_input = True
    else: 
        break

# Converting the decimal degree inputs to radians; the first value in
# the list is the latitude, and the second is the longitude.
latitude_1 = math.radians(coordinate_1[0])
longitude_1 = math.radians(coordinate_1[1])

latitude_2 = math.radians(coordinate_2[0])
longitude_2 = math.radians(coordinate_2[1])

# I stored the sines and cosines in their own variables to
# make the final equation a little easier to read and write.
latitude_1_sine = math.sin(latitude_1)
latitude_1_cosine = math.cos(latitude_1)

latitude_2_sine = math.sin(latitude_2)
latitude_2_cosine = math.cos(latitude_2)

# Calculating the great circle distance using the spherical distance formula
great_circle_distance_angle = math.acos( (latitude_1_sine * latitude_2_sine) + \
(latitude_1_cosine * latitude_2_cosine) * math.cos(longitude_1 - longitude_2)) 

# converting the distance to kilometers
great_circle_distance_converted = great_circle_distance_angle * 6300

# Printing the result
print "The great circle distance between", coordinate_1, "and", coordinate_2,  \
"is", great_circle_distance_converted, "km."