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
    if debug:
        print "================="
        print "Currently parsing"
        print s, t
        
    #gracefully handle cases where we are reaching the end
    if len(s) == 1 or len(t) == 1:
        if s[0] == t[0]:
            if len(s) == len(t):
                result = 0
            else:
                if len(s) == 1:
                    result = edit_distance(s, t[1:])
                else:
                    result = edit_distance(s[1:], t)
        else:
            if len(s) == len(t):
                result = 1
            else:
                if len(s) == 1:
                    result = edit_distance(s, t[1:])+1
                else:
                    result = edit_distance(s[1:], t)+1
        
    #if len(s) == 1 or len(t) == 1:
    #    result = 1
    #    if debug:
    #        print "One of the string reached near the end"
    #        print len(s),  len(t)
    #    #if business as usual
    #    if s[0] == t[0]:
    #        "print add nothing"
    #       if len(s) == 1:
     #           result = edit_distance(s, t[1:])
    #        elif len(t) == 1:
     #           result = edit_distance(s[1:], t)
     #       else:
    #            result = 0
    #    #Current rsult not the same
    #    else: 
    #        #when one is bigger than the other
     #       if len(s) != len(t):
     #           if len(s) == 1 and len(t) != 1:
     #               print "add 1"
     #               result = edit_distance(s, t[1:]) + 1
      #          elif len(t) == 1 and len(s) !=1:
      #              print "add 1"
      #              result = edit_distance(s[1:], t) + 1
      #          #both = 1
      #          else:
      #              print "add 0"
      #              result = 0
      #          #result = abs(len(s) - len(t))
    #case same so skip
    elif s[0] == t[0]:
        if debug:
            print "s current = t current:", s[0], t[0]
        result = edit_distance(s[1:], t[1:])
    #case for replace
    elif s[1] == t[1]:
        if debug:
            print "s next = t next:", s[1], t[1]
            print "add 1"
        result = edit_distance(s[1:], t[1:]) + 1
    #case for remove
    elif s[1] == t[0]:
        if debug:
            print "s next = t current:", s[1], t[0]
            print "add 1"
        result = edit_distance(s[1:], t) + 1
    #case for insert
    elif s[0] == t[1]:
        if debug:
            print "s current = t next:", s[0], t[1]
            print "add 1"
        result = edit_distance(s, t[1:]) +1
    #when more than one is not the same
    else:
        ####Old code#####
        #if s[1] != '':
        #result1 = edit_distance(s[1:], t[1:]) +1
        #else:
        #    result = 1
        #Jiggle check every case
        if debug:
            print "Nothing's the same recursive call each case"
        if debug:
            print "case s[1:], t[1:]"
        result1 = edit_distance(s[1:], t[1:]) +1
        if debug:
            print "case s[1:], t"
        result2 = edit_distance(s[1:], t) +1
        if debug:
            print "case s, t[1:]"
        result3 = edit_distance(s, t[1:])+1
        if debug:
            print "result1", result1, "result2", result2, "result3", result3
        result = min(result1, result2, result3)
    
    return result
         
#For example:

# Delete the 'a'
#print edit_distance('audacity', 'udacity')
#>>> 1

# Delete the 'a', replace the 'u' with 'U'
#print edit_distance('audacity', 'Udacity')
#>>> 2

# Five replacements
#print edit_distance('peter', 'sarah')
#>>> 5

# One deletion
print edit_distance('pete', 'peter') == 1
print edit_distance('audacity', 'udacity') == 1
print edit_distance('audacity', 'Udacity') ==2
print edit_distance('peter', 'sarah')==5
print edit_distance('pete', 'peter')==1
print edit_distance('udc','audacity')==5
print edit_distance('audacity','udc')==5
print edit_distance('audacity', 'udacious')==4
print edit_distance('python', 'pytohn')==2
print edit_distance('udacity', 'university')==6
print edit_distance('university', 'udacity')==6
