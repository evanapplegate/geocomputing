# Initialize the counter for the dataset:
npts = 0
        # Open the data file:
orig_file = open("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 10 - file IO/LandTemp.txt","rt")
fahr_file = open("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 10 - file IO/temp_new.csv","w+")

columnHeads = "Long, Lat, Temp_in_F"
fahr_file.write(columnHeads)
fahr_file.write("\n")

for line in orig_file:
    fields = line.split()
    lon = float(fields[0])
    lat = float(fields[1])
    temp_in_C = float(fields[2])
    T_fahr = (temp_in_C*(9.0/5))+32
    
    if lon > 20 and lon < 30 and lat > 10 and lat < 40:
        values = str(lon) + "," + \
                str(lat) + "," + \
                str(T_fahr)
        fahr_file.write(values)
        fahr_file.write("\n")
fahr_file.close()