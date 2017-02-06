import numpy as np
import numpy.linalg as alg
import time
import math
import control
import ctypes
from ctypes import *
from matplotlib.pylab import *

import Initialisation_CoMax 
import InitPlus


def mainCollabo(positionIn) :
    

    

    EposCmd = ctypes.windll.LoadLibrary("C:/Users/Robot/Desktop/Commande_Collabo_avec_Python/EposCmd.dll")
    
    
    
     
    
    MaxAcceleration = 100000 # (rpm)
    MaxDeceleration = 20000 # (rpm/s)
    MaxVitesse = 6000  #  (rpm)
    MaxErreurDynamique = 3000 #  (qc)
    MaxPosition = 150000 #  (qc)
    MinPosition = 0 #  (qc)
    
    
    def tic():
        #Homemade version of matlab tic and toc functions
        import time
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()
    
    def toc():
        import time
        if 'startTime_for_tictoc' in globals():
            return (time.time() - startTime_for_tictoc)
    
    
    # Localiser l'objet MyEpos et les pointeurs
    MyEpos = Initialisation_CoMax.MyEpos
    pErrorCode_i = Initialisation_CoMax.pErrorCode_i
    pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
    pPositionIs_i = Initialisation_CoMax.pPositionIs_i
    pAnalogValue = Initialisation_CoMax.pAnalogValue
    pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
    pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i
    
   
    # Initialiser la position saisie depuis TestGraphique
    InitPlus.main(positionIn)
    
    
    
    # On impose le mode Velocity Profile Mode
    pMode= ctypes.POINTER(ctypes.c_int)
    pMode_i = ctypes.c_int(0)
    pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
    Mode = c_int(3)
    MyEpos.setOperationMode(Mode, pErrorCode_i)
    MyEpos.getOperationMode(pMode2, pErrorCode_i)
    
    # set enable state
    MyEpos.setEnableState(pErrorCode_i)
    
    # get enabled state
    res = MyEpos.getEnableState(pIsEnabled_i, pErrorCode_i)
    
    # Choix du Gain du capteur de Force
    Gain = 3
    
    
    # Filtre rejecteur
    Te=0.005
    Xi1=0.01
    Xi2=0.7
    freq1=9.5 
    freq2=4
    freqP=5
    Omega1=2*math.pi*freq1
    Omega2=2*math.pi*freq2
    FiltreC1=control.matlab.tf([1/(Omega1*Omega1),2*Xi1/Omega1,1 ],[1/(Omega1*Omega1),2*Xi2/Omega1,1])  
    FiltreC2=control.matlab.tf([1/(Omega2*Omega2),2*Xi1/Omega2,1 ],[1/(Omega2*Omega2),2*Xi2/Omega2,1])  
    FiltreC=FiltreC1*FiltreC2
    FiltreD=control.matlab.c2d(FiltreC,Te,'matched')
    [numF,denF]=control.matlab.tfdata(FiltreD) 
    numF_liste = [numF[0][0][0], numF[0][0][1], numF[0][0][2], numF[0][0][3], numF[0][0][4]]
    denF_liste = [denF[0][0][0], denF[0][0][1], denF[0][0][2], denF[0][0][3], denF[0][0][4]]
    EntreeF= [0]*len(numF_liste)
    SortieF=[0]*len(numF_liste)
    VitConsiFiltre=[]
    freqP=-.4
    tabVitSorti = []
    qc2mm =294
    freqMax = 100
    freqMin = 0.6
    N = 20
    
    
    dureeExp = 20
    
    
    MyEpos.setOperationMode(c_int(1),pErrorCode_i)
    MyEpos.waitForTargetReached(c_long(3000),pErrorCode_i)   
    time.sleep(1)
    MyEpos.setOperationMode(c_int(3),pErrorCode_i)
        
    Temps=[]
    tabVitConsi=[]
    tabForce=[]
    tabPositionSortie=[]

    TabPosition = []
    TabVitesse = []
    TabCourant = []
    
    tic()
    while(toc() < dureeExp):
         t1=toc()
         Temps.append(t1)
         
         MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
         MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
         MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
         TabPosition.append(pPositionIs_i.contents.value/qc2mm)
         TabVitesse.append(pVelocityIs_i.contents.value)
         TabCourant.append(pCurrentIs_i.contents.value)
         
         InputNumber = c_int(1)
         
         MyEpos.getAnalogInput(InputNumber,pAnalogValue,pErrorCode_i)
         MyEpos.getAnalogInput2(InputNumber,pAnalogValue.contents,pErrorCode_i)
         
         tabForce.append(pAnalogValue.contents.value-2499)
         MyEpos.getPositionIs(pPositionIs_i,pErrorCode_i)# mesure de position initiale
         MyEpos.getPositionIs2(pPositionIs_i.contents,pErrorCode_i)
         tabPositionSortie.append(pPositionIs_i.contents.value/qc2mm)
         
         
         # Calcul consigne vitesse (Commande Collaborative)
         VitesseSorti = Gain*((pAnalogValue.contents.value)-2499)
         tabVitSorti.append(VitesseSorti)
         VitesseConsi =  Gain*((pAnalogValue.contents.value)-2499)# à partir de la force appliquée sur la languette, on en déduit la vitesse à laquelle doit se déplacer le bras. On retranchela position d'équilibre de la languette.
         tabVitConsi.append(VitesseConsi)
         EntreeF = [tabVitConsi[-1]] + EntreeF
         del EntreeF[-1]
         SortieF = [np.sum(np.asarray(EntreeF)*np.asarray(numF_liste))-np.sum(np.asarray([0] + SortieF[0:len(SortieF)-1])*np.asarray(denF_liste))] +  SortieF[0:len(SortieF)-1]
         VitConsiFiltre=[VitConsiFiltre, SortieF[0]]   
          
        
         if ((pPositionIs_i.contents.value/qc2mm)>450) and ((pAnalogValue.contents.value)>2499):
            MyEpos.moveWithVelocity(0,pErrorCode_i)
         elif ((pPositionIs_i.contents.value/qc2mm)<50) and ((pAnalogValue.contents.value)<2499):
            MyEpos.moveWithVelocity(0,pErrorCode_i)
         else:
            MyEpos.moveWithVelocity(c_long(math.floor(SortieF[0])),pErrorCode_i)
    
    
    MyEpos.moveWithVelocity(0,pErrorCode_i)

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