# encoding: utf-8
import sys

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

# this is just a test statement
# print DMS_to_DD(-30,30,00)

# Question 2: this function takes a single value and converts it to decimal degrees
def DD_to_DMS(decimal_degrees):
    
    # if the degree value is positive, then run the DMS > DD formula as below.
    # values converted to integers per the formula
        # but M has to be converted back into a float because otherwise any decimal
        # values will be dropped to zero
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

# this is just a test statement    
# print DD_to_DMS(102.263888889)

user_input = raw_input("Enter a latitude or longitude value in DMS or DD format. Just numbers, commas between values, \
and no spaces: ")

user_input_evaluation = user_input.split(",")

if len(user_input_evaluation) == 1:
    DD_value_to_convert = float(user_input_evaluation[0])
    DD_to_DMS_function_output = DD_to_DMS(DD_value_to_convert)
    D_value = DD_to_DMS_function_output[0]
    M_value = DD_to_DMS_function_output[1]
    S_value = DD_to_DMS_function_output[2]
    print "The input value is in DD form."
    print "Its DMS form is "+ str(D_value)+"º " + str(M_value)+"' "+ str(S_value)+"\""

if len(user_input_evaluation) == 3:
    degrees = float(user_input_evaluation[0])
    minutes = float(user_input_evaluation[1])
    seconds = float(user_input_evaluation[2])
    #DMS_value_to_convert = str(degrees) minutes, seconds 
    DMS_to_DD_function_output = DMS_to_DD(degrees, minutes, seconds)
    print "The input value is in DMS form."
    print "Its DD form is "+ str(DMS_to_DD_function_output)+"º"