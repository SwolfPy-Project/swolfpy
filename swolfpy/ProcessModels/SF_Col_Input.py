# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 22:52:32 2019

@author: msmsa
"""
from .InputData import InputData
from pathlib import Path

class SF_Col_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/SF_collection_Input.csv'
        
        # Initialize the superclass 
        super().__init__(self.input_data_path)