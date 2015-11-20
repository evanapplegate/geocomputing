# -*- coding: utf-8 -*-
import os
import sys
import csv

"""
The name of your class should be City.
• Your class should have an __init__ method to assign values to the following attributes:
    city name, city label, latitude, longitude, population values from 1970 to 2010 (consider to store them in a dictionary). DONE
• Create a list called Cities to store the city instances based on reading the entries in CityPop.csv.
• Print out the attributes of all cities at the end.
• Like last lab, you need to deal with bad inputs when trying to read the file.

define class, give it initial values
Create empty list “Cities”
creat those 40 discrete lists of cities
City(x,y,z…) = creates an instance of class “City”; loop through each row and fill each instance with the data. use reader.lines
to append these instances to list “Cities”
"""

# for some reason my python install cant find stuff in the current directory
# of the script, so this tells it to change directories to wherever the heck 
# the script lives
os.chdir(os.path.dirname(sys.argv[0]))


# defining the class and setting default values; the default values
# have impossible values which tell when something isn't loaded right
class City:
    def __init__(self, name = 'n/a', label = 'n/a_label', lat = -999, \
                lon = -999, pop_1970 = -1, pop_1975 = -1, pop_1980 = -1, \
                pop_1985 = -1, pop_1990 = -1, pop_1995 = -1, pop_2000 = -1, \
                pop_2005 = -1, pop_2010 = -1):
        self.name = name
        self.label = label
        self.lat = lat
        self.lon = lon
        self.pop_1970 = pop_1970 
        self.pop_1975 = pop_1975
        self.pop_1980 = pop_1980
        self.pop_1985 = pop_1985
        self.pop_1990 = pop_1990 
        self.pop_1995 = pop_1995
        self.pop_2000 = pop_2000
        self.pop_2005 = pop_2005
        self.pop_2010 = pop_2010
        
# this opens the CSV file
spreadsheet = open("CityPop.csv","rt")

#City.city_instance = ()

# this reads in the CSV, splits  splits discrete LISTS by newline character,
# then splits list entries by comma
# strip off \r\n with rstrip?
Cities = []
reader = spreadsheet.readlines()
for row in reader[1:]:
    row = row.split(",")
    #City_name = row[4]
    Cities.append(City(name = str(row[3]),
                       label = str(row[4]),
                       lat = float(row[1]),
                       lon = float(row[2])))
    # just printing Cities yields nonsense, but think of it this way: Cities[position in list = row].column header you just
    # defined up there. so Cities[1].label gets you "New Delhi" while Cities[1].lon gets you 77.2008133. if you try
    # printing Cities[1].pop_1970 without defining its source from the CSV it will spit back -1, i.e. the init value
    # you gave above
print Cities[1].pop_1970
    #City_instance = City_name(name = str(row[3]))#, label = str(row[4]), lat = float(row[1]), lon = float(row[2]))
    #print City_instance
