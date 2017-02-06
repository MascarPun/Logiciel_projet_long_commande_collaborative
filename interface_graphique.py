import numpy as np
import numpy.linalg as alg
import time
import ctypes
from ctypes import *
import math
import control

import scipy as sp

 
from tkinter import * 
from tkinter.messagebox import *

fenetre = Tk()


fenetre['bg']='white'

# frame 1
Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=30, pady=30)

# frame 2
Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=10, pady=10)


#Label
l = LabelFrame(fenetre, text="Commande Collaborative", padx=50, pady=50)
l.pack(fill="both", expand="yes")
 
Label(l, text="Position de départ souhaité").pack()

#Label
l2 = LabelFrame(fenetre, text="Commande en position", padx=50, pady=50)
l2.pack(fill="both", expand="yes")
 
Label(l2, text="Position souhaitée").pack()

#Bouton de sortie
#bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
#bouton.pack()     Fait bugger !!!


def alert():
    showinfo("alerte", "Bravo!")

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=alert)
menu1.add_command(label="Editer", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Coller", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

def recupere():
    showinfo("Alerte", entree.get())

value = StringVar() 
value.set("")
global entree
entree = Entry(l, textvariable=value, width=30)
entree.pack()

bouton = Button(l, text="Valider", command=recupere)
bouton.pack()


def recupere2():
    showinfo("Alerte", entree2.get())

value2 = StringVar() 
value2.set("")
global entree2
entree2 = Entry(l2, textvariable=value2, width=30)
entree2.pack()

bouton = Button(l2, text="Valider", command=recupere2)
bouton.pack()

def saisie():
    return int(entree.get()) #recupére la valeur saisie

def saisie2():
    return int(entree2.get()) #recupére la valeur saisie


fenetre.config(menu=menubar)

fenetre.mainloop()