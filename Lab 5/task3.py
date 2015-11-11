import os
import sys
import csv
import math

# for some reason my python install cant find stuff in the current directory
# of the script, so this tells it to change directories to wherever the heck 
# the script lives
os.chdir(os.path.dirname(sys.argv[0]))

# this opens the CSV file
spreadsheet = open("CityPop.csv","rt")

restart = True

# I used a dict to store the information, keyed by the column "label." 
# csv.DictReader loops through each line of the CSV and adds each row to its own
# dict entry.
# dicts dont store dupes, so when label and city match it throws one out.
# but if you use "label" it uses the correct non-stupid-underscore key value,
my_dict = {}
reader = csv.DictReader(spreadsheet)
for row in reader:
    key = row.pop("label")
    my_dict[key] = row


# This function calculates the great circle distance between two lat/long pairs
def great_circle_calculator(first_city_lat, first_city_long, second_city_lat, second_city_long):      
    # Converting the decimal degree inputs to radians; the first value in
    # the list is the latitude, and the second is the longitude.
    latitude_1 = math.radians(float(first_city_lat))
    longitude_1 = math.radians(float(first_city_long))
    
    latitude_2 = math.radians(float(second_city_lat))
    longitude_2 = math.radians(float(second_city_long))
    
    # I stored the sines and cosines in their own variables to
    # make the final equation a little easier to read.
    latitude_1_sine = math.sin(latitude_1)
    latitude_1_cosine = math.cos(latitude_1)
    
    latitude_2_sine = math.sin(latitude_2)
    latitude_2_cosine = math.cos(latitude_2)
    
    # Calculating the great circle distance using the spherical distance formula
    great_circle_distance_angle = math.acos((latitude_1_sine * latitude_2_sine) + \
    (latitude_1_cosine * latitude_2_cosine) * math.cos(longitude_1 - longitude_2)) 
    
    # converting the distance to kilometers
    great_circle_distance_converted = great_circle_distance_angle * 6300
    
    print "The great circle distance between", user_input_city1, "and", user_input_city2,  \
                "is approximately", round(great_circle_distance_converted), "km."


# This function collects the city coordinates from the dict
def distance_query(city1, city2):
    first_city_lat = my_dict[user_input_city1]["latitude"]
    first_city_long = my_dict[user_input_city1]["longitude"]
    second_city_lat = my_dict[user_input_city2]["latitude"]
    second_city_long = my_dict[user_input_city2]["longitude"]
    great_circle_calculator(first_city_lat, first_city_long, second_city_lat, second_city_long)   
    restart = False
    sys.exit()


# run this code when the restart value equals true
while restart == True:
# this asks the user to enter two cities; if the inputs
# aren't found in the dict, it asks the user to try again
    user_input_city1 = raw_input("Please enter the first city > ")
    if user_input_city1 in my_dict:
        user_input_city2 = raw_input("Please enter the second city > ")
        if user_input_city2 in my_dict:
            distance_query(user_input_city1, user_input_city2)
        else:
            print "Invalid second city; please type another city."
            print " "
            restart = True
    else: 
        print "Invalid first city; please type another city."
        print " "
        restart = True 

# while the restart value = True, the script will restart. This is what
# counts for error handling here    
while restart == False:
    sys.exit()