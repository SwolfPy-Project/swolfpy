# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 22:52:32 2019

@author: msmsa
"""
import pandas as pd
import numpy as np
from stats_arrays import *
from MC import *

class SF_collection_Input(MC):
    def __init__(self):
        self.Data=pd.read_csv('SF_collection_Input.csv',dtype={'amount':float,'uncertainty_type':float,'loc':float,
                                                      'scale':float,'shape':float,'minimum':float,'maximum':float})
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
        
        




