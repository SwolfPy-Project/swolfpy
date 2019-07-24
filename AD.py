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

class AD:
    def __init__(self):
        self.CommonData = CommonData()
        self.AD_input= AD_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'AD', index_col = 'Parameter')
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
        #self.Assumed_Comp = pd.Series(self.AD_Input.Assumed_Comp,index=self.Index)
        self.SD=pd.read_excel('AD_stat.xlsx', index_col = 'Index')
                ### Mass Flows
        self.Mass_flows=pd.DataFrame(index = self.Index)
    def calc(self):
        pass
    def calc2(self):
        self.LCI=pd.DataFrame(index = self.Index)

### Biogenic Carbon Balance        
        self.LCI['Direct Carbon Storage and Humus Formation'] = (self.SD['Carbon sequestered due to humus formation'][2:]+self.SD['Carbon sequestered for 100 years']) * \
                                                self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['C']['amount'] 
        self.LCI.loc ['Unit','Direct Carbon Storage and Humus Formation'] = 'kg CO2/Mg'
        
        self.LCI['CO2-biogenic emissions from digested liquids treatment'] = self.SD['Mass of BOD removed'][2:] * self.CommonData.Leachate_treat['co2bod']['amount']
        self.LCI.loc ['Unit','CO2-biogenic emissions from digested liquids treatment'] = 'kg CO2/Mg'

### Liquid Treatment Effluent         
        self.LCI['COD'] = self.SD['COD'][2:] * (100-self.CommonData.WWT['cod_rem']['amount'])/100
        self.LCI.loc ['Unit','COD'] = 'kg/Mg'
        
        self.LCI['BOD'] = self.SD['BOD'][2:] * (100-self.CommonData.WWT['bod_rem']['amount'])/100
        self.LCI.loc ['Unit','BOD'] = 'kg/Mg'
        
        self.LCI['Total suspended solids'] = self.SD['Total suspended solids'][2:] * (100-self.CommonData.WWT['tss_rem']['amount'])/100
        self.LCI.loc ['Unit','Total suspended solids'] = 'kg/Mg'
        
        key1 =['Iron','Copper','Cadmium','Arsenic','Mercury','Selenium','Chromium','Lead','Zinc','Barium','Silver']
        for i in key1:    
            self.LCI[i] = self.SD[i][2:] * (100-self.CommonData.WWT['metals_rem']['amount'])/100
            self.LCI.loc ['Unit',i] = 'kg/Mg'
        
        self.LCI['Phosphate'] = self.SD['Phosphate'][2:] * (100-self.CommonData.WWT['p_rem']['amount'])/100
        self.LCI.loc ['Unit','Phosphate'] = 'kg/Mg'
        
        self.LCI['Total N'] = self.SD['Total N'][2:] * (100-self.CommonData.WWT['n_rem']['amount'])/100
        self.LCI.loc ['Unit','Total N'] = 'kg/Mg'
        
### Biodegradation in Curing and Land Application     
        self.LCI['Ammonia'] = (self.SD['Nitrogen remaining in final compost'][2:]*self.AD_input.Land_app['perNasNH3fc']['amount']/100*self.AD_input.Land_app['perNH3evap']['amount']/100*\
                            self.process_data['Percent NPK available as nutrient or emission (in addition to MFE)'][3:]/100 + self.SD['Ammonia emissions from cured digestate'][2:]) *\
                            self.CommonData.MW['Ammonia']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Ammonia'] = 'kg/Mg'
        
        self.LCI['Dinitrogen monoxide'] = (self.SD['Nitrogen remaining in final compost'][2:]*self.AD_input.Land_app['perN2Oevap']['amount']/100*\
                            self.process_data['Percent NPK available as nutrient or emission (in addition to MFE)'][3:]/100 + self.SD['N2O production during curing'][2:]) *\
                            self.CommonData.MW['Nitrous_Oxide']['amount']/self.CommonData.MW['N']['amount']
        self.LCI.loc ['Unit','Dinitrogen monoxide'] = 'kg/Mg'
        
        self.LCI['Carbon dioxide, non-fossil _ Curing'] = self.SD['C loss during curing'][1:]*(1-self.AD_input.Curing_Bio['ad_pCasCH4']['amount'])*\
                                                    self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil _ Curing'] = 'kg/Mg'
        
        self.LCI['Methane, non-fossil'] = self.SD['Methane production during curing'][1:] * self.CommonData.MW['CH4']['amount'] / self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Methane, non-fossil'] = 'kg/Mg'
        
        self.LCI['NMVOC, non-methane volatile organic compounds, unspecified origin'] = self.SD['VOC emissions from cured digestate'][1:]
        self.LCI.loc ['Unit','NMVOC, non-methane volatile organic compounds, unspecified origin'] = 'kg/Mg'
        
        self.LCI['Carbon dioxide, non-fossil _ Land application'] = self.SD['CO2 biomass released after land application'][1:] *  self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil _ Land application'] = 'kg/Mg'

### Nutrient/Soil Offsets     
        self.LCI['Peat Equivalent mass to offset'] = self.AD_input.AD_operation['choice_BU']['amount'] *self.AD_input.AD_operation['peatOff']['amount'] *\
                                                   self.SD['Volume of post-screened compost'][2:]/1000*self.AD_input.Land_app['ad_PeatSubFac']['amount']\
                                                   *self.AD_input.Land_app['ad_densPeat']['amount']*self.SD['Peat offset Allocation Factor'][2:]
        self.LCI.loc ['Unit','Peat Equivalent mass to offset'] = 'Mg/Mg'
        
        self.LCI['Nitrogen Mineral Fertilizer Equivalent mass to offset'] = self.AD_input.AD_operation['choice_BU']['amount'] *self.AD_input.AD_operation['fertOff']['amount']\
                                                                            *self.SD['Nitrogen remaining in final compost'][2:]*self.CommonData.Land_app['MFEN']['amount']*\
                                                                            (self.process_data['Percent NPK available as nutrient or emission (in addition to MFE)'][3:]/100)
        self.LCI.loc ['Unit','Nitrogen Mineral Fertilizer Equivalent mass to offset'] = 'kg/Mg'
        
        self.ad_PtoN =  1
        self.ad_KtoN =  0.46892645

        self.LCI['Phosphorous Mineral Fertilizer Equivalent mass to offset'] = self.AD_input.AD_operation['choice_BU']['amount'] *self.AD_input.AD_operation['fertOff']['amount']\
                                                                            *self.SD['Phosphorus in solid digestate'][2:]*self.CommonData.Land_app['MFEP']['amount']*self.ad_PtoN\
                                                                            *(self.process_data['Percent NPK available as nutrient or emission (in addition to MFE)'][3:]/100)
        self.LCI.loc ['Unit','Phosphorous Mineral Fertilizer Equivalent mass to offset'] = 'kg/Mg'
 
        self.LCI['Potassium Mineral Fertilizer Equivalent mass to offset'] = self.AD_input.AD_operation['choice_BU']['amount'] *self.AD_input.AD_operation['fertOff']['amount']\
                                                                            *self.SD['Potassium in digestate'][2:]*self.CommonData.Land_app['MFEK']['amount']*self.ad_KtoN\
                                                                            *(self.process_data['Percent NPK available as nutrient or emission (in addition to MFE)'][3:]/100)
        self.LCI.loc ['Unit','Potassium Mineral Fertilizer Equivalent mass to offset'] = 'kg/Mg'
        
### Biogas Emission
        self.LCI['Carbon dioxide, non-fossil (in biogas)'] = self.SD['Mass of CO2 produced (as carbon)'][2:] * self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['C']['amount']
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil (in biogas)'] = 'kg/Mg'
        
        self.LCI['Fugitive (Leaked) Methane'] = self.SD['Total mass of methane produced (as carbon)'][2:] * (1-self.AD_input.Biogas_gen['ad_collEff']['amount']) \
                                                *(self.CommonData.MW['CH4']['amount'] / self.CommonData.MW['C']['amount'])
        self.LCI.loc ['Unit','Fugitive (Leaked) Methane'] = 'kg/Mg'
        
        self.LCI['Mass of Methane Combusted for Energy Recovery'] = self.SD['Total mass of methane produced (as carbon)'][2:] * self.AD_input.Biogas_gen['ad_collEff']['amount']  * (1-self.AD_input.Biogas_gen['ad_downTime']['amount']) \
                                                *(self.CommonData.MW['CH4']['amount'] / self.CommonData.MW['C']['amount'])
        self.LCI.loc ['Unit','Mass of Methane Combusted for Energy Recovery'] = 'kg/Mg'
        
        self.LCI['Energy of Methane Combusted for Energy Recovery'] = self.SD['Volume of methane produced'][2:] * self.AD_input.Biogas_gen['ad_collEff']['amount']  * (1-self.AD_input.Biogas_gen['ad_downTime']['amount']) \
                                                                        * self.AD_input.Biogas_gen['ad_ch4EngCont']['amount']
        self.LCI.loc ['Unit','Energy of Methane Combusted for Energy Recovery'] = 'MJ CH4/Mg'
        
        self.LCI['Mass of Methane Combusted in Flare'] = self.SD['Total mass of methane produced (as carbon)'][2:] * self.AD_input.Biogas_gen['ad_collEff']['amount']  * self.AD_input.Biogas_gen['ad_downTime']['amount'] \
                                                *(self.CommonData.MW['CH4']['amount'] / self.CommonData.MW['C']['amount'])
        self.LCI.loc ['Unit','Mass of Methane Combusted in Flare'] = 'kg/Mg'
        
        self.LCI['Energy of Methane Combusted in Flare'] = self.SD['Volume of methane produced'][2:] * self.AD_input.Biogas_gen['ad_collEff']['amount']  * self.AD_input.Biogas_gen['ad_downTime']['amount'] \
                                                                        * self.AD_input.Biogas_gen['ad_ch4EngCont']['amount']
        self.LCI.loc ['Unit','Energy of Methane Combusted in Flare'] = 'MJ CH4/Mg'
        

### Emissions from the biogass combustion
        self.LCI['Carbon dioxide, non-fossil from comubstion'] = (self.LCI['Mass of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['CH4_destruction']['amount']+\
                                                                self.LCI['Mass of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['CH4_destruction']['amount'])*\
                                                                (self.CommonData.MW['CO2']['amount'] / self.CommonData.MW['CH4']['amount'])
        self.LCI.loc ['Unit','Carbon dioxide, non-fossil from comubstion'] = 'kg/Mg'
        
        self.LCI['Methane, non-fossil (unburned)'] = self.LCI['Mass of Methane Combusted in Flare'][2:]*(1-self.AD_input.emission_factor['Flare']['CH4_destruction']['amount'])+\
                                                                self.LCI['Mass of Methane Combusted for Energy Recovery'][2:]*(1-self.AD_input.emission_factor['Engine']['CH4_destruction']['amount'])
        self.LCI.loc ['Unit','Methane, non-fossil (unburned)'] = 'kg/Mg'
        
        self.LCI['Carbon monoxide (CO)'] = (self.LCI['Energy of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['CO']['amount']+ \
                                             self.LCI['Energy of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['CO']['amount'])/10**6
        self.LCI.loc ['Unit','Carbon monoxide (CO)'] = 'kg/Mg'
        
        self.LCI['Nitrogen oxides (as NO2)'] = (self.LCI['Energy of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['NO2']['amount']+ \
                                             self.LCI['Energy of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['NO2']['amount'])/10**6
        self.LCI.loc ['Unit','Nitrogen oxides (as NO2)'] = 'kg/Mg'
        
        self.LCI['Sulfur dioxide (SO2)'] = (self.LCI['Energy of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['SO2']['amount']+ \
                                             self.LCI['Energy of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['SO2']['amount'])/10**6
        self.LCI.loc ['Unit','Sulfur dioxide (SO2)'] = 'kg/Mg'
        
        self.LCI['NMVOCs'] = (self.LCI['Energy of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['NMVOC']['amount']+ \
                            self.LCI['Energy of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['NMVOC']['amount'])/10**6
        self.LCI.loc ['Unit','NMVOCs'] = 'kg/Mg'
        
        self.LCI['PM2.5'] = (self.LCI['Energy of Methane Combusted in Flare'][2:]*self.AD_input.emission_factor['Flare']['PM']['amount']+ \
                            self.LCI['Energy of Methane Combusted for Energy Recovery'][2:]*self.AD_input.emission_factor['Engine']['PM']['amount'])/10**6
        self.LCI.loc ['Unit','PM2.5'] = 'kg/Mg'

### Equipment Fuel Use          
        self.LCI['AD Diesel Equipment'] = self.SD['Diesel equipment fuel use for anaerobic digestion']
        
        self.LCI['Front end loader'] = self.SD['Fuel used by front end loaders for curing']

        self.LCI['Windrow turner'] = self.SD['Fuel used by windrow turner']
        
        self.LCI['Tub grinder'] = self.SD['Fuel used by wood chipping'][2:] + self.SD['Fuel used by tub grinder to shred secondary overs'][2:]  
        self.LCI.loc ['Unit','Tub grinder'] = 'L/Mg feedstock'
        
        self.LCI['Digestate\compost application'] = self.SD['Diesel used to apply digestate/compost']

        self.LCI['Diesel Total'] = self.LCI['AD Diesel Equipment'][2:] + self.LCI['Front end loader'] + self.LCI['Windrow turner']  + self.LCI['Tub grinder'] + self.LCI['Digestate\compost application']
        self.LCI.loc ['Unit','Diesel Total'] = 'L/Mg feedstock'

###  Full Transportation       
        self.LCI['Full_Heavy-duty truck transportation for leachate to POTW'] = self.SD['Heavy duty truck transportation to POTW']
        
        self.LCI['Full_Heavy-duty truck transportation for sludge to landfill'] = self.SD['Heavy duty truck transportation of sludge to landfill']
        
        self.LCI['Full_Total heavy duty truck tranport'] = self.LCI['Full_Heavy-duty truck transportation for leachate to POTW'][1:] + self.LCI['Full_Heavy-duty truck transportation for sludge to landfill']
        self.LCI.loc ['Unit','Full_Total heavy duty truck tranport'] = 'kg-km/Mg'
        
        self.LCI['Full_Medium-duty truck transport of compost to land application'] = self.SD['Medium duty truck used to transport digestate/compost']
        
### Empty Return Transportation
        self.LCI['Empty_Heavy-duty truck transportation for leachate to POTW']=((self.SD['Mass of liquid digestate sent to treatment plant'][2:]/1000)/self.AD_input.Digestate_treatment['payload_POTW']['amount'])*\
                                                                        self.AD_input.Digestate_treatment['ad_distPOTW']['amount']*self.AD_input.Digestate_treatment['ad_erPOTW']['amount']
        self.LCI.loc ['Unit','Empty_Heavy-duty truck transportation for leachate to POTW'] = 'vkm'

        self.LCI['Empty_Heavy-duty truck transportation for sludge to landfill']=((self.SD['Total sludge generated'][2:]/1000)/self.AD_input.Digestate_treatment['payload_LFPOTW']['amount'])*\
                                                                self.AD_input.Digestate_treatment['wwtp_lf_dist']['amount']*self.AD_input.Digestate_treatment['er_wwtpLF']['amount']
        self.LCI.loc ['Unit','Empty_Heavy-duty truck transportation for sludge to landfill'] = 'vkm'
        
        self.LCI['Empty_Total heavy duty truck empty return']= self.LCI['Empty_Heavy-duty truck transportation for sludge to landfill'][2:] + self.LCI['Empty_Heavy-duty truck transportation for leachate to POTW']
        self.LCI.loc ['Unit','Empty_Total heavy duty truck empty return'] = 'vkm'
        
        self.LCI['Empty_Medium-duty truck transport return from land application']= ((self.SD['Total mass to be land applied (inlcudes added water)'][2:]/1000)/self.AD_input.Land_app['land_payload']['amount'])*\
                                                                                self.AD_input.Land_app['distLand']['amount']*self.AD_input.Land_app['erLand']['amount']
        self.LCI.loc ['Unit','Empty_Medium-duty truck transport return from land application'] = 'vkm'

### Electricity
        self.LCI['Electricity Use']= self.SD['Total AD Facility Electricity Use'][2:] + self.SD['Total net electricity use'][2:]
        self.LCI.loc ['Unit','Electricity Use'] = 'kWh/Mg'
        
        self.LCI['Electricity Production']= self.SD['Gross electricity generation']

### Residual Mass
        self.LCI['Residual']= self.SD['Total mass sent to the landfill'][2:]/1000
        self.LCI.loc ['Unit','Residual'] = 'Mg/Mg'
   
    
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
            for y in self.Index[2:]:
                x[y]={}
                                                       
               
        for y in self.Index[2:]:
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
            
            Technosphere[y][('Technosphere', 'Nitrogen_Fertilizer')] = -self.LCI['Nitrogen Mineral Fertilizer Equivalent mass to offset'][y]
            
            Technosphere[y][('Technosphere', 'Phosphorous_Fertilizer')] = -self.LCI['Phosphorous Mineral Fertilizer Equivalent mass to offset'][y]
            
            Technosphere[y][('Technosphere', 'Potassium_Fertilizer')] = -self.LCI['Potassium Mineral Fertilizer Equivalent mass to offset'][y]
            
            Technosphere[y][('Technosphere', 'Peat')] = -self.LCI['Peat Equivalent mass to offset'][y]
            
### Output Biosphere Database
            Biosphere[y][('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014')]= self.LCI['Ammonia'][y] #Ammonia ('air',)
            
            Biosphere[y][('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6')]= -self.LCI['Direct Carbon Storage and Humus Formation'][y]# Carbon dioxide, from soil or biomass stock ('air',)
            
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

        return(self.AD)    


A=AD()
A.calc2()
BBB = A.LCI
CC = A.report() 


