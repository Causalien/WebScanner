################################################################################
#Multi-word Queries

#Triple Gold Star

#For this question, your goal is to modify the search engine to be able to
#handle multi-word queries.  To do this, we need to make two main changes:

#    1. Modify the index to keep track of not only the URL, but the position
#    within that page where a word appears.

#    2. Make a version of the lookup procedure that takes a list of target
#    words, and only counts a URL as a match if it contains all of the target
#    words, adjacent to each other, in the order they are given in the input.

#For example, if the search input is "Monty Python", it should match a page that
#contains, "Monty Python is funny!", but should not match a page containing
#"Monty likes the Python programming language."  The words must appear in the
#same order, and the next word must start right after the end of the previous
#word.

#Modify the search engine code to support multi-word queries. Your modified code
#should define these two procedures:

#    crawl_web(seed) => index, graph
#        A modified version of crawl_web that produces an index that includes
#        positional information.  It is up to you to figure out how to represent
#        positions in your index and you can do this any way you want.  Whatever
#        index you produce is the one we will pass into your multi_lookup(index,
#        keyword) procedure.

#    multi_lookup(index, list of keywords) => list of URLs
#        A URL should be included in the output list, only if it contains all of
#        the keywords in the input list, next to each other.


def multi_lookup(index, query):
    debuglookup = False
    debugsequence = False  
    result = []
    lookupresult = {}
    compare = []
    dictionary = {}
    sequence = []
    together = True
    #special case for one query to strip the keyword position from index
    if debuglookup:
        print "======================="
        print "Begin lookup"
        print "======================="
    if len(query) == 1:
        #print query[0]
        temp = lookup(index,query[0])
        if temp:
            for e in temp:
                if debuglookup:
                    print "appending", e
                result.append(e[0])
        else:
            result = []
        return result
    #normal operation for multikeyword lookup
    else:
        #use the first keyword as reference and dig through each url
        for e in query:
            #lookup the keyword and its corresponding info
            test = lookup(index, e)
            #Add to lookup result if result is not empty
            if test:
                if debuglookup:
                    print ""
                    print "======================="
                    print "Found keyword '"+e+"' at:"
                    print test
                    print "======================="
                temp = lookup(index, e)
                #create dictionary based on keyword
                #case for not already exist in result
                if e not in lookupresult:
                    #Go through each URL and add as dictionary
                    tempdict = {}
                    for x in temp:
                        #cases for url exists or not
                        if x[0] not in tempdict:
                            tempdict[x[0]] = list()
                            tempdict[x[0]].append(x[1])
                        else:
                            tempdict[x[0]].append(x[1])
                    lookupresult[e] = tempdict
                    if debuglookup:
                        print "New result added:"
                        print tempdict
                        print "======================="
                #case for already exist
                else:
                    #Go through each element in found result and see 
                    #if url already exists, if not, add new url
                    #go through found result
                    tempdict = {}
                    for x in temp:
                        #then go through the result storage
                        if x[0] not in tempdict:
                            tempdict[x[0]] = list()
                            tempdict[x[0]].append(x[1])
                        else:
                            tempdict[x[0]].append(x[1])
                    lookupresult[e] = tempdict
                    if debuglookup:
                        print "Existing result added:"
                        print tempdict
                        print "======================="
            #Case for when the result is empty
            else:
                lookupresult[e] = {}
            if debuglookup:
                print "Result now look like:"
                print lookupresult
                print "======================="
    if debuglookup:
        print ""
        print "======================="
        print "End lookup"
        print "======================="
        print ""

    if debugsequence:
        print "======================="
        print "Begin test for sequential appearance"
        print "======================="
    #Go throught the query string sequentially
    if debugsequence:
        print "Going through these url:"
        print lookupresult[query[0]]
        print "======================="
    #Do the sequence test only for the urls that exist in the first wrod
    #Test for empty strings
    isempty = False
    for e in query:
        if not lookupresult[e]:
            isempty = True
    if debugsequence:
        print "isempty", isempty
    if not isempty:
        for e in lookupresult[query[0]]:
            if debugsequence:
                print "Checking url:"
                print e
                print "======================="
            for k in lookupresult[query[0]][e]:
                if debugsequence:
                    print "Checking position:", k, "for '"+query[0]+"'"
                    print "======================="
                #Test for existence in the url sequentially from the query
                issequence = True
                for j in range(1, len(query),1):
                    if e in lookupresult[query[j]]:
                        if debugsequence:
                            print "Next word '"+query[j]+"':"
                            #go through each position of the first word
                            print "comparing if k+j ", (k+j), " exists in keyword:", query[j], lookupresult[query[j]][e]
                        if (k + j) not in lookupresult[query[j]][e]:
                            if debugsequence:
                                print "Not sequential"
                            issequence = False
                    else:
                        if debugsequence:
                            print "query empty"
                        issequence = False
                if issequence:
                    result.append(e)
                    if debugsequence:
                        print "======================="
                        print "valid url", e
                        print "======================="
    else:
        result = []
    if debugsequence:
        print "======================="
        print "End test for sequential appearance"
        print "Result is:"
        print result
        print "======================="        
    return result

def qsort(L):
    if len(L) <= 1: return L
    return qsort( [ lt for lt in L[1:] if lt < L[0] ] )  +  [ L[0] ]  +  qsort( [ ge for ge in L[1:] if ge >= L[0] ] )
        
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    i = 0
    for word in words:        
        add_to_index(index, word, url, i)
        i+=1
def add_to_index(index, keyword, url, position):
    if keyword in index:
        #index[keyword].append(url)
        index[keyword].append([url, position])
    else:
        #index[keyword] = [url]
        index[keyword] = [[url, position]]
        
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
    



cache = {
   'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""", 
   'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""", 
   'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None
    





#Here are a few examples from the test site:

index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')

#print multi_lookup(index, ['Python'])
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

#print multi_lookup(index, ['Monty', 'Python'])
#>>> ['http://www.udacity.com/cs101x/final/a.html']

#print multi_lookup(index, ['Python', 'programming', 'language'])
#>>> ['http://www.udacity.com/cs101x/final/b.html']

#print multi_lookup(index, ['Thomas', 'Jefferson'])
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

#print multi_lookup(index, ['most', 'powerful', 'weapon'])
#>>> ['http://www.udacity.com/cs101x/final/a.html']

