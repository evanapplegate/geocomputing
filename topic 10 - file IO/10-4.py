import sys
import math


try:
    radius = float(sys.argv[1])
    area = float(math.pi*(radius**2))
    print "The area of a circle with radius %f is %f" % (radius, area)
except:
    print "Sorry, just put in a single radius value."