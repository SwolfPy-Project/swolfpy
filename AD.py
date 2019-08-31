# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:35:15 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
from AD_Input import *
from CommonData import *
from stats_arrays import *
from flow import *

class AD:
    def __init__(self):
        self.CommonData = CommonData()
        self.AD_input= AD_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'AD', index_col = 'Parameter')
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
        self.Assumed_Comp = pd.Series(self.AD_input.Assumed_Comp,index=self.Index)
                ### Mass Flows
    def calc(self):
        self.LCI = pd.DataFrame(index = self.Index)
### Initial mass 
        self.Input = flow(self.Material_Properties[4:])
        self.Input.init_flow(1000)
        
### Primary Pre_screen     
        self.S1_unders,self.S1_overs=AD_screen(self.Input,self.process_data['Percent screened out in primary pre-screening (not sent to reactor)'][3:]/100, self.Material_Properties[4:],self.LCI)
    
### Secondary Pre_screen         
        self.S2_to_curing,self.S2_residuls=AD_screen(self.S1_overs,self.process_data['Percent screened out in secondary pre-screening (residual not sent to composting)'][3:]/100, self.Material_Properties[4:],self.LCI)
        # Dsl use for grinding
        add_LCI('Diesel Total', self.S2_to_curing.data['mass']/1000 *self.AD_input.shredding['Mtgp']['amount']*self.AD_input.shredding['Mtgf']['amount'] ,self.LCI) 
        
        add_LCI('Residual', self.S2_residuls.data['mass']/1000 ,self.LCI) 
        
        
### Adding Water   
        water_flow = (self.S1_unders.data['mass']*self.AD_input.Material_Properties['ad_mcReactor']['amount'] - self.S1_unders.data['moist_cont'])\
                        /(1-self.AD_input.Material_Properties['ad_mcReactor']['amount'])
        self.to_reactor = add_water_AD(self.S1_unders,water_flow,self.Material_Properties[4:])

### Reactor                 
        self.digestate = Reactor(self.to_reactor,self.CommonData,self.process_data[3:],self.AD_input,self.Material_Properties[4:],self.AD_input.emission_factor,self.LCI)

### Dewatering    
        self.Dig_to_Curing_1,self.liq_rem,self.liq_treatment_vol = Dewater(self.digestate,self.CommonData,self.process_data[3:],self.AD_input,self.Material_Properties[4:],water_flow,self.Assumed_Comp,self.LCI)

### Mix Dig_to_Curing_1 and S2_to_curing
        self.Dig_to_Curing = AD_mix(self.Dig_to_Curing_1,self.S2_to_curing,self.Material_Properties[4:])

### Curing
        self.compot_to_ps,self.WC_SC = AD_curing(self.Dig_to_Curing,self.to_reactor,self.CommonData,self.process_data[3:],self.AD_input,self.Assumed_Comp,self.Material_Properties[4:],self.LCI)
    
### Post_screen
        self.FinalCompost = AD_Post_screen(self.compot_to_ps,self.WC_SC,self.AD_input,self.Assumed_Comp,self.Material_Properties[4:],self.LCI)
        
###  POTW       
        POTW (self.liq_treatment_vol,self.liq_rem,self.to_reactor,self.Dig_to_Curing,self.FinalCompost,self.Index,self.AD_input,self.Assumed_Comp,self.Material_Properties[4:],self.CommonData,self.LCI)    

### AD Diesel and electricity use (general)    
        add_LCI('Diesel Total', self.AD_input.Fac_Energy['Dsl_facility']['amount'] ,self.LCI)  
        add_LCI('Electricity Use', self.AD_input.Fac_Energy['elec_facility']['amount'] ,self.LCI)
        add_LCI('Electricity Use', self.AD_input.Fac_Energy['elec_preproc']['amount'] ,self.LCI) 

### Compost use
        AD_compost_use(self.FinalCompost,self.CommonData,self.process_data[3:],self.Material_Properties[4:],self.Assumed_Comp,self.AD_input,self.LCI)

### Transportation Compost
        add_LCI('Full_Medium-duty truck transport of compost to land application', self.FinalCompost.data['mass'] * self.AD_input.Land_app['distLand']['amount'] ,self.LCI)
        add_LCI('Empty_Medium-duty truck transport return from land application', self.FinalCompost.data['mass']/1000 / self.AD_input.Land_app['land_payload']['amount']* self.AD_input.Land_app['distLand']['amount'] ,self.LCI)

### process_data update    
    def create_uncertainty_from_inputs(self,seed=None):
        self.process_data_1=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'AD', index_col = 'Parameter')
        self.uncertain_dict = dict()
        cols = list(self.process_data_1)
        for col in range(0,len(cols),7):
            self.uncertain_dict[cols[col]] = list()
            for val in range(len(self.process_data[cols[col]][3:])):
                self.uncertain_dict[cols[col]].append(dict())
                if not np.isnan(self.process_data_1[cols[col+1]][3+val]):
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = int(self.process_data_1[cols[col+1]][3+val])
                    self.uncertain_dict[cols[col]][val]['loc'] = self.process_data_1[cols[col+2]][3+val]
                    self.uncertain_dict[cols[col]][val]['scale'] = self.process_data_1[cols[col+3]][3+val]
                    self.uncertain_dict[cols[col]][val]['shape'] = self.process_data_1[cols[col+4]][3+val]
                    self.uncertain_dict[cols[col]][val]['minimum'] = self.process_data_1[cols[col+5]][3+val]
                    self.uncertain_dict[cols[col]][val]['maximum'] = self.process_data_1[cols[col+6]][3+val]
                else:
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = 1
							
        self.variables = dict()
        self.rng = dict()
        for key in self.uncertain_dict.keys():
            self.variables[key] = UncertaintyBase.from_dicts(*self.uncertain_dict[key])
            self.rng[key] = MCRandomNumberGenerator(self.variables[key],seed=seed)
		
    def uncertainty_input_next(self):
        data = dict()
        for key in self.rng.keys():
            data[key] = self.rng[key].next()
            for val in range(len(self.process_data[key][3:])):
                if not np.isnan(data[key][val]):			
                    self.process_data.at[(self.process_data_1.index.values[3+val]),key] = data[key][val]

    def setup_MC(self,seed=None):
        self.AD_input.setup_MC(seed)
        #self.create_uncertainty_from_inputs()
    
    def MC_calc(self):      
        input_list = self.AD_input.gen_MC()
        #self.uncertainty_input_next()
        self.calc()
        return(input_list)
        
    def report(self):
### Output
        self.AD = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.AD ["process name"] = 'COMP'
        self.AD  ["Waste"] = Waste
        self.AD  ["Technosphere"] = Technosphere
        self.AD  ["Biosphere"] = Biosphere
        
        for x in [Waste,Technosphere, Biosphere]:
            for y in self.Index:
                x[y]={}
                                                       
               
        for y in self.Index:
### Output Waste Database 
            Waste[y]['Other_Residual'] = self.LCI['Residual'][y]
            
### Output Technospphere Database
            Technosphere[y][('Technosphere', 'Electricity_production')] = self.LCI['Electricity Production'][y]
            Technosphere[y][('Technosphere', 'Electricity_consumption')] = self.LCI['Electricity Use'][y]
            Technosphere[y][('Technosphere', 'Equipment_Diesel')] = self.LCI['Diesel Total'][y]
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')] = self.LCI['Full_Total heavy duty truck tranport'][y]
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck')] = self.LCI['Full_Medium-duty truck transport of compost to land application'] [y]
            Technosphere[y][('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck')] = self.LCI['Empty_Total heavy duty truck empty return'][y]
            Technosphere[y][('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck')] = self.LCI['Empty_Medium-duty truck transport return from land application'][y]
            
            if self.AD_input.AD_operation['fertOff']['amount'] == 1 and self.AD_input.AD_operation['choice_BU']['amount'] == 1:
                Technosphere[y][('Technosphere', 'Nitrogen_Fertilizer')] = self.LCI['Nitrogen Mineral Fertilizer Equivalent mass to offset'][y]
                Technosphere[y][('Technosphere', 'Phosphorous_Fertilizer')] = self.LCI['Phosphorous Mineral Fertilizer Equivalent mass to offset'][y]
                Technosphere[y][('Technosphere', 'Potassium_Fertilizer')] = self.LCI['Potassium Mineral Fertilizer Equivalent mass to offset'][y]
            else:
                Technosphere[y][('Technosphere', 'Nitrogen_Fertilizer')] = 0
                Technosphere[y][('Technosphere', 'Phosphorous_Fertilizer')] = 0
                Technosphere[y][('Technosphere', 'Potassium_Fertilizer')] = 0
            
            if self.AD_input.AD_operation['peatOff']['amount'] == 1 and self.AD_input.AD_operation['choice_BU']['amount'] == 1:
                Technosphere[y][('Technosphere', 'Peat')] = self.LCI['Peat Equivalent mass to offset'][y]
            else:
                Technosphere[y][('Technosphere', 'Peat')] = 0
            
            if self.AD_input.AD_operation['choice_BU']['amount'] == 0:
                Technosphere[y][('Technosphere', 'compost_to_LF')] = self.LCI['compost_to_LF'][y]
            else:
                Technosphere[y][('Technosphere', 'compost_to_LF')] = 0
            
### Output Biosphere Database
            Biosphere[y][('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014')]= self.LCI['Ammonia'][y] #Ammonia ('air',)
            Biosphere[y][('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6')]= self.LCI['Direct Carbon Storage and Humus Formation'][y]# Carbon dioxide, from soil or biomass stock ('air',)
            Biosphere[y][('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')]= self.LCI['CO2-biogenic emissions from digested liquids treatment'][y] +  self.LCI['Carbon dioxide, non-fossil _ Curing'][y]\
                                                                                + self.LCI['Carbon dioxide, non-fossil _ Land application'][y] + self.LCI['Carbon dioxide, non-fossil (in biogas)'][y] \
                                                                                + self.LCI['Carbon dioxide, non-fossil from comubstion'][y] # Carbon dioxide, non-fossil ('air',)
            Biosphere[y][('biosphere3', '2cb2333c-1599-46cf-8435-3dffce627524')]= self.LCI['Carbon monoxide (CO)'][y] # Carbon monoxide, non-fossil ('air',)
            Biosphere[y][('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98')]= self.LCI['Dinitrogen monoxide'][y] # Dinitrogen monoxide ('air',)
            Biosphere[y][('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8')]= self.LCI['Methane, non-fossil'][y] + self.LCI['Methane, non-fossil (unburned)'][y] \
                                                                                    + self.LCI['Fugitive (Leaked) Methane'][y] # Methane, non-fossil ('air',)
            Biosphere[y][('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457')]= self.LCI['Nitrogen oxides (as NO2)'][y] # Nitrogen oxides ('air',)
            Biosphere[y][('biosphere3', 'd3260d0e-8203-4cbb-a45a-6a13131a5108')]= self.LCI['NMVOC, non-methane volatile organic compounds, unspecified origin'][y] + self.LCI['NMVOCs'][y]#NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
            Biosphere[y][('biosphere3', '21e46cb8-6233-4c99-bac3-c41d2ab99498')]= self.LCI['PM2.5'][y] #Particulates, < 2.5 um ('air',)
            Biosphere[y][('biosphere3', 'fd7aa71c-508c-480d-81a6-8052aad92646')]= self.LCI['Sulfur dioxide (SO2)'][y] # Sulfur dioxide ('air',)
            Biosphere[y][('biosphere3', '8c8ffaa5-84ed-4668-ba7d-80fd0f47013f')]= self.LCI['Arsenic'][y] # Arsenic, ion ('water', 'surface water') 
            Biosphere[y][('biosphere3', '2c872773-0a29-4831-93b9-d49b116fa7d5')]= self.LCI['Barium'][y]  # Barium ('water', 'surface water')
            Biosphere[y][('biosphere3', '70d467b6-115e-43c5-add2-441de9411348')]= self.LCI['BOD'][y] # BOD5, Biological Oxygen Demand ('water', 'surface water')
            Biosphere[y][('biosphere3', 'af83b42f-a4e6-4457-be74-46a87798f82a')]= self.LCI['Cadmium'][y] # Cadmium, ion ('water', 'surface water')
            Biosphere[y][('biosphere3', 'e34d3da4-a3d5-41be-84b5-458afe32c990')]= self.LCI['Chromium'][y] # Chromium, ion ('water', 'surface water')
            Biosphere[y][('biosphere3', 'fc0b5c85-3b49-42c2-a3fd-db7e57b696e3')]= self.LCI['COD'][y] # COD, Chemical Oxygen Demand ('water', 'surface water')
            Biosphere[y][('biosphere3', '6d9550e2-e670-44c1-bad8-c0c4975ffca7')]= self.LCI['Copper'][y] # Copper, ion ('water', 'surface water')
            Biosphere[y][('biosphere3', '7c335b9c-a403-47a8-bb6d-2e7d3c3a230e')]= self.LCI['Iron'][y] # Iron, ion ('water', 'surface water')
            Biosphere[y][('biosphere3', 'b3ebdcc3-c588-4997-95d2-9785b26b34e1')]= self.LCI['Lead'][y] # Lead ('water', 'surface water')          
            Biosphere[y][('biosphere3', '66bfb434-78ab-4183-b1a7-7f87d08974fa')]= self.LCI['Mercury'][y] # Mercury ('water', 'surface water')
            Biosphere[y][('biosphere3', 'ae70ca6c-807a-482b-9ddc-e449b4893fe3')]= self.LCI['Total N'][y] # Nitrogen ('water', 'surface water')  
            Biosphere[y][('biosphere3', '1727b41d-377e-43cd-bc01-9eaba946eccb')]= self.LCI['Phosphate'][y]  # Phosphate ('water', 'surface water')   
            Biosphere[y][('biosphere3', '544dbea9-1d18-44ff-b92b-7866e3baa6dd')]= self.LCI['Selenium'][y] # Selenium ('water', 'surface water')
            Biosphere[y][('biosphere3', 'af9793ba-25a1-4928-a14a-4bcf7d5bd3f7')]= self.LCI['Silver'][y]  # Silver, ion ('water', 'surface water')
            Biosphere[y][('biosphere3', '3844f446-ded5-4727-8421-17a00ef4eba7')]= self.LCI['Total suspended solids'][y] # Suspended solids, unspecified ('water', 'surface water')   
            Biosphere[y][('biosphere3', '541b633c-17a3-4047-bce6-0c0e4fdb7c10')]= self.LCI['Zinc'][y] # Zinc, ion ('water', 'surface water')           

            if self.AD_input.AD_operation['choice_BU']['amount'] == 1:
                Biosphere[y][('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33')]= self.LCI['Nitrate (ground water)'][y] #Nitrate ('water', 'ground-')
                Biosphere[y][('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35')]= self.LCI['Nitrate (Surface water)'][y] #Nitrate ('water', 'surface water')
            else:
                Biosphere[y][('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33')]= 0 #Nitrate ('water', 'ground-')
                Biosphere[y][('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35')]= 0 #Nitrate ('water', 'surface water')



            if self.AD_input.AD_operation['choice_BU']['amount'] == 0:
                Biosphere[y][('biosphere3', '736f52e8-9703-4076-8909-7ae80a7f8005')]= self.LCI['Ammonium, ion (ground water)'][y] #'Ammonium, ion' (kilogram, None, ('water', 'ground-'))
                Biosphere[y][('biosphere3', '13331e67-6006-48c4-bdb4-340c12010036')]= self.LCI['Ammonium, ion (surface water)'][y] # 'Ammonium, ion' (kilogram, None, ('water', 'surface water'))  
            else:
                Biosphere[y][('biosphere3', '736f52e8-9703-4076-8909-7ae80a7f8005')]= 0 #'Ammonium, ion' (kilogram, None, ('water', 'ground-'))
                Biosphere[y][('biosphere3', '13331e67-6006-48c4-bdb4-340c12010036')]= 0 # 'Ammonium, ion' (kilogram, None, ('water', 'surface water'))  
     
        
        return(self.AD)    

"""
A=AD()
A.calc()
AA=A.report()
AAA=A.LCI
"""
from time import time
B = time()
A=AD()
for i in range(100):
    A.calc() 
    A.report()
print(time()-B)

