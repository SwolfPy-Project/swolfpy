# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:41:00 2019

@author: msardar2
"""
import pandas as pd
from brightway2 import *
from biosphere_keys import *
def import_methods():
    keys = biosphere_keys
    
    bd=Database("biosphere3")
    
    bio_flows=[]
    for i in keys:
        bio_flows.append([keys[i][0],bd.get(keys[i][0][1])] )
      
    jj= pd.DataFrame(bio_flows)   
    
    ###jj.to_csv("SWOLF _ IPPC.csv") 
    ### Add the Characterization factors to the SWOLF_IPPC.csv file from the SWOLF and read it again to have characterization factors
    
    
    Data = pd.read_csv("SWOLF _ IPPC.csv")
    
    SWOLF_IPCC = []
    SWOLF_Acidification = []
    SWOLF_Eutrophication = []
    SWOLF_PhotochemicalSmog  = []
    SWOLF_CED = []
    SWOLF_Ecotoxicity = []
    SWOLF_HumanToxicity = []
    
    for i in range(len(Data.key)):
        if Data.CF1[i] != 0:
            SWOLF_IPCC.append(( jj[0][i], Data.CF1[i]))
        if Data.CF2[i] != 0:
            SWOLF_Acidification.append(( jj[0][i], Data.CF2[i]))
        if Data.CF3[i] != 0:
            SWOLF_Eutrophication.append(( jj[0][i], Data.CF3[i]))
        if Data.CF4[i] != 0:
            SWOLF_PhotochemicalSmog.append(( jj[0][i], Data.CF4[i]))
        if Data.CF5[i] != 0:
            SWOLF_CED.append(( jj[0][i], Data.CF5[i]))
        if Data.CF6[i] != 0:
            SWOLF_Ecotoxicity.append(( jj[0][i], Data.CF6[i]))
        if Data.CF7[i] != 0:
            SWOLF_HumanToxicity.append(( jj[0][i], Data.CF7[i]))
    
    Method(('SWOLF_IPCC','SWOLF')).register()
    Method(('SWOLF_IPCC','SWOLF')).write(SWOLF_IPCC)    
    
    Method(('SWOLF_Acidification','SWOLF')).register()
    Method(('SWOLF_Acidification','SWOLF')).write(SWOLF_Acidification)  
    
    Method(('SWOLF_Eutrophication','SWOLF')).register()
    Method(('SWOLF_Eutrophication','SWOLF')).write(SWOLF_Eutrophication)  
    
    Method(('SWOLF_PhotochemicalSmog','SWOLF')).register()
    Method(('SWOLF_PhotochemicalSmog','SWOLF')).write(SWOLF_PhotochemicalSmog)  
    
    Method(('SWOLF_CED','SWOLF')).register()
    Method(('SWOLF_CED','SWOLF')).write(SWOLF_CED)  
    
    Method(('SWOLF_Ecotoxicity','SWOLF')).register()
    Method(('SWOLF_Ecotoxicity','SWOLF')).write(SWOLF_Ecotoxicity)  
    
    Method(('SWOLF_HumanToxicity','SWOLF')).register()
    Method(('SWOLF_HumanToxicity','SWOLF')).write(SWOLF_HumanToxicity)  
    
    methods.flush()
