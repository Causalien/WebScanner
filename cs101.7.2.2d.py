#Spelling Correction

#Double Gold Star

#For this question, your goal is to build a step towards a spelling corrector,
#similarly to the way Google used to respond,

#    "Did you mean: audacity"


#when you searched for "udacity" (but now considers "udacity" a real word!).

#One way to do spelling correction is to measure the edit distance between the
#entered word and other words in the dictionary.  Edit distance is a measure of
#the number of edits required to transform one word into another word.  An edit
#is either: (a) replacing one letter with a different letter, (b) removing a
#letter, or (c) inserting a letter.  The edit distance between two strings s and
#t, is the minimum number of edits needed to transform s into t.

#Define a procedure, edit_distance(s, t), that takes two strings as its inputs,
#and returns a number giving the edit distance between those strings.

#Note: it is okay if your edit_distance procedure is very expensive, and does
#not work on strings longer than the ones shown here.

#The built-in python function min() returns the mininum of all its arguments.

#print min(1,2,3)
#>>> 1
debug = False
def edit_distance(s,t):
    result = 0
    ways = []
    searched = []
    newsearch = []
    wordsearch = ""
    searchstring = ''
    size = 0
    mask = []

    for i in range(0, len(s), 1):
        mask = []
        for x in s:
            mask.append(1)
            while x < len(s):
                mask[x%len(s)] = 0
                x +=1
            
        print mask
    
    if t.find(s) > 0:
        return len(t) - len(s)
    #try different combination
    else:
        i = 0
        #iterate through differnt length of string
        for x in range(len(s), 1, -1):
            if debug:
                print 'length x=', repr(x)
            #iterate through different starting position
            for y in range(0, len(s), 1):
                mask = []
                searchstring = ''
                #initialize windowing mask
                for e in s:
                    mask.append(0)
                for m in range(0, len(s), 1):
                    mask[(m+y)%len(mask)] = 1
                for m in range (0, len(s), 1):
                    if mask[m]:
                        searchstring+=s[m]
                print mask
                print 'y', y, "string", repr(searchstring)
                if debug:
                    #print 'y', y, "string", repr(s[y:x+y])
                    print 'y', y, "string", repr(searchstring[y:x+y])
                    #newword = s[y]
                for z in range (0, x , 1):
                    if debug:
                        print "x", x, "y", y, 'z', z
                        print 's[y:z+y]:', searchstring[y:z+y], ' s[z+1+y:x+y]:', searchstring[z+1+y:x+y]
                    #newword = s[y] + s[y+1:z]+s[z+1:x-(z+1)]
                    newword = searchstring[y:z+y] + searchstring[z+1+y:x+y]
                    if debug:
                        print repr(newword)
                    if newword not in newsearch:
                        newsearch.append(newword)
    print newsearch
    return result

#For example:

# Delete the 'a'
#print edit_distance('audacity', 'udacity')
#>>> 1

# Delete the 'a', replace the 'u' with 'U'
#print edit_distance('audacity', 'Udacity')
#>>> 2

# Five replacements
print edit_distance('peter', 'sarah')
#>>> 5

# One deletion
#print edit_distance('pete', 'peter')
#>>> 1
