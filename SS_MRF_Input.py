# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:11:58 2020

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *
from MC import *

class SS_MRF_input(MC):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = 'AD_Input.csv'
            
        self.Data=pd.read_csv(self.input_data_path,dtype={'amount':float,'uncertainty_type':float,'loc':float,
                                                      'scale':float,'shape':float,'minimum':float,'maximum':float})
        # Setting uncertainty type to 0 : Undefined ; when it is not defined
        self.Data['uncertainty_type'].fillna(0,inplace=True)    
        self.Data=self.Data.where((pd.notnull(self.Data)),None)    
        self.Input_list = {}
        self.keys = self.Data.columns[3:]
        for i in range(len(self.Data)):
            if self.Data.Category[i] not in self.Input_list.keys():
                exec("self.%s = {}" % self.Data.Dictonary_Name[i])
                exec("self.Input_list[self.Data.Category[i]] = self.%s" % self.Data.Dictonary_Name[i])
                exec("self.%s[self.Data.Parameter[i]] = dict(zip(self.keys,self.Data.loc[i,'Name':]))" % self.Data.Dictonary_Name[i])
            else:
                exec("self.%s[self.Data.Parameter[i]] = dict(zip(self.keys,self.Data.loc[i,'Name':]))" % self.Data.Dictonary_Name[i])



### Assumed Composition 
        self.Assumed_Comp = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.9,0.000001,19.5,17.8,0.000001,0.6,
                             0.000001,0.000001,0.000001,29.7,2.7,1.1,0.000001,2.1,0.6,0.000001,0.000001,0.6,1.5,1.2,0.4,0.7,0.2,
                             0.000001,0.4,0.000001,5.0,7.1,5.3,0.000001,0.3,0.6,1.5,0.000001,0.000001,0.000001,0.000001,0.000001,
                             0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,
                             0.000001,0.000001,0.000001,0.000001]  
### Monte_carlo          
    def setup_MC(self,seed=None):
        super().__init__(self.Input_list)
        super().setup_MC(seed)




