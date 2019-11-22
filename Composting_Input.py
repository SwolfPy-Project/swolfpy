# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:56:34 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *
from MC import *

class Composting_input(MC):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = 'Composting_Input.csv'
            
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
        self.Assumed_Comp = [0.1915,0.1447,0.1414,0.3977,0.0221,0.0035,0.0000,0.0031,0.0004,0.0035,0.0102,0.0019,0.0006,0.0015,
                             0.0019,0.0015,0.0000,0.0206,0.0011,0.0020,0.0038,0.0000,0.0000,0.0000,0.0055,0.0158,0.0008,0.0002,
                             0.0005,0.0006,0.0000,0.0000,0.0001,0.0077,0.0033,0.0022,0.0000,0.0000,0.0000,0.0102,0.0000,0.0000,
                             0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]


### Monte_carlo          
    def setup_MC(self,seed=None):
        super().__init__(self.Input_list)
        super().setup_MC(seed)





