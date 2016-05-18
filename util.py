from config import *

##############################################################################################################################
def isSublist(A, B):
# returns True if A is a sublist of B, False otherwise
    sub = True

    for item in A:
        if item not in B:
            sub = False
            break
    
    return sub
##############################################################################################################################


##############################################################################################################################
def findAllCommonContiguousSublists(A, B, turnToLowerCases=True): # this is a very inefficient implementation, you can use suffix trees to devise a much faster method
# returns all the contiguous sublists in order of decreasing length
# output format (0-indexed):
# [
#    [[indices in 'A' for common sublist 1], [indices in 'B' for common sublist 1]],
#    ...,
#    [[indices in 'A' for common sublist n], [indices in 'B' for common sublist n]]
# ]

    a = []
    b = []
    for item in A:
        a.append(item)
    for item in B:
        b.append(item)

    if turnToLowerCases:
        for i in xrange(len(a)):
            a[i] = a[i].lower()
        for i in xrange(len(b)):
            b[i] = b[i].lower()
            

    commonContiguousSublists = []

    swapped = False
    if len(a) > len(b):
        temp = a
        a = b
        b = temp
        swapped = True

    maxSize = len(a)
    for size in xrange(maxSize, 0, -1):
        startingIndicesForA = [item for item in xrange(0, len(a)-size+1)]
        startingIndicesForB = [item for item in xrange(0, len(b)-size+1)]
        for i in startingIndicesForA:
            for j in startingIndicesForB:
                if a[i:i+size] == b[j:j+size]:
                    # check if a contiguous superset has already been inserted; don't insert this one in that case
                    alreadyInserted = False
                    currentAIndices = [item for item in xrange(i,i+size)]
                    currentBIndices = [item for item in xrange(j,j+size)]
                    for item in commonContiguousSublists:
                        if isSublist(currentAIndices, item[0]) and isSublist(currentBIndices, item[1]):
                            alreadyInserted = True
                            break
                    if not alreadyInserted:
                        commonContiguousSublists.append([currentAIndices, currentBIndices])
    
    
    

    if swapped:
        for item in commonContiguousSublists:
            temp = item[0]
            item[0] = item[1]
            item[1] = temp

                        
    return commonContiguousSublists
##############################################################################################################################



##############################################################################################################################
def findTextualNeighborhood(sentenceDetails, wordIndex, leftSpan, rightSpan):
# return the lemmas in the span [wordIndex-leftSpan, wordIndex+rightSpan] and the positions actually available, left and right

    global punctuations

    sentenceLength = len(sentenceDetails)

    startWordIndex = max(1, wordIndex-leftSpan)
    endWordIndex = min(sentenceLength, wordIndex+rightSpan)

    lemmas = []
    wordIndices = []
    for item in sentenceDetails[startWordIndex-1:wordIndex-1]:
        if item[3] not in stopwords + punctuations:
            lemmas.append(item[3])
            wordIndices.append(item[1])
    for item in sentenceDetails[wordIndex:endWordIndex]:
        if item[3] not in stopwords + punctuations:
            lemmas.append(item[3])
            wordIndices.append(item[1])
    return [wordIndices, lemmas, wordIndex-startWordIndex, endWordIndex-wordIndex]
##############################################################################################################################


##############################################################################################################################
def isAcronym(word, namedEntity):
# returns whether 'word' is an acronym of 'namedEntity', which is a list of the component words
    canonicalWord = word.replace('.', '')
    if not canonicalWord.isupper() or len(canonicalWord) <> len(namedEntity) or canonicalWord.lower() in ['a', 'i']:
        return False

    acronym = True    
    for i in xrange(len(canonicalWord)):
        if canonicalWord[i] <> namedEntity[i][0]:
            acronym = False
            break

    return acronym
##############################################################################################################################

import time
class TicToc():
    """
    This class provide 2 methods to print time during an execution
    """
    def __init__(self, marker="-->", msgSeparator=" | message: ", maxDecimal=2):
        self.startTime = None;
        self.previousTime = None;
        self.marker = marker;
        self.msgSeparator = msgSeparator;
        self.maxDecimal = maxDecimal;
    
    def setMaxDecimal(self, maxDecimal):
        self.maxDecimal = maxDecimal;
    
    def tic(self, msg=None):
        """
        This method start the timer and print it, or print the time between the previous tic()
        and the current tic(). You can print a message by giving it in parameters.
        """
        if msg is None:
            msg = "";
        else:
            msg = self.msgSeparator + msg;
        if self.startTime is None:
            self.startTime = time.time();
            self.previousTime = self.startTime;
            print self.marker + " tictoc starts..." + msg;
            return -1;
        else:
            currentTime = time.time();
            diffTime = currentTime - self.previousTime;
            diffTime = float(float(int(diffTime * (10**self.maxDecimal))) / float((10**self.maxDecimal)));
            print self.marker + " tic time duration from the previous tic(): " + str(diffTime) + " seconds" + msg;
            self.previousTime = currentTime;
            return diffTime;
            
    
    def toc(self, msg=None):
        """
        This method print the elapsed time from the first tic().
        You can print a message by giving it in parameters.
        """
        if self.startTime is not None:
            if msg is None:
                msg = "";
            else:
                msg = self.msgSeparator + msg;
            currentTime = time.time();
            diffTime = currentTime - self.startTime;
            diffTime = float(float(int(diffTime * (10**self.maxDecimal))) / float((10**self.maxDecimal)));
            print self.marker + " toc total duration: " + str(diffTime) + " seconds" + msg;
            return diffTime;
        return -1;
