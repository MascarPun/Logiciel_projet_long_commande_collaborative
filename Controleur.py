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
import time

#pwet

class Controleur:



    def __init__(self):

        self.parametres = Parametre()
        self.carteEpos = Initialisation_CoMax.self.carteEpos
        self.interface = Ui_MainWindow(self)
        self.interface.controleur = self


    def run(self):
        print("setTiVit")
        self.parametres.setTivit(300)
        self.parametres.getTivit()
        self.parametres.setDureeExp(10)
        mm2qc = 294

        pErrorCode_i = Initialisation_CoMax.pErrorCode_i
        pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
        pPositionIs_i = Initialisation_CoMax.pPositionIs_i
        pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
        pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i

        NominalCurrent = self.parametres.getNominalCurrent()  # Parametre du logiciel Comax
        MaxOutputCurrent = self.parametres.getMaxOutputCurrent()  # Parametre du logiciel Comax
        ThermalTimeConstant = self.parametres.getThermalTimeConstant()  # Parametre du logiciel Comax
        MaxAcceleration = self.parametres.getMaxAcceleration()  # Parametre du logiciel Comax

        self.carteEpos.setDcMotorParameter(NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i)
        self.carteEpos.setMaxAcceleration(MaxAcceleration, pErrorCode_i)


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

    def echelonPosition(self, posFinale):

        Mode = c_int(-1)
        self.carteEpos.setOperationMode(Mode, pErrorCode_i)
        self.parametres.setPosFinale(posFinale)

        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)

        # set enable state
        self.carteEpos.setDisableState(pErrorCode_i)
        self.carteEpos.setEnableState(pErrorCode_i)

        # get enabled state
        res = self.carteEpos.getEnableState(pIsEnabled_i, pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale

        Timeout_i = c_long(5000)
        positionFinaleMm = self.parametres.getPosFinale()


        if (positionFinaleMm > 500 or positionFinaleMm < 0):  # Il faut définir des conditions de sécurité
            print('Cette valeur est interdite')
        else:
            positionFinaleQc = c_long(math.floor(positionFinaleMm * mm2qc))

            self.carteEpos.setPositionMust(positionFinaleQc, pErrorCode_i)  # on initialise la position à l'origine
            # définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
        return("fini")


    def profilEchelonPosition(self):

        Te = 0.001
        # On impose le mode Position Mode

        Mode = c_int(1)

        self.carteEpos.setOperationMode(Mode, pErrorCode_i)

        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(pErrorCode_i)

        # get enabled state
        res = self.carteEpos.getEnableState(pIsEnabled_i, pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale

        Timeout_i = c_long(5000)

        positionInitialeMm = positionConsigne

        # créer les tableaux pour enregistrer les valeurs
        TabPosition = []
        TabVitesse = []
        TabCourant = []
        Temps = []
        t = time.time()
        while (time.time() - t < self.parametres.getDureeExp()):
            if (positionInitialeMm > 500 or positionInitialeMm < 0):  # Il faut définir des conditions de sécurité
                print('Cette valeur est interdite')
            else:
                positionInitialeQc = c_long(math.floor(positionInitialeMm * 294))

                self.carteEpos.moveToPosition(positionInitialeQc, 1, 1, pErrorCode_i)  # on initialise la position à l'origine définie précédemment.
                #  On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
                #            self.carteEpos.waitForTargetReached(Timeout_i, pErrorCode_i)
                print('Bras en déplacement')

            time.sleep(Te)

            Temps.append(time.time()-t)
            self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
            self.carteEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
            self.carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
            TabPosition.append(pPositionIs_i.contents.value / mm2qc)
            TabVitesse.append(float(pVelocityIs_i.contents.value))
            TabCourant.append(float(pCurrentIs_i.contents.value))

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

    def echelonVitesse(self, vitesseConsigne):


        # imposer Mode Velocity
        self.carteEpos.setOperationMode(c_int(-2), pErrorCode_i)

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(pErrorCode_i)
        # get enabled state
        res = self.carteEpos.getEnableState(pIsEnabled_i, pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale

        # durée de l'expérimentation
        Timeout_i = c_long(5000)

        Temps = []
        TabPosition = []
        TabVitesse = []
        TabCourant = []

        # sécurité
        t = time.time()
        while (time.time() - t < self.parametres.getDureeExp()):
            self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
            if ((pPositionIs_i.contents.value / mm2qc) > 490):
                if vitesseConsigne > 0:
                    self.carteEpos.setVelocityMust(c_long(0), pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break
                else:
                    self.carteEpos.setVelocityMust(c_long(vitesseConsigne), pErrorCode_i)

            if ((pPositionIs_i.contents.value / mm2qc) < 10):
                if vitesseConsigne < 0:
                    self.carteEpos.setVelocityMust(c_long(0), pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break
                else:
                    self.carteEpos.setVelocityMust(c_long(vitesseConsigne), pErrorCode_i)

            else:
                self.carteEpos.setVelocityMust(c_long(vitesseConsigne), pErrorCode_i)

            t1 = time.time() - t
            Temps.append(t1)
            self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
            self.carteEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
            self.carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
            TabPosition.append(float(pPositionIs_i.contents.value) / float(mm2qc))
            TabVitesse.append(pVelocityIs_i.contents.value)
            TabCourant.append(pCurrentIs_i.contents.value)

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


c=Controleur()
c.run()
c.launch()