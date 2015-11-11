import os
import sys
import csv
import math

# for some reason my python install cant find stuff in the current directory
# of the script, so this tells it to change directories to wherever the heck 
# the script lives
os.chdir(os.path.dirname(sys.argv[0]))

# this opens the original CSV file
spreadsheet = open("CityPop.csv","rt")

# this creates the target CSV file and writes the column headers
output = open("CityPopChg.csv", "wt")

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

print "This script calculates the population change between a pair of years for all cities in the spreadsheet."

# run this code when the restart value equals true
while restart == True:
    
# this asks the user to enter two years; if the inputs
# aren't found in the dict, it asks the user to try again
    user_input_year1 = raw_input("Please enter the earlier year (between 1970-2010, 5 year increments) > ")
    if "yr"+user_input_year1 in my_dict["Kinshasa"]:
        user_input_year2 = raw_input("Please enter the later year (between 1970-2010, 5 year increments) > ")
        if "yr"+user_input_year2 in my_dict["Kinshasa"]:
            # writes column headers, including a custom one that changes depending on the user's year inputs
            col_head1 = "id"
            col_head2 = "city"
            col_head3 = "population_change_from_" + str(user_input_year1) + "_to_" + str(user_input_year2)
            output.write(col_head1 + "," + col_head2 + "," + col_head3)
            output.write("\n")
            # a loop to write the id, city name, and the actual population change
            for city in my_dict:
                output.write(my_dict[city]["id"] + "," + \
                             my_dict[city]["city"]  + "," + \
                             str(float(my_dict[city]["yr"+user_input_year2]) - float(my_dict[city]["yr"+user_input_year1])))
                output.write("\n")
            output.close()
            print "Cool, it worked; check the directory of this script to find your CSV."
            sys.exit()
        else:
            print "Invalid second year; please type another year."
            print " "
            restart = True
    else: 
        print "Invalid first year; please type another year."
        print " "
        restart = True 

# while the restart value = True, the script will restart. This is what
# counts for error handling here    
while restart == False:
    sys.exit()