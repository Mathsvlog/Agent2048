from util import *
from PIL import ImageGrab
import time
import sys
from state import *
from expectimax import *

class WebAgent2048:

    def __init__(self, box=(570, 402, 935, 767), tileSize=121, depth=1, reduceSuccessors=False):
        
        self.box = box
        self.tileSize = tileSize

        #self.getTilePixel = lambda i,j: (startTile[0]+tileSize*j, startTile[1]+tileSize*i)
        self.getTilePixel = lambda i,j: (tileSize*j, tileSize*i)
        self.extractImageState()
        self.expectimax = Expectimax2048(depth,reduceSuccessors)
        self.actionToKey = dict(zip(Action2048.ACTION_LIST, [U,R,D,L]))        
        self.printState()

    def playGame(self):
        time.sleep(1)
        while True:
            action = self.expectimax.getAction(self.state)
            hitKey(self.actionToKey[action])
            time.sleep(0.25)
            self.extractImageState()
            self.printState()

    def printState(self):
        print "SCORE: %s"%self.state.getScore()
        print "VALUE: %s"%self.expectimax.utility(self.state)
        print self.state

    def extractImageState(self):
        img = ImageGrab.grab(self.box)
        bad = 0
        board = []
        for i in range(4):
            row = []
            for j in range(4):
                #color = img.getpixel(self.getTilePixel(i,j))
                color = img.getpixel((self.tileSize*j, self.tileSize*i))
                if color in colors:
                    idx = colors.index(color)
                else:
                    idx, diff = closestColorIdx(color)
                    if diff>0:
                        bad += 1
                row.append(idx)
            board.append(row)
        if bad>8:
            print "GAME OVER DETECTED"
            sys.exit(0)
        self.state = State2048(board)
