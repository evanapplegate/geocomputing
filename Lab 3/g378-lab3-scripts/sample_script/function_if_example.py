'''
This script shows an example of functions and if statements.
The import statement loads a random number generator module.
The function neatly contains the code and can be called later.
The if statements magically predict the answer of the user's question
depending on what number they enter.
'''


import random

def magicEightball():

    question = raw_input('Enter a yes/no question: ')

    num = random.randrange(1,7,1) #pick a number 1-6
      
    if num == 1:

        print "It is certain."
        
    elif num == 2:

        print "You may rely on it."

    elif num == 3:

        print "Reply hazy try again."

    elif num == 4:

        print "Ask again later."

    elif num == 5:

        print "Don't count on it."

    else:

        print "My sources say no."

magicEightball()
