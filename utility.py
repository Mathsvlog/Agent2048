"""
True uses board utility defined in cexpectimax
False uses getRowUtility
"""
useRowUtility = False

"""
Defines the utility for a single row
inner is true for the second or third row
"""
def getRowUtility(a,b,c,d,inner=True):
	row = (a,b,c,d)
	u = 0
	b = 0
	l = -1
	for i in row:
		if i>0:
			if i==l:
				u += 2**(i+1)
			else:
				u += 2**i
			l = i
		elif i==0:
			b += 1
	m = max(row)
	inside = b==m or c==m
	outside = a==m or d==m
	u += b*2**(1+max(row))
	
	if inner:
		if inside and not outside:
			u -= 2**m
	else:
		if inside and not outside:
			u -= 2**(m-1)	

	return u