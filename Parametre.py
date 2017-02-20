
# classe definissant tous les parametre utile pour le controleur


class Parametre:
    def __init__(self):

        # parametre du corecteur pid pour la boucle de position
        self.kpos = 1
        self.tipos = 1
        self.tdpos = 1

        # parametre de corecteur pid pour la boucle de vitesse
        self.kvit = 1
        self.tivit = 1
        self.tdvit = 1

        # parametre de corecteur pour la boucle de courant
        self.kcour = 1
        self.ticour = 1
        self.tdcour = 1

        self.cascade = 0    # si est egale a 0 on ne fait pas de correction en cascade

        self.mode = 0       # si 0 position si 1 vitesse si 2 courant si 3 collaboratif

        self.dureeExp = 1

        global pErrorCode_i
        pErrorCode = ctypes.POINTER(ctypes.c_long)
        pErrorCode2 = ctypes.c_long(0)
        pErrorCode_i = ctypes.cast(ctypes.addressof(pErrorCode2), pErrorCode)

        global pIsEnabled_i
        pIsEnabled = ctypes.POINTER(ctypes.c_bool)
        pIsEnabled2 = ctypes.c_bool(0)
        pIsEnabled_i = ctypes.cast(ctypes.addressof(pIsEnabled2), pIsEnabled)

        global pPositionIs_i
        pPositionIs = ctypes.POINTER(ctypes.c_long)
        pPositionIs2 = ctypes.c_long(0)
        pPositionIs_i = ctypes.cast(ctypes.addressof(pPositionIs2), pPositionIs)

        global pAnalogValue
        pAnalogValue_i = ctypes.POINTER(ctypes.c_int)
        pAnalogValue2 = ctypes.c_int(0)
        pAnalogValue = ctypes.cast(ctypes.addressof(pAnalogValue2), pAnalogValue_i)

        global pVelocityIs_i
        pVelocityIs = ctypes.POINTER(ctypes.c_long)
        pVelocityIs2 = ctypes.c_long(0)
        pVelocityIs_i = ctypes.cast(ctypes.addressof(pVelocityIs2), pVelocityIs)

        global pCurrentIs_i
        pCurrentIs = ctypes.POINTER(ctypes.c_short)
        pCurrentIs2 = ctypes.c_short(0)
        pCurrentIs_i = ctypes.cast(ctypes.addressof(pCurrentIs2), pCurrentIs)



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
            self.tspos = k

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

