import ctypes
import time

GetCursorPos = ctypes.windll.user32.GetCursorPos
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

L = 0x25
U = 0x26
R = 0x27
D = 0x28

colors = [(205,192,180),# blank
#(205,193,180),# blank
(238,228,218),# 2
(237,224,200),# 4
(242,177,121),# 8
(245,149,99),# 16
(246,124,95),# 32
(246,94,59),# 64
(237,207,114),# 128
(237,204,97),# 256
(237,200,80),# 512
(237,197,63),# 1024
(237,194,46)# 2048
]

dist = lambda c1,c2:abs(c1[0]-c2[0])+abs(c1[1]-c2[1])+abs(c1[2]-c2[2])
def closestColorIdx(c2):
    distances = map(lambda c:dist(c,c2), colors)
    idx = distances.index(min(distances))
    return (idx, distances[idx])

#startTile = (577,406)
#tileSize = 121

# EMULATE KEY PRESS
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def hitKey(key, holdTime=.01):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( key, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    #time.sleep(holdTime)
    #ii_.ki = KeyBdInput( key, 0x48, 0, 0, ctypes.pointer(extra) )
    #SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# GET MOUSE POSITION
class GetPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def getCurrMousePos():
    pt = GetPoint()
    GetCursorPos(ctypes.byref(pt))
    return (int(pt.x), int(pt.y))
