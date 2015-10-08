'''
def propertiesRect(width, height) :
    area = width*height  #area of rectangle
    perimeter = (width*2) + (height*2) #perimeter of rectangle
    return area, perimeter #the actual spit-out output of this function is equal to
    # the gallons value * the gasPrice value, which is the 3rd argument)

rect_area,rect_perimeter = propertiesRect(5,10)
print "The rectangle has an area of", rect_area, "and a perimeter of", rect_perimeter

'''

#or you can do this far simpler to get a tuple
def propertiesRect(width, height):
    return width*height, (width*2) + (height*2)

print propertiesRect(5,10)
print propertiesRect(5,10)[0]