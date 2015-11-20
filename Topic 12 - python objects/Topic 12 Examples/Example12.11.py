#Example 11
class City:
   def __init__(self, name='n/a', lat = 0, lon = 0):
      self.name = name
      self.setLonLat(lon,lat)
    
   def setLonLat(self,lon,lat):
      if -90  <= lat <= 90  : self._lat  = float(lat)
      if -180 <= lon <= 180 : self._lon  = float(lon)
       
   def getLonLat(self):
      return (self._lon,self._lat)

#create a city with a valid location
m = City(name='Madison',lat=43,lon=-89)

#this leaves _lon and _lat unchanged
m.setLonLat(999,999)

print 'The lon and lat of',m.name,'are',m.getLonLat()

