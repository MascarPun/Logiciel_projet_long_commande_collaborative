from Parametre import Parametre
from interface import *
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
import Correcteurs
from Commandes import *


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

            if ((pPositionIs_i.contents.value / mm2q) < 10):
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

    def rampePosition(self, coef_dir, posFinale, dureeExp):
        Mode = c_int(-3)
        self.carteEpos.setOperationMode(Mode, pErrorCode_i)
        self.parametres.setRampe(coef_dir)

        if posFinale > 490 or posFinale < 10:
            return ('Cette valeur est interdite')
        else:
            self.parametres.setPosFinale(posFinale)
            self.parametres.setDureeExp(dureeExp)

            Te = self.parametres.getTe()


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
            t0= time.time()
            t=time.time()
            hauteur = positionFinaleMm - (pPositionIs_i.contents.value / mm2qc)
            dureeDeplacement = hauteur / coef_dir
            nombrePasEchantillonageMontee = int(dureeDeplacement/Te)
            #offset ou pas ? -> on met juste le deplacement relatif
            consignePos = [coef_dir*Te*i for i in range(nombrePasEchantillonageMontee)]
            nombrePasEchantillonageStatique = int((self.parametres.getDureeExp() - dureeDeplacement)/Te)
            for i in range(nombrePasEchantillonageStatique):
                consignePos.append(hauteur)

            return self.commandeCascade(consignePos)

    def sinusPosition(self, Frequence, Amplitude):
        self.echelonPosition(250)

        Mode = c_int(-3)
        self.carteEpos.setOperationMode(Mode, pErrorCode_i)
        self.parametres.setFrequence(Frequence)

        if Amplitude > 200:
            return ('Amplitude trop grande')
        else:
            self.parametres.setAmplitude(Amplitude)

            Te = self.parametres.getTe()

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
            t0 = time.time()
            t = time.time()

            nombrePasEchantillonage = int(self.parametres.getDureeExp() / Te)

            consignePos = [Amplitude * sinus(2*pi*Frequence*i*Te) for i in range(nombrePasEchantillonage)]

        return self.commandeCascade(consignePos)

    def commandeCascade(self, consignePos):

        Kpos = self.parametres.getKpos()
        Tipos = self.parametres.getTipos()
        Tdpos = self.parametres.getTdpos()

        Kvit = self.parametres.getKvit()
        Tivit = self.parametres.getTivit()
        Tdvit = self.parametres.getTdvit()

        Kcour = self.parametres.getKcour()
        Ticour = self.parametres.getTicour()
        Tdcour = self.parametres.getTdcour()

        i = 0
        positions = []
        vitesses = []
        courants = []
        consigneVit = []
        consigneCour = []
        courantImposePI = []
        mm2qc = 294
        # pPositionIs = c_long(0)
        erreurPos = [0, 0]
        erreurVit = [0, 0]
        erreurCour = [0, 0]
        sommeErreurPos = 0
        sommeErreurVit = 0
        sommeErreurCour = 0
        while t - t0 < dureeExp:
            while time.time() - t < Te:
                a = 0
            t = time.time()

            carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
            positionLueMm = pPositionIs_i.contents.value / mm2qc  # conversion qc en mm
            positions.append(positionLueMm)
            consigneVit.append(Correcteurs.pos2velocity(Kpos, Tipos, Tdpos, consignePos[i], positionLueMm,
                                                            erreurPos, sommeErreurPos))

            carteEpos.getVelocityIs(pVelocityIs, pErrorCode_i)
            vitesseLue = pVelocityIs_i.contents.value  # en tour par minute ATTENTION ERREUR UNITE SOMMATEUR!
            vitesses.append(vitesseLue)
            consigneCour.append(Correcteurs.velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1], vitesseLue,
                                                                 erreurVit, sommeErreurVit))

            carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
            courantLu = pCurrentIs_i.contents.value / 1000  # en A
            courants.append(courantLu)
            courantImposePI.append(Correcteurs.courant_cmd(consigneCour[-1], courantLu, erreurCour, sommeErreurCour,
                                                           Kcour, Ticour, Tdcour))
            self.carteEpos.setCurrentMust(courantImposePI[-1], pErrorCode_i)

            i = i + 1

        return ("fini")

c=Controleur()
#c.run()
c.launch()
c.interface.actualisationAffichage(c.interface,12)
