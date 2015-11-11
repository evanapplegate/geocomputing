import math
f = open("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 10 - file IO/trig.csv","wt")
columnHeads = 'Angle, Sin(A), Cos(A)'
f.write(columnHeads)
f.write('\n')
for x in range(0,365,15):
    sinX = round(math.sin(math.radians(x)), 3)
    cosX = round(math.cos(math.radians(x)), 3)
    values = str(x)    + ',' + \
            str(sinX) + ',' + \
            str(cosX)
    f.write(values)
    f.write('\n')
f.close()