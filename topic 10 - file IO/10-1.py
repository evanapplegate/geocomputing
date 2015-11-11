classFile = open("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 10 - file IO/ClassRoster.txt")
for student in classFile:
    newStudent = student.rstrip("\r\n")
    print newStudent