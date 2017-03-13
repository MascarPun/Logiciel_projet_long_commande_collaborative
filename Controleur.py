from Parametre import Parametre
from Interface import *
from EposData import *
import numpy as np
import numpy.linalg as alg
import time
import math
import Initialisation_CoMax
import ctypes
from ctypes import *
from matplotlib.pylab import *

#pwet

class Controleur:



    def __init__(self):

        self.parametres = Parametre()
        self.carteEpos = Initialisation_CoMax.MyEpos
        self.interface = Ui_MainWindow(self)
        self.interface.controleur = self


    def run(self):
        print("setTiVit")
        self.parametres.setTivit(300)
        self.parametres.getTivit()
        self.parametres.setDureeExp(3)
        self.parametres.setPosFinale(150)
        qc2mm = 294


        pErrorCode_i = Initialisation_CoMax.pErrorCode_i
        pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
        pPositionIs_i = Initialisation_CoMax.pPositionIs_i
        pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
        pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i
        Mode = c_int(-1)

#        pErrorCode_i = self.carteEpos.pErrorCode_i
#        pIsEnabled_i = self.carteEpos.pIsEnabled_i
#        pPositionIs_i = self.carteEpos.pPositionIs_i
#        pCulocityIrrentIs_i = self.carteEpos.pCurrentIs_i
#        pVes_i = self.carteEpos.pVelocityIs_i
#        Mode = c_int(-1)

        NominalCurrent = self.parametres.getNominalCurrent()  # Parametre du logiciel Comax
        MaxOutputCurrent = self.parametres.getMaxOutputCurrent()  # Parametre du logiciel Comax
        ThermalTimeConstant = self.parametres.getThermalTimeConstant()  # Parametre du logiciel Comax
        MaxAcceleration = self.parametres.getMaxAcceleration()  # Parametre du logiciel Comax

        self.carteEpos.setDcMotorParameter(NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i)
        self.carteEpos.setMaxAcceleration(MaxAcceleration, pErrorCode_i)
        self.carteEpos.setOperationMode(Mode, pErrorCode_i)

        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)
        print('lala')
        # set enable state
        self.carteEpos.setDisableState(pErrorCode_i)
        self.carteEpos.setEnableState(pErrorCode_i)

        # get enabled state
        res = self.carteEpos.getEnableState(pIsEnabled_i, pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / qc2mm  # conversion qc en mm

        Timeout_i = c_long(5000)
        # On va définir la position initiale
        #    dlg_title = "Initialisation"
        #    prompt = {'Position initiale voulue en mm'}
        #    answer = inputdlg(prompt,dlg_title,1) # création de la boite de dialogue
        #    positionInitialeMm = str2num(answer{1}) # conversion de la chaine de caractère en entier
        #    positionInitialeMm = float(input("Position initiale voulue en mm : "))
        positionFinaleMm = self.parametres.getPosFinale()


        if (positionFinaleMm > 500 or positionFinaleMm < 0):  # Il faut définir des conditions de sécurité
            print('Cette valeur est interdite')
        else:
            positionFinaleQc = c_long(math.floor(positionFinaleMm * qc2mm))

            self.carteEpos.setPositionMust(positionFinaleQc, pErrorCode_i)  # on initialise la position à l'origine
            # définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
        return("fini")

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

    def launch(self):
        self.interface.launch(self)

    def test(self):
        print("ca marche")
        self.run()



c=Controleur()
c.run()
c.launch()