# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:59:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
from Comp_Input_1 import *
from CommonData import *
from stats_arrays import *

class Comp:
    def __init__(self):
        self.CommonData = CommonData()
        self.Comp_input= Comp_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'Composting', index_col = 'Parameter')
        self.process_data.fillna(0,inplace=True)
        self.Index = ['Unit','Total based on assumed_Comp' ,'Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
                      'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
                      'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
                      'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
                      'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
                      'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
                      'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
                      'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
                      'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        self.Assumed_Comp = pd.Series(self.Comp_input.Assumed_Comp,index=self.Index)
        self.SD=pd.read_excel('comp_stat.xlsx', index_col = 'Index')
                ### Mass Flows
        self.Mass_flows=pd.DataFrame(index = self.Index)
    def calc(self):
### Pretreatment and screan   
        
        self.Mass_flows ['Mass at tipping floor'] = 1000
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass at tipping floor'] = sum(self.Mass_flows ['Mass at tipping floor'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit', 'Mass at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass at tipping floor'] = self.Mass_flows ['Mass at tipping floor'] * (1 - self.Material_Properties['Moisture Content'][4:]/100)
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Dry mass at tipping floor'] = sum(self.Mass_flows ['Dry mass at tipping floor'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit', 'Dry mass at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash at tipping floor'] = self.Mass_flows ['Dry mass at tipping floor'] * self.Material_Properties['Ash Content'][4:]/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of ash at tipping floor'] = sum(self.Mass_flows ['Mass of ash at tipping floor'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit', 'Mass of ash at tipping floor'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)'] = self.Mass_flows ['Mass at tipping floor'] * ( 1- self.process_data['Percent screened out in primary pre-screening (shredded)'][3:]/100)
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of unders in primary pre-screen (not shredded)'] = sum(self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit', 'Mass of unders in primary pre-screen (not shredded)'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of overs from primary screen'] = self.Mass_flows ['Mass at tipping floor'][2:] - self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)']
        self.Mass_flows.loc ['Total based on assumed_Comp','Mass of overs from primary screen'] = sum(self.Mass_flows ['Mass of overs from primary screen'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of overs from primary screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'] = self.Mass_flows ['Mass of overs from primary screen'] * self.process_data['Percent screened out in secondary pre-screening (residual not sent to composting)'][3:]/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass screened out in secondary pre-screen (to residual)'] = sum(self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass screened out in secondary pre-screen (to residual)'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass screened out in secondary pre-screen'] =  self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'] * (1 - self.Material_Properties['Moisture Content'][4:]/100)
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Dry mass screened out in secondary pre-screen'] = sum(self.Mass_flows ['Dry mass screened out in secondary pre-screen'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Dry mass screened out in secondary pre-screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash screened out in secondary pre-screen'] =  self.Mass_flows ['Dry mass screened out in secondary pre-screen'] * self.Material_Properties['Ash Content'][4:]/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of ash screened out in secondary pre-screen'] = sum(self.Mass_flows ['Mass of ash screened out in secondary pre-screen'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of ash screened out in secondary pre-screen'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass to shredding'] =  self.Mass_flows ['Mass of overs from primary screen'] - self.Mass_flows ['Mass screened out in secondary pre-screen (to residual)'][2:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass to shredding'] = sum(self.Mass_flows ['Mass to shredding'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass to shredding'] = 'kg/Mg feedstock'

### Substrate to active composting  
        
        self.Mass_flows ['Mass of substrate to active composting'] =  self.Mass_flows ['Mass to shredding'][2:] + self.Mass_flows ['Mass of unders in primary pre-screen (not shredded)']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of substrate to active composting'] = sum(self.Mass_flows ['Mass of substrate to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of substrate to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Dry mass of substrate to active composting'] =  self.Mass_flows ['Mass of substrate to active composting'][2:] * (1 - self.Material_Properties['Moisture Content'][4:]/100) 
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Dry mass of substrate to active composting'] = sum(self.Mass_flows ['Dry mass of substrate to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Dry mass of substrate to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of VS in substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Volatile Solids'][4:]/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of VS in substrates to active composting'] = sum(self.Mass_flows ['Mass of VS in substrates to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of VS in substrates to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash in substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][2:] - self.Mass_flows ['Mass of VS in substrates to active composting'][2:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of ash in substrates to active composting'] = sum(self.Mass_flows ['Mass of ash in substrates to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of ash in substrates to active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of C in degradable substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Biogenic Carbon Content'][4:]/100 *self.process_data['Degrades'][3:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of C in degradable substrates to active composting'] = sum(self.Mass_flows ['Mass of C in degradable substrates to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of C in degradable substrates to active composting'] = 'kg-C/Mg feedstock'
        
        self.Mass_flows ['Mass of N in degradable substrates to active composting'] =  self.Mass_flows ['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Nitrogen Content'][4:]/100 *self.process_data['Degrades'][3:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of N in degradable substrates to active composting'] = sum(self.Mass_flows ['Mass of N in degradable substrates to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of N in degradable substrates to active composting'] = 'kg-N/Mg feedstock'
        
        self.Mass_flows ['Mass of water in substrates sent to active composting'] =  self.Mass_flows ['Mass of substrate to active composting'][2:] - self.Mass_flows ['Dry mass of substrate to active composting'][2:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of water in substrates sent to active composting'] = sum(self.Mass_flows ['Mass of water in substrates sent to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of water in substrates sent to active composting'] = 'kg/Mg feedstock'

### wood chips and screen rejects
        
        self.Mass_flows ['Mass of wood chips and screen rejects'] =  self.Mass_flows ['Mass of substrate to active composting'][2:] * self.process_data['Wood chips/screen reject requirement'][3:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of wood chips and screen rejects'] = sum(self.Mass_flows ['Mass of wood chips and screen rejects'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of wood chips and screen rejects'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of water in wood chips and screen rejects'] =  self.Mass_flows ['Mass of wood chips and screen rejects'][2:] * self.Comp_input.Substrate_Parameters['Sawdust']['Moisture_Content']['amount']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of water in wood chips and screen rejects'] = sum(self.Mass_flows ['Mass of water in wood chips and screen rejects'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of water in wood chips and screen rejects'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of solids in wood chips and screen rejects'] =  self.Mass_flows ['Mass of wood chips and screen rejects'][2:] - self.Mass_flows ['Mass of water in wood chips and screen rejects'][2:]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of solids in wood chips and screen rejects'] = sum(self.Mass_flows ['Mass of solids in wood chips and screen rejects'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of solids in wood chips and screen rejects'] = 'kg/Mg feedstock'
        
### Saw dust        
        
        self.SD_mass = max((self.Mass_flows ['Mass of C in degradable substrates to active composting'][1] - self.Comp_input.Degradation_Parameters['CN']['amount'] * self.Mass_flows ['Mass of N in degradable substrates to active composting'][1] ) \
                       /(self.Comp_input.Degradation_Parameters['CN']['amount']*(self.Comp_input.Substrate_Parameters['Sawdust']['N_Cont']['amount']/100)-(self.Comp_input.Substrate_Parameters['Sawdust']['C_Cont']['amount']/100)),0) 
        self.Mass_flows ['Mass of solids in saw dust'] = self.SD_mass * self.Mass_flows ['Mass of N in degradable substrates to active composting'][2:]/self.Mass_flows ['Mass of N in degradable substrates to active composting'][1]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of solids in saw dust'] = self.SD_mass
        self.Mass_flows.loc ['Unit','Mass of solids in saw dust'] = 'kg/Mg feedstock'
        
# =============================================================================
# =============================================================================
# =============================================================================
# # #              Mass of solids in saw dust should be checked  -  is Nonlinear
# =============================================================================
# =============================================================================
# =============================================================================
        
        self.Mass_flows ['Mass of added saw dust'] = self.Mass_flows ['Mass of solids in saw dust'][2:]/(1-self.Comp_input.Substrate_Parameters["Sawdust"]['Moisture_Content']['amount'])
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of added saw dust'] = sum(self.Mass_flows ['Mass of added saw dust'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of added saw dust'] = 'kg/Mg feedstock'
                
        self.Mass_flows ['Mass of VS in sawdust'] = self.Mass_flows ['Mass of solids in saw dust'][2:]*self.Comp_input.Substrate_Parameters["Sawdust"]['Volatile Solids']['amount']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of VS in sawdust'] = sum(self.Mass_flows ['Mass of VS in sawdust'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of VS in sawdust'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of C in sawdust'] = self.Mass_flows ['Mass of solids in saw dust'][2:]*self.Comp_input.Substrate_Parameters["Sawdust"]['C_Cont']['amount']/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of C in sawdust'] = sum(self.Mass_flows ['Mass of C in sawdust'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of C in sawdust'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash in sawdust'] = self.Mass_flows ['Mass of solids in saw dust'][1:] - self.Mass_flows ['Mass of VS in sawdust']
        self.Mass_flows.loc ['Unit','Mass of ash in sawdust'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of water in sawdust'] = self.Mass_flows ['Mass of added saw dust'] - self.Mass_flows ['Mass of solids in saw dust'][1:]
        self.Mass_flows.loc ['Unit','Mass of water in sawdust'] = 'kg/Mg feedstock'
        

### Active Composting
        
        self.moist_befor_add_water =   (self.Mass_flows ['Mass of water in sawdust'][1]+ self.Mass_flows ['Mass of water in wood chips and screen rejects'][1]+self.Mass_flows ['Mass of water in substrates sent to active composting'][1])\
                                        /(self.Mass_flows ['Mass of added saw dust'][1]+ self.Mass_flows ['Mass of wood chips and screen rejects'][1]+self.Mass_flows ['Mass of substrate to active composting'][1])    
        
        self.water_demand = 0 if self.moist_befor_add_water >= self.Comp_input.Degradation_Parameters['initMC']['amount'] else (self.Comp_input.Degradation_Parameters['initMC']['amount'] * \
                            (self.Mass_flows ['Mass of added saw dust'][1]+ self.Mass_flows ['Mass of wood chips and screen rejects'][1]+self.Mass_flows ['Mass of substrate to active composting'][1]) \
                            -(self.Mass_flows ['Mass of water in sawdust'][1]+ self.Mass_flows ['Mass of water in wood chips and screen rejects'][1]+self.Mass_flows ['Mass of water in substrates sent to active composting'][1])) \
                            /(1-self.Comp_input.Degradation_Parameters['initMC']['amount'])
        
        self.Mass_flows ['Water added to compost'] = (self.Mass_flows ['Mass of solids in saw dust'][2:]+ self.Mass_flows ['Dry mass of substrate to active composting'][2:]+self.Mass_flows ['Mass of solids in wood chips and screen rejects'][2:])\
                                                    /(self.Mass_flows ['Mass of solids in saw dust'][1]+ self.Mass_flows ['Dry mass of substrate to active composting'][1]+self.Mass_flows ['Mass of solids in wood chips and screen rejects'][1]) *self.water_demand
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Water added to compost'] = self.water_demand
        self.Mass_flows.loc ['Unit','Water added to compost'] = 'kg/Mg feedstock'
        
# =============================================================================
# =============================================================================
# =============================================================================
# # #              'Water added to compost' is Nonlinear
# =============================================================================
# =============================================================================
# =============================================================================
        self.Mass_flows ['Total mass to active composting (including amendments)'] = self.Mass_flows ['Mass of added saw dust'][1:]+ self.Mass_flows ['Mass of wood chips and screen rejects']+self.Mass_flows ['Mass of substrate to active composting']+self.Mass_flows ['Water added to compost']
        self.Mass_flows.loc ['Unit','Total mass to active composting (including amendments)'] = 'kg/Mg feedstock'
        
        
        self.Mass_flows ['Total dry mass to active composting (including amendments)'] = self.Mass_flows ['Mass of solids in saw dust'][1:]+ self.Mass_flows ['Dry mass of substrate to active composting']+self.Mass_flows ['Mass of solids in wood chips and screen rejects']
        self.Mass_flows.loc ['Unit','Total dry mass to active composting (including amendments)'] = 'kg/Mg feedstock'
        

        self.Mass_flows ['Total mass of water to active composting (including amendments)'] = self.Mass_flows ['Total mass to active composting (including amendments)'][1:]-self.Mass_flows ['Total dry mass to active composting (including amendments)']
        self.Mass_flows.loc ['Unit','Total mass of water to active composting (including amendments)'] = 'kg/Mg feedstock'


        self.Mass_flows ['C loss of substrates during active composting'] =  self.Mass_flows ['Mass of C in degradable substrates to active composting'][2:]*self.process_data['Percent C-loss during composting']/100 * self.Comp_input.Degradation_Parameters['acDegProp']['amount']/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'C loss of substrates during active composting'] = sum(self.Mass_flows ['C loss of substrates during active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','C loss of substrates during active composting'] = 'kg/Mg feedstock'

        self.Mass_flows ['N loss of substrates during active composting'] =  self.Mass_flows ['Mass of N in degradable substrates to active composting'][2:]*self.process_data['Percent N-loss during composting']/100 * self.Comp_input.Degradation_Parameters['acDegProp']['amount']/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'N loss of substrates during active composting'] = sum(self.Mass_flows ['N loss of substrates during active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','N loss of substrates during active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['VS loss of substrates during active composting'] =  self.Mass_flows ['C loss of substrates during active composting'][2:]*self.process_data['Mass VS loss per mass C-loss']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'VS loss of substrates during active composting'] = sum(self.Mass_flows ['VS loss of substrates during active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','VS loss of substrates during active composting'] = 'kg/Mg feedstock'
        
                               
        self.Mass_flows ['C  loss of sawdust during active composting'] = self.Mass_flows ['Mass of C in sawdust'][2:] * self.Comp_input.Degradation_Parameters['acDegProp']['amount']/100 * \
                                                                            self.Comp_input.Substrate_Parameters["Sawdust"]['C Emitted']['amount']/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'C  loss of sawdust during active composting'] = sum(self.Mass_flows ['C  loss of sawdust during active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','C  loss of sawdust during active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['VS loss of sawdust during active composting'] = self.Mass_flows ['C  loss of sawdust during active composting'][2:]*self.Comp_input.Substrate_Parameters["Sawdust"]['VS loss per C loss']['amount']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'VS loss of sawdust during active composting'] = sum(self.Mass_flows ['VS loss of sawdust during active composting'][2:] * self.Assumed_Comp[2:]) 
        self.Mass_flows.loc ['Unit','VS loss of sawdust during active composting'] = 'kg/Mg feedstock'
        
### Substrates after active composting        
        
        self.Mass_flows ['Mass of VS remaining in subtrates after active composting'] = self.Mass_flows ['Mass of VS in substrates to active composting'][1:]-self.Mass_flows ['VS loss of substrates during active composting']
        self.Mass_flows.loc ['Unit','Mass of VS remaining in subtrates after active composting'] = 'kg/Mg feedstock'
        
        
        self.Mass_flows ['Mass of ash remaining in substrates after active composting'] = self.Mass_flows ['Mass of ash in substrates to active composting']

        
        
        self.Mass_flows ['Dry mass in subtrates after active composting'] = self.Mass_flows ['Mass of ash remaining in substrates after active composting'][1:]+self.Mass_flows ['Mass of VS remaining in subtrates after active composting']
        self.Mass_flows.loc ['Unit','Dry mass in subtrates after active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of C in substrates after active composting'] = self.Mass_flows ['Mass of C in degradable substrates to active composting'][1:]-self.Mass_flows ['C loss of substrates during active composting']
        self.Mass_flows.loc ['Unit','Mass of C in substrates after active composting'] = 'kg C/Mg feedstock'        
        
        self.Mass_flows ['C content of substrates after active composting'] = (self.Mass_flows ['Mass of C in substrates after active composting'][1:]/self.Mass_flows ['Dry mass in subtrates after active composting'][1:].apply(lambda x: 1 if x<=0 else x ))
        self.Mass_flows.loc ['Unit','C content of substrates after active composting'] = 'kg/kg TS'
        
        self.Mass_flows ['Mass of N in substrates after active composting'] = self.Mass_flows ['Mass of N in degradable substrates to active composting'][1:]-self.Mass_flows ['N loss of substrates during active composting']
        self.Mass_flows.loc ['Unit','Mass of N in substrates after active composting'] = 'kg N/Mg feedstock'        
        
        self.Mass_flows ['N content of substrates after active composting'] = (self.Mass_flows ['Mass of N in substrates after active composting'][1:]/self.Mass_flows ['Dry mass in subtrates after active composting'][1:].apply(lambda x: 1 if x<=0 else x ))
        self.Mass_flows.loc ['Unit','N content of substrates after active composting'] = 'kg/kg TS'
        

### Saw dust after active composting         
        
        self.Mass_flows ['Mass of VS remaining in sawdust after active composting'] = self.Mass_flows ['Mass of VS in sawdust'][1:] - self.Mass_flows ['VS loss of sawdust during active composting']
        self.Mass_flows.loc ['Unit','Mass of VS remaining in sawdust after active composting'] = 'kg/Mg feedstock'
        
        self.Mass_flows ['Mass of ash remaining in sawdust after active composting'] =self.Mass_flows ['Mass of ash in sawdust']
        
        self.Mass_flows ['Dry mass of sawdust after active composting'] = self.Mass_flows ['Mass of VS remaining in sawdust after active composting'][1:] +self.Mass_flows ['Mass of ash remaining in sawdust after active composting']
        self.Mass_flows.loc ['Unit','Dry mass of sawdust after active composting'] = 'kg/Mg feedstock'
        
###  wood chips/screen rejects after active composting       
        
        self.Mass_flows ['Dry mass of wood chips/screen rejects after composting'] =self.Mass_flows ['Mass of solids in wood chips and screen rejects']
        
### Total mass after active composting
        self.Mass_flows ['Mass of solids after active composting (including amendments)'] = self.Mass_flows ['Dry mass in subtrates after active composting'][1:]+self.Mass_flows ['Dry mass of sawdust after active composting']\
                                                                                            +self.Mass_flows ['Dry mass of wood chips/screen rejects after composting']
        self.Mass_flows.loc ['Unit','Mass of solids after active composting (including amendments)'] = 'kg/Mg feedstock'
        
        self.water_after_ac = self.Mass_flows ['Mass of solids after active composting (including amendments)'][1]/(1-self.Comp_input.Degradation_Parameters['MCac']['amount']) * \
                                self.Comp_input.Degradation_Parameters['MCac']['amount']
        
        self.Mass_flows ['Water in compost after active composting (including amendments)']=self.water_after_ac*self.Mass_flows ['Total mass of water to active composting (including amendments)'][2:]/ \
                                                                                            self.Mass_flows ['Total mass of water to active composting (including amendments)'][1]
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Water in compost after active composting (including amendments)'] = sum(self.Mass_flows ['Water in compost after active composting (including amendments)'][2:] * self.Assumed_Comp[2:]) 
        self.Mass_flows.loc ['Unit','Water in compost after active composting (including amendments)'] = 'kg/Mg feedstock'
 
        self.Mass_flows ['Mass of water evaporated (including amendments)']=self.Mass_flows ['Total mass of water to active composting (including amendments)'][1:]-self.Mass_flows ['Water in compost after active composting (including amendments)']
        self.Mass_flows.loc ['Unit','Mass of water evaporated (including amendments)'] = 'kg/Mg feedstock'
        

        

        
        
    def calc2(self):

### Carbon Balance        
        self.Mass_flows['Mass of C loss during composting'] = self.SD['C loss of substrates during active composting'][1:]+self.SD['Mass of C loss from substrates in curing'][1:]
        self.Mass_flows.loc ['Unit','Mass of C loss during composting'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C emitted as CH4'] = self.Mass_flows['Mass of C loss during composting'][1:] * self.Comp_input.Biological_Degredation['pCasCH4']['amount']
        self.Mass_flows.loc ['Unit','Mass of C emitted as CH4'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C emitted as CO2b'] = self.Mass_flows['Mass of C loss during composting'][1:] - self.Mass_flows['Mass of C emitted as CH4'][1:]
        self.Mass_flows.loc ['Unit','Mass of C emitted as CO2b'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C emitted as CH4 from the biofilter'] = self.Mass_flows['Mass of C emitted as CH4'][1:] * (1 - self.Comp_input.Biological_Degredation['bfCH4re']['amount'])
        self.Mass_flows.loc ['Unit','Mass of C emitted as CH4 from the biofilter'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of CO2b generated in the biofilter'] = self.Mass_flows['Mass of C emitted as CH4'][1:]  - self.Mass_flows['Mass of C emitted as CH4 from the biofilter']
        self.Mass_flows.loc ['Unit','Mass of CO2b generated in the biofilter'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C in final compost'] = self.SD['Mass of C in substrates sent to curing'][1:] - self.SD['Mass of C loss from substrates in curing'][1:] 
        self.Mass_flows.loc ['Unit','Mass of C in final compost'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C remaining after 100 years'] = self.Mass_flows['Mass of C in final compost'][1:] * self.Comp_input.Biological_Degredation['percCStor']['amount']/100
        self.Mass_flows.loc ['Unit','Mass of C remaining after 100 years'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of CO2b released after land application'] = self.Mass_flows['Mass of C in final compost'][1:] - self.Mass_flows['Mass of C remaining after 100 years']
        self.Mass_flows.loc ['Unit','Mass of CO2b released after land application'] = 'kg C/Mg feedstock'
        
        self.Mass_flows['Mass of C stored due to humus formation'] = self.Mass_flows['Mass of C in final compost'] * self.Comp_input.Biological_Degredation['humFormFac']['amount']
        self.Mass_flows.loc ['Unit','Mass of C stored due to humus formation'] = 'kg C/Mg feedstock'

### Nitrogen Balance
        self.Mass_flows['Mass of incoming N to active composting'] = self.SD['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Nitrogen Content'][4:]/100
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of incoming N to active composting'] = sum(self.Mass_flows['Mass of incoming N to active composting'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of incoming N to active composting'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N loss during composting'] = self.SD['N loss of substrates during active composting'][1:] + self.SD['Mass of N loss from substrates in curing'][1:] 
        self.Mass_flows.loc ['Unit','Mass of N loss during composting'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N loss as NH3'] = self.Mass_flows['Mass of N loss during composting'][1:] * self.Comp_input.Biological_Degredation['pNasNH3']['amount']
        self.Mass_flows.loc ['Unit','Mass of N loss as NH3'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N loss as N2O'] = self.Mass_flows['Mass of N loss during composting'][1:] * self.Comp_input.Biological_Degredation['pNasN2O']['amount']
        self.Mass_flows.loc ['Unit','Mass of N loss as N2O'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of NH3 removed by the biofilter'] = self.Mass_flows['Mass of N loss as NH3'][1:] * self.Comp_input.Biological_Degredation['bfNH3re']['amount']/100
        self.Mass_flows.loc ['Unit','Mass of NH3 removed by the biofilter'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N2O removed by the biofilter'] = self.Mass_flows['Mass of N loss as NH3'][1:] * self.Comp_input.Biological_Degredation['bfN2Ore']['amount']/100
        self.Mass_flows.loc ['Unit','Mass of N2O removed by the biofilter'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N2O produced in the biofilter'] = self.Mass_flows['Mass of NH3 removed by the biofilter'] * self.Comp_input.Biological_Degredation['preNH3toN2O']['amount']
        self.Mass_flows.loc ['Unit','Mass of N2O produced in the biofilter'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of NOx produced in the biofilter'] = self.Mass_flows['Mass of NH3 removed by the biofilter'] * self.Comp_input.Biological_Degredation['preNH3toNOx']['amount']
        self.Mass_flows.loc ['Unit','Mass of NOx produced in the biofilter'] = 'kg N/Mg feedstock'
        
        self.Mass_flows['Mass of N in the final compost'] = (self.Mass_flows['Mass of incoming N to active composting'][2:] - self.Mass_flows['Mass of N loss during composting'])\
                                                            * (self.SD['Dry mass of final compost'][2:]/self.SD['Dry mass after curing (including amendments)'][2:])
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Mass of N in the final compost'] = sum(self.Mass_flows['Mass of N in the final compost'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Mass of N in the final compost'] = 'kg N/Mg feedstock'
        
### Available Nutrients        
        self.Mass_flows['Navail'] = self.Mass_flows['Mass of N in the final compost'][1:] * self.CommonData.Land_app['MFEN']['amount']
        self.Mass_flows.loc ['Unit','Navail'] = 'kg/Mg feedstock'
        
        self.Mass_flows['Pavail'] = self.SD['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Phosphorus Content'][4:]/100 * \
                                        (self.SD['Dry mass of final compost'][2:]/self.SD['Dry mass after curing (including amendments)'][2:])*\
                                        self.CommonData.Land_app['MFEP']['amount']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Pavail'] = sum(self.Mass_flows['Pavail'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Pavail'] = 'kg/Mg feedstock'
        
        self.Mass_flows['Kavail'] = self.SD['Dry mass of substrate to active composting'][2:] * self.Material_Properties['Potassium Content'][4:]/100 * \
                                (self.SD['Dry mass of final compost'][2:]/self.SD['Dry mass after curing (including amendments)'][2:])*\
                                self.CommonData.Land_app['MFEK']['amount']
        self.Mass_flows.loc ['Total based on assumed_Comp', 'Kavail'] = sum(self.Mass_flows['Kavail'][2:] * self.Assumed_Comp[2:])
        self.Mass_flows.loc ['Unit','Kavail'] = 'kg/Mg feedstock'
        
    
### Life-Cycle Inventory
        self.LCI = pd.DataFrame(index = self.Index)
        
        self.LCI['VOCs generated']=(self.SD['Mass of VS loss from substrates in curing'][2:]+self.SD['VS loss of substrates during active composting'][2:]) * \
                                                    self.process_data['VOC emissions']/10**6
        self.LCI.loc ['Total based on assumed_Comp', 'VOCs generated'] = sum(self.LCI ['VOCs generated'][2:] * self.Assumed_Comp[2:])
        self.LCI.loc ['Unit','VOCs generated'] = 'kg/Mg feedstock'
    
        self.LCI['VOCs emitted'] = self.LCI['VOCs generated'][1:] *  (1 - self.Comp_input.Biological_Degredation['bfVOCre']['amount']/100)
        self.LCI.loc ['Unit','VOCs emitted'] = 'kg/Mg feedstock'
        
        self.LCI['Carbon dioxide, non-fossil'] = (self.Mass_flows['Mass of C emitted as CO2b'][1:] + self.Mass_flows['Mass of CO2b generated in the biofilter'][1:] + self.Mass_flows['Mass of CO2b released after land application'][1:]) *\
                                                    self.CommonData.MW['CO2']['amount']/self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil'] = 'kg/Mg feedstock'
        
        self.LCI['Carbon dioxide, non-fossil storage'] = (self.Mass_flows['Mass of C remaining after 100 years'][1:] + self.Mass_flows['Mass of C stored due to humus formation'][1:])\
                                                        * self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil storage'] = 'kg/Mg feedstock'
        
        
        self.LCI['Methane, non-fossil'] = (self.Mass_flows['Mass of C emitted as CH4 from the biofilter'][1:]) * self.CommonData.MW['CH4']['amount']/self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Methane, non-fossil'] = 'kg/Mg feedstock'
        
        self.LCI['Dinitrogen monoxide'] = (self.Mass_flows['Mass of N loss as N2O'][1:] - self.Mass_flows['Mass of N2O removed by the biofilter'][1:] + \
                                            self.Mass_flows['Mass of N in the final compost'][1:] * self.Comp_input.Land_app['perN2Oevap']['amount']/100) * \
                                            self.CommonData.MW['Nitrous_Oxide']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Dinitrogen monoxide'] = 'kg/Mg feedstock'
        
        self.LCI['Nitrogen oxides'] = self.Mass_flows['Mass of NOx produced in the biofilter'][1:] * self.CommonData.MW['NOx']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Nitrogen oxides'] = 'kg/Mg feedstock'
        
        self.LCI['Ammonia'] = (self.Mass_flows['Mass of N loss as NH3'][1:]-self.Mass_flows['Mass of NH3 removed by the biofilter'][1:] + self.Mass_flows['Mass of N in the final compost'][1:] \
                                * self.Comp_input.Land_app['perNH3evap']['amount']/100 *  self.Comp_input.Land_app['perNasNH3fc']['amount']/100) \
                                * self.CommonData.MW['Ammonia']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Ammonia'] = 'kg/Mg feedstock'
        
        self.LCI['Nitrate (ground water)'] = self.Mass_flows['Mass of N in the final compost'][1:] * self.CommonData.Land_app['NO3leach']['amount'] \
                                            * self.CommonData.MW['Nitrate']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Nitrate (ground water)'] = 'kg/Mg feedstock'
        
        self.LCI['Nitrate (Surface water)'] = self.Mass_flows['Mass of N in the final compost'][1:] * self.CommonData.Land_app['NO3runoff']['amount'] \
                                                * self.CommonData.MW['Nitrate']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Nitrate (Surface water)'] = 'kg/Mg feedstock'
    
### Electricity use
        self.LCI['Pre-screen'] = self.Comp_input.Screen['Mtr']['amount']
        self.LCI.loc ['Unit','Pre-screen'] = 'kWh/Mg feedstock'
        
        self.LCI['Forced aeration'] = self.SD['Dry mass of substrate to active composting'][1:]/self.SD['Dry mass at tipping floor'][1:] *\
                                        self.Comp_input.AC_Aeration['Breq']['amount'] * self.Comp_input.AC_Aeration['Bhp']['amount'] * self.Comp_input.AC_Aeration['Aeff']['amount']\
                                        * self.Comp_input.AC_Aeration['blPropON']['amount'] * 24 * self.Comp_input.Op_Param['Tact']['amount']
        self.LCI.loc ['Unit','Forced aeration'] = 'kWh/Mg feedstock'
        
        self.LCI['In-vessel reactor'] = self.Comp_input.Vessel['Minv']['amount'] * self.SD['Mass of substrate to active composting'][1:]/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','In-vessel reactor'] = 'kWh/Mg feedstock'
        

# =============================================================================
# =============================================================================
# # Formula for the odor control system should be checked!!!!         
# =============================================================================
# =============================================================================
        
        self.LCI['Odor control'] = self.Comp_input.Odor_Cont['Moc']['amount'] * self.Comp_input.Odor_Cont['ocReqAF']['amount'] * (1/self.Comp_input.Op_Param['Taod']['amount']) * (1/60)
        self.LCI.loc ['Unit','Odor control'] = 'kWh/Mg feedstock'
        
        self.LCI['Post screen'] = self.Comp_input.Screen['Mtr']['amount'] * self.SD['Total mass entering post-screen (including amendments)'][1:]/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Post screen'] = 'kWh/Mg feedstock'
        
        self.LCI['Post screen'] = self.Comp_input.Screen['Mtr']['amount'] * self.SD['Total mass entering post-screen (including amendments)'][1:]/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Post screen'] = 'kWh/Mg feedstock'

# =============================================================================
# =============================================================================
# # Formula for the Office  should be checked!!!!         
# =============================================================================
# =============================================================================
        
        self.LCI['Office'] = ( self.Comp_input.Office['Mta']['amount'] * self.Comp_input.Office['Mea']['amount'] / 1000 ) /self.Comp_input.Op_Param['Taod']['amount'] 
        self.LCI.loc ['Unit','Office'] = 'kWh/Mg feedstock'
        
        self.LCI['Vacuum'] =  self.Comp_input.Vaccum_sys['vacElecFac']['amount'] * self.SD['Total mass entering vacuum'][1:] / 1000
        self.LCI.loc ['Unit','Vacuum'] = 'kWh/Mg feedstock'
        
        self.LCI['Electricity_consumption'] = self.LCI['Pre-screen'][1:] + self.LCI['Forced aeration'] + self.LCI['In-vessel reactor'] + self.LCI['Odor control'] + \
                                                self.LCI['Post screen'] + self.LCI['Office'] + self.LCI['Vacuum']
        self.LCI.loc ['Unit','Electricity_consumption'] = 'kWh/Mg feedstock'

        
### Diesel Fuel use        
        self.LCI['Branch shredding energy requirement'] = self.Comp_input.Shredding['Mtgp']['amount'] * self.SD['Mass to shredding'][1:]/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Branch shredding energy requirement'] = 'kWh/Mg feedstock'
        
        self.LCI['Branch shredding diesel consumption'] = self.Comp_input.Shredding['Mtgf']['amount'] * self.LCI['Branch shredding energy requirement'][1:]
        self.LCI.loc ['Unit','Branch shredding diesel consumption'] = 'L/Mg feedstock'
        
        self.LCI['Active composting windrow turner energy requirement'] = self.Comp_input.Op_Param['Tact']['amount'] * self.Comp_input.AC_Turning['Fta']['amount'] *  self.Comp_input.AC_Turning['Mwta']['amount'] \
                                                                            * (self.SD['Mass of substrate to active composting'][1:]+self.SD['Mass of added saw dust'][1:])/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Active composting windrow turner energy requirement'] = 'kWh/Mg feedstock'
        
        self.LCI['Active composting windrow turning diesel consumption'] = self.Comp_input.AC_Turning['Mwfa']['amount'] * self.LCI['Active composting windrow turner energy requirement'][1:]
        self.LCI.loc ['Unit','Active composting windrow turning diesel consumption'] = 'L/Mg feedstock'
        
        self.LCI['Front end loaders energy use'] =  self.Comp_input.Loader['hpfel']['amount'] * self.Comp_input.Op_Param['Tdoh']['amount']
        self.LCI.loc ['Unit','Front end loaders energy use'] = 'kWh/Mg feedstock'
        
        self.LCI['Front end loaders fuel consumptions'] =  self.Comp_input.Loader['Mffel']['amount'] * self.LCI['Front end loaders energy use'][1:]
        self.LCI.loc ['Unit','Front end loaders fuel consumptions'] = 'L/Mg feedstock'
        
        self.LCI['Curing windrow turner energy requirement'] =  self.Comp_input.Curing['Ftc']['amount'] * self.Comp_input.Op_Param['Tcur']['amount'] * self.Comp_input.AC_Turning['Mwta']['amount']\
                                                                * (self.SD['Total mass sent to screen (including amendments)'][1:]+self.SD['Mass of added saw dust'][1:])/self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Curing windrow turner energy requirement'] = 'kWh/Mg feedstock'
        
        self.LCI['Curing windrow turning diesel consumption'] =  self.Comp_input.AC_Turning['Mwfa']['amount'] * self.LCI['Curing windrow turner energy requirement'][1:]
        self.LCI.loc ['Unit','Curing windrow turning diesel consumption'] = 'L/Mg feedstock'
        
        self.LCI['Vacuum diesel use'] =  self.Comp_input.Vaccum_sys['vacDiesFac']['amount'] * self.SD['Total mass entering vacuum'][1:] / 1000
        self.LCI.loc ['Unit','Vacuum diesel use'] = 'L/Mg feedstock'
        
        self.LCI['Diesel used to apply compost'] =  self.CommonData.Land_app['cmpLandDies']['amount'] * self.SD['Total mass of final compost'][1:] / self.SD['Mass at tipping floor'][1:]
        self.LCI.loc ['Unit','Diesel used to apply compost'] = 'L/Mg feedstock'
        
        self.LCI['Total Diesel'] = self.LCI['Branch shredding diesel consumption'][1:] + self.LCI['Active composting windrow turning diesel consumption'] + self.LCI ['Front end loaders fuel consumptions']\
                                    + self.LCI['Curing windrow turning diesel consumption'] + self.LCI['Vacuum diesel use'] + self.LCI['Diesel used to apply compost']
        self.LCI.loc ['Unit','Total Diesel'] = 'L/Mg feedstock'
        
### Transportation         
        self.LCI['Medium-duty truck transportation to land application'] =  self.SD['Mass to soil amendment'][1:]/self.SD['Mass at tipping floor'][1:] * self.Comp_input.Land_app['distLand']['amount']
        self.LCI.loc ['Unit','Medium-duty truck transportation to land application'] = 'Mg-km/Mg'
        
        self.LCI['Medium-duty empty return '] =  self.LCI['Medium-duty truck transportation to land application'][1:] /  self.Comp_input.Land_app['land_payload']['amount']
        self.LCI.loc ['Unit','Medium-duty empty return '] = 'vkm/Mg'


    def setup_MC(self):
        self.Comp_input.setup_MC()
    
    def MC_calc(self):      
        self.Comp_input.gen_MC()
        self.calc2()
        
    def report(self):
### Output
        self.COMP = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.COMP ["process name"] = 'COMP'
        self.COMP  ["Waste"] = Waste
        self.COMP  ["Technosphere"] = Technosphere
        self.COMP  ["Biosphere"] = Biosphere
        
        for x in [Waste,Technosphere, Biosphere]:
            for y in self.Index[2:]:
                x[y]={}
                                                       
               
        for y in self.Index[2:]:
### Output Waste Database 
            Waste[y]['Other_Residual'] = self.SD['Mass of residuals'][y]
            
### Output Technospphere Database
            Technosphere[y][('Technosphere', 'Electricity_consumption')] =  self.LCI['Electricity_consumption'][y]
            Technosphere[y][('Technosphere', 'Equipment_Diesel')] =  self.LCI['Total Diesel'][y]
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck')] =  self.LCI['Medium-duty truck transportation to land application'][y] * 1000
            Technosphere[y][('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck')] =  self.LCI['Medium-duty empty return '][y]
            Technosphere[y][('Technosphere', 'Nitrogen_Fertilizer') ] = self.Comp_input.Fertilizer_offsest['choice_BU']['amount'] * self.Comp_input.Fertilizer_offsest['fertOff']['amount'] * self.Mass_flows['Navail'][y]
            Technosphere[y][('Technosphere', 'Phosphorous_Fertilizer')] = self.Comp_input.Fertilizer_offsest['choice_BU']['amount'] * self.Comp_input.Fertilizer_offsest['fertOff']['amount'] * self.Mass_flows['Pavail'][y]
            Technosphere[y][('Technosphere', 'Potassium_Fertilizer')] = self.Comp_input.Fertilizer_offsest['choice_BU']['amount'] * self.Comp_input.Fertilizer_offsest['fertOff']['amount'] * self.Mass_flows['Kavail'][y]
            Technosphere[y][('Technosphere', 'Peat')] = self.Comp_input.Fertilizer_offsest['choice_BU']['amount'] * self.Comp_input.Fertilizer_offsest['peatOff']['amount'] * self.SD['Mass to soil amendment'][y] / 1000
            
### Output Biosphere Database
            Biosphere[y][('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014')]= self.LCI['Ammonia'][y] #  Ammonia ('air',)
            Biosphere[y][('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6')]= self.LCI['Carbon dioxide, non-fossil storage'][y] #Carbon dioxide, from soil or biomass stock ('air',)
            Biosphere[y][('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')]= self.LCI['Carbon dioxide, non-fossil'][y] #Carbon dioxide, non-fossil ('air',)
            Biosphere[y][('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98')]= self.LCI['Dinitrogen monoxide'][y] #Dinitrogen monoxide ('air',)
            Biosphere[y][('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8')]= self.LCI['Methane, non-fossil'][y] #Methane, non-fossil ('air',)
            Biosphere[y][('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457')]= self.LCI['Nitrogen oxides'][y] #Nitrogen oxides ('air',)
            Biosphere[y][('biosphere3', 'd3260d0e-8203-4cbb-a45a-6a13131a5108')]= self.LCI['VOCs emitted'][y] #NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
            Biosphere[y][('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33')]= self.LCI['Nitrate (ground water)'][y] #Nitrate ('water', 'ground-')
            Biosphere[y][('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35')]= self.LCI['Nitrate (Surface water)'][y] #Nitrate ('water', 'surface water')
        return(self.COMP)







# =============================================================================
# A=Comp()
# DD=A.calc2()
# from time import time
# c= time()
# for i in range(100):
#     A.calc2()
#     A.report()
# print(time()-c)
# =============================================================================

        
   
        
        
