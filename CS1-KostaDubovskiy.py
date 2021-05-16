# 1
inputF = open('/Users/kosta/Desktop/Sigma/Sigma 2021/input.txt', 'r')  # replace directory with the correct local one of course
outputF = open('/Users/kosta/Desktop/Sigma/Sigma 2021/output.txt', 'w')  # replace directory with the correct local one of course
lines = inputF.readlines()
a = (lines[0])[:-2]
b = (lines[1])


def seqFinder(string):
    """
    This function will return a dictionary, allSeq, given a string of only digits.
    The dictionary will have key value pairs of:
    each key is a string of a diff digit
    the value of that key is the length of the longest contiguous homogeneous subpart consisting of the digit in the key
    we will find these values by iterating through the inputed string, and whenever two consecutive digits are equal,
    we initialize a temporary sequence 'currSeq', then since we don't yet know the length of this currSeq,
    we'll use a while loop to wait until the next digit is not equal to the one we're on.
    Once the currSeq ends, we'll check if the length of it is longer than the current value this digit holds in our
    allSeq dictionary, if it is, we reassign the value to be this length, if not, we move on.
    """
    allSeq = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0
    }
    i = 0
    while i < len(string) - 1:  # i is the index we're on in the string
        if string[i] == string[i - 1]:  # when two consec digits are equal:
            currSeq = string[i]  # currSeq initialized as the digit we're on

            while string[i] == currSeq[0] and i < len(string):  # i can't be >= the len of the string, it'll be beyond the end of it
                currSeq += string[i]  # add the string of the curr digit to our growing curr Seq
                i += 1  # index goes up one
                if i == len(string):
                    # if we reach the end, to avoid the while statement checking-
                    # - if an invalid index in the string is equal to currSeq[0], we break the loop
                    break

            if allSeq[currSeq[0]] < len(currSeq):  # if curr len is longer than value, reassign
                allSeq[currSeq[0]] = len(currSeq)
        else:
            if allSeq[string[i]] == 0:  # if curr value is 0, make it one even though the seq is 1, sequences of 1 still count (imagine comparing '1' to '1')
                allSeq[string[i]] = 1
            i += 1
    
    return allSeq


def commonSeqFinder(stringA, stringB):
    """
    Takes in 2 strings
    Uses previous function to get the dicts of each strings appropriate seqs(sequences)
    Will use a dict 'commons', which has same key-value idea except now it's the common seqs
    we find the values by just going through each key and checking if seqA dict has a shorter seq for that digit or
    seqB dict does, reassign it the shorter value, since that's common to both
    finally, using a lambda function and sorted, create 'orderedCommons' list of tuple pairs in order by their values.
    Then return the key(string digit which is first elem in first tuple) times the value(second elem first tuple).
    """
    seqA = seqFinder(stringA)
    seqB = seqFinder(stringB)
    commons = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0
    }

    for i in '0123456789':  # the iteration to check which value is less
        if seqA[i] > seqB[i]:
            commons[i] = seqB[i]
        else:
            commons[i] = seqA[i]

    orderedCommons = sorted(commons.items(), reverse=True, key=lambda x: x[1])  # the sorting

    return orderedCommons[0][1] * orderedCommons[0][0]  # the longest seq reconstruction


outputF.write(commonSeqFinder(a, b))  # write our longest common sequence to the doc & close
outputF.close()
inputF.close()
