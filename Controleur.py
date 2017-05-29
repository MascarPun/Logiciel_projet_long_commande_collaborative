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
from Correcteurs import *
from Commandes import *


class Controleur:



    def __init__(self):

        self.parametres = Parametre()
        self.carteEpos = Initialisation_CoMax.MyEpos
        self.interface = Ui_MainWindow(self)
        self.interface.controleur = self
        self.pErrorCode_i = Initialisation_CoMax.pErrorCode_i
        self.pIsEnabled_i = Initialisation_CoMax.pIsEnabled_i
        self.pPositionIs_i = Initialisation_CoMax.pPositionIs_i
        self.pCurrentIs_i = Initialisation_CoMax.pCurrentIs_i
        self.pVelocityIs_i = Initialisation_CoMax.pVelocityIs_i


    def run(self):
        print("setTiVit")
        self.parametres.setTivit(300)
        self.parametres.getTivit()
        self.parametres.setDureeExp(10)
        mm2qc = 294

        NominalCurrent = self.parametres.getNominalCurrent()  # Parametre du logiciel Comax
        MaxOutputCurrent = self.parametres.getMaxOutputCurrent()  # Parametre du logiciel Comax
        ThermalTimeConstant = self.parametres.getThermalTimeConstant()  # Parametre du logiciel Comax
        MaxAcceleration = self.parametres.getMaxAcceleration()  # Parametre du logiciel Comax

        self.carteEpos.setDcMotorParameter(NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, self.pErrorCode_i)
        self.carteEpos.setMaxAcceleration(MaxAcceleration, self.pErrorCode_i)


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



####################FONCTION DES AUTRES##############################

    def echelonPosition(self, posFinale):

        Mode = c_int(-1)
        self.carteEpos.setOperationMode(Mode, self.pErrorCode_i)
        self.parametres.setPosFinale(posFinale)

        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

        # set enable state
        self.carteEpos.setDisableState(self.pErrorCode_i)
        self.carteEpos.setEnableState(self.pErrorCode_i)

        # get enabled state
        res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

        Timeout_i = c_long(5000)
        positionFinaleMm = self.parametres.getPosFinale()


        if (positionFinaleMm > 500 or positionFinaleMm < 0):  # Il faut définir des conditions de sécurité
            print('Cette valeur est interdite')
        else:
            positionFinaleQc = c_long(math.floor(positionFinaleMm * mm2qc))

            self.carteEpos.setPositionMust(positionFinaleQc, self.pErrorCode_i)  # on initialise la position à l'origine
            # définie précédemment. On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
        return("fini")







    def profilEchelonPosition(self):

        Te = 0.001
        # On impose le mode Position Mode

        Mode = c_int(1)

        self.carteEpos.setOperationMode(Mode, self.pErrorCode_i)

        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(self.pErrorCode_i)

        # get enabled state
        res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

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

                self.carteEpos.moveToPosition(positionInitialeQc, 1, 1, self.pErrorCode_i)  # on initialise la position à l'origine définie précédemment.
                #  On met 1 en second argument pour un déplacement absolu, 0 pour un déplacement relatif
                #            self.carteEpos.waitForTargetReached(Timeout_i, self..pErrorCode_i)
                print('Bras en déplacement')

            time.sleep(Te)

            Temps.append(time.time()-t)
            self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
            self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
            self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
            TabPosition.append(self.pPositionIs_i.contents.value / mm2qc)
            TabVitesse.append(float(self.pVelocityIs_i.contents.value))
            TabCourant.append(float(self.pCurrentIs_i.contents.value))

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
        self.carteEpos.setOperationMode(c_int(-2), self.pErrorCode_i)

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(self.pErrorCode_i)
        # get enabled state
        res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

        # durée de l'expérimentation
        Timeout_i = c_long(5000)

        Temps = []
        TabPosition = []
        TabVitesse = []
        TabCourant = []

        # sécurité
        t = time.time()
        while (time.time() - t < self.parametres.getDureeExp()):
            self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
            if ((self.pPositionIs_i.contents.value / mm2qc) > 490):
                if vitesseConsigne > 0:
                    self.carteEpos.setVelocityMust(c_long(0), self.pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break
                else:
                    self.carteEpos.setVelocityMust(c_long(vitesseConsigne), self.pErrorCode_i)

            if ((self.pPositionIs_i.contents.value / mm2q) < 10):
                if vitesseConsigne < 0:
                    self.carteEpos.setVelocityMust(c_long(0), self.pErrorCode_i)
                    print("Le bras ne peut pas descendre car il va taper la butée !!!")
                    break
                else:
                    self.carteEpos.setVelocityMust(c_long(vitesseConsigne), self.pErrorCode_i)

            else:
                self.carteEpos.setVelocityMust(c_long(vitesseConsigne), self.pErrorCode_i)

            t1 = time.time() - t
            Temps.append(t1)
            self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
            self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
            self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
            TabPosition.append(float(self.pPositionIs_i.contents.value) / float(mm2qc))
            TabVitesse.append(self.pVelocityIs_i.contents.value)
            TabCourant.append(self.pCurrentIs_i.contents.value)

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


#######################NOS FONCTIONS##################################


    def echelon_position(self):
        # initialisation des constantes
        ValMaxCourEpos = 5000  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
        mm2qc = 294
        dureeExp=self.parametres.getDureeExp()
        posFinale=self.interface.getposfinechelonpos() #a coder en dur pour les tests

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
        satPos = 150  # en attente de l'interface
        Kvit = self.parametres.getKvit()
        Tivit = self.parametres.getTivit()
        Tdvit = self.parametres.getTdvit()
        satVit = 1  # en attente de l'interface
        Kcour = self.parametres.getKcour()
        Ticour = self.parametres.getTicour()
        Tdcour = self.parametres.getTdcour()
        satCour = 1500  # en attente de l'interface

        # initialiser le pointeur pMode
        pMode = ctypes.POINTER(ctypes.c_int)
        pMode_i = ctypes.c_int(0)
        pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)

        # récupérer le Mode acutuel
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        #pPositionIs = c_long(0)
        #self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale
        #positionDepartLueMm = pPositionIs.value / mm2qc  # conversion qc en mm

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
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                if ((self.pPositionIs_i.contents.value / mm2qc) > 490):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((self.pPositionIs_i.contents.value / mm2qc) < -2):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
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
                        #je tente de convertir le positionn en qc pour les calculs
                        consigneCour.append(pos2current_sat(Kpos, Tipos, Tdpos, satPos, consignePos[-1]*mm2qc,
                                                            self.pPositionIs_i.contents.value, errPos,
                                                            sommeErrPos,Te))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 4000
                        c=int(consigneCour[-1])
                        self.carteEpos.setCurrentMust(c_short(c), self.pErrorCode_i)
                    else:
                        consigneCour.append(pos2current(Kpos, Tipos, Tdpos, consignePos[-1]*mm2qc,
                                                        self.pPositionIs_i.contents.value, errPos,
                                                        sommeErrPos,Te))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 4000
                        c = int(consigneCour[-1])
                        self.carteEpos.setCurrentMust(c_short(c), self.pErrorCode_i)
                compt+=1
                Temps.append(time.time() - debut)
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
                self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
                TabPosition.append(self.pPositionIs_i.contents.value / mm2qc)
                TabVitesse.append(self.pVelocityIs_i.contents.value)
                TabCourant.append(self.pCurrentIs_i.contents.value)


        elif self.interface.groupebuttoncor() == 4:  # si correction en cascade

            debut = time.time()
            while (compt <= nombreEch - 1):  # a priori meme condition mais la deuxième peut peut etre eviter des pb (pour le moment c est provisoir)
                t = time.time()
                # On verfie que le mouvement est possible
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                if ((self.pPositionIs_i.contents.value / mm2qc) > 490):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((self.pPositionIs_i.contents.value / mm2qc) < -2):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
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
                        consigneVit.append(pos2velocity_sat(Kpos, Tipos, Tdpos, satPos, consignePos[-1]*mm2qc,
                                                                        self.pPositionIs_i.contents.value, errPos,
                                                                        sommeErrPos,Te))
                    else:
                        consigneVit.append(pos2velocity(Kpos, Tipos, Tdpos, consignePos[-1]*mm2qc,
                                                                    self.pPositionIs_i.contents.value, errPos,
                                                                    sommeErrPos,Te))

                    self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
                    if satVit != 0:
                        consigneCour.append(velocity2current_sat(Kvit, Tivit, Tdvit, satVit, consigneVit[-1],
                                                             self.pVelocityIs_i.contents.value, errVit, sommeErrVit,Te))
                    else:
                        consigneCour.append(velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1],
                                                                         self.pVelocityIs_i.contents.value, errVit,
                                                                         sommeErrVit,Te))

                    self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
                    if satCour != 0:
                        courantCorrige.append(courant_cmd_sat(Kcour, Ticour, Tdcour, satCour, consigneCour[-1],
                                                        self.pCurrentIs_i.contents.value, errCour, sommeErrCour,Te))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 4000
                        c = int(courantCorrige[-1])
                        self.carteEpos.setCurrentMust(c_short(c), self.pErrorCode_i)
                    else:
                        courantCorrige.append(courant_cmd(Kcour, Ticour, Tdcour, consigneCour[-1],
                                                                      self.pCurrentIs_i.contents.value, errCour,
                                                                      sommeErrCour,Te))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 4000
                        c = int(courantCorrige[-1])
                        self.carteEpos.setCurrentMust(c_short(c), self.pErrorCode_i)
                compt+=1
                Temps.append(time.time() - debut)
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
                self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
                TabPosition.append(self.pPositionIs_i.contents.value / mm2qc)
                TabVitesse.append(self.pVelocityIs_i.contents.value)
                TabCourant.append(self.pCurrentIs_i.contents.value)

        return ("fin")






    def echelon_vitesse(self):
        # initialisation des constantes
        ValMaxCourEpos = 5000  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
        mm2qc = 294
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
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / mm2qc  # conversion qc en mm

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
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                if ((self.pPositionIs_i.contents.value / mm2qc) > 490):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((self.pPositionIs_i.contents.value / mm2qc) < -2):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
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
                                                                             self.pVelocityIs_i.contents.value, errVit,
                                                                             sommeErrVit,Te))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 4000
                        MyEpos.setCurrentMust(c_short(consigneCour[-1]), self.pErrorCode_i)
                    else:
                        consigneCour.append(Correcteurs.velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1],
                                                                         self.pVelocityIs_i.contents.value, errVit,
                                                                         sommeErrVit,Te))
                        if consigneCour[-1] > ValMaxCourEpos:
                            consigneCour[-1] = 4000
                        MyEpos.setCurrentMust(c_short(consigneCour[-1]), self.pErrorCode_i)

                compt+=1
                Temps.append(time.time() - debut)
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
                self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
                TabPosition.append(self.pPositionIs_i.contents.value / mm2qc)
                TabVitesse.append(self.pVelocityIs_i.contents.value)
                TabCourant.append(self.pCurrentIs_i.contents.value)

        return ("fin")




    def echelon_courant(self):
        # initialisation des constantes
        ValMaxCourEpos = 5000  # on s'arrange pour ne pas depasser 5A en courant dans tous les cas
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
        self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
        self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)
        self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)

        # set enable state
        self.carteEpos.setEnableState(self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
        pPositionIs = c_long(0)
        self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale
        positionDepartLueMm = pPositionIs.value / mm2qc  # conversion qc en mm

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
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                if ((self.pPositionIs_i.contents.value / mm2qc) > 490):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
                    print("Le bras ne peut pas monter car il va taper la butée !!!")
                    break

                if ((self.pPositionIs_i.contents.value / mm2qc) < -2):
                    self.carteEpos.setOperationMode(c_int(3), self.pErrorCode_i)
                    self.carteEpos.moveWithVelocity(c_long(0), self.pErrorCode_i)
                    self.carteEpos.setOperationMode(c_int(-3), self.pErrorCode_i)
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
                                                                             self.pCurrentIs_i.contents.value, errCour,
                                                                             sommeErrCour,Te))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 4000
                        MyEpos.setCurrentMust(c_short(courantCorrige[-1]), self.pErrorCode_i)
                    else:
                        courantCorrige.append(Correcteurs.courant_cmd(Kcour, Ticour, Tdcour, courantCorrige[-1],
                                                                         self.pCurrentIs_i.contents.value, errCour,
                                                                         sommeErrCour,Te))
                        if courantCorrige[-1] > ValMaxCourEpos:
                            courantCorrige[-1] = 4000
                        MyEpos.setCurrentMust(c_short(courantCorrige[-1]), self.pErrorCode_i)

                compt += 1
                Temps.append(time.time() - debut)
                self.carteEpos.getPositionIs(self.pPositionIs_i, self.pErrorCode_i)
                self.carteEpos.getVelocityIs(self.pVelocityIs_i, self.pErrorCode_i)
                self.carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
                TabPosition.append(self.pPositionIs_i.contents.value / mm2qc)
                TabVitesse.append(self.pVelocityIs_i.contents.value)
                TabCourant.append(self.pCurrentIs_i.contents.value)

        return ("fin")






    def rampePosition(self, coef_dir, posFinale, dureeExp):
        Mode = c_int(-3)
        self.carteEpos.setOperationMode(Mode, self.pErrorCode_i)
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
            self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
            self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

        # set enable state
            self.carteEpos.setDisableState(self.pErrorCode_i)
            self.carteEpos.setEnableState(self.pErrorCode_i)

        # get enabled state
            res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

        # Phase de commande du bras pour aller d'une position à une autre
            pPositionIs = c_long(0)
            self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

            Timeout_i = c_long(5000)
            positionFinaleMm = self.parametres.getPosFinale()
            t0= time.time()
            t=time.time()
            hauteur = positionFinaleMm - (self.pPositionIs_i.contents.value / mm2qc)
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
        self.carteEpos.setOperationMode(Mode, self.pErrorCode_i)
        self.parametres.setFrequence(Frequence)

        if Amplitude > 200:
            return ('Amplitude trop grande')
        else:
            self.parametres.setAmplitude(Amplitude)

            Te = self.parametres.getTe()

            pMode = ctypes.POINTER(ctypes.c_int)
            pMode_i = ctypes.c_int(0)
            pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
            self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
            self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

            # set enable state
            self.carteEpos.setDisableState(self.pErrorCode_i)
            self.carteEpos.setEnableState(self.pErrorCode_i)

            # get enabled state
            res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

            # Phase de commande du bras pour aller d'une position à une autre
            pPositionIs = c_long(0)
            self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

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
        self.carteEpos.setOperationMode(Mode, self.pErrorCode_i)
        self.parametres.setFrequence(Frequence)

        if Amplitude > 200:
            return ('Amplitude trop grande')
        else:
            self.parametres.setAmplitude(Amplitude)

            Te = self.parametres.getTe()

            pMode = ctypes.POINTER(ctypes.c_int)
            pMode_i = ctypes.c_int(0)
            pMode2 = ctypes.cast(ctypes.addressof(pMode_i), pMode)
            self.carteEpos.getOperationMode(pMode2, self.pErrorCode_i)
            self.carteEpos.getOperationMode2(pMode2.contents, self.pErrorCode_i)

            # set enable state
            self.carteEpos.setDisableState(self.pErrorCode_i)
            self.carteEpos.setEnableState(self.pErrorCode_i)

            # get enabled state
            res = self.carteEpos.getEnableState(self.pIsEnabled_i, self.pErrorCode_i)

            # Phase de commande du bras pour aller d'une position à une autre
            pPositionIs = c_long(0)
            self.carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale

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

            carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale
            positionLueMm = self.pPositionIs_i.contents.value / mm2qc  # conversion qc en mm
            positions.append(positionLueMm)
            consigneVit.append(Correcteurs.pos2velocity(Kpos, Tipos, Tdpos, consignePos[i], positionLueMm,
                                                            erreurPos, sommeErreurPos))

            carteEpos.getVelocityIs(pVelocityIs, self.pErrorCode_i)
            vitesseLue = self.pVelocityIs_i.contents.value  # en tour par minute ATTENTION ERREUR UNITE SOMMATEUR!
            vitesses.append(vitesseLue)
            consigneCour.append(Correcteurs.velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1], vitesseLue,
                                                                 erreurVit, sommeErreurVit))

            carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
            courantLu = self.pCurrentIs_i.contents.value / 1000  # en A
            courants.append(courantLu)
            courantImposePI.append(Correcteurs.courant_cmd(consigneCour[-1], courantLu, erreurCour, sommeErreurCour,
                                                           Kcour, Ticour, Tdcour))
            self.carteEpos.setCurrentMust(c_long(courantImposePI[-1]), self.pErrorCode_i)

            i = i + 1

        return ("fini")

c=Controleur()
#c.run()
c.launch()
c.interface.actualisationAffichage(c.interface,12)
