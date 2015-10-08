# STRING
# lower/upper function
myStr = 'ABC'
print myStr.lower()
myStr = 'abc'
print myStr.upper()

# split function
# Return a list of the words in the string, using "," as the delimiter string
myStr = '1,2,3'
myList = myStr.split(',')
print myList

myStr = '1,,2'
myList = myStr.split(',')
print myList

myStr = '1<>2<>3'
myList = myStr.split('<>')
print myList

myStr = ''
myList = myStr.split(',')
print myList

# replace function
# Return a copy of the string with all occurrences of old substring replaced by new substring.
myStr = 'A ,B  , C '
myList = myStr.split(',')
print myList
myStr = myStr.replace(' ', '') # replace space with nothing
myList = myStr.split(',')
print myList

