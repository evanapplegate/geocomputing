# encoding: utf-8

# Question 1: this function takes a tuple of three values and converts them to decimal degrees
def DMS_to_DD(degrees, minutes, seconds):   
    
    # if the degree value is positive, then run the DMS > DD formula as below.
    # all input values are converted to floats to ensure precision
    # no error handling if someone tries to put in an illegal coordinate value, but there should be
    if degrees >= 0:
        DD = float(degrees) + (float(minutes)/60) + (float(seconds)/3600)
        return DD
    
    # if the degree value is negative, then run the same DMS > DD formula 
    # but make the minute and seconds values negative as well.
    if degrees < 0:
        DD = float(degrees) + (float(minutes*-1)/60) + (float(seconds*-1)/3600)
        return DD

# this is a test statement
# print DMS_to_DD(-30,30,0)

# Question 2: this function takes a single value and converts it to decimal degrees
def DD_to_DMS(decimal_degrees):
    
    # if the degree value is positive, then run the DMS > DD formula as below.
    # M (the minutes value) has to be converted back into a float because otherwise any decimal values will be dropped to zero
    # no error handling if someone tries to put in an illegal coordinate value, but there should be

    if decimal_degrees >= 0:
        D = int(decimal_degrees)
        M = int((decimal_degrees - D)*60)
        S = int((decimal_degrees - D - (float(M)/60))*3600)
        return D, M, S
    
    # if the degree value is negative, then run the DMS > DD formula same as
    # above, but return the absolute values of M and S
    if decimal_degrees < 0:
        D = int(decimal_degrees)
        M = int((decimal_degrees - D)*60)
        S = int((decimal_degrees - D - (float(M)/60))*3600)
        return D, abs(M), abs(S)

# this is a test statement
# print DD_to_DMS(25.51251)

# This asks the user to type in a coordinate
user_input = raw_input("Enter a latitude or longitude value in DMS or DD format. Just numbers, commas between values, \
and no spaces: ")

# This converts the input string to a list of values 
user_input_evaluation = user_input.split(",")

# If the input string has only 1 value, i.e. it's a list with 1 item, then this assumes
# that the input is a decimal degree coordinate
if len(user_input_evaluation) == 1:
    DD_value_to_convert = float(user_input_evaluation[0])
    DD_to_DMS_function_output = DD_to_DMS(DD_value_to_convert)
    
    # the return of the DD_to_DMS function is a list with 3 values. Here, the D, M, and S
    # values are split into separate variables; the D is the first item in the list,
    # M is the second value, and S is the third value.
    D_value = DD_to_DMS_function_output[0]
    M_value = DD_to_DMS_function_output[1]
    S_value = DD_to_DMS_function_output[2]
    
    # This prints the result with string concatentation.
    print "The input value is in DD form."
    print "Converted to DMS, it would read "+ str(D_value)+"º " + str(M_value)+"' "+ str(S_value)+"\""

# If the input string has 3 values, i.e. it's a list with 3 items, then this assumes
# that the input is a DMS coordinate
if len(user_input_evaluation) == 3:
    
    # the three input values are converted from strings to floats before being sent
    # to the DMS_to_DD function
    degrees = float(user_input_evaluation[0])
    minutes = float(user_input_evaluation[1])
    seconds = float(user_input_evaluation[2])
    DMS_to_DD_function_output = DMS_to_DD(degrees, minutes, seconds)
    
    # This prints the result with string concatentation.
    print "The input value is in DMS form."
    print "Converted to DD, it would read "+ str(DMS_to_DD_function_output)+"º"