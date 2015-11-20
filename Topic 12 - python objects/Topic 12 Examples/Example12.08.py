#Example 8
class Base:
    def __init__(self,a=2,b=3):
        self.a = a
        self.b = b
        
    def ApB(self):
        return self.a + self.b


class SubClass(Base):
    def __init__(self):
        Base.__init__(self) #call parent's initializer
        self.c = 4
    
    def ApB(self): #over-rides parent's definition
        return self.a * self.b


child = SubClass()
print 'child.c is',child.c
print 'child.a is',child.a

