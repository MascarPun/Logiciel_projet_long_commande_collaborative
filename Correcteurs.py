#Ensemble des correcteurs du modèle
#chaque fonction rend un tableau de valeurs
#veiller a preciser deux conditions initiales

import numpy as np
import matplotlib as mat

#K,Ti,Td les parametres du correcteur
#Te periode echantillonnage
#retourne le kieme terme
# cmd, E1 et E2 sont les termes k, k-1 et k-2 en entree du pid
#S1 et S2 sont les termes en k-1 et k-2 de la sortie
def pid(K,Ti,Td,cmd,E1,E2,S1,S2,Te):
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

def pi(K,Ti,cmd,E1,S1,Te):
    num=[]
    denom=[]
    num.append(K+K*Te/(2*Ti))
    num.append(K*Te/(2*Ti)-K)
    denom.append(1)
    denom.append(-1)
    result=(num[1]*E1+num[0]*cmd-denom[1]*S1)/denom[0]
    return result