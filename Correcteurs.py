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
def pi(K,Ti,err):
    somme_err=sum(err[k] for k in range(len(err)-1))
    result=K*err[-1]+(K/Ti)*somme_err
    return result



def pi_sat(K,Ti,err,Sat,ValParDefaut):
    somme_err = sum(err[k] for k in range(len(err) - 1))
    result = K * err[-1] + (K / Ti) * somme_err
    if Sat==0:
        Sat=ValParDefaut
    if result>Sat:
        result = K*err[-1] + ((Sat-result)/Ti+(K / Ti))*somme_err
    return result

#pid bourrin (mais qui marche bien)
def pid(K,Ti,Td,err):
    somme_err=sum(err[k] for k in range(len(err)-1))
    delta_err=err[-1]-err[-2]
    result=K*err[-1]+(K/Ti)*somme_err+(K*Td)*delta_err
    return result


def pid_sat(K,Ti,Td,err,Sat,ValParDefaut):
    somme_err=sum(err[k] for k in range(len(err)-1))
    delta_err=err[-1]-err[-2]
    result=K*err[-1]+(K/Ti)*somme_err+(K*Td)*delta_err
    if Sat==0:
        Sat=ValParDefaut
    if result>Sat:
        result = K*err[-1] + ((Sat-result)/Ti+(K / Ti))*somme_err + (K*Td)*delta_err
    return result

#correcteur proportionnel
def prop(K,err):
    return K*err[-1]



#version de correction qui n'utlise pas de transformation bilinéaire
#prend en argument un tableau avec les valeurs de la commande et la periode d echantillonnage
#On suppose que la carte epos est deja initialisee



#LES FONCTIONS SUIVANTES SONT A ITERER

#permet d'avoir en sortie un courant qu'il faudra ensuite corriger avec current_cmd()
def pos2current(K,Ti,Td,cmd,carteEpos,S,courant,err,pErrorCode_i):
    qc2mm = 294
    pPositionIs = c_long(0)
    carteEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/qc2mm # conversion qc en mm
    S.append(positionDepartLueMm)
    err.append(cmd-S[-1])
    if Td=='' and Ti!='':
        courant.append(pi(K,Ti,err))
    elif Td=='' and Ti=='':
        courant.append(prop(K,err))
    else:
        courant.append(pid(K,Ti,Td,err))
    return [courant,S,err]


def pos2current_sat(K,Ti,Td,Sat,ValParDefaut,cmd,carteEpos,S,courant,err,pErrorCode_i):
    qc2mm = 294
    pPositionIs = c_long(0)
    carteEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/qc2mm # conversion qc en mm
    S.append(positionDepartLueMm)
    err.append(cmd-S[-1])
    if Td=='' and Ti!='':
        courant.append(pi_sat(K,Ti,err,Sat,ValParDefaut))
    elif Td=='' and Ti=='':
        courant.append(prop(K,err))
    else:
        courant.append(pid_sat(K,Ti,Td,err,Sat,ValParDefaut))
    return [courant,S,err]


#permet d'avoir en sortie une vitesse qu'il faudra ensuite corriger avec vit2current puis current_cmd()
#fonction identique à la precedente mais nom différent pour plus de lisibilite
def pos2velocity(K,Ti,Td,cmd,carteEpos,S,vitesse,err,pErrorCode_i):
    qc2mm = 294
    pPositionIs = c_long(0)
    carteEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/qc2mm # conversion qc en mm
    S.append(positionDepartLueMm)
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        vitesse.append(pi(K,Ti,err))
    elif Td==0 and Ti==0:
        vitesse.append(prop(K,err))
    else:
        vitesse.append(pid(K,Ti,Td,err))
    return [vitesse,S,err]


def pos2velocity_sat(K,Ti,Td,Sat,ValParDefaut,cmd,carteEpos,S,vitesse,err,pErrorCode_i):
    qc2mm = 294
    pPositionIs = c_long(0)
    carteEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/qc2mm # conversion qc en mm
    S.append(positionDepartLueMm)
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        vitesse.append(pi_sat(K,Ti,err,Sat,ValParDefaut))
    elif Td==0 and Ti==0:
        vitesse.append(prop(K,err))
    else:
        vitesse.append(pid_sat(K,Ti,Td,err,Sat,ValParDefaut))
    return [vitesse,S,err]


#conversion de la vitesse en courant
def velocity2current(K,Ti,Td,cmd,carteEpos,S,courant,err,pErrorCode_i,pVelocityIs_i):
    S.append(carteEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i))
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        courant.append(pi(K,Ti,err))
    elif Td==0 and Ti==0:
        courant.append(prop(K,err))
    else:
        courant.append(pid(K,Ti,Td,err))
    return [courant,S,err]

def velocity2current_sat(K,Ti,Td,Sat,ValParDefaut,cmd,carteEpos,S,courant,err,pErrorCode_i,pVelocityIs_i):
    S.append(carteEpos.getVelocityIs(pVelocityIs_i, pErrorCode_i))
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        courant.append(pi_sat(K,Ti,err,Sat,ValParDefaut))
    elif Td==0 and Ti==0:
        courant.append(prop(K,err))
    else:
        courant.append(pid_sat(K,Ti,Td,err,Sat,ValParDefaut))
    return [courant,S,err]


#boucle de courant avec pi courant
#S sortie en courant du modele et courantC est le courant en sortie du correcteur
def courant_cmd(cmd,S,err,carteEpos,K,Ti,Td,courantC,pErrorCode_i,pCurrentIs_i):
    S.append(carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)) #je reprends la notation du controleur
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        courantC.append(pi(K,Ti,err))
    elif Td==0 and Ti==0:
        courantC.append(prop(K,err))
    else:
        courantC.append(pid(K,Ti,Td,err))
    return [courantC,S,err]


def courant_cmd_sat(cmd,S,err,Sat,ValParDefaut,carteEpos,K,Ti,Td,courantC,pErrorCode_i,pCurrentIs_i):
    S.append(carteEpos.getCurrentIs(pCurrentIs_i, pErrorCode_i)) #je reprends la notation du controleur
    err.append(cmd-S[-1])
    if Td==0 and Ti!=0:
        courantC.append(pi_sat(K,Ti,err,Sat,ValParDefaut))
    elif Td==0 and Ti==0:
        courantC.append(prop(K,err))
    else:
        courantC.append(pid_sat(K,Ti,Td,err,Sat,ValParDefaut))
    return [courantC,S,err]

#pour l instant bcp d'arguments mais visuellement c est plsu simple a comprendre que des tableaux
#def regulation_cascade(Kvit,Kpos,Kcour,Tivit,Tipos,Ticour,Tdvit,Tdpos,Tdcour,cmd,errvit,errpos,errcour,Svit,Spos,Scour,courantC,vitesseC,pErrorCode_i,pCurrentIs_i,pVelocityIs_i,carteEpos):
#    cmdVit=pos2velocity(Kpos, Tipos, Tdpos, cmd, carteEpos, Spos, vitesseC, errpos, pErrorCode_i)[0] #on recupere la vitesse corrigee
#    cmdCurrent=velocity2current(Kvit,Tivit,Tdvit,cmdVit,carteEpos,Svit,courant,errvit,pErrorCode_i,pVelocityIs_i)





#def regulation_vitesse():



#def regulation_position():


#def regulation_courant():






