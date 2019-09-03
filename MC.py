# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:49:46 2019

@author: msardar2
"""
from stats_arrays import *
import numpy as np

class MC():
    def __init__(self,input_list):
        self.input_list = input_list
        
    def setup_MC(self,seed=None):
        self.list_var = list()
        self.sens_analysis={}
        self.run_index=0
        self.max_run = 10000000
        k=0
        for x in self.input_list.values():
            for y in x:
                self.list_var.append(x[y])
                if 'list' in x[y].keys():
                    self.sens_analysis[k] = x[y]['list']
                    self.max_run = min(self.max_run,len(x[y]['list']))
                k+=1
        self.Vars  = UncertaintyBase.from_dicts(*self.list_var)
        self.rand = MCRandomNumberGenerator(self.Vars,seed=seed)
      
    def gen_MC(self):
        data = self.rand.next()
        if len(self.sens_analysis) > 0:
            for x in self.sens_analysis.keys():
                data[x] = self.sens_analysis[x][self.run_index] 
            self.run_index+=1
            if self.run_index >= self.max_run:
                raise ValueError('Number of runs are more than the number of defined inputs') 
        i=0
        Variables = []
        for x in self.input_list.keys():
            for y in self.input_list[x]:
                if not np.isnan(data[i]):  
                    self.input_list[x][y]['amount'] = data[i]
                    Variables.append( ( (x , y) , data[i]) )
                i+=1
        return(Variables)
