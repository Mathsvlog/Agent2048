from webutil import *
from PIL import ImageGrab
from time import sleep
import sys
from state import *
from cexpectimax import getAction
from depth import getDepth

class WebAgent2048:

    def __init__(self, box=(570, 402, 935, 767), tileSize=121, depth=3, reduceSuccessors=False):
        
        self.box = box
        self.tileSize = tileSize

        self.getTilePixel = lambda i,j: (tileSize*j, tileSize*i)
        self.extractImageState()
        self.actionToKey = dict(zip(Action2048.ACTION_LIST, [U,R,D,L]))        
        self.value = ""
        self.printState()
        self.depth = depth
        self.reduceSuccessors = reduceSuccessors

    def playGame(self):
        sleep(1)
        while True:
            depth = getDepth(self.depth, self.state.board)
            action,self.value = getAction(self.state.board, depth, self.reduceSuccessors)
            hitKey(self.actionToKey[action])
            sleep(0.25)
            self.extractImageState()
            print "ACTION: "+action
            print "DEPTH: "+str(depth)
            self.printState()

    def printState(self):
        print "SCORE: %s"%self.state.getScore()
        print "VALUE: %s"%self.value
        print self.state

    def extractImageState(self):
        img = ImageGrab.grab(self.box)
        bad = 0
        board = array("b", [0 for _ in range(16)])
        for i in range(4):
            row = []
            for j in range(4):
                color = img.getpixel((self.tileSize*j, self.tileSize*i))
                if color in colors:
                    idx = colors.index(color)
                else:
                    idx, diff = closestColorIdx(color)
                    if diff>0:
                        bad += 1
                board[i*4+j] = idx
        if bad>8:
            print "GAME OVER DETECTED"
            sys.exit(0)
        self.state = State2048(board)
