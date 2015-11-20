#Example 5
class Base:
    def __init__(self,a=2,b=3):
        self.a = a
        self.b = b
        
    def ApB(self):
        return self.a + self.b

class SubClass(Base):
    pass

child = SubClass()
print 'Child a,b,ApB : ',child.a,  child.b,  child.ApB()

