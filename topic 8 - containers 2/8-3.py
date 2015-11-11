def boundingBox(pts):
    '''Find bounding box for sequence of points   pts[0], pts[1]...
    For each member p of pts, the x- and y-coordinates
    are p[0] and p[1] respectively'''
    xmin = ymin =  1.e300
    xmax = ymax = -1.e300
    for p in pts:
        xmin = min(xmin,p[0])
        ymin = min(ymin,p[1])
        xmax = max(xmax,p[0])
        ymax = max(ymax,p[1])
        #return corners as list of tuples (2 tuples, not 4 values!!)
    return [(xmin,ymin),(xmax,ymax) ]
#list of 3 points
wellLocations = [ [-5,5], [10,-15], [12,3] ]

print "      points:",wellLocations
print "bounding box:",boundingBox(wellLocations),'\n'

ll,ur = boundingBox(wellLocations)
print 'lower left  corner:', ll
print 'upper right corner:', ur