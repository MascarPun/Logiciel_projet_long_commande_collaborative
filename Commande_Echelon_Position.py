import numpy as np
import numpy.linalg as alg
import time
import math
import control
import ctypes
from ctypes import *
from EposData import *
import Initialisation_CoMax 
from matplotlib.pylab import *


def mainEchelonPosition(positionEchelonConsigne):
    # On impose le mode Position Mode

    def tic():
        #Homemade version of matlab tic and toc functions
        import time
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()

    def toc():
        import time
        if 'startTime_for_tictoc' in globals():
            return (time.time() - startTime_for_tictoc)
            
    dureeExp = 3
    qc2mm = 294
    
   
    MyEpos = Initialisation_CoMax.MyEpos
    pErrorCode_i = Initialisation_CoMax.pErrorCode_i
    pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
    pPositionIs_i = Initialisation_CoMax.pPositionIs_i
    pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
    pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i
    Mode = c_int(-1)
    
    NominalCurrent = 5000 #Parametre du logiciel Comax
    MaxOutputCurrent =7500 #Parametre du logiciel Comax
    ThermalTimeConstant =70  #Parametre du logiciel Comax
    MaxAcceleration = 10000 #Parametre du logiciel Comax
    
    MyEpos.setDcMotorParameter(NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i)
    MyEpos.setMaxAcceleration(MaxAcceleration, pErrorCode_i)
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
    positionInitialeMm =  positionEchelonConsigne
    
    TabPosition = []
    TabVitesse = []
    TabCourant = []
    Temps = []    
    
    if (positionInitialeMm > 500 or positionInitialeMm < 0): # Il faut définir des conditions de sécurité
        print('Cette valeur est interdite')
    else:
        positionInitialeQc = c_long(math.floor(positionInitialeMm*294))
    
        MyEpos.setPositionMust(positionInitialeQc, pErrorCode_i) # on initialise la position à l'origine
        # définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
    
       
       
        
        tic()
        while (toc() < dureeExp):
            t1=toc()
            Temps.append(t1)
            MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
            MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
            MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
            TabPosition.append(pPositionIs_i.contents.value/qc2mm)
            TabVitesse.append(pVelocityIs_i.contents.value)
            TabCourant.append(pCurrentIs_i.contents.value)
       
    positionInitialeLueMm = pPositionIs.value/294
    
        # On mesure l'écart à la consigne
    erreurPositionInitiale = positionInitialeQc.value - pPositionIs.value

    plot(Temps, TabPosition, 'green')
    grid(True)
    title('Position instantanée du bras')
    ylabel('Position (mm)')
    xlabel('Temps (s)')
    show()

    plot(Temps, TabVitesse, 'red')
    grid(True)
    title('Vitesse instantanée du bras')
    ylabel('Vitesse (rpm)')
    xlabel('Temps (s)')
    show()
    
    plot(Temps, TabCourant, 'blue')
    grid(True)
    title('Courant instantané du bras')
    ylabel('Courant (mA)')
    xlabel('Temps (s)')
    show()