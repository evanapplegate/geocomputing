"""
Construct a dictionary to store the courses you took last semester by course number
(e.g., 'GEOG378'). Each course should have a course title and professor name.
(Hint: you may want to use tuples to store the information for each course.)

Then print each course above 300 level
"""

myCourses = {"GEOG 378":(378,"geocomputing","goring"),
             "GEOG 372":(372,"intermediate remote sensing","scheider"),
             "GEOG 578":(578,"GIS applications","zhu")}

for key in myCourses: # loop through key in dict myCourses
    if myCourses[key][0] > 400: # if the first value in each key is more than 400...
        print myCourses[key][0:] # print every value in the key