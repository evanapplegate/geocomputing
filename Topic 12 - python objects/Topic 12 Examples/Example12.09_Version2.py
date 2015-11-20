#Example 9 Revised
import math

class Point:
   def __init__(self,x = 0, y = 0):
        self.x = x
        self.y = y
        
class Polygon:
    def __init__(self,pts = []):
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

    def angle(self,pC,p1,p2):
       '''Return central angle of points p1,pC,p2 in radians
          with sign positive if counter-clockwise from p1 to p2,
          otherwise negative'''

       #vector a
       ax = p1.x - pC.x
       ay = p1.y - pC.y

       #vector b
       bx = p2.x - pC.x
       by = p2.y - pC.y

       #their lengths
       la = math.sqrt( ax*ax + ay*ay)
       lb = math.sqrt( bx*bx + by*by)

       if la <= 1.e-30 or la < 1.e-30: return 0

       #cosine of angle: dot product a.b  / |a||b|
       arg   = max(-1.0,min(1.0, (ax*bx + ay*by)/(la*lb) ) )
        
       #negative angle if "2-d cross-product" < 0
       if ax*by - ay*bx < 0: return -math.acos(arg)
       else:                 return  math.acos(arg)

    def surroundsPt(self,p):
       angleSum = 0
       for i in range(0,len(self.pts)):
          angleSum += self.angle(p,self.pts[i],self.pts[i-1])

       if abs(angleSum) < .01: return False
       else                  : return True
       
    def surroundsPt2(self,p):
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
    def __init__(self,name = '',population = 0,pts = []):
        Polygon.__init__(self,pts)
        self.name = name
        self.pop  = population

        
class Parcel(Polygon):
    def __init__(self,owner = '', number = 0, assesment = 0, pts=[]):
        Polygon.__init__(self,pts)
        self.owner      = owner
        self.number     = number
        self.assessment = assessment


class County(Polygon):
    def __init__(self,name = '',seat = '', cityCount = 0, pts=[]):
        Polygon.__init__(self,pts)
        self.name      = name
        self.seat      = seat
        self.cityCount = cityCount




triCo = County(name='Tri County')
triCo.pts = [Point(20,20),Point(40,40),Point(70,17)]

print 'Does tri surround (50.,50.)?',triCo.surroundsPt(Point(50.,50))


p = Point(0.0,30.0)
for j in xrange(0,100):
    p.x = 15.1+ j*.5
    print "Does tri surround (",p.x,p.y,")?",triCo.surroundsPt(p)

