
# classe definissant tous les parametre utile pour le controleur
import ctypes

class Parametre:
    def __init__(self):

        # parametre du corecteur pid pour la boucle de position
        self.kpos = 18740
        self.tipos = 0.062
        self.tdpos = 0.016

        # parametre de corecteur pid pour la boucle de vitesse
        self.kvit = 0.024
        self.tivit = 0.17
        self.tdvit = 1

        # parametre de corecteur pour la boucle de courant
        self.kcour = 1
        self.ticour = 1
        self.tdcour = 1

        # parametres de correcteur d'effort
        self.kfor = 100
            #la correction integrale et derivee necessite d'abord l'integration de l'accelerometre
        self.tifor = 1
        self.tdfor = 1

        self.cascade = 0    # si est egale a 0 on ne fait pas de correction en cascade

        self.mode = 0       # si 0 position si 1 vitesse si 2 courant si 3 collaboratif

        self.dureeExp = 5

        # Parametres du logiciel Comax
        self.NominalCurrent = 5000
        self.MaxOutputCurrent = 7500
        self.ThermalTimeConstant = 70
        self.MaxAcceleration = 10000

        #parametre de commande
        self.position = 0
        self.posfinale = 0
        self.frequence = 5
        self.amplitude = 2000
        self.rampe = 10000

        self.Te = 0.001

        self.collaborativeRunning = False


    def getKpos(self):
        return (self.kpos)

    def setKpos(self,k):
        self.kpos = k

    def getTipos(self):
        return (self.tipos)

    def setTipos(self,k):
        self.tipos = k

    def getTdpos(self):
        return (self.tdpos)

    def setTdpos(self,k):
        self.tdpos = k

    def getKvit(self):
        return (self.kvit)

    def setKvit(self,k):
        self.kvit = k

    def getTivit(self):
        return (self.tivit)

    def setTivit(self,k):
        self.tivit = k

    def getTdvit(self):
        return (self.tdvit)

    def setTdvit(self,k):
        self.tdvit = k

    def getKcour(self):
        return (self.kcour)

    def setKcour(self,k):
        self.kcour = k

    def getTicour(self):
        return (self.ticour)

    def setTicour(self,k):
        self.ticour = k

    def getTdcour(self):
        return (self.tdcour)

    def setTdcour(self,k):
        self.tdcour = k

    def getKfor(self):
        return (self.kfor)

    def setKfor(self,k):
        self.kfor = k

    def getTifor(self):
        return (self.tifor)

    def setTifor(self,k):
        self.tifor = k

    def getTdfor(self):
        return (self.tdfor)

    def setTdfor(self,k):
        self.tdfor = k

    def getCascade(self):
        return (self.cascade)

    def setCascade(self, a):
        self.cascade = a

    def getMode(self):
        return (self.mode)

    def setMode(self, mode):
        self.mode = mode

    def getDureeExp(self):
        return(self.dureeExp)

    def setDureeExp(self,d):
        self.dureeExp = d

    def getCorPos(self):
        tab = []
        tab[0] = self.kpos
        tab[1] = self.tipos
        tab[2] = self.tdpos
        return tab

    def setCorPos(self, tab):
        self.kpos = tab[0]
        self.tipos = tab[1]
        self.tdpos = tab[2]

    def getCorVit(self):
        tab = []
        tab[0] = self.kvit
        tab[1] = self.tivit
        tab[2] = self.tdvit
        return tab

    def setCorVit(self, tab):
        self.kvit = tab[0]
        self.tivit = tab[1]
        self.tdvit = tab[2]

    def getCorCour(self):
        tab = []
        tab[0] = self.kcour
        tab[1] = self.ticour
        tab[2] = self.tdcour
        return tab

    def setCorCour(self, tab):
        self.kcour = tab[0]
        self.ticour = tab[1]
        self.tdcour = tab[2]

    def getNominalCurrent(self):
        return self.NominalCurrent

    def getMaxOutputCurrent(self):
        return self.MaxOutputCurrent

    def getThermalTimeConstant(self):
        return self.ThermalTimeConstant

    def getMaxAcceleration(self):
        return self.MaxAcceleration

    def setPosition(self,p):
        self.position = p

    def getPosition(self):
        return(self.position)

    def setPosFinale(self,p):
        self.posfinale = p

    def getPosFinale(self):
        return(self.posfinale)

    def setFrequence(self,f):
        self.frequence = f

    def getFrequence(self):
        return (self.frequence)

    def setAmplitude(self,a):
        self.amplitude = a

    def getAmplitude(self):
        return (self.amplitude)

    def setRampe(self, r):
        self.rampe = r

    def getRampe(self):
        return (self.rampe)

    def setTe(self, t):
        self.Te = t

    def getTe(self):
        return (self.Te)

    def setCollaborativeRunning(self, b):
        self.collaborativeRunning = b

    def getCollaborativeRunning(self):
        return (self.collaborativeRunning)