#Example 2
class BadCity:
    def printLatitude(self):
         print "lat is",lat


lat = 999
LA = BadCity()
LA.name = "Los Angeles"
LA.lat = 33.93

Mad = BadCity()
Mad.name = "Madison"
Mad.lat  = 43.08

LA.printLatitude()
Mad.printLatitude()
