"""
True: always invokes reduceSuccessors after depth 1
False: only invokes reduceSuccessors if -r or --reduce option is used
"""
reduceAfterFirstDepth = True

"""
given a starting depth and board state,
compute a reasonable depth value
"""
def getDepth(depth, board, staticDepth=False):
    if not staticDepth:
        numBlanks = board.count(0)
        if numBlanks <= 6:
            depth += 1
            if numBlanks <= 3:
                depth += 1
                if numBlanks==0:
                    depth += 1
    return depth
