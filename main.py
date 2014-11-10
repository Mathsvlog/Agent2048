from agent import *
import optparse, sys
from time import sleep

# Windows specific code (webagent, boxfinder, util)
if os.name=="nt":
	from webagent import *
	from boxFinder import *

if __name__ == "__main__":
	o = optparse.OptionParser()
	o.add_option("-m", "--mode", type="str", dest="mode", default="a", help="'a':Agent, 'w':WebAgent, 'b':BoxFinder->WebAgent")
	o.add_option("-d", "--depth", type="int", dest="depth", default=2, help="depth used in expectimax")
	o.add_option("-r", "--reduce", dest="reduce", default=False, action="store_true", help="only uses 2 tiles in successors")
	o.add_option("-l", "--lastBox", dest="lastBox", default=False, action="store_true", help="uses the box from last use of BoxFinder")
	(options, _) = o.parse_args()

	if options.depth < 1:
		print "DEPTH MUST BE AT LEAST 1"
		sys.exit()

	if options.mode=="a":
		a = Agent2048(depth=options.depth, reduceSuccessors=options.reduce)
		a.playGame()

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