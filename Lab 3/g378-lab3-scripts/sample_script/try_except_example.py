'''
This program demonstrates an example to convert the input value into a numeric 
	type. It keeps asking the user for a convertible value until a successful 
	conversion is made or after 4 times.
'''

loopCount = 0
# The "while" statement keeps looping until its condition (loopCount<4) made False. 
while loopCount<4:
	# loopCount will increase 1 for each loop
	loopCount += 1
	
    print '\n----------- start program ---------'
    
    #the variable a is assigned a string value of whatever the user enters
    a = raw_input('\nTry entering an integer, float, or string value (or anything else!): ')     

    # try statement attempts to execute each statement below.
    # if try statement failed, it skips the remaining part and jumps to the except statement
    try:                                
        print '\nyour input is',a, 'which has a type of',type(a)
        
        # the float function attempts to convert the value of variable "a" into a float type
        a = float(a)      

        # If the conversion was successful, "a" becomes a numeric type, 
        # 	which could be used in any further calculation.
        # The while loop breaks after that.
        print '\nAfter a succssful conversion, the type of "a" is now: ',a, type(a)
        break 
        
    # If the conversion failed, the except statement will give an error message
    # 	and continue to a new loop.
    except:         
        print '\nyou entered a string value that can NOT be converted to an int or float value'



