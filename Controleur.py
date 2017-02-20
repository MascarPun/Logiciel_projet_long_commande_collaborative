import Parametre
import Vue
from EposData import *
import Initialisation_CoMax
import numpy as np
import numpy.linalg as alg
import time
import math
import control
import ctypes
from ctypes import *
from matplotlib.pylab import *



class Controleur:

    def __init__(self):

        self.parametres = Parametre()
        self.carteEpos = Initialisation_CoMax.MyEpos #PAS PROPRE
        self.vue = Vue()
        self.vue.controleur = self
        self.carteEpos.exitEpos(pErrorCode_i)
        self.carteEpos.initEpos(pErrorCode_i)

    def run(self):
        self.parametres.setDureeExp(3)
        qc2mm = 294

        MyEpos = Initialisation_CoMax.MyEpos
        pErrorCode_i = Initialisation_CoMax.pErrorCode_i
        pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
        pPositionIs_i = Initialisation_CoMax.pPositionIs_i
        pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
        pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i
        Mode = c_int(-1)

        NominalCurrent = 5000  # Parametre du logiciel Comax
        MaxOutputCurrent = 7500  # Parametre du logiciel Comax
        ThermalTimeConstant = 70  # Parametre du logiciel Comax
        MaxAcceleration = 10000  # Parametre du logiciel Comax

        MyEpos.setDcMotorParameter(NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i)
        MyEpos.setMaxAcceleration(MaxAcceleration, pErrorCode_i)
        MyEpos.setOperationMode(Mode, pErrorCode_i)

        pMode = ctypes.POINTER(ctypes.c_int)
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
        MyEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / 294  # conversion qc en mm

        Timeout_i = c_long(5000)
        # On va définir la position initiale
        #    dlg_title = "Initialisation"
        #    prompt = {'Position initiale voulue en mm'}
        #    answer = inputdlg(prompt,dlg_title,1) # création de la boite de dialogue
        #    positionInitialeMm = str2num(answer{1}) # conversion de la chaine de caractère en entier
        #    positionInitialeMm = float(input("Position initiale voulue en mm : "))
        positionInitialeMm = positionEchelonConsigne


        if (positionInitialeMm > 500 or positionInitialeMm < 0):  # Il faut définir des conditions de sécurité
            print('Cette valeur est interdite')
        else:
            positionInitialeQc = c_long(math.floor(positionInitialeMm * qc2mm))

            MyEpos.setPositionMust(positionInitialeQc, pErrorCode_i)  # on initialise la position à l'origine
            # définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
        return

    def setMode(self, i):
        self.parametres.setMode(i)

    def setCorPos(self, paraPos):
        self.parametres.setCorPos(paraPos)

    def setCorVit(self, paraVit):
        self.parametres.setCorVit(paraVit)

    def setCorCour(self, paraCour):
        self.parametres.setCorCour(paraCour)

    def setCascade(self, i):
        self.parametres.setCascade(i)

    def setKpos(self, k):
        self.parametres.setKpos(k)

    def setTipos(self, ti):
        self.parametres.setTipos(ti)

    def setTdpos(self, td):
        self.parametres.setTdpos(td)

    def setKvit(self, kv):
        self.parametres.setKvit(kv)

    def setTdvit(self, td):
        self.parametres.setTdvit(td)

    def setTivit(self, ti):
        self.parametres.setTivit(ti)

    def setKcour(self, kc):
        self.parametres.setKcour(kc)

    def setTicour(self, ti):
        self.parametres.setTicour(ti)

    def setTdcour(self, td):
        self.parametres.setTdcour(td)


