from random import random,choice,randint
from t import *

class Action2048:
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    ACTION_LIST = [UP,RIGHT,DOWN,LEFT]

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

class State2048:

    def __init__(self, board=None):
        # create initial state if not specified
        if board==None:
            board = [0 for _ in range(16)]
            idx = randint(0,15)
            board[idx] = 1 if random()<0.9 else 2
            idx2 = randint(0,15)
            while idx2==idx:
                idx2 = randint(0,15)
            board[idx2] = 1 if random()<0.9 else 2

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
        asdf = []
        for action in Action2048.ACTION_LIST:
            t()
            newBoard, valid = self._computeBoardTransition(action)
            t(0)
            if valid:
                successors[action] = newBoard
        self.transitions = successors

    def _computeBoardTransition(self, action):
        b = self.board[:]
        isValid = False

        if action == Action2048.UP:
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

        elif action == Action2048.DOWN:
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

        elif action == Action2048.LEFT:
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
        
        elif action == Action2048.RIGHT:
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
        
        return map(lambda i:abs(i),b), isValid
        """
        newBoard = self.board[:]
        isValid = False
        xyMap = lambda i,j,k:(k,j) if action in [Action2048.UP,Action2048.DOWN] else (i,k)

        # determine what to iterate over based on direction
        if action==Action2048.UP:
            iRange, jRange, kMap = range(1,4), range(0,4), lambda i,j:range(i-1,-1,-1)
        elif action==Action2048.DOWN:
            iRange, jRange, kMap = range(2,-1,-1), range(0,4), lambda i,j:range(i+1,4)
        elif action==Action2048.LEFT:
            iRange, jRange, kMap = range(0,4), range(1,4), lambda i,j:range(j-1,-1,-1)
        elif action==Action2048.RIGHT:
            iRange, jRange, kMap = range(0,4), range(2,-1,-1), lambda i,j:range(j+1,4)
        
        for i in iRange:
            for j in jRange:
                ij = i*4+j
                if newBoard[ij]!=0:

                    # detect if space needs to move/merge
                    merge = False
                    for k in kMap(i,j):
                        x,y = xyMap(i,j,k)
                        xy = x*4+y
                        if newBoard[xy] != 0:
                            merge = newBoard[ij]==newBoard[xy]
                            if not merge:
                                k += 1 if action in [Action2048.UP,Action2048.LEFT] else -1
                                x,y = xyMap(i,j,k)
                            break

                    # move and merge
                    if merge:
                        # make negative so it wont be merged again in this transition
                        newBoard[xy] = -(newBoard[ij]+1)
                        newBoard[ij] = 0
                        isValid = True

                    # move, don't merge
                    elif i != x  or j!=y:
                        newBoard[xy] = newBoard[ij]
                        newBoard[ij] = 0
                        isValid = True

        # make all items positive
        #newBoard = map(lambda row:[abs(i) for i in row], newBoard)
        newBoard = map(lambda i:abs(i), newBoard)
        return newBoard, isValid
        """


    def getScore(self):
        if self.score==None:
            self._computeScore()        
        return self.score

    def getTransitions(self):
        #if self.transitions==None:
        #    self._computeTransitions()
        return self.transitions

    def move(self, action):
        if action not in self.transitions:
            return None
        newBoard = list(self.transitions[action])
        blanks = getBoardBlanks(newBoard)
        try:
            i = choice(blanks)
        except:
            print blanks
            print newBoard
            print action
            exit()
        newBoard[i] = 1 if random() <= 0.9 else 2
        return State2048(newBoard)
