import math

def areaCalc(radius):
    area = math.pi*(radius*radius)
    perimeter = 2*math.pi*radius
    return (area, perimeter)

area,perimeter = areaCalc(3) 
print area,perimeter