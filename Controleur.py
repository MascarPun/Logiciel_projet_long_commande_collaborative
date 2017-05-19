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

    def echelon_position(self):
        # initialisation des constantes
        ValMaxCourEpos = 5  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
        qc2mm = 294
        dureeExp=self.interface.getdurexppos()
        posFinale=self.interface.getposfinechelonpos()

        if posFinale > 490 or posFinale < 10:
            return ('Cette valeur est interdite')
        else:
            self.parametres.setPosFinale(posFinale)
            self.parametres.setDureeExp(dureeExp)

            Te = self.parametres.getTe() #Te est en secondes

        # on verifie que la bonne correction est activee
        if self.interface.groupebuttoncor() == 2:  # si correction en vitesse
            return ("erreur il faut une commande en vitesse pour faire une correction en vitesse")

        if self.interface.groupebuttoncor() == 3:  # si correction en courant
            return ("erreur il faut une commande en vitesse pour faire une correction en vitesse")

        # Recuperation des paramètres des correcteurs (voir si on passe par interface)
        Kpos = self.parametres.getKpos()
        Tipos = self.parametres.getTipos()
        Tdpos = self.parametres.getTdpos()
        satPos = 1  # en attente de l'interface
        Kvit = self.parametres.getKvit()
        Tivit = self.parametres.getTivit()
        Tdvit = self.parametres.getTdvit()
        satVit = 1  # en attente de l'interface
        Kcour = self.parametres.getKcour()
        Ticour = self.parametres.getTicour()
        Tdcour = self.parametres.getTdcour()
        satCour = 1  # en attente de l'interface

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / qc2mm  # conversion qc en mm

        # initialisaton des tableaux pour les représentations graphiques
        Temps = []
        TabPosition = []
        TabVitesse = []
        TabCourant = []

        # initialisation de la consigne et des erreurs (il faut remplir les tableaux d'erreurs avec deux elements (si on a un pid)
        consignePos = []
        consigneVit = []
        consigneCour = []
        courantCorrige = []

        errPos = [0, 0]
        errVit = [0, 0]
        errCour = [0, 0]
        sommeErrPos = 0
        sommeErrVit = 0
        sommeErrCour = 0
        nombreEch = dureeExp // Te
        compt = 0

        if self.interface.groupebuttoncor() == 1:  # si correction en position

            debut = time.time()
            while (compt <= nombreEch - 1):  # a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
                t = time.time()
                # On verfie que le mouvement est possible
                self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                if ((pPositionIs_i.contents.value / qc2mm) > 490):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((pPositionIs_i.contents.value / qc2mm) < -2):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break

                else:
                    while (time.time() - t < Te):
                        pass
                        # groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
                        # Pour l'instant il fait rien mais on peut lui ajouter une action à réaliser pour pas avoir de temps où il ne fait rien

                    # On calcule ce que la commande renvoie comme courant
                    consignePos.append(posFinale)

                    if satPos != 0:
                        consigneCour.append(pos2current_sat(Kpos, Tipos, Tdpos, satPos, consignePos[-1],
                                                            pPositionIs_i.contents.value / qc2mm, errPos,
                                                            sommeErrPos))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 5
                        self.carteEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)
                    else:
                        consigneCour.append(pos2current(Kpos, Tipos, Tdpos, consignePos[-1],
                                                        pPositionIs_i.contents.value / qc2mm, errPos,
                                                        sommeErrPos))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 5
                        self.carteEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)
                compt+=1
                Temps.append(time.time() - debut)
                MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
                TabPosition.append(pPositionIs_i.contents.value / qc2mm)
                TabVitesse.append(pVelocityIs_i.contents.value)
                TabCourant.append(pCurrentIs_i.contents.value)


        elif self.interface.groupebuttoncor() == 4:  # si correction en position

            debut = time.time()
            while (compt <= nombreEch - 1):  # a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
                t = time.time()
                # On verfie que le mouvement est possible
                self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                if ((pPositionIs_i.contents.value / qc2mm) > 490):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((pPositionIs_i.contents.value / qc2mm) < -2):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break

                else:
                    while (time.time() - t < Te):
                        pass
                        # groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
                        # Pour l'instant il fait rien mais on peut lui ajouter une action à réaliser pour pas avoir de temps où il ne f
                    # On calcule ce que la commande renvoie comme courant
                    consignePos.append(posFinale)

                    if satPos != 0:
                        consigneVit.append(pos2velocity_sat(Kpos, Tipos, Tdpos, satPos, consignePos[-1],
                                                                        pPositionIs_i.contents.value / qc2mm, errPos,
                                                                        sommeErrPos))
                    else:
                        consigneVit.append(pos2velocity(Kpos, Tipos, Tdpos, consignePos[-1],
                                                                    pPositionIs_i.contents.value / qc2mm, errPos,
                                                                    sommeErrPos))

                    self.carteEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                    if satVit != 0:
                        consigneCour.append(velocity2current_sat(Kvit, Tivit, Tdvit, satVit, consigneVit[-1],
                                                             pVelocityIs_i.contents.value, errVit, sommeErrVit))
                    else:
                        consigneCour.append(velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1],
                                                                         pVelocityIs_i.contents.value, errVit,
                                                                         sommeErrVit))

                    self.carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
                    if satCour != 0:
                        courantCorrige.append(courant_cmd_sat(Kcour, Ticour, Tdcour, satCour, consigneCour[-1],
                                                        pCurrentIs_i.contents.value, errCour, sommeErrCour))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 5
                        self.carteEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)
                    else:
                        courantCorrige.append(courant_cmd(Kcour, Ticour, Tdcour, consigneCour[-1],
                                                                      pCurrentIs_i.contents.value, errCour,
                                                                      sommeErrCour))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 5
                        self.carteEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)
                compt+=1
                Temps.append(time.time() - debut)
                MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
                TabPosition.append(pPositionIs_i.contents.value / qc2mm)
                TabVitesse.append(pVelocityIs_i.contents.value)
                TabCourant.append(pCurrentIs_i.contents.value)

        return ("fin")

    def echelon_vitesse(self):
        # initialisation des constantes
        ValMaxCourEpos = 5  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
        qc2mm = 294
        dureeExp=self.interface.getdurexppos()
        vitFinale=3         #en attente interface
        rapportReduction = 0.1082 / (2 * math.pi * 15.88)
        posFinale = 2 * math.pi * rapportReduction * dureeExp * vitFinale

        if posFinale > 490 or posFinale < 10:
            return ('Cette valeur est interdite')
        else:
            self.parametres.setPosFinale(posFinale)
            self.parametres.setDureeExp(dureeExp)

            Te = self.parametres.getTe() #Te est en secondes

        # on verifie que la bonne correction est activee
        if interface.groupebuttoncor() == 4:  # si correction en cascade
            return ("erreur il faut une commande en position pour faire une correction en cascade")

        if interface.groupebuttoncor() == 3:  # si correction en courant
            return ("erreur il faut une commande en courant pour faire une correction en courant")

        if interface.groupebuttoncor() == 1:  # si correction en position
            return ("erreur il faut une commande en position pour faire une correction en position")

        # Recuperation des paramètres des correcteurs (voir si on passe par interface)
        Kvit = self.parametres.getKvit()
        Tivit = self.parametres.getTivit()
        Tdvit = self.parametres.getTdvit()
        satVit = 1  # en attente de l'interface
        Kcour = self.parametres.getKcour()
        Ticour = self.parametres.getTicour()
        Tdcour = self.parametres.getTdcour()
        satCour = 1  # en attente de l'interface

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / qc2mm  # conversion qc en mm

        # initialisaton des tableaux pour les représentations graphiques
        Temps = []
        TabPosition = []
        TabVitesse = []
        TabCourant = []

        # initialisation de la consigne et des erreurs (il faut remplir les tableaux d'erreurs avec deux elements (si on a un pid)
        consigneVit = []
        consigneCour = []
        courantCorrige = []

        errVit = [0, 0]
        errCour = [0, 0]
        sommeErrVit = 0
        sommeErrCour = 0
        nombreEch = dureeExp // Te
        compt = 0

        if self.interface.groupebuttoncor() == 2:  # si correction en vitesse

            debut = time.time()
            while (compt <= nombreEch - 1):  # a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
                t = time.time()
                # On verfie que le mouvement est possible
                self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                if ((pPositionIs_i.contents.value / qc2mm) > 490):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((pPositionIs_i.contents.value / qc2mm) < -2):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break

                else:
                    while (time.time() - t < Te):
                        pass
                        # groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
                        # Pour l'instant il fait rien mais on peut lui ajouter une action à réaliser pour pas avoir de temps où il ne fait rien

                    # On calcule ce que la commande renvoie comme courant
                    consigneVit.append(vitFinale)

                    if SatVit != 0:
                        consigneCour.append(Correcteurs.velocity2current_sat(Kvit, Tivit, Tdvit, Savit, consigneVit[-1],
                                                                             pVelocityIs_i.contents.value, errVit,
                                                                             sommeErrVit))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 5
                        MyEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)
                    else:
                        consigneCour.append(Correcteurs.velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1],
                                                                         pVelocityIs_i.contents.value, errVit,
                                                                         sommeErrVit))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 5
                        MyEpos.setCurrentMust(c_short(consigneCour[-1]), pErrorCode_i)

                compt+=1
                Temps.append(time.time() - debut)
                MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
                TabPosition.append(pPositionIs_i.contents.value / qc2mm)
                TabVitesse.append(pVelocityIs_i.contents.value)
                TabCourant.append(pCurrentIs_i.contents.value)

        return ("fin")

    def echelon_courant(self):
        # initialisation des constantes
        ValMaxCourEpos = 5  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
        dureeExp = self.interface.getdurexppos()
        courFinal= 3 #à relier ensuite avec interface
        posFinale=250 #temporaire, à exprimer en fonction du courant

        if posFinale > 490 or posFinale < 10:
            return ('Cette valeur est interdite')
        else:
            self.parametres.setPosFinale(posFinale)
            self.parametres.setDureeExp(dureeExp)

            Te = self.parametres.getTe()  # Te est en secondes

        # on verifie que la bonne correction est activee
        if interface.groupebuttoncor() == 4:  # si correction en cascade
            return ("erreur il faut une commande en position pour faire une correction en cascade")

        if interface.groupebuttoncor() == 2:  # si correction en vitesse
            return ("erreur il faut une commande en courant pour faire une correction en courant")

        if interface.groupebuttoncor() == 1:  # si correction en position
            return ("erreur il faut une commande en position pour faire une correction en position")

        # Recuperation des paramètres des correcteurs (voir si on passe par interface)
        Kcour = self.parametres.getKcour()
        Ticour = self.parametres.getTicour()
        Tdcour = self.parametres.getTdcour()
        satCour = 3  # en attente de l'interface

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / qc2mm  # conversion qc en mm

        # initialisaton des tableaux pour les représentations graphiques
        Temps = []
        TabPosition = []
        TabVitesse = []
        TabCourant = []

        # initialisation de la consigne et des erreurs (il faut remplir les tableaux d'erreurs avec deux elements (si on a un pid)
        consigneCour = []
        courantCorrige = []

        errCour = [0, 0]
        sommeErrCour = 0
        nombreEch = dureeExp // Te
        compt = 0

        if self.interface.groupebuttoncor() == 3:  # si correction en courant

            debut = time.time()
            while (
                compt <= nombreEch - 1):  # a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
                t = time.time()
                # On verfie que le mouvement est possible
                self.carteEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                if ((pPositionIs_i.contents.value / qc2mm) > 490):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((pPositionIs_i.contents.value / qc2mm) < -2):
                    self.carteEpos.setOperationMode(c_int(3), pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break

                else:
                    while (time.time() - t < Te):
                        pass
                        # groupBoutonCore renvoie 1 2 3 4 suivant la correction choisie (defini dans interface.py)
                        # Pour l'instant il fait rien mais on peut lui ajouter une action à réaliser pour pas avoir de temps où il ne fait rien

                    # On calcule ce que la commande renvoie comme courant
                    consigneCour.append(courFinal)

                    if satCour != 0:
                        courantCorrige.append(Correcteurs.courant_cmd_sat(Kcour, Ticour, Tdcour, satCour, consigneCour[-1],
                                                                             pCurrentIs_i.contents.value, errCour,
                                                                             sommeErrCour))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 5
                        MyEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)
                    else:
                        courantCorrige.append(Correcteurs.courant_cmd(Kcour, Ticour, Tdcour, courantCorrige[-1],
                                                                         pCurrentIs_i.contents.value, errCour,
                                                                         sommeErrCour))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 5
                        MyEpos.setCurrentMust(c_short(courantCorrige[-1]), pErrorCode_i)

                compt += 1
                Temps.append(time.time() - debut)
                MyEpos.getPositionIs(pPositionIs_i, pErrorCode_i)
                MyEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i)
                MyEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)
                TabPosition.append(pPositionIs_i.contents.value / qc2mm)
                TabVitesse.append(pVelocityIs_i.contents.value)
                TabCourant.append(pCurrentIs_i.contents.value)

        return ("fin")

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
        self.echelonPosition(250) #On impose un echelon avant de commencer ? (pcq il manque qq arguments)

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

    def sinusPosition_modif(self, Frequence, Amplitude,dureeExp):
        tpsPrep=500
        echelon_position(self,tpsPrep,250,self.carteEpos,self.interface) #On impose un echelon avant de commencer ? (pcq il manque qq arguments)

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
            self.carteEpos.setCurrentMust(c_long(courantImposePI[-1]), pErrorCode_i)

            i = i + 1

        return ("fini")

c=Controleur()
#c.run()
c.launch()
c.interface.actualisationAffichage(c.interface,12)
