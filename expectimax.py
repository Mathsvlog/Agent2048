from state import *

class Expectimax2048:

	def __init__(self, dVal, reduceSuccessors):
		self.dVal = dVal
		self.successorFunc = computeTransSuccessorsTwo if reduceSuccessors else computeTransSuccessors

	def utility(self, state):
		score = 0.
		for row in state.board:
			for i in row:
				if i>0:
					score += 2**i
		#score = state.getScore()
		numBlank = len(getBoardBlanks(state.board))+1
		numFilled = 16-numBlank
		return score / numFilled**2 * (numBlank)**2

	def getFailScore(self):
		return 0

	def getAction(self, state):
		"""
		numBlank = len(getBoardBlanks(state.board))
		self.calls=0
		self.dVal = 2 if numBlank>4 else 3
		if numBlank in [0,1,2,5,6]:
			self.successorFunc = computeTransSuccessors
		else:
			self.successorFunc = computeTransSuccessorsTwo
		"""

		def expectimax(state, d=self.dVal):
			#self.calls += 1

			# losing state
			if len(state.getTransitions())==0:
				return self.getFailScore()

			# depth reached
			elif d==0:
				return self.utility(state)

			bestAction, bestScore = -float("inf"), None
			trans = state.getTransitions()
			for action in trans:
				successors = self.successorFunc(trans[action])
				score = 0
				for newState in successors:
					score += successors[newState]*expectimax(newState, d-1)
				if bestScore < score:
					bestAction, bestScore = action, score

			return bestAction if d==self.dVal else bestScore

		return expectimax(state)
		"""
		action = expectimax(state)
		
		print numBlank, (4*numBlank)**2, (4*numBlank)**3
		print "CALLS: "+str(self.calls)
		return action
		"""