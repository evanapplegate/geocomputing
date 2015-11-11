"""
Construct a dictionary to store the courses you took last semester by course number
(e.g., 'GEOG378'). Each course should have a course title and professor name.
(Hint: you may want to use tuples to store the information for each course.)

Then print each course above 300 level
"""

myCourses = {"GEOG 378":(378,"Geocomputing","Goring"),
             "GEOG 372":(372,"Intermediate remote sensing","Schneider"),
             "GEOG 578":(578,"GIS applications","Zhu")}
        
userInput = raw_input("Enter a course number to see some details about it >")
if userInput in myCourses:
    print "course",userInput,"is titled",myCourses[userInput][1],"and is taught by professor",myCourses[userInput][2]n