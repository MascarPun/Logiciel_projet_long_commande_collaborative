import numpy as np
import numpy.linalg as alg
import math
import control
import ctypes
from ctypes import *
from matplotlib.pylab import *

def echelon_position(dureeExp,Te,posFinale,MyEpos):

    qc2mm=294

    def tic():
        # Homemade version of matlab tic and toc functions
        import time
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()

    def toc():
        import time
        if 'startTime_for_tictoc' in globals():
            return (time.time() - startTime_for_tictoc)

    qc2mm = 294

    # imposer Mode Courant
    MyEpos.setOperationMode(c_int(-3), pErrorCode_i)

    # initialiser le pointeur pMode
    pMode = ctypes.POINTER(ctypes.c_int)
    pMode_i = ctypes.c_int(0)
    pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

    # récupérer le Mode acutuel
    MyEpos.getOperationMode(pMode2, pErrorCode_i)
    MyEpos.getOperationMode2(pMode2.contents, pErrorCode_i)

    # set enable state
    MyEpos.setEnableState(pErrorCode_i)

    # Phase de commande du bras pour aller d'une position à une autre
    pPositionIs = c_long(0)
    MyEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
    positionDepartLueMm = pPositionIs.value / qc2mm  # conversion qc en mm

    Temps = []
    TabPosition = []
    TabVitesse = []
    TabCourant = []
    consigne=[]

    debut=time.time()
    while (debut-time.time() < dureeExp):
        t=time.time()
        while(time.time()-t<Te):
        #groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
        if ((pPositionIs_i.contents.value / qc2mm) > 490):
            MyEpos.setOperationMode(c_int(3), pErrorCode_i)
            MyEpos.moveWithVelocity(c_long(0), pErrorCode_i)
            MyEpos.setOperationMode(c_int(-3), pErrorCode_i)
            print("Le bras ne peut pas monter car il va taper la butée !!!")
            break

        if ((pPositionIs_i.contents.value / qc2mm) < 10):
            MyEpos.setOperationMode(c_int(3), pErrorCode_i)
            MyEpos.moveWithVelocity(c_long(0), pErrorCode_i)
            MyEpos.setOperationMode(c_int(-3), pErrorCode_i)
            print("Le bras ne peut pas descendre car il va taper la butée !!!")
            break


        else:
            MyEpos.setCurrentMust(c_short(courantConsigne), pErrorCode_i)

        Temps.append(time.time()-debut)
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
        MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
        MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
        TabPosition.append(pPositionIs_i.contents.value / qc2mm)
        TabVitesse.append(pVelocityIs_i.contents.value)
        TabCourant.append(pCurrentIs_i.contents.value)

