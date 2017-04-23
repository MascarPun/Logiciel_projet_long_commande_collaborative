#Ensemble des correcteurs du modèle
#chaque fonction rend un tableau de valeurs
#veiller a preciser deux conditions initiales

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
def pi(K,Ti,err):
    somme_err=sum(err[k] for k in range(len(err)-1))
    result=K*err[-1]+(K/Ti)*somme_err
    return result

def pid(K,Ti,Td,err):
    somme_err=sum(err[k] for k in range(len(err)-1))
    delta_err=err[-1]-err[-2]
    result=K*err[-1]+(K/Ti)*somme_err+(K*Td)*delta_err
    return result

#version de correction qui n'utlise pas de transformation bilinéaire
#prend en argument un tableau avec les valeurs de la commande et la periode d echantillonnage
#On suppose que la carte epos est deja initialisee

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        return (time.time() - startTime_for_tictoc)

def pos2current(Kpid,Tipid,Tdpid,cmd,Te,carteEpos,S,current,err):
    qc2mm = 294
    pPositionIs = c_long(0)
    carteEpos.getPositionIs(pPositionIs, pErrorCode_i) # mesure de position initiale
    positionDepartLueMm = pPositionIs.value/qc2mm # conversion qc en mm
    S.append(positionDepartLueMm)
    err.append(cmd-S[-1])
    current.append(pid(Kpid,Tipid,Tdpid,cmd,S,err))
    return [current,S,err]


