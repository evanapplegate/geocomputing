#Example 9
class Point:
   def __init__(self,x = 0, y = 0):
        self.x = x
        self.y = y
        
class Polygon:
    def __init__(self,pts = []): #could be initialized with set of points
        self.pts    = pts
        self.computeCenter()
        self.computeArea()
           
    def computeCenter(self):
        'Find the average (x,y) of perimeter'
        n = len(self.pts)
        self.center = Point(0,0)
        if n > 0:
            for point in self.pts:
                self.center.x += point.x
                self.center.y += point.y

            self.center.x /= float(n)
            self.center.y /= float(n)

        return self.center

    def computeArea(self):
        'Find area defined by perimeter'
        n = len(self.pts)
        self.area = 0
        if n > 2:
            for i in xrange(-1,n-1):

                xi = self.pts[i].x
                yi = self.pts[i].y
                
                xj = self.pts[i+1].x
                yj = self.pts[i+1].y

                self.area = self.area + xi*yj - xj*yi
                
            self.area = abs(self.area)/2.
            
        return self.area
    
    def surroundsPt(self,p):
        'Point in Polygon test using ray count method'
        n = len(self.pts)
        if n < 3: return false

        x = p.x
        y = p.y
        
        crossingCount = 0
      
        for i in xrange(-1,n-1):
          xi = self.pts[i].x
          yi = self.pts[i].y
               
          xj = self.pts[i+1].x
          yj = self.pts[i+1].y

          if((yi <= y and y < yj) or (yj <= y and y < yi)):

             xCross = float(xj-xi)*(y-yi)/(yj-yi) + xi
             
             if  (x < xCross): crossingCount += 1

        #odd crossingCount means (x,y) is inside
        if crossingCount % 2 == 1: return True
        else                     : return False


class City(Polygon):
    def __init__(self,name = '',population = 0, pts = []):
        Polygon.__init__(self,pts)
        self.name = name
        self.pop  = population

        
class Parcel(Polygon):
    def __init__(self,owner = '', number = 0, assesment = 0, pts = []):
        Polygon.__init__(self,pts)
        self.owner      = owner
        self.number     = number
        self.assessment = assessment
        

class County(Polygon):
    def __init__(self,name = '',seat = '', cityCount = 0, pts = []):
        Polygon.__init__(self, pts)
        self.name      = name
        self.seat      = seat
        self.cityCount = cityCount
        Polygon.__init__(self)


triangle = Polygon([Point(20,20),Point(40,40),Point(60,20)])

print 'triangle center:',triangle.center.x,triangle.center.y
print 'triangle   area:',triangle.area,'\n\n'

a_city = City(name='c1',population = 200,pts = [Point(20,20),Point(40,40),Point(60,20)])

print "a_city's properties:"
print '   name:',a_city.name
print '    pop:',a_city.pop
print '   area:',a_city.area
print ' center:',a_city.center.x,a_city.center.y

print ' '


bTown = City('Boxton, WI',117)
print "City with default center and area"
vals = (bTown.name, bTown.pop, \
        bTown.center.x, bTown.center.y, bTown.area)
fmt = "%s (population %d) is centered on (%.1f,%.1f), its area is %.1f\n"

print fmt % vals

bTown.pts = [ Point(0,0), Point(0,1), Point(2,1), Point(2,0)]
bTown.computeArea()
bTown.computeCenter()


vals = (bTown.name, bTown.pop, \
        bTown.center.x, bTown.center.y, bTown.area)

print "City with revised attributes"
print fmt % vals

        
print 'Is (.1,.1) inside boxTown?',bTown.surroundsPt(Point(.1,.1))
print 'Is   (3,3) inside boxTown?',bTown.surroundsPt(Point(3,3))


print '\n\n'


triCo = County(name='Tri County')
triCo.pts = [Point(20,20),Point(40,40),Point(80,17)]

print 'Does tri surround (50.,50.)?',triCo.surroundsPt(Point(50.,50))

assert False

#test for series of points at y=30, x =20,21,...99
p = Point(0,30)
for j in xrange(20,100):
    p.x = j
    print "Does tri surround (",p.x,p.y,")?",triCo.surroundsPt(p)

