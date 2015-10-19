# -*- coding: utf-8 -*-
import math

def distance(point1,point2):
    dist = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    assert dist > 1e-9, ’program cannot handle duplicate points’
    return dist
point1 = [0,0]
point2 = [2,2]

print ’Distance between two different points:’, distance(point1, point2)