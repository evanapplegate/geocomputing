# this program evaluates latitude and longitude inputs and says where they are.

print "This program gives extremely general locations if you feed it latitude and longitude coordinates."

# prompts the user to enter latitude and longitude values.
latitude = input("Please enter a decimal latitude: ")
longitude = input("Please enter a decimal longitude: ")
print

# the code below evaluates the latitude input and prints its general location.
if latitude == 0:
    print "That location is on the equator."
elif 0 < latitude < 90:
    print "That location is north of the equator."
elif -90 < latitude < 0:
    print "That location is south of the equator."
else:
    print "That location does not have a valid latitude!"
    
# the code below evaluates the longitude input and prints its general location.
if longitude == 0:
    print "That location is on the prime meridian."
elif 0 < longitude < 180:
    print "That location is east of the prime meridian."
elif -180 < longitude < 0:
    print "That location is west of the prime meridian."
else:
    print "That location does not have a valid longitude!"