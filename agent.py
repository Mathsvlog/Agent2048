from state import State2048
from random import choice
from expectimax import Expectimax2048

class Agent2048:

	def __init__(self, depth=1, reduceSuccessors=False, doPrint=True):
		self.state = State2048()
		self.expectimax = Expectimax2048(depth, reduceSuccessors)
		self.doPrint = doPrint
		self.printState()

	def playGame(self):
		while len(self.state.getTransitions())>0:
			action = self.expectimax.getAction(self.state)
			self.state = self.state.move(action)
			self.printState()
		if self.doPrint:
			print "GAME OVER"

	def printState(self):
		if self.doPrint:
			print "SCORE: %s"%self.state.getScore()
			print "VALUE: %s"%self.expectimax.utility(self.state)
			print self.state
		