# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:59:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
from Comp_Input import *
from CommonData import *
from stats_arrays import *

class Comp:
    def __init__(self):
        self.CommonData = CommonData()
        self.Comp_input= Comp_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'Composting', index_col = 'Parameter')
        self.Index = self.CommonData.Index
        
    def calc(self):

        ### Mass Flows
        self.Mass_flows=pd.DataFrame(index = self.Index)
        
        self.Mass_flows ['Mass at tipping floor'] = 1000
        self.Mass_flows.loc ['Unit', 'Mass at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass at tipping floor'] = self.Mass_flows ['Mass at tipping floor'] * (1 - self.Material_Properties['Moisture Content'][4:]/100)
        self.Mass_flows.loc ['Unit', 'Dry mass at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash at tipping floor'] = self.Mass_flows ['Dry mass at tipping floor'] * self.Material_Properties['Ash Content'][4:]/100
        self.Mass_flows.loc ['Unit', 'Mass of ash at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)'] = self.Mass_flows ['Mass at tipping floor'] * ( 1- self.process_data['Percent screened out in primary pre-screening (shredded)'][3:]/100)
        self.Mass_flows.loc ['Unit', 'Mass of unders in primary pre-screen (not shredded)'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of overs from primary screen'] = self.Mass_flows ['Mass at tipping floor'][1:] - self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)']
        self.Mass_flows.loc ['Unit','Mass of overs from primary screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'] = self.Mass_flows ['Mass of overs from primary screen'] * self.process_data['Percent screened out in secondary pre-screening (residual not sent to composting)'][3:]/100
        self.Mass_flows.loc ['Unit','Mass screened out in secondary pre-screen (to residual)'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass screened out in secondary pre-screen'] =  self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'] * (1 - self.Material_Properties['Moisture Content'][4:]/100)
        self.Mass_flows.loc ['Unit','Dry mass screened out in secondary pre-screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash screened out in secondary pre-screen'] =  self.Mass_flows ['Dry mass screened out in secondary pre-screen'] * self.Material_Properties['Ash Content'][4:]/100
        self.Mass_flows.loc ['Unit','Mass of ash screened out in secondary pre-screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass to shredding'] =  self.Mass_flows ['Mass of overs from primary screen'] - self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'][1:]
        self.Mass_flows.loc ['Unit','Mass to shredding'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of substrate to active composting'] =  self.Mass_flows ['Mass to shredding'][1:] + self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)']
        self.Mass_flows.loc ['Unit','Mass of substrate to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass of substrate to active composting'] =  self.Mass_flows ['Mass of substrate to active composting'][1:] * (1 - self.Material_Properties['Moisture Content'][4:]/100) 
        self.Mass_flows.loc ['Unit','Dry mass of substrate to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of VS in substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][1:] * self.Material_Properties['Volatile Solids'][4:]/100
        self.Mass_flows.loc ['Unit','Mass of VS in substrates to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash in substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][1:] - self.Mass_flows ['Mass of VS in substrates to active composting'][1:]
        self.Mass_flows.loc ['Unit','Mass of ash in substrates to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of C in degradable substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][1:] * self.Material_Properties['Biogenic Carbon Content'][4:]/100 *self.process_data['Degrades'][3:]
        self.Mass_flows.loc ['Unit','Mass of C in degradable substrates to active composting'] = 'kg-C/Mg feedstock'
        
        self.Mass_flows ['Mass of N in degradable substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][1:] * self.Material_Properties['Nitrogen Content'][4:]/100 *self.process_data['Degrades'][3:]
        self.Mass_flows.loc ['Unit','Mass of N in degradable substrates to active composting'] = 'kg-N/Mg feedstock'
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# =============================================================================
# Index(['abbreviation', 'Moisture Content', 'Volatile Solids', 'Ash Content',
#        'Lower Heating Value', 'Methane Yield', 'Lab Decay Rate',
#        'Bulk Density', 'Carbon Storage Factor', 'Biogenic Carbon Content',
#        'Ultimate Biogenic C Converted to Biogas', 'Fossil Carbon Content',
#        'Hydrogen Content', 'Oxygen Content', 'Nitrogen Content',
#        'Phosphorus Content', 'Potassium Content', 'Iron', 'Copper', 'Cadmium',
#        'Arsenic', 'Mercury', 'Selenium', 'Chromium', 'Lead', 'Zinc', 'Barium',
#        'Antimony', 'Nickel', 'Silver', 'Chlorine', 'Sulphur', 'Aluminum',
#        'Methane Yield.1']
        
# =============================================================================
#         Index(['Substrate mass flows inputs',
#        'Percent screened out in primary pre-screening (shredded)',
#        'Percent screened out in secondary pre-screening (residual not sent to composting)',
#        'Percent post screened out', 'Percent vacuumed out (vacprop)',
#        'Percent C-loss during composting', 'Mass VS loss per mass C-loss',
#        'Percent N-loss during composting', 'VOC emissions', 'Degrades',
#        'Unnamed: 11', 'Bulking Agent Requirements', 'Parameter.1',
#        'Wood chips/screen reject requirement'],
#       dtype='object')
# =============================================================================
# =============================================================================
