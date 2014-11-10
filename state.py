from random import random,choice,randint
from array import array
from t import *

def _getRowTrans(s):
    for i in xrange(1,4):
        if s[i]!=0:
            j = i
            while j>0 and s[j-1] in [0,s[i]]:
                j-=1
            if i==j:
                pass
            elif s[i]==s[j]:
                s[i],s[j] = 0, -s[j]-1
            else:
                s[i],s[j] = 0, s[i]
    return tuple(map(lambda i: abs(i), s))

rowTrans = {}
for a in xrange(16):
    for b in xrange(16):
        for c in xrange(16):
            for d in xrange(16):
                s = (a,b,c,d)
                rowTrans[s] = _getRowTrans(list(s))

# return list of (i,j) tuples where board has a blank space
getBoardBlanks = lambda board: [i for i, x in enumerate(board) if x == 0]

def computeTransSuccessors2(board):
    return _successors(board, 1)

def computeTransSuccessors4(board):
    return _successors(board, 2)

def _successors(board, i):
    blanks = getBoardBlanks(board)
    if len(blanks)==0:
        return []
    successors = []
    weight = 1./len(blanks)
    for x in blanks:
        newBoard = board[:]
        newBoard[x] = i
        s = State2048(newBoard)
        successors.append(s)

    return successors

def initialState():
    board = array("b", [0 for _ in range(16)])
    idx = randint(0,15)
    board[idx] = 1 if random()<0.9 else 2
    idx2 = randint(0,15)
    while idx2==idx:
        idx2 = randint(0,15)
    board[idx2] = 1 if random()<0.9 else 2
    return board

class Action2048:
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    ACTION_LIST = [UP,RIGHT,DOWN,LEFT]

class State2048:

    def __init__(self, board):
        self.board = board
        self._computeTransitions()
        self.score = None

    def __repr__(self):
        s = ""
        for i in range(4):
            for j in range(4):
                num = 2**self.board[i*4+j]
                if num==1:
                    num = "-"
                s += str(num)+"\t"
            s += "\n"
        return s

    def _computeScore(self):
        score = 0
        for idx in self.board:
            if idx>1:
                score += (idx-1)*2**idx
        self.score = score

    def _computeTransitions(self):
        successors = {}
        for action in Action2048.ACTION_LIST:
            newBoard, valid = self._computeBoardTransition(action)
            if valid:
                successors[action] = newBoard
        self.transitions = successors

    def _computeBoardTransition(self, action):
        b = self.board[:]
        isValid = False

        if action == Action2048.UP:
            for i in xrange(4):
                b[i],b[i+4],b[i+8],b[i+12] = rowTrans[(b[i],b[i+4],b[i+8],b[i+12])]
            isValid = b!=self.board
            """
            for i in filter(lambda x:b[x] and b[x-4] in [0,b[x]], xrange(4,16)):
                j = i
                while j>3 and b[j-4] in [0,b[i]]:
                    j-=4
                if b[j]==b[i]:
                    isValid = True
                    b[i], b[j] = 0, -b[j]-1
                else:
                    isValid = True
                    b[i], b[j] = 0, b[i]
            """

        elif action == Action2048.DOWN:
            for i in xrange(3,-1,-1):
                b[i+12],b[i+8],b[i+4],b[i] = rowTrans[(b[i+12],b[i+8],b[i+4],b[i])]
            isValid = b!=self.board
            """
            for i in filter(lambda x:b[x] and b[x+4] in [0,b[x]], xrange(11,-1,-1)):
                j = i
                while j<12 and b[j+4] in [0,b[i]]:
                    j+=4
                if b[j]==b[i]:
                    isValid = True
                    b[i], b[j] = 0, -b[j]-1
                else:
                    isValid = True
                    b[i], b[j] = 0, b[i]
            """

        elif action == Action2048.LEFT:
            for i in xrange(0,13,4):
                b[i],b[i+1],b[i+2],b[i+3] = rowTrans[(b[i],b[i+1],b[i+2],b[i+3])]
            isValid = b!=self.board
            """
            for x in xrange(1,4):
                for y in xrange(4):
                    i = x+y*4
                    if b[i] and b[i-1] in [0,b[i]]:
                        j = i
                        while j%4!=0 and b[j-1] in [0,b[i]]:
                            j-=1
                        if b[j]==b[i]:
                            isValid = True
                            b[i], b[j] = 0, -b[j]-1
                        else:
                            isValid = True
                            b[i], b[j] = 0, b[i]
            """
        
        elif action == Action2048.RIGHT:
            for i in xrange(0,13,4):
                b[i+3],b[i+2],b[i+1],b[i] = rowTrans[(b[i+3],b[i+2],b[i+1],b[i])]
            isValid = b!=self.board
            """
            for x in xrange(2,-1,-1):
                for y in xrange(4):
                    i = x+y*4
                    if b[i] and b[i+1] in [0,b[i]]:
                        j = i
                        while j%4!=3 and b[j+1] in [0,b[i]]:
                            j+=1
                        if b[j]==b[i]:
                            isValid = True
                            b[i], b[j] = 0, -b[j]-1
                        else:
                            isValid = True
                            b[i], b[j] = 0, b[i]
            """
        
        for i in xrange(16):
            if b[i]<0:
                b[i]*=-1
        return b, isValid

    def getScore(self):
        if self.score==None:
            self._computeScore()        
        return self.score

    def getTransitions(self):
        return self.transitions

    def move(self, action):
        if action not in self.transitions:
            return None
        newBoard = self.transitions[action][:]
        blanks = getBoardBlanks(newBoard)
        i = choice(blanks)
        newBoard[i] = 1 if random() <= 0.9 else 2
        return State2048(newBoard)
