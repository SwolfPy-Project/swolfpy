# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:16:05 2019

@author: msardar2
"""
from .InputData import InputData
from pathlib import Path

class AD_Input(InputData):
    def __init__(self,input_data_path = None):
        if input_data_path:
            self.input_data_path = input_data_path
        else:
            self.input_data_path = Path(__file__).parent.parent/'Data/AD_Input.csv'
        # Initialize the superclass 
        super().__init__(self.input_data_path)
            
### Assumed Composition 
        self.Assumed_Comp = [0.1587847314,0.1199794853,0.1172076820,0.3296762444,0.0824190611,0.0065468408,0.0000264482,
                             0.0058447349,0.0006849813,0.0065073226,0.0191333727,0.0034644248,0.0010472311,0.0028584798,
                             0.0036027383,0.0027399253,0.0000264482,0.0385170270,0.0021076349,0.0038200882,0.0070342313,
                             0.0000264482,0.0000264482,0.0000264482,0.0103537562,0.0295859243,0.0015148626,0.0002897998,
                             0.0009484357,0.0012118900,0.0000264482,0.0000264482,0.0001317272,0.0143846079,0.0061648320,
                             0.0041098880,0.0000264482,0.0000264482,0.0000264482,0.0190635573,0.0,0.0,0.0,0.0,0.0,0.0,
                             0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]  