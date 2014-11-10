from state import State2048
from agent import Agent2048
from t import *

#s = State2048([[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,0]])
s = State2048([0,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0])
print s

for d in range(1,5):
	a = Agent2048(d,True, False)
	a.state = s
	td = time()
	print "D: "+str(d)
	print "ACTION: "+a.expectimax.getAction(a.state)
	for i in range(len(ti)):
			print "T%i: %f"%(i,ti[i])
	print "TIME: "+str(time()-td)
	print
