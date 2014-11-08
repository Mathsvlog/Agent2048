from state import *
from random import choice
from expectimax import *

class Agent2048:

	def __init__(self, depth=1, reduceSuccessors=False):
		self.state = State2048()
		self.expectimax = Expectimax2048(depth, reduceSuccessors)
		self.printState()

	def playGame(self):
		while len(self.state.getTransitions())>0:
			action = self.expectimax.getAction(self.state)
			self.state = self.state.move(action)
			self.printState()
		print "GAME OVER"

	def printState(self):
		print "SCORE: %s"%self.state.getScore()
		print "VALUE: %s"%self.expectimax.utility(self.state)
		print self.state
		