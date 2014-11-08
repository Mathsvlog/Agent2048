from PIL import ImageGrab, ImageTk
import Tkinter
from random import random
import time

pos1, pos2 = (0,0),(0,0)
def runBoxFinder():
	img = ImageGrab.grab()
	root = Tkinter.Tk()
	tkimage = ImageTk.PhotoImage(img)

	canvas = Tkinter.Canvas(root, width=tkimage.width(), height=tkimage.height())
	canvas.pack()
	canvas.create_image((tkimage.width()/2,tkimage.height()/2),image=tkimage)

	def motion(event):
		x,y = event.x, event.y
		print x,y

	def mouseL(event):
		global pos1,pos2
		x,y = event.x, event.y
		pos1 = (x,y)
		drawGrid()

	def mouseR(event):
		global pos1,pos2
		x,y = event.x, event.y
		pos2 = (x,y)
		drawGrid()

	def mouseM(event):
		root.destroy()

	def drawGrid():
		canvas.create_image((tkimage.width()/2,tkimage.height()/2),image=tkimage)
		x1,y1=pos1
		x2,y2=pos2
		y2 = x2+y1-x1
		dx,dy = x2-x1,y2-y1
		for i in range(4):
			x = x1+int(dx*i/3)
			y = y1+int(dy*i/3)
			canvas.create_line(x, y1, x, y2)
			canvas.create_line(x1, y, x2, y)
		print "self.box = (%i, %i, %i, %i)"%(x1,y1,x2,y2)
		print "self.tileSize = %i"%int(dx/3)
		print "WebAgent2048((%i, %i, %i, %i), %i)"%(x1,y1,x2,y2,int(dx/3))
		print

	root.bind("<Button-1>", mouseL)
	root.bind("<Button-2>", mouseM)
	root.bind("<Button-3>", mouseR)
	root.mainloop()

	x1,y1=pos1
	x2,y2=pos2
	y2 = x2+y1-x1
	dx = x2-x1
	return ((x1,y1,x2,y2),int(dx/3)-1)
