# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:26:54 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *

class LF_input:
    def __init__(self):
        self.Data=pd.read_csv('LF_Input.csv',dtype={'amount':float,'uncertainty_type':float,'loc':float,
                                                      'scale':float,'shape':float,'minimum':float,'maximum':float})
        #self.Data.fillna('',inplace=True)
        self.Input_list = {}
        self.keys = self.Data.columns[3:]
        for i in range(len(self.Data)):
            if self.Data.Category[i] not in self.Input_list.keys():
                exec("self.%s = {}" % self.Data.Dictonary_Name[i])
                exec("self.Input_list[self.Data.Category[i]] = self.%s" % self.Data.Dictonary_Name[i])
                exec("self.%s[self.Data.Parameter[i]] = dict(zip(self.keys,self.Data.loc[i,'Name':]))" % self.Data.Dictonary_Name[i])
            else:
                exec("self.%s[self.Data.Parameter[i]] = dict(zip(self.keys,self.Data.loc[i,'Name':]))" % self.Data.Dictonary_Name[i])

A = LF_input()
AAA=A.Data
AAAA=A.Input_list                    
