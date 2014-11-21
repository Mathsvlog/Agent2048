from state import State2048, initialState
from random import choice
from cexpectimax import getAction
from depth import getDepth

class Agent2048:

    def __init__(self, depth=3, reduceSuccessors=False, doPrint=True):

        self.depth = depth
        self.reduceSuccessors = reduceSuccessors

        self.state = State2048(initialState())
        self.doPrint = doPrint
        self.value = ""
        self.printState()

    def playGame(self):
        while len(self.state.getTransitions())>0:
            depth = getDepth(self.depth, self.state.board)
            action,self.value = getAction(self.state.board, depth, self.reduceSuccessors)
            self.state = self.state.move(action)
            print "ACTION: "+action
            print "DEPTH: "+str(depth)
            self.printState()
        if self.doPrint:
            print "GAME OVER"

    def printState(self):
        if self.doPrint:
            print "SCORE: %s"%self.state.getScore()
            print "VALUE: %s"%self.value
            print self.state
