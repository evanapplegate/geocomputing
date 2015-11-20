class City:
    def printLatitude(self):
        print "%s is at latitude %.2f" %(self.name, self.lat)
    # okay string formatting is annoying af but it seems to make sense; %s is for strings, %f is for floating point decimals  
    def printLongitude(self):
        print "%s is at longitude %.2f" %(self.name, self.long)    

LA = City()
LA.name = "Los Angeles"
LA.lat  = 33.93
LA.long  = -118.24

LA.printLatitude()
LA.printLongitude()