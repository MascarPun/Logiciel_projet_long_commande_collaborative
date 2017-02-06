import numpy as np
import numpy.linalg as alg
import time
import ctypes
from ctypes import *
import math
import control
from PIL import Image, ImageTk
import scipy as sp


from tkinter import * 
from tkinter.messagebox import *


try :
    
    fenetre = Tk()
        
    fenetre['bg']='white'
    

#    scrollbar = Scrollbar(fenetre)
#    scrollbar.pack(side=RIGHT, fill=Y)
#
#    listbox = Listbox(fenetre, yscrollcommand=scrollbar.set)
#    for i in range(1000):
#        listbox.insert(END, str(i))
#    listbox.pack(side=LEFT, fill=BOTH)
#
#    scrollbar.config(command=fenetre.yview)
#    
    
    
    
    #Label1
    l = LabelFrame(fenetre, text="Commande Collaborative", padx=20, pady=20)
#    l.pack(fill="both", expand="yes")
    l.grid(row=1,column=1)
     
    Label(l, text="Position de départ souhaitée").pack()
    
    #Label2
    l2 = LabelFrame(fenetre, text="Commande en profil de position", padx=20, pady=20)
#    l2.pack(fill="both", expand="yes")
    l2.grid(row=1,column=2)
     
    Label(l2, text="Position souhaitée").pack()
    
    #Label3
    l3 = LabelFrame(fenetre, text="Commande en echelon de position", padx=20, pady=20)
#    l3.pack(fill="both", expand="yes")
    l3.grid(row=2,column=1)
     
    Label(l3, text="Position souhaitée").pack()
    
    #Label4
    l4 = LabelFrame(fenetre, text="Commande en profil de vitesse", padx=20, pady=20)
#    l4.pack(fill="both", expand="yes")
    l4.grid(row=2,column=2)
     
    Label(l4, text="Vitesse souhaitée").pack()
    
    #Label5
    l5 = LabelFrame(fenetre, text="Commande en echelon de vitesse", padx=20, pady=20)
#    l5.pack(fill="both", expand="yes")
    l5.grid(row=3,column=1)
     
    Label(l5, text="Vitesse souhaitée").pack()
    
    #Label6
    l6 = LabelFrame(fenetre, text="Commande en courant", padx=20, pady=20)
#    l6.pack(fill="both", expand="yes")
    l6.grid(row=3,column=2)
     
    Label(l6, text="Courant souhaité").pack()
    
    #Label7
    l7 = LabelFrame(fenetre, text="Reset", padx=90, pady=50)
    #    l7.pack(fill="both", expand="yes")
    l7.grid(row=4,column=1)
    
    #Label8
    l8 = LabelFrame(fenetre, text="Quitter", padx=90, pady=50)
    #    l7.pack(fill="both", expand="yes")
    l8.grid(row=4,column=2)
     

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
    
    
    
    #variable en commande collaborative
    positionInitiale = DoubleVar()
    positionInitiale.set("")
    
    #variable en commande profil position
    positionProfilCommandee = DoubleVar() 
    positionProfilCommandee.set("")
    
    #variable en commande echelon position
    positionEchelonCommandee = DoubleVar() 
    positionEchelonCommandee.set("")
    
    
    #variable en commande profil vitesse
    vitesseProfilCommandee = IntVar()
    vitesseProfilCommandee.set("")
    
    #variable en commande echelon vitesse
    vitesseEchelonCommandee = IntVar()
    vitesseEchelonCommandee.set("")
    
    #variable en commande courant
    courantCommande = IntVar()
    courantCommande.set("")
    
    #commande collaborative
    def commandeCollaborative():
        import Commande_Collabo_spyder
        Commande_Collabo_spyder.mainCollabo(positionInitiale.get())
        
    
    #commande en profil position
    def commandeProfilPosition() :
        import Commande_Profil_Position
        Commande_Profil_Position.mainProfilPosition(positionProfilCommandee.get())
    
    
    def commandeEchelonPosition():
        import Commande_Echelon_Position
        Commande_Echelon_Position.mainEchelonPosition(positionEchelonCommandee.get())
    
    
    #commande en profil vitesse
    def commandeProfilVitesse():
        import Commande_Profil_Vitesse
        Commande_Profil_Vitesse.mainVitesse(vitesseProfilCommandee.get())
    
    #commande en enchelon vitesse
    def commandeEchelonVitesse():
        import Commande_Echelon_Vitesse
        Commande_Echelon_Vitesse.mainVitesse(vitesseEchelonCommandee.get()) 
        
        
    #commande en courant
    def commandeCourant():
        import Commande_Courant
        Commande_Courant.mainCourant(courantCommande.get())
        
    def resetMachine():
        import reset
        reset.mainReset()

    
    def callback():
        if askyesno('Titre 1', 'Êtes-vous sûr de vouloir faire ça?'):
            fenetre.destroy()
            top = Tk()
            top.title("Singe...")
            photo = PhotoImage(file="./maxresdefault_converted.gif") 
            label = Label(image=photo)
            label.image = photo # keep a reference!
            canvas = Canvas(top,width=500, height=500)
            canvas.create_image(0, 0, anchor=NW, image=photo)
            canvas.pack()
            
      
            
        else:
            showinfo('Titre 3', 'Vous avez peur!')
            showerror("Titre 4", "Aha")

        
        
    #entrée commande collaborative    
    entree = Entry(l, textvariable = positionInitiale, width=30)
    entree.pack()
    bouton = Button(l, text="Valider", command=commandeCollaborative)
    bouton.pack()
    
  
    #entrée commande en profil position
    entree2 = Entry(l2, textvariable=positionProfilCommandee, width=30)
    entree2.pack()
    bouton = Button(l2, text="Valider", command=commandeProfilPosition)
    bouton.pack()
    
    
    #entrée commande en profil position
    entree3 = Entry(l3, textvariable=positionEchelonCommandee, width=30)
    entree3.pack()
    bouton = Button(l3, text="Valider", command=commandeEchelonPosition)
    bouton.pack()
    
    
    #entrée commande en profil vitesse
    entree4 = Entry(l4, textvariable=vitesseProfilCommandee, width=30)
    entree4.pack()
    bouton = Button(l4, text="Valider", command=commandeProfilVitesse)
    bouton.pack()
    
    #entrée commande en echelon vitesse
    entree5 = Entry(l5, textvariable=vitesseEchelonCommandee, width=30)
    entree5.pack()
    bouton = Button(l5, text="Valider", command=commandeEchelonVitesse)
    bouton.pack()
    
    #entrée commande en courant
    entree6 = Entry(l6, textvariable=courantCommande, width=30)
    entree6.pack()
    bouton = Button(l6, text="Valider", command=commandeCourant)
    bouton.pack()
    
    #bouton Reset
    bouton = Button(l7, text="Reset", command=resetMachine)
    bouton.pack()
    
    #bouton Quitter
    boutonQuitter = Button(l8, text="Quitter", command=callback)
    boutonQuitter.pack()
    
    
    
    fenetre.config(menu=menubar)
    
    fenetre.mainloop()

  
    
except KeyboardInterrupt:
    print("Ne pas utiliser ce bouton pour arrêter la fenêtre !!!")
    fenetre.destroy()

    