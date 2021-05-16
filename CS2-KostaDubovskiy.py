# 2
# import all libraries
import math

# open input file -- change dir accordingly.
with open('/Users/kosta/Desktop/Sigma/Sigma 2021/input.txt', 'r') as inputF:
    lines = inputF.readlines()
    a = (lines[0])[:-1]
    b = (lines[1])


def nCr(n, r):
    """Combinatorics 'choose' function
    n, r --->  number of ways to pick r items from n items given order does not matter"""
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def numLenSeq(string):
    """
    returns number of all possible sequences that are:
        the same length as string, start at digit s, end at digit e
    use Choose combinatorics formula and it's applications with building up and rightwards paths on a grid
    to calculate number of such paths starting from digit s and ending at digit e of same length as string
    see solution 2 for a possibly better explanation:
        https://brilliant.org/wiki/rectangular-grid-walk-no-restriction/
    Each step up on the grid indicates increasing the next digit by one, each step right keeps the next digit the same
    as the one before it.
    """
    s = int(string[0])
    e = int(string[-1])
    # if we were given random inputs then we would have to watch out for the start and end points being too far
    # apart, thus making a contiguous sequence impossible, but since we're guaranteed a sequence that is contiguous,
    # we don't need to worry.
    try:
        numSeq = nCr(len(string) - 1, e - s)
        return numSeq
    except:
        return 'This is not a working or possible sequence. Please try again.'


def numAllSeq(length):
    """
    Returns num of all possible contiguous seq of same **length** as string
    Utilize previous function, iterate through all possible startDigit - endDigit pairs and pass in a string starting with
    startDigit and ending with endDigit of proper length, what's in between does not matter
    Be careful around what the endDigit can be!
    """
    num = 0
    for startDigit in range(10):  # for every starting digit 0-9
        if startDigit + length < 11:
            # if the starting digit is far away from 9 that no matter how quickly it increases it can't surpass the digit '9'
            # then go through all possible end digits(they will be between the start digit and the end of the most rapidly increasing sequence)
            # and add to the number of sequences the number of sequences that start and end with these digits and are of the fixed length
            # utilizes numLenSeq function from above
            for endDigit in range(startDigit, startDigit + length):
                increment = numLenSeq(str(startDigit) * (length - 1) + str(endDigit))
                num += increment
        else:
            # if the start digit is too high and there is a risk of going over the digit '9'
            #   i.e start digit is 9 and we have 2 digits in our sequence, we can't blindly walk up our sequences grid
            # then do the same as in the if statement above but the range of the end digit is from start digit to 9
            for endDigit in range(startDigit, 10):
                increment = numLenSeq(str(startDigit) * (length - 1) + str(endDigit))
                num += increment

    return num


def consecutiveSubString(string):
    """
    gives all substring of the given sequence(but only in consecutive chunks, thus preserving the desired contiguity)
    """
    res = [string[i: j] for i in range(len(string))
           for j in range(i + 1, len(string) + 1)]
    res.remove(string)  # remove the full 'substring' that's not really a substring
    return res


def supSeqFinder(string):
    """
    Use a dict:
        key is length of a sequence, value is set of longest corresponding sequences found in the raw string
            note: at first this set will only have the sequences found by going through once, we will go through the set again to
            add all sub sequences
    """
    allSeq = {  # our dict, described above
        1: set()  # len seq: set of seqs of key length
    }

    i = 0
    while i < len(string) - 1:  # i is the index we're on in the string
        if 0 <= int(string[i + 1]) - int(string[i]) <= 1:  # when next digit is +1 or +0(diff always int, so <= works here):
            currSeq = string[i]  # currSeq initialized as the digit we're on

            while 0 <= int(string[i + 1]) - int(string[i]) <= 1 and i < len(string) - 1:  # i can't be >= the len of the string, it'll be beyond the end of it
                i += 1  # index goes up one
                currSeq += string[i]  # add the string of the curr digit to our growing curr Seq
                if i == len(string) - 1:
                    # if we reach the end, to avoid the while statement checking-
                    # - if an invalid index in the string is equal to currSeq[0], we break the loop
                    break

            i += 1

            if len(currSeq) in allSeq:
                # not this --> if len(allSeq[str(len(currSeq))]) < numLenSeq(currSeq): # if the corresponding set to our seqs length isn't already complete
                # because seqs of 6 may start from diff spots
                allSeq[len(currSeq)] = allSeq[len(currSeq)].union({currSeq})

            else:  # if no seqs of such length exist yet, add our current one
                allSeq[len(currSeq)] = {currSeq}

        else:
            # if single digit, add to set
            if len(allSeq[len(string[i])]) < 10:
                allSeq[len(string[i])] = allSeq[len(string[i])].union({string[i]})
            i += 1

    allSeqSortedByKey = {k: allSeq[k] for k in sorted(allSeq)}  # sort by key value, will be useful in next step

    return allSeqSortedByKey


def subSeqFinder(string):
    """
    Get the set of 'super'sequences(the ones in the set generated by the previous function that omits subsequences)
    To get all subsequences added, union all subsequences of each string to the corresponding key/set
    This way we have all subsequences in the set too
    Next, we can just go down the highest common keys until we get a common element in the next function
    """
    allSupSeq = supSeqFinder(string)
    allSubSeq = allSupSeq.copy()

    for seqLength in allSupSeq:
        # for each key value(super sequence lengths)
        for string in allSupSeq[seqLength]:
            # then for each super sequence in this key set
            subStrings = consecutiveSubString(string)
            # create a list of all substrings of the super sequence using our handy function
            for subString in subStrings:
                # if the key of the new subsequence is already in our main set, union it in
                # otherwise initialize the key-value(set) pair with the substring as it's first element
                if len(subString) in allSubSeq:
                    allSubSeq[len(subString)] = allSubSeq[len(subString)].union({subString})
                else:
                    allSubSeq[len(subString)] = {subString}

    return allSubSeq


# create our all-sequence sets from the input file strings
subSeqA = subSeqFinder(a)
subSeqB = subSeqFinder(b)

# get the set of the intersection of these sets' keys
keyInter = subSeqA.keys() & subSeqB.keys()

inter = ''  # initialize intersection

for commKey in sorted(keyInter, reverse=True):
    # for each key intersection(go downwards in order of keys, to get the highest keys first)
    if len(subSeqA[commKey] & subSeqB[commKey]) > 0:
        # if the intersection of the corresponding sets of our input strings(the sets that contain sequence length-set of subsequences pairs)
        # is not empty, we have found our intersection, set 'inter' to that intersection and break.
        inter = subSeqA[commKey] & subSeqB[commKey]
        break


# Testing:
# print(a)
# print(b)
# print(subSeqA)
# print(subSeqB)
# print(inter)

with open('/Users/kosta/Desktop/Sigma/Sigma 2021/output.txt', 'w+') as outputF:
    outputF.write(str(max(inter)))
    # notice the max here, that is to make sure we write only one longest sequence(there could be multiple)
    # which one it is is not all that important
    # in fact it would not be so wrong to assume there should only be one, that seems implied by the problem
    # so this should hopefully not omit any solutions in theory

outputF.close()
inputF.close()
