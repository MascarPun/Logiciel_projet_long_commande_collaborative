import numpy as np
import numpy.linalg as alg
import time
import math
import control
import ctypes
from ctypes import *
from EposData import *
import Initialisation_CoMax 

EposCmd = ctypes.windll.LoadLibrary("C:/Users/Robot/Desktop/Commande_Collabo_avec_Python/EposCmd.dll")

    
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

pErrorCode= ctypes.POINTER(ctypes.c_long)
pErrorCode2 = ctypes.c_long(0)
pErrorCode_i = ctypes.cast(ctypes.addressof(pErrorCode2), pErrorCode)

pIsEnabled= ctypes.POINTER(ctypes.c_bool)
pIsEnabled2 = ctypes.c_bool(0)
pIsEnabled_i = ctypes.cast(ctypes.addressof(pIsEnabled2), pIsEnabled)

pPositionIs= ctypes.POINTER(ctypes.c_long)
pPositionIs2 = ctypes.c_long(0)
pPositionIs_i = ctypes.cast(ctypes.addressof(pPositionIs2), pPositionIs)

pAnalogValue_i= ctypes.POINTER(ctypes.c_int)
pAnalogValue2 = ctypes.c_int(0)
pAnalogValue = ctypes.cast(ctypes.addressof(pAnalogValue2), pAnalogValue_i)

global MyEpos
MyEpos = EposData('EposCmd','Definitions.h',EPOS_i,MAXON_SERIAL_V2_i,USB_i,USB0_i,Baudrate_i,NodeId_i) #classe EposData

def main(positionIn):
    # On impose le mode Position Profile Mode


    Mode = c_int(1)
    MyEpos.setOperationMode(Mode,pErrorCode_i)
    
    pMode= ctypes.POINTER(ctypes.c_int)
    pMode_i = ctypes.c_int(0)
    pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
    MyEpos.getOperationMode(pMode2, pErrorCode_i)
    MyEpos.getOperationMode2(pMode2.contents, pErrorCode_i)
    
    # set enable state
    MyEpos.setEnableState(pErrorCode_i)

    # get enabled state
    res = MyEpos.getEnableState(pIsEnabled_i, pErrorCode_i)

    # Phase de commande du bras pour aller d'une position à une autre
    pPositionIs = c_long(0)
    MyEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/294 # conversion qc en mm

    Timeout_i = c_long(5000)
    # On va définir la position initiale
#    dlg_title = "Initialisation"
#    prompt = {'Position initiale voulue en mm'}
#    answer = inputdlg(prompt,dlg_title,1) # création de la boite de dialogue
#    positionInitialeMm = str2num(answer{1}) # conversion de la chaine de caractère en entier
#    positionInitialeMm = float(input("Position initiale voulue en mm : "))
    positionInitialeMm =  positionIn
    
    
    if (positionInitialeMm > 500 or positionInitialeMm < 0): # Il faut définir des conditions de sécurité
        print('Cette valeur est interdite')
    else:
        positionInitialeQc = c_long(math.floor(positionInitialeMm*294))
    
        MyEpos.moveToPosition(positionInitialeQc,1,1, pErrorCode_i) # on initialise la position à l'origine définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
    
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i) # on fait 2 getpositionis : un avant et un après le waitfortargetreached pour mettre en évidence le caractère instantané de la mesure
        MyEpos.getPositionIs2(pPositionIs_i.contents, pErrorCode_i)
        MyEpos.waitForTargetReached(Timeout_i, pErrorCode_i)
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i) # après
        MyEpos.getPositionIs2(pPositionIs_i.contents, pErrorCode_i)        
        positionInitialeLueMm = pPositionIs.value/294
    
        # On mesure l'écart à la consigne
        erreurPositionInitiale = positionInitialeQc.value - pPositionIs.value


#main()