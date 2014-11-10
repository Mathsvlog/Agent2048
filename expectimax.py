from state import *
from time import time
from t import t

def _getRowUtility(s):
    u = 0
    for i in s:
		if i>0:
			u += 2**i
    return u

rowUtility = {}
for a in xrange(16):
    for b in xrange(16):
        for c in xrange(16):
            for d in xrange(16):
                s = (a,b,c,d)
                rowUtility[s] = _getRowUtility(list(s))
                #rowUtility[a|b<<4|c<<8|d<<16] = _getRowUtility(list(s))

class Expectimax2048:

	def __init__(self, dVal, reduceSuccessors):
		self.dVal = dVal
		self.reduceSuccessors = reduceSuccessors
		#self.successorFunc = computeTransSuccessorsTwo if reduceSuccessors else computeTransSuccessors

	def utility(self, state):
		u = 0
		for i in xrange(4):
			u += rowUtility[(state.board[i],state.board[i+4],state.board[i+8],state.board[i+12])]
		return u
		"""
		score = 100.
		for i in state.board:
			if i>0:
				score += 2**i
		score = state.getScore()
		numBlank = len(getBoardBlanks(state.board))+1
		numFilled = 16-numBlank
		return score / numFilled**2 * (numBlank)**2
		"""

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
				u = self.utility(state)
				return u
				#return self.utility(state)

			bestAction, bestScore = -float("inf"), None
			trans = state.getTransitions()
			for action in trans:
				score = 0
				successors = computeTransSuccessors2(trans[action])
				percent = (1.0 if self.reduceSuccessors else 0.9)/len(successors)
				for newState in successors:
					score += percent*expectimax(newState, d-1)

				if not self.reduceSuccessors:
					successors = computeTransSuccessors4(trans[action])
					percent = 0.1/len(successors)
					for newState in successors:
						score += percent*expectimax(newState, d-1)

				if bestScore < score:
					bestAction, bestScore = action, score

			return bestAction if d==self.dVal else bestScore

		#self.calls=0
		#action = expectimax(state)
		#print "CALLS: "+str(self.calls)
		#return action
		return expectimax(state)
		