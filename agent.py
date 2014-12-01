from state import State2048, initialState
from random import choice
from cexpectimax import getAction
from depth import getDepth
from time import time

class Agent2048:

    def __init__(self, depth=3, reduceSuccessors=False, doPrint=True):

        self.depth = depth
        self.reduceSuccessors = reduceSuccessors

        self.state = State2048(initialState())
        self.doPrint = doPrint
        self.value = ""
        self.printState()

    def playGame(self):
        t = time()
        t2048 = None
        hasAchieved2048 = False

        while len(self.state.getTransitions())>0:
            depth = getDepth(self.depth, self.state.board)
            action,self.value = getAction(self.state.board, depth, self.reduceSuccessors)
            self.state = self.state.move(action)
            if not hasAchieved2048 and 11 in self.state.board:
                t2048 = time()-t
                hasAchieved2048 = True
            if self.doPrint:
                print("ACTION: "+action)
                print("DEPTH: "+str(depth))
                self.printState()
        if self.doPrint:
            print("GAME OVER")
        return time()-t, t2048

    def printState(self):
        if self.doPrint:
            print("SCORE: %s"%self.state.getScore())
            print("VALUE: %s"%self.value)
            print(self.state)
