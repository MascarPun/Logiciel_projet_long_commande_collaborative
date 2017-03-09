import numpy as np
import numpy.linalg as alg
import time
import math
import ctypes
from ctypes import *

#EposCmd = ctypes.windll.LoadLibrary("C:/Users/Robot/Desktop/Commande_Collabo_avec_Python/EposCmd.dll")
from EposData import *


# définition de l'objet MyEpos de la classe EposData regroupant :


Mode = c_int(1)
    
EPOS_i = c_char_p(b'EPOS2')
EPOS = byref(EPOS_i)


MAXON_SERIAL_V2_i = c_char_p(b'MAXON SERIAL V2')
MAXON_SERIAL_V2 = byref(MAXON_SERIAL_V2_i)

USB_i = c_char_p(b'USB')
USB = byref(USB_i)

USB0_i = c_char_p(b'USB0')
USB0 = byref(USB0_i)

Baudrate_i = c_long(100000)


NodeId_i = c_int(1)

global pErrorCode_i
pErrorCode= ctypes.POINTER(ctypes.c_long)
pErrorCode2 = ctypes.c_long(0)
pErrorCode_i = ctypes.cast(ctypes.addressof(pErrorCode2), pErrorCode)

global pIsEnabled_i
pIsEnabled= ctypes.POINTER(ctypes.c_bool)
pIsEnabled2 = ctypes.c_bool(0)
pIsEnabled_i = ctypes.cast(ctypes.addressof(pIsEnabled2), pIsEnabled)

global pPositionIs_i
pPositionIs= ctypes.POINTER(ctypes.c_long)
pPositionIs2 = ctypes.c_long(0)
pPositionIs_i = ctypes.cast(ctypes.addressof(pPositionIs2), pPositionIs)

global pAnalogValue
pAnalogValue_i= ctypes.POINTER(ctypes.c_int)
pAnalogValue2 = ctypes.c_int(0)
pAnalogValue = ctypes.cast(ctypes.addressof(pAnalogValue2), pAnalogValue_i)

global pVelocityIs_i
pVelocityIs= ctypes.POINTER(ctypes.c_long)
pVelocityIs2 = ctypes.c_long(0)
pVelocityIs_i = ctypes.cast(ctypes.addressof(pVelocityIs2), pVelocityIs)

global pCurrentIs_i
pCurrentIs= ctypes.POINTER(ctypes.c_short)
pCurrentIs2 = ctypes.c_short(0)
pCurrentIs_i = ctypes.cast(ctypes.addressof(pCurrentIs2), pCurrentIs)

global MyEpos
MyEpos = EposData('EposCmd','Definitions.h',EPOS_i,MAXON_SERIAL_V2_i,USB_i,USB0_i,Baudrate_i,NodeId_i) #classe EposData


MyEpos.exitEpos(pErrorCode_i)

MyEpos.initEpos(pErrorCode_i)


