#Example 4
class City:
    def __init__(self, name='n/a', lat = -999, lon = -999):
        self.name = name
        self.lat  = lat
        self.lon  = lon
        
    def printLatitude(self):
        print "%s is at latitude %.2f" % (self.name,self.lat)
        
    def printMilesNorth(self,city):
        dist = (self.lat-city.lat)*24859./360.
        fmt  = '%s is %.1f miles north of %s'
        vals = (self.name, dist, city.name)
        print fmt % vals

        
#create LA and over-ride all default values
LA = City()
LA.name = "Los Angeles"
LA.lat  = 33.93
LA.lon  = -120. 

#create Mad and over-ride some default values
Mad = City()
Mad.name = "Madison"
Mad.lat  = 43.08

print "longitude of LA is",LA.lon
print "longitude of Mad is",Mad.lon
