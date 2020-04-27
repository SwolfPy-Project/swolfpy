# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:46:21 2020

@author: msardar2
"""
import numpy as np
import pandas as pd
from .ProcessModel import *
from .Reproc_Input import *

class Reproc(ProcessModel):
    Process_Type = 'Reprocessing'
    def __init__(self,input_data_path=None,CommonDataObjct=None):
        super().__init__(CommonDataObjct)
        
        self.InputData= Reproc_Input(input_data_path)
        
    def calc(self):
        self.Biosphere = {}
        self.Technosphere = {}
        self.Waste={}
        
        for act in self.CommonData.Reprocessing_Index:
            self.Biosphere[act] = {}
            self.Technosphere[act] = {}
            self.Waste[act] = {}
            if act in self.InputData.Input_list.keys():
                for exchange in self.InputData.Input_list[act].keys():
                    if exchange[0] == 'Technosphere':
                        self.Technosphere[act][exchange]=self.InputData.Input_list[act][exchange]['amount']
                    elif exchange[0] == 'biosphere3':
                        self.Biosphere[act][exchange]=self.InputData.Input_list[act][exchange]['amount']
                        
        #self.LCI = self.Reprocessing.read_output_from_SWOLF('ReProc',Path(__file__).parent.parent/"Data/Material_Reprocessing_BW2.csv")
    
    def setup_MC(self,seed=None):
        self.InputData.setup_MC(seed)
    
    def MC_calc(self):      
        input_list = self.InputData.gen_MC()
        self.calc()
        return(input_list)

        
    def report(self):
        self.REPROC = {}
        self.REPROC["process name"] = 'REPROC'
        self.REPROC["Biosphere"] = self.Biosphere
        self.REPROC["Technosphere"] = self.Technosphere
        self.REPROC["Waste"]= self.Waste
        return(self.REPROC)
