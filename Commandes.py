
######ATTENTION IMPORTER SYS POUR QUE CELA FONCTIONNE############


import numpy as np
import numpy.linalg as alg
import math
import ctypes
from ctypes import *
from matplotlib.pylab import *
import interface
import sys

def echelon_position(dureeExp,Te,posFinale,MyEpos,interface):
    #initialisation des constantes
    ValMaxCourEpos=5 #on s'arrange pour ne pas depasser 5A en courant dans tous les cas
    qc2mm = 294

    #on verifie que la bonne correction est activee
    if groupebuttoncor(interface) == 2:  # si correction en vitesse
        print("erreur il faut une commande en vitesse pour faire une correction en vitesse")
        sys.exit() #voir si cela ne va pas faire tomber le bras

    if groupebuttoncor(interface) == 3:  # si correction en courant
        print("erreur il faut une commande en vitesse pour faire une correction en vitesse")
        sys.exit()


    def tic():
        # Homemade version of matlab tic and toc functions
        import time
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()

    def toc():
        import time
        if 'startTime_for_tictoc' in globals():
            return (time.time() - startTime_for_tictoc)


    #Recuperation des paramètres des correcteurs
    Kpos= getKpos(interface)
    Tipos=getTipos(interface)
    Tdpos=getTdpos(interface)
    Satpos=1 #en attente de l'interface
    ValParDefautSatPos=1
    optionSatPos=False
    Kvit=getKvit(interface)
    Tivit=getTivit(interface)
    Tdvit=getTdvit(interface)
    Satvit=1 #en attente de l'interface
    ValParDefautSatVit=1
    optionSatVit=False
    Kcour=getKcour(interface)
    Ticour=getTicour(interface)
    Tdcour=getTdcour(interface)
    Satcour=1 #en attente de l'interface
    ValParDefautSatCour=1
    optionSatCour=False

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

    #initialisaton des tableaux pour les représentations graphiques
    Temps = []
    TabPosition = []
    TabVitesse = []
    TabCourant = []

    #initialisation de la consigne et des erreurs (il faut remplir les tableaux d'erreurs avec deux elements (si on a un pid)
    consignePos=[]
    consigneVit=[]
    consigneCour=[]
    courantCorrige=[]

    errPos=[0,0]
    errVit=[0,0]
    errCour=[0,0]
    sommeErrPos=0
    sommeErrVit=0
    sommeErrCour=0
    nombreEch=dureeExp//Te
    compt=0

    debut=time.time()
    while (time.time()-debut < dureeExp and compt<=nombreEch-1): #a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
        t=time.time()
        #On verfie que le mouvement est possible
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
            while(time.time()-t<Te):
                pass
                #groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
                #Pour l'instant il fait rien mais on peut lui ajouter une action à réaliser pour pas avoir de temps où il ne fait rien

            #On calcule ce que la commande renvoie comme courant
            consignePos.append(posFinale)

            if groupebuttoncor(interface)==1:#si correction en position

                if optionSatPos:
                    consigneCour.append(pos2current_sat(Kpos, Tipos, Tdpos,Satpos,ValParDefautSatPos, consignePos[-1], pPositionIs_i.contents.value / qc2mm, errPos, sommeErrPos))
                    if consigneCour[-1]>ValMaxCourEpos:
                        consigneCour[-1]=5
                    MyEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)
                else:
                    consigneCour.append(pos2current(Kpos, Tipos, Tdpos, consignePos[-1], pPositionIs_i.contents.value / qc2mm, errPos, sommeErrPos))
                    if consigneCour[-1]>ValMaxCourEpos:
                        consigneCour[-1]=5
                    MyEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)



            elif groupebuttoncor(interface) ==4:#si correction en cascade

                if optionSatPos:
                    consigneVit.append(pos2velocity_sat(Kpos, Tipos, Tdpos,Satpos,ValParDefautSatPos, consignePos[-1], pPositionIs_i.contents.value / qc2mm, errPos, sommeErrPos))
                else:
                    consigneVit.append(pos2velocity(Kpos, Tipos, Tdpos, consignePos[-1], pPositionIs_i.contents.value / qc2mm, errPos, sommeErrPos))

                MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                if optionSatVit:
                    consigneCour.append(velocity2current_sat(Kvit, Tivit, Tdvit, Satvit, ValParDefautSatVit, consigneVit[-1],pVelocityIs_i.contents.value, errVit, sommeErrVit))
                else:
                    consigneCour.append(velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1], pVelocityIs_i.contents.value, errVit,sommeErrVit))

                MyEpos.getCurrentIs(pCurrentIs_i,pErrorCode_i)
                if optionSatCour:
                    courantCorrige.append(courant_cmd_sat(Kcour, Ticour, Tdcour, Satcour, ValParDefautSatCour, consigneCour[-1],pCurrentIs_i.contents.value, errCour, sommeErrCour))
                    if courantCorrige[-1]>ValMaxCourEpos:
                        courantCorrige[-1]=5
                    MyEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)
                else:
                    courantCorrige.append(courant_cmd(Kcour, Ticour, Tdcour, consigneCour[-1], pCurrentIs_i.contents.value, errCour,sommeErrCour))
                    if courantCorrige[-1]>ValMaxCourEpos:
                        courantCorrige[-1]=5
                    MyEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)
            compt+=1


        Temps.append(time.time()-debut)
        MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
        MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
        MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
        TabPosition.append(pPositionIs_i.contents.value / qc2mm)
        TabVitesse.append(pVelocityIs_i.contents.value)
        TabCourant.append(pCurrentIs_i.contents.value)

