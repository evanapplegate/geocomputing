def gasCost(miles, mpg, gasPrice) :
    gallons = float(miles)/mpg       #gallons consumed
    return gallons*gasPrice #the actual spit-out output of this function is equal to the gallons value * the gasPrice value, which is the 3rd argument)
 
cost = gasCost(125, 27, 3.90)
roundedCost = round(cost)
print gallons