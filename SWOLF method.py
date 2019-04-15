# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:41:00 2019

@author: msardar2
"""
import pandas as pd
from brightway2 import *
from biosphere_keys import *

keys = biosphere_keys

bd=Database("biosphere3")

bio_flows=[]
for i in keys:
    bio_flows.append([keys[i][0],bd.get(keys[i][0][1])] )
  
jj= pd.DataFrame(bio_flows)   

###jj.to_csv("SWOLF _ IPPC.csv") 
### Add the Characterization factors to the SWOLF_IPPC.csv file from the SWOLF and read it again to have characterization factors


Data = pd.read_csv("SWOLF _ IPPC.csv")

IPCC_SWOLF = []
for i in range(len(Data.key)):
    if Data.CF[i] != 0:
        IPCC_SWOLF.append(( jj[0][i], Data.CF[i]))

Method(('IPCC_2007_SWOLF','climate change','GWP100yr')).register()
Method(('IPCC_2007_SWOLF','climate change','GWP100yr')).write(IPCC_SWOLF)    
methods.flush()
