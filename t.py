from time import time

if "ti" not in globals():
	ti = [0,0,0,0,0,0]
	t0 = time()
	
def t(i=None):
	global t0, ti
	if i!=None:
		ti[i] += time()-t0
	t0 = time()