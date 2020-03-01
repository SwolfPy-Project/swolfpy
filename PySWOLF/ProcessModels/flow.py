# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:41:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd

### Flow
class flow:
    def __init__(self,Material_Properties):
        self.prop = Material_Properties
        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
              'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
              'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
              'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
              'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
              'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
              'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
              'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
              'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        self.data = pd.DataFrame(index = self.Index,columns=['mass','sol_cont','moist_cont','vs_cont','ash_cont'])
### Update flow        
    def update(self,assumed_comp): 
        self.flow = sum(self.data['mass'].values*assumed_comp.values)
        self.water = sum(self.data['moist_cont'].values*assumed_comp.values)
        self.moist_cont = self.water / self.flow
        self.ash = sum(self.data['ash_cont'].values*assumed_comp.values)
        self.solid = sum(self.data['sol_cont'].values*assumed_comp.values)

### Create new flow
    def init_flow(self,massflows):
        self.data['mass']= massflows
        self.data['sol_cont'] = self.data['mass'].values * (1-self.prop['Moisture Content'].values/100)
        self.data['moist_cont'] = self.data['mass'].values * (self.prop['Moisture Content'].values/100)
        self.data['vs_cont'] = self.data['sol_cont'].values * self.prop['Volatile Solids'].values/100
        self.data['ash_cont'] = self.data['sol_cont'].values * self.prop['Ash Content'].values/100