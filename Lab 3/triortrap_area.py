# This program calculates the area of a triangle or trapezoid, depending on the user's fancy.

import sys

# To ensure the script restarts if the user inputs something other than triangle or trapezoid,
# I have a simple boolean condition: the "invalid_input" variable is set to true to start, and
# if it stays that way, the program will continue and run the area-finding function. 

invalid_input = True

# I wrapped my if/elif/else statements into a function

def area_calculator() :

# This asks the user what shape they'd like to start with.
    shape = raw_input("This program finds the area of a triangle or a trapezoid. Please type either \"triangle\" or \"trapezoid\": ")
    if shape == "triangle": 
        
        # if the user chooses triangle, they are prompted to enter the height and base.
        print "Okay, let's find the area of a triangle."
        triangle_height = input("Please enter the triangle's height: ")
        triangle_base = input("Please enter the triangle's base length: ")
        
        # the calculation is performed and the inputs are concatenated into the result statement along with the triangle's area.
        triangle_area = 0.5 * triangle_height * triangle_base
        print "The area of a triangle with height", triangle_height, "and base", triangle_base, "is", triangle_area,"."
        
        # since everything was successfully executed, the script stops.
        sys.exit()
        
        
    elif shape == "trapezoid":
        
        # if the user chooses trapezoid, they are prompted to enter the height and two bases.
        print "Okay, let's find the area of a trapezoid."
        trapezoid_height = input("Please enter the trapezoid's height: ")
        trapezoid_base1 = input("Please enter the length of the trapezoid's lower base: ")
        trapezoid_base2 = input("Please enter the length of the trapezoid's upper base: ")
        
        # the calculation is performed; I had to make the denominator 2.0 instead of 2 
        # because python won't promote the quotient of two integers to a float.
        trapezoid_area = ((trapezoid_base1 + trapezoid_base2)/2.0) * trapezoid_height
        
        # the inputs are concatenated into the result statement along with the trapezoid's area.
        print "The area of a trapezoid with height", trapezoid_height, "and a lower base of", trapezoid_base1, \
        "and an upper base of", trapezoid_base2, "is", trapezoid_area, "."
        
        # since everything was successfully executed, the script stops.
        sys.exit()
        
        
    else:
        print "You can only type trapezoid or triangle. Don't get cute."
        
        # if the user enters anything other than triangle or trapezoid, the
        # invalid_input variable is set to True
        invalid_input = True

# while invalid_input is True (i.e. the user typed anything but triangle or
# trapezoid), the function will restart.

while invalid_input == True :
    area_calculator()