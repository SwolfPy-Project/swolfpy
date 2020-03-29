# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:35:15 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
#from AD_Input_script import *
from .AD_Input import *
from .CommonData import *
from stats_arrays import *
from .flow import *
from .AD_subprocess import *
from pathlib import Path

class AD:
    def __init__(self,input_data_path=None,CommonDataObjct=None):
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()
            
        self.Process_Type = 'Treatment'
        self.InputData= AD_input(input_data_path)
        ### Read Material properties
        self.Material_Properties=pd.read_excel(Path(__file__).parent.parent/"Data/Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel(Path(__file__).parent.parent/"Data/Material properties - process modles.xlsx", sheet_name = 'AD', index_col = 'Parameter')
        self.process_data.fillna(0,inplace=True)
        self.Index = self.CommonData.Index
        self.Assumed_Comp = pd.Series(self.InputData.Assumed_Comp,index=self.Index)
        self.flow_init = flow(self.Material_Properties[4:])


    def calc(self):
        self.LCI = pd.DataFrame(index = self.Index)
        self.LCI_index = False
### Initial mass 
        self.Input = flow(self.Material_Properties[4:])
        self.Input.init_flow(1000)
        
### Primary Pre_screen     
        self.S1_unders,self.S1_overs=AD_screen(self.Input,self.process_data['Percent screened out in primary pre-screening (not sent to reactor)'][3:].values/100, self.Material_Properties[4:],self.LCI,self.flow_init)
    
### Secondary Pre_screen         
        self.S2_to_curing,self.S2_residuls=AD_screen(self.S1_overs,self.process_data['Percent screened out in secondary pre-screening (residual not sent to composting)'][3:].values/100, self.Material_Properties[4:],self.LCI,self.flow_init)
        # Dsl use for grinding
        add_LCI(('Technosphere', 'Equipment_Diesel'), self.S2_to_curing.data['mass'].values/1000 *self.InputData.shredding['Mtgp']['amount']*self.InputData.shredding['Mtgf']['amount'] ,self.LCI) 
        
        add_LCI('Residual', self.S2_residuls.data['mass'].values/1000 ,self.LCI) 
        
        
### Adding Water   
        water_flow = (self.S1_unders.data['mass'].values*self.InputData.Material_Properties['ad_mcReactor']['amount'] - self.S1_unders.data['moist_cont'].values)\
                        /(1-self.InputData.Material_Properties['ad_mcReactor']['amount'])
        self.to_reactor = add_water_AD(self.S1_unders,water_flow,self.Material_Properties[4:],self.flow_init)

### Reactor                 
        self.digestate = Reactor(self.to_reactor,self.CommonData,self.process_data[3:],self.InputData,self.Material_Properties[4:],self.InputData.emission_Engine,self.InputData.emission_Flare,self.LCI,self.flow_init)

### Dewatering    
        self.Dig_to_Curing_1,self.liq_rem,self.liq_treatment_vol = Dewater(self.digestate,self.CommonData,self.process_data[3:],self.InputData,self.Material_Properties[4:],water_flow,self.Assumed_Comp.values,self.LCI,self.flow_init)

### Mix Dig_to_Curing_1 and S2_to_curing
        self.Dig_to_Curing = AD_mix(self.Dig_to_Curing_1,self.S2_to_curing,self.Material_Properties[4:],self.flow_init)

### Curing
        self.compot_to_ps,self.WC_SC = AD_curing(self.Dig_to_Curing,self.to_reactor,self.CommonData,self.process_data[3:],self.InputData,self.Assumed_Comp,self.Material_Properties[4:],self.LCI,self.flow_init)
    
### Post_screen
        self.FinalCompost = AD_Post_screen(self.compot_to_ps,self.WC_SC,self.InputData,self.Assumed_Comp.values,self.Material_Properties[4:],self.LCI,self.flow_init)
        
###  POTW       
        POTW (self.liq_treatment_vol,self.liq_rem,self.to_reactor,self.Dig_to_Curing,self.FinalCompost,self.Index,self.InputData,self.Assumed_Comp.values,self.Material_Properties[4:],self.CommonData,self.LCI)    

### AD Diesel and electricity use (general)    
        add_LCI(('Technosphere', 'Equipment_Diesel'), self.InputData.Fac_Energy['Dsl_facility']['amount'] ,self.LCI)  
        add_LCI(('Technosphere', 'Electricity_consumption'), self.InputData.Fac_Energy['elec_facility']['amount'] ,self.LCI)
        add_LCI(('Technosphere', 'Electricity_consumption'), self.InputData.Fac_Energy['elec_preproc']['amount'] ,self.LCI) 

### Compost use
        AD_compost_use(self.FinalCompost,self.CommonData,self.process_data[3:],self.Material_Properties[4:],self.Assumed_Comp.values,self.InputData,self.LCI)

### Transportation Compost
        add_LCI(('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck'), self.FinalCompost.data['mass'].values * self.InputData.Land_app['distLand']['amount'] ,self.LCI)
        add_LCI(('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck'), self.FinalCompost.data['mass'].values/1000 / self.InputData.Land_app['land_payload']['amount']* self.InputData.Land_app['distLand']['amount'] ,self.LCI)

    def setup_MC(self,seed=None):
        self.InputData.setup_MC(seed)
        #self.create_uncertainty_from_inputs()
    
    def MC_calc(self):      
        input_list = self.InputData.gen_MC()
        #self.uncertainty_input_next()
        self.calc()
        return(input_list)
        
    def report(self):
### Output
        self.AD = {}
        self.AD["process name"] = 'AD'

        # Set the value zero if the flow is not in the LCI dataframe.
        for i in [('Technosphere', 'Nitrogen_Fertilizer'),
                  ('Technosphere', 'Phosphorous_Fertilizer'),
                  ('Technosphere', 'Potassium_Fertilizer'),
                  ('Technosphere', 'Peat'),
                  ('Technosphere', 'compost_to_LF'),
                  'Ammonium, ion (ground water)',
                  'Ammonium, ion (surface water)',
                  'Nitrate (ground water)',
                  'Nitrate (Surface water)']:
            if i not in self.LCI.columns:
                self.LCI[i] = 0
        
        self.LCI['report_Methane, non-fossil'] =  self.LCI['Methane, non-fossil'].values + self.LCI['Methane, non-fossil (unburned)'].values \
                                                                                    + self.LCI['Fugitive (Leaked) Methane'].values # Methane, non-fossil ('air',)
    
        self.LCI['report_ CO2 non-fossil'] = self.LCI['CO2-biogenic emissions from digested liquids treatment'].values +  self.LCI['Carbon dioxide, non-fossil _ Curing'].values\
                                                                                + self.LCI['Carbon dioxide, non-fossil _ Land application'].values + self.LCI['Carbon dioxide, non-fossil (in biogas)'].values \
                                                                                + self.LCI['Carbon dioxide, non-fossil from comubstion'].values # Carbon dioxide, non-fossil ('air',)
        
        self.LCI['report_ NMVOC'] =self.LCI['NMVOC, non-methane volatile organic compounds, unspecified origin'].values + self.LCI['NMVOCs'].values #NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
        
        
        bio_rename_dict = { 'Ammonia':('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014'), #Ammonia ('air',)
                            'Direct Carbon Storage and Humus Formation':('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6'),# Carbon dioxide, from soil or biomass stock ('air',)
                            'report_ CO2 non-fossil':('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7'), # Carbon dioxide, non-fossil ('air',)
                            'Carbon monoxide (CO)':('biosphere3', '2cb2333c-1599-46cf-8435-3dffce627524'), # Carbon monoxide, non-fossil ('air',)
                            'Dinitrogen monoxide':('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98'), # Dinitrogen monoxide ('air',)
                            'report_Methane, non-fossil':('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8') , # Methane, non-fossil ('air',)
                            'Nitrogen oxides (as NO2)':('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457'), # Nitrogen oxides ('air',)
                            'report_ NMVOC':('biosphere3', 'd3260d0e-8203-4cbb-a45a-6a13131a5108'),#NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
                            'PM2.5':('biosphere3', '21e46cb8-6233-4c99-bac3-c41d2ab99498'), #Particulates, < 2.5 um ('air',)
                            'Sulfur dioxide (SO2)':('biosphere3', 'fd7aa71c-508c-480d-81a6-8052aad92646'), # Sulfur dioxide ('air',)
                            'Arsenic':('biosphere3', '8c8ffaa5-84ed-4668-ba7d-80fd0f47013f'), # Arsenic, ion ('water', 'surface water') 
                            'Barium':('biosphere3', '2c872773-0a29-4831-93b9-d49b116fa7d5'),  # Barium ('water', 'surface water')
                            'BOD':('biosphere3', '70d467b6-115e-43c5-add2-441de9411348'), # BOD5, Biological Oxygen Demand ('water', 'surface water')
                            'Cadmium':('biosphere3', 'af83b42f-a4e6-4457-be74-46a87798f82a'), # Cadmium, ion ('water', 'surface water')
                            'Chromium':('biosphere3', 'e34d3da4-a3d5-41be-84b5-458afe32c990'), # Chromium, ion ('water', 'surface water')
                            'COD':('biosphere3', 'fc0b5c85-3b49-42c2-a3fd-db7e57b696e3'), # COD, Chemical Oxygen Demand ('water', 'surface water')
                            'Copper':('biosphere3', '6d9550e2-e670-44c1-bad8-c0c4975ffca7'), # Copper, ion ('water', 'surface water')
                            'Iron':('biosphere3', '7c335b9c-a403-47a8-bb6d-2e7d3c3a230e'), # Iron, ion ('water', 'surface water')
                            'Lead':('biosphere3', 'b3ebdcc3-c588-4997-95d2-9785b26b34e1'), # Lead ('water', 'surface water')          
                            'Mercury':('biosphere3', '66bfb434-78ab-4183-b1a7-7f87d08974fa'), # Mercury ('water', 'surface water')
                            'Total N':('biosphere3', 'ae70ca6c-807a-482b-9ddc-e449b4893fe3'), # Nitrogen ('water', 'surface water')  
                            'Phosphate':('biosphere3', '1727b41d-377e-43cd-bc01-9eaba946eccb'),  # Phosphate ('water', 'surface water')   
                            'Selenium':('biosphere3', '544dbea9-1d18-44ff-b92b-7866e3baa6dd'), # Selenium ('water', 'surface water')
                            'Silver':('biosphere3', 'af9793ba-25a1-4928-a14a-4bcf7d5bd3f7'),  # Silver, ion ('water', 'surface water')
                            'Total suspended solids':('biosphere3', '3844f446-ded5-4727-8421-17a00ef4eba7'), # Suspended solids, unspecified ('water', 'surface water')   
                            'Zinc':('biosphere3', '541b633c-17a3-4047-bce6-0c0e4fdb7c10'), # Zinc, ion ('water', 'surface water')           
                            'Nitrate (ground water)':('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33'), #Nitrate ('water', 'ground-')
                            'Nitrate (Surface water)':('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35'), #Nitrate ('water', 'surface water')
                            'Ammonium, ion (ground water)':('biosphere3', '736f52e8-9703-4076-8909-7ae80a7f8005'), #'Ammonium, ion' (kilogram, None, ('water', 'ground-'))
                            'Ammonium, ion (surface water)':('biosphere3', '13331e67-6006-48c4-bdb4-340c12010036') # 'Ammonium, ion' (kilogram, None, ('water', 'surface water'))  
                            }
        
        tech_flows=[('Technosphere', 'Electricity_production'),
                   ('Technosphere', 'Electricity_consumption'),
                   ('Technosphere', 'Equipment_Diesel'),
                   ('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck'),
                   ('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck'),
                   ('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck'),
                   ('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck'),
                   ('Technosphere', 'Nitrogen_Fertilizer'),
                   ('Technosphere', 'Phosphorous_Fertilizer'),
                   ('Technosphere', 'Potassium_Fertilizer'),
                   ('Technosphere', 'Peat'),
                   ('Technosphere', 'compost_to_LF')]
        
        
        self.Waste = {}
        for y in self.Index:
            self.Waste[y]={}
            self.Waste[y]['Other_Residual'] = self.LCI['Residual'][y]
        self.AD["Waste"] = self.Waste
        
        self.Technosphere = self.LCI[tech_flows].transpose().to_dict()
        self.AD["Technosphere"] = self.Technosphere
        
        # report function rename the LCI dataframe, so we use the self.LCI_index to rename LCI only one time 
        # unless the we call the calc function
        if not self.LCI_index:
            self.LCI=self.LCI.rename(columns=bio_rename_dict)
            self.LCI_index = True
        
        self.Biosphere = self.LCI[bio_rename_dict.values()].transpose().to_dict()
        self.AD["Biosphere"] = self.Biosphere
        
        return(self.AD)    


# =============================================================================
# from time import time
# A=AD()
# B = time()
# for i in range(100):
#     A.calc() 
#     A.report()
# print(time()-B)
# =============================================================================


