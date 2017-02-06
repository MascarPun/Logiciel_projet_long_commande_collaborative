import numpy as np
import numpy.linalg as alg
import time
import math
import control
import ctypes
from ctypes import *
from EposData import *
import Initialisation_CoMax 
from matplotlib.pylab import *

def mainReset():
    
    MyEpos = Initialisation_CoMax.MyEpos
    pErrorCode_i = Initialisation_CoMax.pErrorCode_i
    MyEpos.exitEpos(pErrorCode_i)
    MyEpos.initEpos(pErrorCode_i)