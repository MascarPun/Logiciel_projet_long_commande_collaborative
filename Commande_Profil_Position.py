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
import matplotlib.pyplot as plt

#
def mainProfilPosition(positionConsigne):
    
    def tic():
        #Homemade version of matlab tic and toc functions
        import time
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()
    
    def toc():
        import time
        if 'startTime_for_tictoc' in globals():
            return (time.time() - startTime_for_tictoc)
        
       
    #    hl, = plt.plot([], [])
    #    def update_line(hl, new_data_x, new_data_y):
    #        hl.set_xdata(np.append(hl.get_xdata(), new_data_x))
    #        hl.set_ydata(np.append(hl.get_ydata(), new_data_y))
    #        plt.draw()
    #        show()
       
       
    dureeExp = 5
    qc2mm = 294
    Te = 0.001
       # On impose le mode Position Mode
    
    MyEpos = Initialisation_CoMax.MyEpos
    pErrorCode_i = Initialisation_CoMax.pErrorCode_i
    pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
    pPositionIs_i = Initialisation_CoMax.pPositionIs_i
    pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
    pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i
    
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
    positionInitialeMm =  positionConsigne
    
    
    #créer les tableaux pour enregistrer les valeurs
    TabPosition = []
    TabVitesse = []
    TabCourant = []
    Temps = []
    
    tic()
    while (toc() < dureeExp):
        if (positionInitialeMm > 500 or positionInitialeMm < 0): # Il faut définir des conditions de sécurité
            print('Cette valeur est interdite')
        else:
            positionInitialeQc = c_long(math.floor(positionInitialeMm*294))
        
            MyEpos.moveToPosition(positionInitialeQc,1,1, pErrorCode_i) # on initialise la position à l'origine définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
#            MyEpos.waitForTargetReached(Timeout_i, pErrorCode_i)  
            print('Bras en déplacement')
                    
      
        t1=toc()
        while ((toc()-t1)<Te):
            t2=(toc()-t1)
        Temps.append(t1)
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
        MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
        MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
        TabPosition.append(pPositionIs_i.contents.value/qc2mm)
        TabVitesse.append(float(pVelocityIs_i.contents.value))
        TabCourant.append(float(pCurrentIs_i.contents.value))
            
    #            update_line(hl, Temps, TabPosition)
            
       
      
    positionInitialeLueMm = pPositionIs.value/294
    
    # On mesure l'écart à la consigne
    erreurPositionInitiale = positionInitialeQc.value - pPositionIs.value
      
    
    
    
    
    
    
    
    
    
    
    plot(Temps, TabPosition,'green')
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
    
    
