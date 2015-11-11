import os
import sys
import csv

# for some reason my python install cant find stuff in the current directory
# of the script, so this tells it to change directories to wherever the heck 
# the script lives
os.chdir(os.path.dirname(sys.argv[0]))

# this opens the CSV file
spreadsheet = open("CityPop.csv","rt")

# I used a dict to store the information, keyed by the column "label." 
# csv.DictReader loops through each line of the CSV and adds each row to its own
# dict entry.
# dicts dont store duplicate values, so when the label and city match it throws one out.
# but if you use "label" it uses the correct non-stupid-underscore key value, 
# so that's good
my_dict = {}
reader = csv.DictReader(spreadsheet)
for row in reader:
    key = row.pop("label")
    my_dict[key] = row
    
print my_dict