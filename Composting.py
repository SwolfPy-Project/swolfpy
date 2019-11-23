# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:59:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
#from Composting_Input_script import *
from Composting_Input import *
from CommonData import *
from flow import *
from Composting_subprocess import *


class Comp:
    def __init__(self,input_data_path=None):
        self.CommonData = CommonData()
        self.Comp_input= Composting_input(input_data_path)
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'Composting', index_col = 'Parameter')
        self.process_data.fillna(0,inplace=True)
        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
                      'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
                      'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
                      'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
                      'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
                      'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
                      'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
                      'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
                      'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        self.Assumed_Comp = pd.Series(self.Comp_input.Assumed_Comp,index=self.Index)
        self.flow_init = flow(self.Material_Properties[4:])

    def calc(self):
        self.LCI = pd.DataFrame(index = self.Index)
### Initial mass at tipping floor  
        self.Input = flow(self.Material_Properties[4:])
        self.Input.init_flow(1000)

### Primary Pre_screen        
        self.S1_unders,self.S1_overs=screen(self.Input,self.process_data['Percent screened out in primary pre-screening (shredded)'][3:].values/100, self.Material_Properties[4:],self.Comp_input.Screen,self.LCI,self.flow_init)
        
### Secondary Pre_screen         
        self.S2_to_shredding,self.S2_residuls=screen(self.S1_overs,self.process_data['Percent screened out in secondary pre-screening (residual not sent to composting)'][3:].values/100, self.Material_Properties[4:],self.Comp_input.Screen,self.LCI,self.flow_init)
### Shredding/Grinding of seconday screen's unders
        self.shred = shredding(self.S2_to_shredding,self.Material_Properties[4:],self.Comp_input.Shredding,self.LCI,self.flow_init)

### Mixing the shredded and screened materials
        self.mixed = mix(self.S1_unders,self.shred,self.Material_Properties[4:],self.flow_init)

### Adding Water
        self.mixed.update(self.Assumed_Comp)
        self.water_added = 0 if self.mixed.moist_cont > self.Comp_input.Degradation_Parameters['initMC']['amount'] else \
                               (self.Comp_input.Degradation_Parameters['initMC']['amount']* self.mixed.flow - self.mixed.water)/(1-self.Comp_input.Degradation_Parameters['initMC']['amount'])
        water_flow = self.water_added * self.mixed.data['sol_cont'].values/self.mixed.solid
        
    
        self.substrate_to_ac = add_water(self.mixed,water_flow,self.Material_Properties[4:],self.process_data[3:],self.flow_init)
    
### Active Composting
        self.substrate_to_ps=ac_comp(self.substrate_to_ac,self.CommonData,self.process_data[3:],self.Comp_input,self.Comp_input.Degradation_Parameters,self.Comp_input.Biological_Degredation,self.Assumed_Comp,self.Material_Properties[4:],self.LCI,self.flow_init)
    
### Post screen
        self.substrate_to_vac,self.ps_res=post_screen(self.substrate_to_ps,self.process_data['Percent post screened out'][3:].values/100, self.Material_Properties[4:],self.Comp_input.Screen,self.LCI,self.flow_init)
    
### Vacuum
        self.substrate_to_cu,self.vac_res=vacuum(self.substrate_to_vac,self.process_data['Percent vacuumed out (vacprop)'][3:].values/100, self.Material_Properties[4:],self.Comp_input.Vaccum_sys,self.LCI,self.flow_init)
    
### Curing
        self.final_comp=curing(self.substrate_to_cu,self.CommonData,self.process_data[3:],self.Comp_input,self.Comp_input.Degradation_Parameters,self.Comp_input.Biological_Degredation,self.Assumed_Comp,self.Material_Properties[4:],self.LCI,self.flow_init)     
    
### Calculating the P and K in final compost
# Assumption: composition of ps_res == composition of vac_res  == composition of mixed , while the composition has changed because of active composting and curing
        self.final_comp.data['P_cont']= (self.mixed.data['sol_cont'].values-self.ps_res.data['sol_cont'].values- self.vac_res.data['sol_cont'].values) * self.Material_Properties['Phosphorus Content'][4:].values/100
        self.final_comp.data['K_cont']= (self.mixed.data['sol_cont'].values-self.ps_res.data['sol_cont'].values- self.vac_res.data['sol_cont'].values) * self.Material_Properties['Potassium Content'][4:].values/100
    
### Compost use
        compost_use(self.final_comp,self.CommonData,self.process_data[3:],self.Material_Properties[4:],self.Comp_input.Biological_Degredation,self.Comp_input.Land_app,self.Comp_input.Fertilizer_offset,self.Comp_input,self.LCI)
    
### office
        Office_elec = ( self.Comp_input.Office['Mta']['amount'] * self.Comp_input.Office['Mea']['amount'] / 1000 ) /self.Comp_input.Op_Param['Taod']['amount'] 
        add_LCI(('Technosphere', 'Electricity_consumption'), Office_elec ,self.LCI)  

### Transportation
        add_LCI('Medium-duty truck transportation to land application', self.final_comp.data['mass'].values * self.Comp_input.Land_app['distLand']['amount'] ,self.LCI)
        add_LCI('Medium-duty empty return', self.final_comp.data['mass'].values/1000 / self.Comp_input.Land_app['land_payload']['amount']* self.Comp_input.Land_app['distLand']['amount'] ,self.LCI)

    def setup_MC(self,seed=None):
        self.Comp_input.setup_MC(seed)
        #self.create_uncertainty_from_inputs()
    
    def MC_calc(self):      
        input_list = self.Comp_input.gen_MC()
        #self.uncertainty_input_next()
        self.calc()
        return(input_list)
        
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
            for y in self.Index:
                x[y]={}
                                                       
               
        for y in self.Index:        
### Output Waste Database 
            Waste[y]['Other_Residual'] = self.ps_res.data['mass'][y]/1000+self.vac_res.data['mass'][y]/1000+self.S2_residuls.data['mass'][y]/1000 
             
### Output Technospphere Database
            Technosphere[y][('Technosphere', 'Electricity_consumption')] =  report_LCI(('Technosphere', 'Electricity_consumption'),self.LCI,y)
            Technosphere[y][('Technosphere', 'Equipment_Diesel')] =  report_LCI(('Technosphere', 'Equipment_Diesel'),self.LCI,y)
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck')] = report_LCI('Medium-duty truck transportation to land application',self.LCI,y) 
            Technosphere[y][('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck')] =report_LCI('Medium-duty empty return',self.LCI,y)  
            Technosphere[y][('Technosphere', 'Nitrogen_Fertilizer') ] = report_LCI(('Technosphere', 'Nitrogen_Fertilizer'),self.LCI,y)
            Technosphere[y][('Technosphere', 'Phosphorous_Fertilizer')] = report_LCI(('Technosphere', 'Phosphorous_Fertilizer'),self.LCI,y)
            Technosphere[y][('Technosphere', 'Potassium_Fertilizer')] = report_LCI(('Technosphere', 'Potassium_Fertilizer'),self.LCI,y)
            Technosphere[y][('Technosphere', 'Peat')] = report_LCI(('Technosphere', 'Peat'),self.LCI,y)
            Technosphere[y][('Technosphere', 'compost_to_LF')] = report_LCI(('Technosphere', 'compost_to_LF'),self.LCI,y)

### Output Biosphere Database
            Biosphere[y][('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014')]= report_LCI('Ammonia',self.LCI,y) #  Ammonia ('air',)
            Biosphere[y][('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6')]= report_LCI('Carbon dioxide, non-fossil storage',self.LCI,y)  #Carbon dioxide, from soil or biomass stock ('air',)
            Biosphere[y][('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')]= report_LCI('Carbon dioxide, non-fossil',self.LCI,y) #Carbon dioxide, non-fossil ('air',)
            Biosphere[y][('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98')]= report_LCI('Dinitrogen monoxide',self.LCI,y) #Dinitrogen monoxide ('air',)
            Biosphere[y][('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8')]= report_LCI('Methane, non-fossil',self.LCI,y) #Methane, non-fossil ('air',)
            Biosphere[y][('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457')]= report_LCI('Nitrogen oxides',self.LCI,y) #Nitrogen oxides ('air',)
            Biosphere[y][('biosphere3', 'd3260d0e-8203-4cbb-a45a-6a13131a5108')]= report_LCI('VOCs emitted',self.LCI,y) #NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
            Biosphere[y][('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33')]= report_LCI('Nitrate (ground water)',self.LCI,y) #Nitrate ('water', 'ground-')
            Biosphere[y][('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35')]= report_LCI('Nitrate (Surface water)',self.LCI,y) #Nitrate ('water', 'surface water')
            Biosphere[y][('biosphere3', '736f52e8-9703-4076-8909-7ae80a7f8005')]= report_LCI('Ammonium, ion (ground water)',self.LCI,y) #'Ammonium, ion' (kilogram, None, ('water', 'ground-'))
            Biosphere[y][('biosphere3', '13331e67-6006-48c4-bdb4-340c12010036')]= report_LCI('Ammonium, ion (surface water)',self.LCI,y) # 'Ammonium, ion' (kilogram, None, ('water', 'surface water'))                
        return(self.COMP)


from time import time
A=Comp()
c= time()
for i in range(100):
    A.calc()
    A.report()
print(time()-c)

