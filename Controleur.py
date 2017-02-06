import Parametre
from EposData import *
import Initialisation_CoMax


class Controleur:

    def __init__(self):

        self.parametres = Parametre()
        self.carteEpos = Initialisation_CoMax.MyEpos #PAS PROPRE
        self.vue = Vue()
        self.vue.controleur = self

    def run(self):


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
