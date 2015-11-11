import os
import sys
import csv

# for some reason my python install cant find stuff in the current directory
# of the script, so this tells it to change directories to wherever the heck 
# the script lives
os.chdir(os.path.dirname(sys.argv[0]))
test = open("CityPop.csv","rt")

restart = True

my_dict = {}

# dicts dont store dupes, so when label and city match it throws one out. great. but if you use label it uses
# the correct non-stupid-underscore key, so let's go with that
reader = csv.DictReader(test)
for row in reader:
    key = row.pop("label")
    my_dict[key] = row
"""  
if "yr2010" in my_dict["Kinshasa"]:
    print my_dict["Kinshasa"]["yr2010"]
else: print "key not found"
  

user_input_city = raw_input("Please enter a city > ")
user_input_year = raw_input("Please choose a year: 1970 through 2010 in increments of 5 years > ")

if user_input_city in my_dict:
    print "The population of "+ user_input_city + " in " + user_input_year + " was " \
                + my_dict[user_input_city]["yr"+user_input_year] + " million people"
else: 
    print "Try another city"


"""  
def population_query():
    user_input_city = raw_input("Please enter a city > ")
    if user_input_city in my_dict:
            user_input_year = raw_input("Please enter a year; it can be from 1970 through 2010 in increments of 5 years > ")
            if "yr"+user_input_year in my_dict[user_input_city]:
                print "The population of "+ user_input_city + " in " + user_input_year + " was " \
                + my_dict[user_input_city]["yr"+user_input_year] + " million people"
                restart = False
            else:
                print "Invalid year; choose a year from 1970-2010 in an increment of 5 years."
                restart = True
    else: 
        print "Invalid city input. Try another city."
        restart = True 

while restart == True:
    population_query()


"""  
#this is insanely sloppy list shit, need to use dicts here
city_list = []
pop_2010_list = []

test.readline()
for row in test:    
    rows = row.split(",")
    id_num = int(rows[0])
    latitude = float(rows[1])
    longitude = float(rows[2])
    city = str(rows[4])
    pop_1970 = float(rows[5])
    pop_1975 = float(rows[6])
    pop_1980 = float(rows[7])
    pop_1985 = float(rows[8])
    pop_1990 = float(rows[9])
    pop_1995 = float(rows[10])
    pop_2000 = float(rows[11])
    pop_2005 = float(rows[12])
    pop_2010 = float(rows[13])
    
    city_list.append(city)
    pop_2010_list.append(pop_2010)


#print pop_2010_list

user_input = raw_input("Please enter a city to find out its 2010 population> ")
if user_input in city_list:
    position = city_list.index(user_input)
    print pop_2010_list[position]
else:
    print "Try another city"
    
"""