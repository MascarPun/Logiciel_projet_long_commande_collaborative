
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

