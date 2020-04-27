# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:11:58 2020

@author: msardar2
"""
from .InputData import InputData
from pathlib import Path

class SS_MRF_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/SS_MRF_Input.csv'
            
        # Initialize the superclass 
        super().__init__(self.input_data_path)

### Assumed Composition 
        self.Assumed_Comp = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.9,0.000001,19.5,17.8,0.000001,0.6,
                             0.000001,0.000001,0.000001,29.7,2.7,1.1,0.000001,2.1,0.6,0.000001,0.000001,0.6,1.5,1.2,0.4,0.7,0.2,
                             0.000001,0.4,0.000001,5.0,7.1,5.3,0.000001,0.3,0.6,1.5,0.000001,0.000001,0.000001,0.000001,0.000001,
                             0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,
                             0.000001,0.000001,0.000001,0.000001]