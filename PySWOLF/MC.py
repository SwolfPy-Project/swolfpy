# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:49:46 2019

@author: msardar2
"""
from stats_arrays import *
import numpy as np
import pandas as pd
from pathlib import Path

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
            if self.run_index > self.max_run:
                raise ValueError('Number of runs are more than the number of defined inputs') 
        i=0
        variables = []
        for x in self.input_list.keys():
            for y in self.input_list[x]:
                if not np.isnan(data[i]):  
                    self.input_list[x][y]['amount'] = data[i]
                    variables.append( ( (x , y) , data[i]) )
                i+=1
        return(variables)
		
    def create_uncertainty_from_inputs(self,sheet_name,process_data,seed=None):
        self.process_data=process_data
        self.process_data_1=pd.read_excel(Path(__file__).parent/'Data/Material properties - process modles.xlsx', sheet_name = sheet_name, index_col = 'Parameter')
        self.uncertain_dict = dict()
        cols = list(self.process_data_1)
        for col in range(0,len(cols),7):
            self.uncertain_dict[cols[col]] = list()
            for val in range(len(self.process_data[cols[col]][3:])):
                self.uncertain_dict[cols[col]].append(dict())
                if not np.isnan(self.process_data_1[cols[col+1]][3+val]):
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = int(self.process_data_1[cols[col+1]][3+val])
                    self.uncertain_dict[cols[col]][val]['loc'] = self.process_data_1[cols[col+2]][3+val]
                    self.uncertain_dict[cols[col]][val]['scale'] = self.process_data_1[cols[col+3]][3+val]
                    self.uncertain_dict[cols[col]][val]['shape'] = self.process_data_1[cols[col+4]][3+val]
                    self.uncertain_dict[cols[col]][val]['minimum'] = self.process_data_1[cols[col+5]][3+val]
                    self.uncertain_dict[cols[col]][val]['maximum'] = self.process_data_1[cols[col+6]][3+val]
                else:
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = 1
							
        self.variables = dict()
        self.rng = dict()
        for key in self.uncertain_dict.keys():
            self.variables[key] = UncertaintyBase.from_dicts(*self.uncertain_dict[key])
            self.rng[key] = MCRandomNumberGenerator(self.variables[key],seed=seed)
		
    def uncertainty_input_next(self):
        data = dict()
        variables = list()
        for key in self.rng.keys():
            data[key] = self.rng[key].next()
            for val in range(len(self.process_data[key][3:])):
                if not np.isnan(data[key][val]):			
                    self.process_data.at[(self.process_data_1.index.values[3+val]),key] = data[key][val]
                    variables.append(((key,self.process_data_1.index.values[3+val]),data[key][val]))
        return variables
	
