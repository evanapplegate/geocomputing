import os
import sys
import csv

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

# This function asks the user to enter a city; if it's a valid input, i.e. it
# exists in the dict, it asks for a year. The year input string gets "yr" stuck to 
# the front and then the script looks up the correct value and prints it in
# a nice way
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

# while the restart value = True, the script will restart. This is what
# counts for error handling here
while restart == True:
    population_query()