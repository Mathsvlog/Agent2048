from agent import *
import optparse, sys
from time import sleep

try:
	from seleniumagent import *
except:
	print("Selenium probably not installed; cannot run SeleniumAgent")
	print("")

# Windows specific code (webagent, boxfinder, util)
import os
if os.name=="nt":
	from webagent import *
	from webboxfinder import *

if __name__ == "__main__":
	o = optparse.OptionParser()
	o.add_option("-m", "--mode", type="str", dest="mode", default="a", help="'a':Agent, 'w':WebAgent, 'b':BoxFinder->WebAgent, 's':SeleniumAgent, default 'a'")
	o.add_option("-d", "--depth", type="int", dest="depth", default=3, help="depth used in expectimax, default 3")
	o.add_option("-r", "--reduce", dest="reduce", default=False, action="store_true", help="only uses 2 tiles in successors")
	o.add_option("-l", "--lastBox", dest="lastBox", default=False, action="store_true", help="uses the box from last use of BoxFinder")
	o.add_option("-s", "--sleep", type="float", dest="delay", default=0, help="seconds SeleniumAgent waits between moves, default 0")
	o.add_option("-f", "--forever", dest="forever", default=False, action="store_true", help="SeleniumAgent will run forever")
	o.add_option("-z", "--staticdepth", dest="staticDepth", default=False, action="store_true", help="Fixes depth so that it is not dynamic")

	(options, _) = o.parse_args()

	if options.depth < 1:
		print("DEPTH MUST BE AT LEAST 1")
		sys.exit()

	if options.mode=="a":
		a = Agent2048(depth=options.depth, reduceSuccessors=options.reduce, staticDepth=options.staticDepth)
		a.playGame(runForever=options.forever)
		

	elif options.mode=="w":
		if options.lastBox:
			from lastBox import l
			box,tilesize = l()
			a = WebAgent2048(box, tilesize, options.depth, options.reduce)
			a.playGame()
		else:
			a = WebAgent2048(depth=options.depth, reduceSuccessors=options.reduce)
			a.playGame()

	elif options.mode=="b":
		box,tilesize = runBoxFinder()
		
		f = open("lastBox.py","w")
		f.write("def l():\n\treturn (%s,%s)"%(str(box),str(tilesize)))
		f.close()

		sleep(0.5)
		a = WebAgent2048(box, tilesize, options.depth, options.reduce)
		a.playGame()

	elif options.mode=="s":
		a = SeleniumAgent2048(delay=options.delay, depth=options.depth, reduceSuccessors=options.reduce, staticDepth=options.staticDepth)
		a.playGame(runForever=options.forever)

	elif options.mode=="f":
		try:
			f = open("output.csv", "r")
			lines = f.readlines()
			f.close()
		except:
			f = open("output.csv", "w")
			lines = []
			f.close()
		i = len(lines)
		while True:
			print i
			a = Agent2048(depth=options.depth, reduceSuccessors=options.reduce, doPrint=False)
			t, t2048, t4096 = a.playGame()
			f = open("output.csv", "a")
			s = ",".join(map(lambda x:str(x),a.state.board))
			s += ",".join(["",str(t),str(t2048),str(t4096)]) + "\n"
			f.write(s)
			f.close()
			i += 1
			print s