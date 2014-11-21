"""
given a starting depth and board state,
compute a reasonable depth value
"""
def getDepth(depth, board):
    numBlanks = board.count(0)
    if numBlanks <= 3:
        depth += 1
        #if numBlanks <= 2:
            #depth += 1
    return depth

"""
def getDepth(depth, board):
    return depth
"""