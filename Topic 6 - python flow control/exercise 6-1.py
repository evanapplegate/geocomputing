def auto_Grader(grade):
    if grade > 90:
        print "The student got an A."
    elif 80 <= grade <= 90:
        print "The student got a B."
    elif 70 <= grade <= 80:
        print "The student got a C."
    elif 60 <= grade <= 70:
        print "The student got a D."
    elif grade < 60:
        print "The student got an F."

test = auto_Grader(50)
test = auto_Grader(70)