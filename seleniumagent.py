from state import *
from cexpectimax import getAction
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep,time
import sys
from depth import getDepth
from os import getcwd

class SeleniumAgent2048:

    def __init__(self, delay=0, depth=3, reduceSuccessors=False):
        self.delay = delay
        self.depth = depth
        self.reduceSuccessors = reduceSuccessors
        self._setupBrowser()
        self.state = State2048(array("b", [0 for _ in range(16)]))
        self.readBoard()
        self.value = ""

    def _setupBrowser(self):
        w = webdriver.Firefox()
        #w.get("https://gabrielecirulli.github.io/2048/")
        #w.get("file:///E:/Desktop/2048/2048web/2048.htm")
        w.get(getcwd()+"\\2048web\\2048.htm")
        w.execute_script("document.styleSheets[0].insertRule('.app-notice{display:none;}', 1);");
        
        self.getTilesScript = """
        var s=[];
        tiles=document.getElementsByClassName('tile-container')[0].childNodes;
        for (var i=0; i<tiles.length; i++){
            s.push(tiles[i].getAttribute('class'));
        }
        return s;
        """

        self.mapVals = {}
        for i in range(1,16):
            self.mapVals[2**i] = i

        self.webdriver = w

    def printState(self):
        print "SCORE: %s"%self.state.getScore()
        print "VALUE: %s"%self.value
        print self.state

    def playGame(self, runForever=False):
        keys2048 = {Action2048.UP:Keys.UP, Action2048.RIGHT:Keys.RIGHT, Action2048.DOWN:Keys.DOWN, Action2048.LEFT:Keys.LEFT}
        body = self.webdriver.find_element_by_tag_name("body")
        doRun = True
        # run forever if option enabled
        while doRun:
            sleep(0.5)
            self.printState()
            t = time()
            t2048 = time()
            hasAchieved2048 = False
            # for each turn
            while len(self.state.getTransitions())>0:
                # if achieved 2048, press continue button
                if not hasAchieved2048 and 11 in self.state.board:
                    print "ACHIEVED 2048 in "+str(time()-t2048)+" s"
                    hasAchieved2048 = True
                    sleep(3)
                    resetButton = self.webdriver.find_element_by_class_name("keep-playing-button")
                    resetButton.click()
                # run expectimax to get acion, value pair
                depth = getDepth(self.depth, self.state.board)
                action,self.value = getAction(self.state.board, depth, self.reduceSuccessors)
                
                # send action key
                body.send_keys(keys2048[action])

                # allow wait time for key to register
                dt = time()-t
                sleep(max(self.delay-dt,0.02))
                t = time()

                # read output
                self.readBoard()
                print "ACTION: "+action
                print "DEPTH: "+str(depth)
                self.printState()
                
            print "GAME OVER"
            if not runForever:
                doRun = False
            else:
                sleep(2)
                self.resetGame()
                self.readBoard()
                print "\nNEW GAME"
        raw_input("ENTER TO CLOSE")
        self.webdriver.close()

    def readBoard(self):
        #boardUpdated = False
        #while not boardUpdated:
        lines = self.webdriver.execute_script(self.getTilesScript)
        tiles = {}
        for line in lines:
            words = line.split(" ")
            tile = tuple(map(lambda i:int(i),words[2][14:].split("-")))
            if tile not in tiles or len(words)==4:
                tiles[tile] = self.mapVals[int(words[1][5:])]# mapValue

        board = array("b", [0 for _ in range(16)])
        for tile in tiles:
            board[tile[1]*4+tile[0]-5] = tiles[tile]

        self.state = State2048(board)
        #newState = State2048(board)
        #if newState.board != self.state.board:
        #    boardUpdated = True
        #    self.state = newState
        #else:
        #    sleep(0.1)
                
    def resetGame(self):
        resetButton = self.webdriver.find_element_by_class_name("restart-button")
        resetButton.click()