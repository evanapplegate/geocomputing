from sys import argv
import math

# this script takes a number parameter if you run it from the command line
# e.g. if you named this quiz.py, you'd type "python quiz.py 1" in the shell
# and it'd return "If your circle has a radius of 1, it has a circumference of 6.28318530718"

# this defines the circle_radius as the 1st item in the argv list
# since argv is a list of strings, it has to be converted to integer
radius = int(argv[1])

# since circumference = 2*radius*pi, I double the radius before multiplying by pi
circumference = (2*radius) * math.pi

# this converts the variables to strings and concatenates them for display
print 'If your circle has a radius of '+str(radius)+', it has a circumference of '+str(circumference)