
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

        self.cascade = 0    # si est egale a 0 on ne fait pas de corection en cascade

        self.mode = 0       # si 0 position si 1 vitesse si 2 courant si 3 collaboratif



        def getkpos(self):
            return (self.kpos)
        def setkpos(self,k):
            self.kpos = k

        def gettipos(self):
            return (self.tipos)
        def settipos(self,k):
            self.tipos = k

        def gettdpos(self):
            return (self.tdpos)
        def settdpos(self,k):
            self.tspos = k

        def getkvit(self):
            return (self.kvit)
        def setkvit(self,k):
            self.kvit = k

        def gettivit(self):
            return (self.tivit)
        def settivit(self,k):
            self.tivit = k

        def gettdvit(self):
            return (self.tdvit)
        def settdvit(self,k):
            self.tdvit = k

        def getkcour(self):
            return (self.kcour)
        def setkcour(self,k):
            self.kcour = k

        def getticour(self):
            return (self.ticour)
        def setticour(self,k):
            self.ticour = k

        def gettdcour(self):
            return (self.tdcour)
        def settdcour(self,k):
            self.tdcour = k

        def getcascade(self):
            return (self.cascade)
        def setCascade(self, a):
            self.cascade = a

        def getmode(self):
            return (self.mode)
        def setmode(self, mode):
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

