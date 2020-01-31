# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:12:21 2020

@author: msardar2
"""
import pandas as pd
import numpy as np

def add_LCI(Name,Flow,LCI):
    if Name in LCI.columns:
        LCI[Name] = Flow + LCI[Name].values
    else:
        LCI[Name] = Flow
        
### Drum Feeder
def Drum_Feeder(input,sep_eff):
    removed =input * sep_eff
    residual =input - removed
    return(residual,removed)


### Drum Feeder
def Man_Sort(input,sep_eff):
    removed =input * sep_eff
    residual =input - removed
    return(residual,removed)

# =============================================================================
# A=flow()
# 
# from time import time
# B = time()
# for i in range(4000):
#     A=flow()
#     #C =deepcopy(A)
# print(time()-B)
# =============================================================================

