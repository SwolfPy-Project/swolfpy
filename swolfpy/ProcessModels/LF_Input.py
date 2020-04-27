# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:26:54 2019

@author: msardar2
"""
from .InputData import InputData
from pathlib import Path

class LF_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/LF_Input.csv'

        # Initialize the superclass 
        super().__init__(self.input_data_path)