# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:51:15 2020

@author: msmsa
"""
from .InputData import InputData
from pathlib import Path

class Reproc_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/Reprocessing_Input.csv'
        
        # Initialize the superclass 
        super().__init__(self.input_data_path,eval_parameter=True)                  