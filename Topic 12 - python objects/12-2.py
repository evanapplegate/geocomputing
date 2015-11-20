class City:
    def printLatitude(self):
        print "%s is at latitude %.2f" (self.name,self.lat)
    def printMilesNorth(self, othercity):
        dist   = (self.lat - othercity.lat) * 24859./360.
        format = "%s is %.1f miles north of %s"
        values = (self.name, dist, othercity.name)
        print format % values
    def printLatDiff(self, othercity):
        diff = abs(self.lat - othercity.lat)
        format = "There's a latitude difference of %.1f degrees between %s and %s"
        values = (diff, self.name, othercity.name)
        print format % values

# this is more specific and less flexibile than the generic methods defined within the class
def hardWayLatDiff(city1, city2):
    diff = abs(city1.lat - city2.lat)
    format = "There's a latitude difference of %.1f degrees between %s and %s"
    values = (diff, city1.name, city2.name)
    print format % values
    
LA = City()
LA.name = "Los Angeles"
LA.lat = 33.93

Mad = City()
Mad.name = "Madison"
Mad.lat  = 43.08

Mad.printMilesNorth(LA)
LA.printMilesNorth(Mad)

Mad.printLatDiff(LA)
hardWayLatDiff(LA, Mad)