# cython: profile=True
from time import time, clock
import utility

# Row of 4 tiles
cdef struct Row:
    char row[4]

# Board of 4 Rows
cdef struct Board:
    Row rows[4]

# UDLR transitions of a Board
cdef struct Transitions:
    Board trans[4]

# stores an action/score pair
cdef struct ActionScore:
    Action action
    int score

# stores all possible successors of a Board (for 2 or 4)
cdef struct Successors:
    Board succ[16]
    int numSuccessors

# ACTIONS
cdef enum Action:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NONE = 4

# compresses Row into a short
cdef unsigned short compressRow(Row r) nogil:
    return r.row[0]<<12 | r.row[1]<<8 | r.row[2]<<4 | r.row[3]

# converts a short into a Row
cdef Row decompressRow(short s) nogil:
    cdef Row r
    r.row[0] = s>>12 & 0xf
    r.row[1] = s>>8 & 0xf
    r.row[2] = s>>4 & 0xf
    r.row[3] = s & 0xf
    return r

# gets transition of a row
cdef short getRowTrans(Row r) nogil:
    cdef char i,j
    for i in range(1,4):
        if r.row[i]!=0:
            j = i
            while j>0 and r.row[j-1] in [0,r.row[i]]:
                j-=1
            if i==j:
                pass
            elif r.row[i]==r.row[j]:
                r.row[i],r.row[j] = 0, -r.row[j]-1
            else:
                r.row[i],r.row[j] = 0, r.row[i]

    for i in range(4):
        if r.row[i]<0:
            r.row[i] *= -1

    return compressRow(r)

# precomputation of row transitions
cdef unsigned short rowTrans[65536]
cdef int rowUtilInner[65536]
cdef int rowUtilOuter[65536]
cdef char a,b,c,d
cdef unsigned short idx,tr
cdef int util
cdef Row r
cdef bint useRowUtility = utility.useRowUtility
for a in range(16):
    r.row[0] = a
    for b in range(16):
        r.row[1] = b
        for c in range(16):
            r.row[2] = c
            for d in range(16):
                r.row[3] = d
                idx = compressRow(r)
                tr = getRowTrans(r)
                if useRowUtility:
                    util = utility.getRowUtility(a,b,c,d,True)
                    rowUtilInner[idx] = util
                    util = utility.getRowUtility(a,b,c,d,True)
                    rowUtilOuter[idx] = util
                if idx!=tr:
                    rowTrans[idx] = tr
                else:
                    rowTrans[idx] = -1

# converts a number into an action
cdef Action charToAction(char a) nogil:
    if a==UP:
        return UP
    if a==DOWN:
        return DOWN
    if a==LEFT:
        return LEFT
    if a==RIGHT:
        return RIGHT
    return NONE

# prints a Row
cdef void printRow(Row r):
    for i in range(4):
        print r.row[i],
    print

# prints a Board
cdef void printBoard(Board b):
    for i in range(4):
        printRow(b.rows[i])
    print

# converts a Board into a transition Board
cdef Board transU(Board b) nogil:
    cdef bint isValid = False
    cdef Row r, newRow
    cdef short rowShort
    cdef char i,j
    for i in range(4):
        for j in range(4):
            r.row[j] = b.rows[j].row[i]
        rowShort = rowTrans[compressRow(r)]
        if rowShort!=-1:
            isValid = True
            newRow = decompressRow(rowShort)
            for j in range(4):
                b.rows[j].row[i] = newRow.row[j]
    if not isValid:
        b.rows[0].row[0] = -1
    return b

cdef Board transD(Board b) nogil:
    cdef bint isValid = False
    cdef Row r, newRow
    cdef short rowShort
    cdef char i,j
    for i in range(4):
        for j in range(4):
            r.row[j] = b.rows[3-j].row[i]
        rowShort = rowTrans[compressRow(r)]
        if rowShort!=-1:
            isValid = True
            newRow = decompressRow(rowShort)
            for j in range(4):
                b.rows[j].row[i] = newRow.row[3-j]
    if not isValid:
        b.rows[0].row[0] = -1
    return b

cdef Board transL(Board b) nogil:
    cdef bint isValid = False
    cdef Row r, newRow
    cdef short rowShort
    cdef char i,j
    for i in range(4):
        for j in range(4):
            r.row[j] = b.rows[i].row[j]
        rowShort = rowTrans[compressRow(r)]
        if rowShort!=-1:
            isValid = True
            newRow = decompressRow(rowShort)
            for j in range(4):
                b.rows[i].row[j] = newRow.row[j]
    if not isValid:
        b.rows[0].row[0] = -1
    return b

cdef Board transR(Board b) nogil:
    cdef bint isValid = False
    cdef Row r, newRow
    cdef short rowShort
    cdef char i,j
    for i in range(4):
        for j in range(4):
            r.row[j] = b.rows[i].row[3-j]
        rowShort = rowTrans[compressRow(r)]
        if rowShort!=-1:
            isValid = True
            newRow = decompressRow(rowShort)
            for j in range(4):
                b.rows[i].row[3-j] = newRow.row[j]
    if not isValid:
        b.rows[0].row[0] = -1
    return b

# creates a Transitions from a Board
cdef Transitions getTransitions(Board b) nogil:
    cdef Transitions trans
    trans.trans[0] = transU(b)
    trans.trans[1] = transD(b)
    trans.trans[2] = transL(b)
    trans.trans[3] = transR(b)
    return trans

# counts the valid Boards in a Transitions
cdef char countTransitions(Transitions t) nogil:
    cdef char num = 0
    cdef char i
    for i in range(4):
        if t.trans[i].rows[0].row[0] >= 0:
            num+=1
    return num

# computes the utility of a board
cdef int getUtility(Board b) nogil:
    cdef int score = 0
    cdef unsigned short idx
    cdef char i,j
    cdef Row r
    if useRowUtility:
        for i in range(4):
            idx = compressRow(b.rows[i])
            score += rowUtilInner[idx]
        
        for i in range(4):
            for j in range(4):
                r.row[i] = b.rows[j].row[i]
            idx = compressRow(r)
            score += rowUtilInner[idx]
        
        return score

    # board utility
    cdef int blanks = 1
    for i in range(4):
        for j in range(4):
            idx = b.rows[i].row[j] 
            if idx==0:
                blanks += 1
            else:
                score += idx**2
    cdef int filled = 16-blanks
    return score / filled**2 * blanks**2
    

# returns count of the number of 0 tiles on a board
cdef char getNumBlanks(Board b) nogil:
    cdef char num = 0
    for i in range(4):
        for j in range(4):
            if b.rows[i].row[j]==0:
                num += 1
    return num

cdef void copyBoard(Board *bd, Board *bs) nogil:
    #memcpy(bd, bs, sizeof(Board))
    for i in range(4):
        for j in range(4):
            bd.rows[i].row[j] = bs.rows[i].row[j]
       
# generates all possible successors of a Board with 2 or 4
cdef Successors getSuccessors(Board b, bint two) nogil:
    cdef char numBlanks = getNumBlanks(b)
    cdef Successors successors
    cdef char curr = 0
    cdef char newTile = 2
    if two:
        newTile = 1

    successors.numSuccessors = numBlanks
    for i in range(4):
        for j in range(4):
            if b.rows[i].row[j]==0:
                copyBoard(&successors.succ[curr], &b)
                successors.succ[curr].rows[i].row[j] = newTile
                curr += 1

    return successors

# runs expectimax, returns the best action/score pair
cdef ActionScore expectimax(Board b, char d, bint reduceSuccessors) nogil:
    cdef Transitions trans = getTransitions(b)
    cdef char numTransitions = countTransitions(trans)
    cdef ActionScore actScore

    # losing state
    if numTransitions==0:
        actScore.score = 0
        actScore.action = NONE
        return actScore

    # depth reached
    elif d==0:
        actScore.score = getUtility(b)
        actScore.action = NONE
        return actScore

    # compute best action/score
    cdef ActionScore bestActionScore
    bestActionScore.action = NONE
    bestActionScore.score = -1
    cdef Successors successors
    cdef int act
    cdef char i
    for i in range(4):
        if trans.trans[i].rows[0].row[0] >= 0:
            totalScore = 0.
            successors = getSuccessors(trans.trans[i], True)
            percent = (1.0 if reduceSuccessors else 0.9)/successors.numSuccessors
            for j in range(successors.numSuccessors):
                actScore = expectimax(successors.succ[j], d-1, reduceSuccessors)
                totalScore += actScore.score*percent

            if not reduceSuccessors:
                successors = getSuccessors(trans.trans[i], False)
                percent = 0.1/successors.numSuccessors
                for j in range(successors.numSuccessors):
                    actScore = expectimax(successors.succ[j], d-1, reduceSuccessors)
                    totalScore += actScore.score*percent

            if totalScore > bestActionScore.score:
                bestActionScore.score = int(totalScore)
                bestActionScore.action = charToAction(i)
    return bestActionScore


actionDict = {UP:"U",DOWN:"D",LEFT:"L",RIGHT:"R"}
def getAction(b,d,r=False):
    cdef Board board
    for i in range(4):
        for j in range(4):
            board.rows[i].row[j] = b[i*4+j]
    #printBoard(board)
    #t = time()
    actScore = expectimax(board,d,r)
    return actionDict[actScore.action], actScore.score
