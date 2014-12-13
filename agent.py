from state import State2048, initialState
from random import choice
from cexpectimax import getAction
from depth import getDepth
from time import time, sleep

class Agent2048:

    def __init__(self, depth=3, reduceSuccessors=False, doPrint=True, staticDepth=False):

        self.depth = depth
        self.reduceSuccessors = reduceSuccessors
        self.staticDepth = staticDepth

        self.state = State2048(initialState())
        self.doPrint = doPrint
        self.value = ""
        self.printState()

    def playGame(self, runForever=False):
        doRun = True
        while doRun:
            t = time()
            t2048 = None
            t4096 = None
            hasAchieved2048 = False
            hasAchieved4096 = False

            while len(self.state.getTransitions())>0:
                depth = getDepth(self.depth, self.state.board, self.staticDepth)
                action,self.value = getAction(self.state.board, depth, self.reduceSuccessors)
                self.state = self.state.move(action)
                if not hasAchieved2048 and 11 in self.state.board:
                    t2048 = time()-t
                    hasAchieved2048 = True
                elif not hasAchieved4096 and 12 in self.state.board:
                    t4096 = time()-t
                    hasAchieved4096 = True
                if self.doPrint:
                    print("ACTION: "+action)
                    print("DEPTH: "+str(depth))
                    self.printState()
            if self.doPrint:
                print("GAME OVER")
            if not runForever:
                doRun = False
            else:
                self.state = State2048(initialState())
                sleep(1)
        return time()-t, t2048, t4096

    def printState(self):
        if self.doPrint:
            print("SCORE: %s"%self.state.getScore())
            print("VALUE: %s"%self.value)
            print(self.state)
