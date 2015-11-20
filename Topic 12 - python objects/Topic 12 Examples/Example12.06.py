#Example 6
class Base:
    def __init__(self,a=2,b=3):
        self.a = a
        self.b = b
        
    def ApB(self):
        return self.a + self.b


class SubClass(Base):
    def ApB(self): #over-rides Base definition
        return self.a * self.b


parent = Base()
child  = SubClass()
print 'Parent a,b,ApB:',parent.a, parent.b, parent.ApB()
print ' Child a,b,ApB:',child.a,  child.b,  child.ApB()

