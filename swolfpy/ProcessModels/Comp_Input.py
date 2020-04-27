# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:56:34 2019

@author: msardar2
"""
from .InputData import InputData
from pathlib import Path

class Comp_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/Composting_Input.csv'

        # Initialize the superclass 
        super().__init__(self.input_data_path)

### Assumed Composition 
        self.Assumed_Comp = [0.1915,0.1447,0.1414,0.3977,0.0221,0.0035,0.0000,0.0031,0.0004,0.0035,0.0102,0.0019,0.0006,0.0015,
                             0.0019,0.0015,0.0000,0.0206,0.0011,0.0020,0.0038,0.0000,0.0000,0.0000,0.0055,0.0158,0.0008,0.0002,
                             0.0005,0.0006,0.0000,0.0000,0.0001,0.0077,0.0033,0.0022,0.0000,0.0000,0.0000,0.0102,0.0000,0.0000,
                             0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]