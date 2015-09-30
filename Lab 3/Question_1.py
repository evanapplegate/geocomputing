# This program calculates the area of a triangle.

# This prints to the console "This program finds the area of a triangle." followed by a blank line.
print "This program finds the area of a triangle."
print 	

# This prompts the user to type a height value, and then a base value.  
height = input("Please enter the height of the triangle: ")
base = input("Please enter the base length of the triangle: ")

# This defines the variable "area" as equal to 0.5 times the height variable
# times the base variable (which were given by the user in the previous block)
area = 0.5 * height * base

# This code concatenates the boilerplate below with the height, base and area values
# calculated by the above code blocks.
print "The area of a triangle with height", height, "and base", base, "is", area, "."