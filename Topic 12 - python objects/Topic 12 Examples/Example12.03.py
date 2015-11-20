#Example 3
class City:
   def printLatitude(self):
      print "%s is at latitude %.2f"% (self.name,self.lat)

   def printMilesNorth(self,othercity):
      dist   = (self.lat - othercity.lat)*24859./360.
      format = '%s is %.1f miles north of %s'
      values = (self.name, dist, othercity.name)
      print format % values

        
LA = City()
LA.name = "Los Angeles"
LA.lat = 33.93

Mad = City()
Mad.name = "Madison"
Mad.lat  = 43.08

Mad.printMilesNorth(LA)
LA.printMilesNorth(Mad)
