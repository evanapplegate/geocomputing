#This script contains basic building blocks of Python Programming.

#math module imported (see below for explanation).
import math

# Statements and Values: print statement ouputs value of 5
print 5
print 5.5
print 'hello cows'

# Type function tells us the data type of an object
print type(5)     #output tells us 5 is an 'int' value, an integer

print type(5.5)   #output tells us 5.5 is a 'float' value, floating-point

print type('hello cows')  #output tells us "hello world" is a 'str' value, string


# Variables: use an assignment statement to create a new variable and give it a value

n = 5
pi = 3.1415926535897931
message = 'hello cows'

print message   #prints the value of message, which is the str 'hello world'
print n     #prints the value of n, which is the int 5
print pi    #prints the value of pi, which is the float 3.121 ...

# Careful, these keyword can NOT be used as variables
'''
and       del       from      not       while
as        elif      global    or        with
assert    else      if        pass      yield
break     except    import    print
class     exec      in        raise
continue  finally   is        return
def       for       lambda    try '''

# Expressions and operators: expressions combine values, variables, operators

a = 4
b = 9
c = a + b
print c     #c equals the sum of a and b, which is 13
print a/b  #this gives us a return value of zero, which isn't correct.  why?

a = 4.0     #a is being reassigned a float value of 4.0
b = 9.0     #same with b, a float value of 9.0
print a/b   #this time, the divison works because we're dividing float numbers which can
            #account for the decimal places

a = 4
b = 9
print float(a)/b  #alt. is toforce the conversion of int values with a float function

# Functions: there are built-in functions and custom functions.  We used the type() function above,
# a built in function.

# Another is the input() function, for integers, and the raw_input() function for strings

age = input('What is your age? ')       #input function
name = raw_input('What is your name? ')

print 'Your name is ', name, 'and you are', age, ' years old.'


# Math functions are provided by the math module (imported at top of this file)

print math.pi   #the name of the math module is specified first, and then the
                # pi function is called using the . (dot notation)

print math.cos(60)  #calls the cos method of the math module and passes the
                    #int 60 as an argument


# New functions can be build using a function definition

def sayHello():
    print 'hello cows'

sayHello()   #this line calls the sayHello function

#Function return values can also be assigned to a variable:

def sayHello():
    return 'hello cows'
    
a = sayHello()
print a


# We can also pass arguments to a function, which are then used as parameters within the function

def saySomething(word):
    print word          #in this case, whatever is passed to the saySomething
                        #function will be printed

saySomething ('hello world again')      #statement calls the saySomething function and passes
                                        #the str 'hello world again' as an argument

def saySomething2(word, num):
    print word,             #comma keeps output of next line on same line
    print num*2

saySomething2('hello world', 5)


# Conditional statements check conditions and change the behavior of the program

j = 2
k = 3
if j > k:           #if statements are structured in a similar way as functions
    print 'j is greater than k'
elif j < k:         #elif statement used to chain conditions together
    print 'j is less than k'
else:               #else clause must be used at end only
    print 'j and k are equal'
	
# You can use keywords to test multiple comparisons at once

if j > 1 and j < 3:
	print 'j is 2'
	
if k < 1 or k > 2:
	print 'k is not 2'

