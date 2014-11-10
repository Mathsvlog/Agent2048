from random import random,choice,randint

class Action2048:
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    ACTION_LIST = [UP,RIGHT,DOWN,LEFT]

# converts board to a tuple of tuples
computeBoardTuple = lambda board: tuple(map(lambda row:tuple(row),board))

# converts board to a list of lists
computeBoardList = lambda board: map(lambda row:list(row),board)

# return list of (i,j) tuples where board has a blank space
def getBoardBlanks(board):
    blanks = []
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                blanks.append((i,j))
    return blanks

# assuming board is a transition from State2048, returns dictionary of possible states
# where a random 2 or 4 has been added, value is chance of that board happening
def computeTransSuccessors(board):
    blanks = getBoardBlanks(board)
    successors = {}
    twoWeight, fourWeight = 0.9/len(blanks), 0.1/len(blanks)
    for i,j in blanks:
        newBoard = computeBoardList(board)
        newBoard[i][j] = 1
        successors[State2048(computeBoardTuple(newBoard))] = twoWeight
        newBoard[i][j] = 2
        successors[State2048(computeBoardTuple(newBoard))] = fourWeight
    return successors

def computeTransSuccessorsTwo(board):
    blanks = getBoardBlanks(board)
    successors = {}
    weight = 1./len(blanks)
    for i,j in blanks:
        newBoard = computeBoardList(board)
        newBoard[i][j] = 1
        successors[State2048(computeBoardTuple(newBoard))] = weight
    return successors




class State2048:

    def __init__(self, board=None):
        
        # create initial state if not specified
        if board==None:
            board = [[0 for _ in range(4)] for _ in range(4)]
            idx = randint(0,15)
            board[idx/4][idx%4] = 1 if random()<0.9 else 2
            idx2 = randint(0,15)
            while idx2==idx:
                idx2 = randint(0,15)
            board[idx2/4][idx2%4] = 1 if random()<0.9 else 2

        self.board = computeBoardTuple(board)
        self.transitions = self._computeTransitions()
        self.score = self._computeScore()

    def __repr__(self):
        s = ""
        for i in range(4):
            for j in range(4):
                num = 2**self.board[i][j]
                if num==1:
                    num = "-"
                s += str(num)+"\t"
            s += "\n"
        return s

    def _computeScore(self):
        score = 0
        for i in range(4):
            for j in range(4):
                idx = self.board[i][j]
                if idx>1:
                    score += (idx-1)*2**idx
        return score

    def _computeTransitions(self):
        successors = {}
        for action in Action2048.ACTION_LIST:
            newBoard, valid = self._computeBoardTransition(action)
            if valid:
                successors[action] = computeBoardTuple(newBoard)
        return successors

    def _computeBoardTransition(self, action):
        newBoard = computeBoardList(self.board) #[row[:] for row in self.board]
        xyMap = lambda i,j,k:(k,j) if action in [Action2048.UP,Action2048.DOWN] else (i,k)
        isValid = False

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
                if newBoard[i][j]!=0:

                    # detect if space needs to move/merge
                    merge = False
                    for k in kMap(i,j):
                        x,y = xyMap(i,j,k)
                        if newBoard[x][y] != 0:
                            merge = newBoard[i][j]==newBoard[x][y]
                            if not merge:
                                k += 1 if action in [Action2048.UP,Action2048.LEFT] else -1
                                x,y = xyMap(i,j,k)
                            break

                    # move and merge
                    if merge:
                        # make negative so it wont be merged again in this transition
                        newBoard[x][y] = -(newBoard[i][j]+1)
                        newBoard[i][j] = 0
                        isValid = True

                    # move, don't merge
                    elif i != x  or j!=y:
                        newBoard[x][y] = newBoard[i][j]
                        newBoard[i][j] = 0
                        isValid = True

        # make all items positive
        newBoard = map(lambda row:[abs(i) for i in row], newBoard)
        return newBoard, isValid

    def getScore(self):
        return self.score

    def getTransitions(self):
        return self.transitions

    def move(self, action):
        if action not in self.transitions:
            return None
        newBoard = computeBoardList(self.transitions[action])
        blanks = getBoardBlanks(newBoard)
        i,j = choice(blanks)
        newBoard[i][j] = 1 if random() <= 0.9 else 2
        return State2048(newBoard)

"""
#s = State2048([[0,1,1,0],[0,0,1,0],[2,1,1,5],[0,0,1,0]])
s = State2048([[3,5,3,1],[6,7,2,4],[2,5,4,1],[1,1,3,2]])
print s
actionMap = {"w":Action2048.UP,"a":Action2048.LEFT,"s":Action2048.DOWN,"d":Action2048.RIGHT}
action = actionMap[raw_input()]

while s.move(action):
    print s
    action = actionMap[raw_input()]
print s
"""