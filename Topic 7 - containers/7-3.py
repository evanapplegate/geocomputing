"""
sentence = "heyooooo"
print sentence.count("o")
"""

def occurrence_counter(user_string, user_character):
    character_tally = user_string.count(user_character)
    return character_tally
    print character_tally
    
user_string = raw_input("Type a sentence and hit enter: ")
user_character = raw_input("Type a single character to tally up in this string and hit enter: ")

output = occurrence_counter(user_string, user_character)

print "The character","\""+user_character+"\"","shows up",output,"times in","\""+user_string+"\""



    
   
    
"""
    for character in xrange(len(inputString)):
        if inputString[character] == inputCharacter
            inputCharacterTally.append()
            
"""