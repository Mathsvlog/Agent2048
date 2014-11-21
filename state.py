from random import random,choice,randint
from array import array

# function used to precompute row transitions
def _getRowTrans(s):
    for i in range(1,4):
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

# precomputation of row transitions
rowTrans = []
for a in range(16):
    x = []
    for b in range(16):
        y = []
        for c in range(16):
            z = []
            for d in range(16):
                s = (a,b,c,d)
                tr = _getRowTrans(list(s))
                if s!=tr:
                    z.append(tr)
                else:
                    z.append(None)
            y.append(tuple(z))
        x.append(tuple(y))
    rowTrans.append(tuple(x))
rowTrans = tuple(rowTrans)

# used by computeTransSuccessors2 and computeTransSuccessors4
def _successors(board, i):
    blanks = getBoardBlanks(board)
    if len(blanks)==0:
        return []
    successors = []
    weight = 1./len(blanks)
    for x in blanks:
        newBoard = board[:]
        newBoard[x] = i
        successors.append(State2048(newBoard))
    return successors

# transition functions for board states
def _transU(board):
    b = board[:]
    isValid = False
    for i in range(4):
        newRow = rowTrans[b[i]][b[i+4]][b[i+8]][b[i+12]]
        if newRow != None:
            isValid = True
            b[i],b[i+4],b[i+8],b[i+12] = newRow
    return b, isValid

def _transD(board):
    b = board[:]
    isValid = False
    for i in range(3,-1,-1):
        newRow = rowTrans[b[i+12]][b[i+8]][b[i+4]][b[i]]
        if newRow != None:
            isValid = True
            b[i+12],b[i+8],b[i+4],b[i] = newRow
    return b, isValid

def _transL(board):
    b = board[:]
    isValid = False
    for i in range(0,13,4):
        newRow = rowTrans[b[i]][b[i+1]][b[i+2]][b[i+3]]
        if newRow != None:
            isValid = True
            b[i],b[i+1],b[i+2],b[i+3] = newRow
    return b, isValid

def _transR(board):
    b = board[:]
    isValid = False
    for i in range(0,13,4):
        newRow = rowTrans[b[i+3]][b[i+2]][b[i+1]][b[i]]
        if newRow != None:
            isValid = True
            b[i+3],b[i+2],b[i+1],b[i] = newRow
    return b, isValid

# return list of (i,j) tuples where board has a blank space
getBoardBlanks = lambda board: [i for i, x in enumerate(board) if x == 0]

# returns all successors with 2 tiles
def computeTransSuccessors2(board):
    return _successors(board, 1)

# returns all successors with 4 tiles
def computeTransSuccessors4(board):
    return _successors(board, 2)

# returns a random initial state with random tiles filled
def initialState():
    board = array("b", [0 for _ in range(16)])
    idx = randint(0,15)
    board[idx] = 1 if random()<0.9 else 2
    idx2 = randint(0,15)
    while idx2==idx:
        idx2 = randint(0,15)
    board[idx2] = 1 if random()<0.9 else 2
    return board

# enum for actions
class Action2048:
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    ACTION_LIST = (UP,RIGHT,DOWN,LEFT)

# represents a single 2048 board state
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
        newBoard, valid = _transU(self.board)
        if valid:
            successors[Action2048.UP] = newBoard
        newBoard, valid = _transD(self.board)
        if valid:
            successors[Action2048.DOWN] = newBoard
        newBoard, valid = _transL(self.board)
        if valid:
            successors[Action2048.LEFT] = newBoard
        newBoard, valid = _transR(self.board)
        if valid:
            successors[Action2048.RIGHT] = newBoard
        self.transitions = successors

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
