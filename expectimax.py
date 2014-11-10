from state import *
from time import time
from t import t

# function used to precompute row utility
def _getRowUtility(s):
    u = 0
    for i in s:
		if i>0:
			u += 2**i
    return u

# precomputation of row utilities
rowUtility = []
for a in xrange(16):
    x = []
    for b in xrange(16):
        y = []
        for c in xrange(16):
            z = []
            for d in xrange(16):
                s = (a,b,c,d)
                z.append(_getRowUtility(list(s)))
            y.append(tuple(z))
        x.append(tuple(y))
    rowUtility.append(tuple(x))
rowUtility = tuple(rowUtility)

class Expectimax2048:

	def __init__(self, dVal, reduceSuccessors):
		self.dVal = dVal
		self.reduceSuccessors = reduceSuccessors

	def utility(self, state):
		# uses precomputed row utilities
		score = 0
		for i in xrange(4):
			score += rowUtility[state.board[i]][state.board[i+4]][state.board[i+8]][state.board[i+12]]
		#return score
		numBlank = len(getBoardBlanks(state.board))+1
		numFilled = 16-numBlank
		return score / numFilled**2 * (numBlank)**2

	def getFailScore(self):
		return 0

	def getAction(self, state):
		"""
		# dynamic depth
		numBlank = len(getBoardBlanks(state.board))
		self.dVal = 2 if numBlank>4 else 3
		"""

		def expectimax(state, d=self.dVal):
			"""
			# increment calls
			self.calls += 1
			"""

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

		"""
		# keep track of calls
		self.calls=0
		action = expectimax(state)
		print "CALLS: "+str(self.calls)
		return action
		"""
		return expectimax(state)
		