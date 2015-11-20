#Example 7
class Base:
    def __init__(self,a=2,b=3):
        self.a = a
        self.b = b
        
    def ApB(self):
        return self.a + self.b


class SubClass(Base):
    def __init__(self):
        self.c = 4
    
    def ApB(self): #over-rides Base definition
        return self.a * self.b


child = SubClass()
print 'child.c is',child.c
print 'child.a is',child.a

