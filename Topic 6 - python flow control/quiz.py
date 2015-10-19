
x = [1,2,1,1,1,2,3,2,1,1,2,2,2,1,1,2,3,2,1,3,2,1,3]
votes_for_1 = 0
votes_for_2 = 0
votes_for_3 = 0

for votes in x:
    if votes == 1:
        votes_for_1 = votes_for_1 + 1
    elif votes == 2:
        votes_for_2 = votes_for_2 + 1
    else:
        votes_for_3 = votes_for_3 + 1

print "That's", votes_for_1, "votes for robot 1."
print "That's", votes_for_2, "votes for robot 2."
print "That's", votes_for_3, "votes for robot 3."

"""
x = 99
while x < 100:
    x = x + 1
    print "Boffo!"
    assert x == 100, "Such a terrible outcome"
"""