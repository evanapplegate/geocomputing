#Example 10

class Point:
   def __init__(self,x = 0, y = 0):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self,pts = []): #could be inititalized with set of points
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
    def __init__(self,name = 'None',population = 0):
        self.name = name
        self.pop  = population
        Polygon.__init__(self)


class State(Polygon):
    def __init__(self,name = 'None',population=0):
        self.name    = name
        self.pop     = population
        self.capital = City(name='None',population=0)
        Polygon.__init__(self)


MadTown = City(name='Madison',population = 245323)
        
WI = State('Wisconsin',5536201)
print 'WI name and pop:',WI.name,WI.pop
print 'WI capital name and capital pop:', \
       WI.capital.name,WI.capital.pop

WI.capital = MadTown;
print 'WI capital name and capital pop:', \
      WI.capital.name,WI.capital.pop



