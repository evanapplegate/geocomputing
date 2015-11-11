#Initialize the dictionary to hold longitude,latitude, and temperature:
lonlatT = {}
        # Initialize the counter for the dataset:
npts = 0
        # Open the data file:
f = open("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 10 - file IO/LandTemp.txt","rt")
for line in f:
    # For each line in the file, split the line at 'space' characters:
    fields = line.split()
    # We know the file structure, it is `lon lat'
    lon = float(fields[0])
    lat = float(fields[1])
    T   = float(fields[2])
    lonlatT[(lon,lat)] = T
    
    npts += 1

f.close()

print "Read", npts, "grid locations"

while True:
    s = raw_input("\nEnter lon,lat (Return to exit) >")
    if len(s) < 1 : break
    
    try:
        s = s.split(',') #split input into lon,lat strings
        lon = round(float(s[0]))
        lat = round(float(s[1]))
        if (lon,lat) in lonlatT:
            print "T at",lon,lat, ":",lonlatT[ (lon,lat) ]
        else:
            print "Sorry,", s[0],s[1], "is not on land."
    except:
        print 'Try again.'