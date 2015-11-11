def tupleConcatenator(tuple1, tuple2): 
    if tuple1 == ():
       newTuple = (0,)
    elif tuple2 == ():
        newTuple = (0,)
    else:
        newTuple = tuple1 + tuple2
    return newTuple
   
tuple1 = ()     
#tuple1 = (1,2,3,4)
tuple2 = (5,6,7,8)

newTuple = tupleConcatenator(tuple1, tuple2)
print newTuple