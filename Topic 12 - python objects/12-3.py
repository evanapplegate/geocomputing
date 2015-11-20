# -*- coding: utf-8 -*-
class City:
    def __init__(self, name='n/a', lat = -999, lon = -999):
        self.name = name
        self.lat  = lat
        self.lon  = lon

LA = City()
LA.name = "Los Angeles"
LA.lat  = 43.08
LA.lon  = -120.

Mad = City()
Mad.name = "Madison"
Mad.lat = 4

print 'longitude of LA is',LA.lon
print 'longitude of Mad is',Mad.lon