# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:46:21 2020

@author: msardar2
"""
import numpy as np
import pandas as pd
from ..process_model_output import *
from stats_arrays import *
from pathlib import Path

class Reprocessing:
    def __init__(self,input_data_path=None,CommonDataObjct=None):
        self.Reprocessing = ProcessModelOutput()
    
    def calc(self):
        self.LCI = self.Reprocessing.read_output_from_SWOLF('ReProc',Path(__file__).parent.parent/"Data/Material_Reprocessing_BW2.csv")
    
    def setup_MC(self,seed=None):
        pass
    
    def MC_calc(self):      
        pass
        
    def report(self):
        return(self.LCI)