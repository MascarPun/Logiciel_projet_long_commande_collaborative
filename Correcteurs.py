#Ensemble des correcteurs du modèle
#chaque fonction rend un tableau de valeurs
#ATTENTION NE FONCTIONNE QUE SI LA CARTE EPOS EST INITIALIEE AVANT

import numpy as np
import matplotlib as mat
from EposData import *
import ctypes
from ctypes import *
from Parametre import Parametre



#K,Ti,Td les parametres du correcteur
#Te periode echantillonnage
#retourne le kieme terme
# cmd, E1 et E2 sont les termes k, k-1 et k-2 en entree du pid
#S1 et S2 sont les termes en k-1 et k-2 de la sortie
def pid_bilin(K,Ti,Td,cmd,E1,E2,S1,S2,Te):
    #ecriture de la transformee en z du pid (num/denom)
    num=[]
    denom=[]
    num.append((K*Te/(2*Ti))+(K*Td/(16*Ti))+(2*K*Td/Te)+K+(K*Td/(8*Te)))
    num.append((1-(Td/(8*Te)))*K*Te/(2*Ti)+(K*Te/(2*Ti))+(K*Td/(16*Ti))+(1+(Td/(8*Te)))*K -4*K*Td/Te-K-K*Td/(8*Te))
    num.append((1-Td/(8*Te))*K*Te/(2*Ti)+2*K*Td/Te-K*(1+Td/(8*Te)))
    denom.append(1+Td/(8*Te))
    denom.append(-Td/(4*Te))
    denom.append(-(1-Td/(8*Te)))
    result = (num[2]*E2 + num[1]*E1 + num[0]*cmd - denom[2]*S2 -denom[1]*S1)/denom[0]
    return result

def pi_bilin(K,Ti,cmd,E1,S1,Te):
    num=[]
    denom=[]
    num.append(K+K*Te/(2*Ti))
    num.append(K*Te/(2*Ti)-K)
    denom.append(1)
    denom.append(-1)
    result=(num[1]*E1+num[0]*cmd-denom[1]*S1)/denom[0]
    return result


#pi mais en version un peu plus bourrin
#err=tableau avec les erreurs
def pi(K,Ti,err,somme_err,Te):
    result=K*err+(K/Ti)*somme_err*Te
    return result



def pi_sat(K,Ti,err,somme_err,Sat,Te):
    result = K * err + (K / Ti) * somme_err*Te
    if result>Sat:
        result = K*err + ((Sat-result)/Ti+(K / Ti))*somme_err*Te
    return result

#pid bourrin (mais qui marche bien)
def pid(K,Ti,Td,err,somme_err,Te):
    delta_err=(err[-1]-err[-2])/Te
    result=K*err[-1]+(K/Ti)*somme_err*Te+(K*Td)*delta_err
    return result


def pid_sat(K,Ti,Td,err,somme_err,Sat,Te):
    delta_err=(err[-1]-err[-2])/Te
    result=K*err[-1]+(K/Ti)*somme_err*Te+(K*Td)*delta_err
    if result>Sat:
        result = K*err[-1] + ((Sat-result)/Ti+(K / Ti))*somme_err*Te + (K*Td)*delta_err
    return result

#correcteur proportionnel
def prop(K,err):
    return K*err



#version de correction qui n'utlise pas de transformation bilinéaire
#prend en argument un tableau avec les valeurs de la commande et la periode d echantillonnage
#On suppose que la carte epos est deja initialisee



#LES FONCTIONS SUIVANTES SONT A ITERER

#permet d'avoir en sortie un courant qu'il faudra ensuite corriger avec current_cmd()
def pos2current(K,Ti,Td,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courant=pi(K,Ti,err[-1],somme_err,Te)
    elif Td=='' and Ti=='':
        courant=prop(K,err[-1])
    else:
        courant=pid(K,Ti,Td,err,somme_err,Te)
    return courant


def pos2current_sat(K,Ti,Td,Sat,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courant=pi_sat(K,Ti,err[-1],somme_err,Sat,Te)
    elif Td=='' and Ti=='':
        courant=prop(K,err[-1])
    else:
        courant=pid_sat(K,Ti,Td,err,somme_err,Sat,Te)
    return courant


#permet d'avoir en sortie une vitesse qu'il faudra ensuite corriger avec vit2current puis current_cmd()
#fonction identique à la precedente mais nom différent pour plus de lisibilite
def pos2velocity(K,Ti,Td,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        vitesse=pi(K,Ti,err[-1],somme_err,Te)
    elif Td=='' and Ti=='':
        vitesse=prop(K,err[-1])
    else:
        vitesse=pid(K,Ti,Td,err,somme_err,Te)
    return vitesse


def pos2velocity_sat(K,Ti,Td,Sat,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        vitesse=pi_sat(K,Ti,err[-1],somme_err,Sat,Te)
    elif Td=='' and Ti=='':
        vitesse=prop(K,err[-1])
    else:
        vitesse=pid_sat(K,Ti,Td,err,somme_err,Sat,Te)
    return vitesse


#conversion de la vitesse en courant
def velocity2current(K,Ti,Td,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courant=pi(K,Ti,err[-1],somme_err,Te)
    elif Td=='' and Ti=='':
        courant=prop(K,err[-1])
    else:
        courant=pid(K,Ti,Td,err,somme_err,Te)
    return courant,somme_err

def velocity2current_sat(K,Ti,Td,Sat,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courant=pi_sat(K,Ti,err[-1],somme_err,Sat,Te)
    elif Td=='' and Ti=='':
        courant=prop(K,err[-1])
    else:
        courant=pid_sat(K,Ti,Td,err,somme_err,Sat,Te)
    return courant,somme_err


#boucle de courant avec pi courant
#S sortie en courant du modele et courantC est le courant en sortie du correcteur
def courant_cmd(K,Ti,Td,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courantC=pi(K,Ti,err[-1],somme_err,Te)
    elif Td=='' and Ti=='':
        courantC=prop(K,err[-1])
    else:
        courantC=pid(K,Ti,Td,err,somme_err,Te)
    return courantC


def courant_cmd_sat(K,Ti,Td,Sat,cmd,S,err,somme_err,Te):
    err[0]=err[1]
    err[1]=cmd-S
    somme_err+=err[1]
    if Td=='' and Ti!='':
        courantC=pi_sat(K,Ti,err[-1],somme_err,Sat,Te)
    elif Td=='' and Ti=='':
        courantC=prop(K,err[-1])
    else:
        courantC=pid_sat(K,Ti,Td,err,somme_err,Sat,Te)
    return courantC

#pour l instant bcp d'arguments mais visuellement c est plsu simple a comprendre que des tableaux
#def regulation_cascade(Kvit,Kpos,Kcour,Tivit,Tipos,Ticour,Tdvit,Tdpos,Tdcour,cmd,errvit,errpos,errcour,Svit,Spos,Scour,courantC,vitesseC,pErrorCode_i,pCurrentIs_i,pVelocityIs_i,carteEpos):
#    cmdVit=pos2velocity(Kpos, Tipos, Tdpos, cmd, carteEpos, Spos, vitesseC, errpos, pErrorCode_i)[0] #on recupere la vitesse corrigee
#    cmdCurrent=velocity2current(Kvit,Tivit,Tdvit,cmdVit,carteEpos,Svit,courant,errvit,pErrorCode_i,pVelocityIs_i)





#def regulation_vitesse():



#def regulation_position():


#def regulation_courant():






