# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:25:05 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from MC import *
class WTE_input(MC):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = 'WTE_Input.csv'
            
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

### Update_Input
    def Update_input(self,NewData):
        for i in NewData.index:
            exec("self.%s[NewData.Parameter[i]] = dict(zip(self.keys,NewData.loc[i,'Name':]))" %NewData.Dictonary_Name[i])
            self.Data.loc[i]=NewData.loc[i]
            
### Monte_carlo          
    def setup_MC(self,seed=None):
        super().__init__(self.Input_list)
        super().setup_MC(seed)