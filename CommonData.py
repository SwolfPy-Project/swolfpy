# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 20:05:32 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *
class CommonData:
    def __init__(self):
        ### Molecular Weights
        self.MW= {"C":{"Name":"Carbon MW","amount":12.011,"unit":"g/mol","Reference":None},
                "P":{"Name":"Phosphorus MW","amount":30.974,"unit":"g/mol","Reference":None},
                "H":{"Name":"Hydrogen MW","amount":1.008,"unit":"g/mol","Reference":None},
                "N":{"Name":"Nitrogen MW","amount":14.007,"unit":"g/mol","Reference":None},
                "O":{"Name":"Oxygen MW","amount":15.999,"unit":"g/mol","Reference":None},
                "K":{"Name":"K MW","amount":39.098,"unit":"g/mol","Reference":None},
                "S":{"Name":"S MW","amount":32.065,"unit":None,"Reference":None},
                "Cl":{"Name":"Cl MW","amount":35.453,"unit":None,"Reference":None},
                "H2":{"Name":"H2 MW","amount":2 * 1.008 ,"unit":"g/mol","Reference":None},
                "CO":{"Name":"CO MW","amount":12.011+15.999  ,"unit":"g/mol","Reference":None},
                "CO2":{"Name":"CO2 MW","amount":15.999 * 2 +12.011 ,"unit":"g/mol","Reference":None},
                "CH4":{"Name":"CH4 MW","amount":12.011 + 4 * 1.008,"unit":"g/mol","Reference":None},
                "H2O":{"Name":"H2O MW","amount":15.999 + 2 * 1.008,"unit":"g/mol","Reference":None},
                "SO2":{"Name":"SO2 MW","amount":2 * 15.999 + 32.065,"unit":"g/mol","Reference":None},
                "HCl":{"Name":"HCl MW","amount": 35.453 + 1.008 ,"unit":"g/mol","Reference":None},
                "NOx":{"Name":"HCl MW","amount": 14.007 + 2 * 15.999 ,"unit":"g/mol","Reference":None},
                "Hydrocarbons":{"Name":"Hydrocarbons MW","amount":86.18,"unit":None,"Reference":None},
                "Nitrous_Oxide":{"Name":"Nitrous_Oxide MW","amount": 2 * 14.007 + 15.999 ,"unit":None,"Reference":None},
                "Ammonia":{"Name":"Ammonia MW","amount": 14.007 + 3 * 1.008 ,"unit":None,"Reference":None}
                }      
        
        ### Unit Conversion
        self.UC = {'BTU_KJ':{"Name":"BTU to KJ","amount":1.055,"unit":"kJ","Reference":None},
                  'KJ_BTU':{"Name":"KJ to BTU","amount":1 / 1.055,"unit":"BTU","Reference":None}}
        
        
        ### STP Measurements
        self.STP = {'mole_to_L':{"Name":"mole to Liter","amount":22.41 ,"unit":"L","Reference":None},
                   'm3CH4_to_kg':{"Name":"m3 CH4 to kg CH4","amount": 0.716 ,"unit":"kg","Reference":None},
                   'm3CO2_to_kg':{"Name":"m3 CO2 to kg","amount": self.MW['CO2']['amount']/22.41 ,"unit":"kg","Reference":None},
                   "Density_Air":{"Name":"Density_Air","amount":22.4,"unit":"L/mol","Reference":None}
                   }
        
        self.Evap_heat = {"Water_Evap_Heat":{"Name":"Water_Evap_Heat","amount":2.26,"unit":"MJ/Kg","Reference":None}}