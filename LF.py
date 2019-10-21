# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:07:56 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
from LF_input_1 import *
from CommonData import *
from stats_arrays import *
import ast

class LF:
    def __init__(self):
        self.CommonData = CommonData()
        self.Input= LF_input()
### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.gas_emission_factor=pd.read_csv("LF_Gas_emission_factors.csv",converters={'Biosphere_key': ast.literal_eval})
        self.gas_emission_factor.fillna('',inplace=True)
        self.lcht_coef = pd.read_csv('LF_Leachate_Coeff.csv',converters={'Surface_water': ast.literal_eval,'Ground_water': ast.literal_eval})
        self.lcht_coef.fillna(0,inplace=True)
        self.lcht_Alloc = pd.read_csv('LF_Leachate_Allocation.csv')
        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
                      'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
                      'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
                      'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
                      'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
                      'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
                      'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
                      'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
                      'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        
        self.timescale = 101
    def add_LCI(self,Name,Flow,LCI):
        if Name in LCI.columns:
            LCI[Name] += Flow
        else:
            LCI[Name] = Flow


# =============================================================================
#        
### Landfill Gas Collection Efficiency
#
# =============================================================================
    def Cal_LFG_Col_Ox(self):
        self.n = self.Input.LF_gas['optime']['amount']+1
        self.param1=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)])  # Parameters for LF operation (timing for LFG collection)

### Parameters for LF operation (timing for LFG collection)
        self.param1['Time to initial collection'] = [max(self.Input.LF_gas['initColTime']['amount']-np.mod(i,self.Input.LF_gas['cellFillTime']['amount']),0) \
                                                             for i in np.arange(0,self.n)]
        self.param1['Time to interim cover'] = [self.Input.LF_gas['cellFillTime']['amount'] - np.mod(i,self.Input.LF_gas['cellFillTime']['amount']) \
                                                     for i in np.arange(0,self.n)]
        self.param1['Time to long term cover'] = [self.Input.LF_gas['incColTime']['amount'] - np.mod(i,self.Input.LF_gas['cellFillTime']['amount']) \
                                             for i in np.arange(0,self.n)]
        
        
### How long is energy on
        self.enrgOff = self.Input.LF_gas['enrgOff1']['amount'] if self.Input.LF_gas['enrgRecovered']['amount']==1 else 0

### Collection efficiency
        self.LFG_Coll_Eff=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)]) # Collection efficiency             
        for j in np.arange(0,self.timescale):
            self.LFG_Coll_Eff['Collection ' + str(j) + ' Years Since Waste Burial'] = [
                                                                      None if i>self.Input.LF_gas['optime']['amount'] else
                                                                      0 if(i+j)>=(max(self.enrgOff,self.Input.LF_gas['flareOff']['amount'])) else
                                                                      self.Input.LF_gas['finColEff']['amount'] if (i+j)>=(self.Input.LF_gas['timeToFinCover']['amount']+self.Input.LF_gas['optime']['amount']) else
                                                                      self.Input.LF_gas['incColEff']['amount'] if j>=self.param1['Time to long term cover']['Waste buried in Year '+str(i)] else
                                                                      self.Input.LF_gas['intColEff']['amount'] if j>=self.param1['Time to interim cover']['Waste buried in Year '+str(i)] else
                                                                      self.Input.LF_gas['initColEff']['amount'] if j>=self.param1['Time to initial collection']['Waste buried in Year '+str(i)] else
                                                                      0 for i in np.arange(0,self.n)
                                                                      ]
            
### Oxidation
        self.LFG_Ox_Eff=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)]) # Oxidation
        for j in np.arange(0,self.timescale):
            self.LFG_Ox_Eff['Oxidation ' + str(j) + ' Years Since Waste Burial'] = [
                                                                      None if i>self.Input.LF_gas['optime']['amount'] else
                                                                      self.Input.Ox['ox_fincov']['amount'] if(i+j)>=(max(self.enrgOff,self.Input.LF_gas['flareOff']['amount'])) else
                                                                      self.Input.Ox['ox_nocol']['amount'] if self.LFG_Coll_Eff['Collection ' + str(j) + ' Years Since Waste Burial']['Waste buried in Year '+str(i)] <self.Input.LF_gas['incColEff']['amount'] else
                                                                      self.Input.Ox['ox_col']['amount']  for i in np.arange(0,self.n)]
                                                                         
            
### calculating average collection and oxdiation            
        self.LFG_Coll_Eff = self.LFG_Coll_Eff.transpose()
        self.LFG_Ox_Eff = self.LFG_Ox_Eff.transpose()
        self.LFG_Coll_Eff['average collection']= self.LFG_Coll_Eff[self.LFG_Coll_Eff.columns[:101]].sum(axis=1)/(self.n) 
        self.LFG_Ox_Eff['average oxidation']= self.LFG_Ox_Eff[self.LFG_Ox_Eff.columns[:101]].sum(axis=1)/(self.n) 

# =============================================================================
#        
### Landfill Gas
#
# =============================================================================

    def Cal_LFG(self):
        self.LCI = pd.DataFrame(index = self.Index) # LCI
        self.param2=pd.DataFrame(index = self.Index) # LFG generation parameter
        self.LFG = pd.DataFrame(index = self.Index)

### LFG generation parameter
        self.param2['k'] = (self.Material_Properties['Lab Decay Rate'][4:]/156) * (self.Input.LF_gas['actk']['amount']/0.04)

        
        self.param2['L0'] = self.Material_Properties['Methane Yield'][4:]

        
        self.param2['solid Content'] = 1 - self.Material_Properties['Moisture Content'][4:]/100


### Methane generation                
        self.Methan_gen_by_year = self.param2['L0']*self.param2['solid Content']* \
                                   (np.e**(-self.param2['k'].apply(lambda x: x * np.arange(0,self.timescale)))-
                                    np.e**(-self.param2['k'].apply(lambda x: x * np.arange(1,self.timescale+1)))
                                                    )        
        self.LFG['Total generated Methane']= self.Methan_gen_by_year.apply(lambda x: x.sum())                                                       
        
        self.LFG['Fraction of L0 Generated']=  self.LFG['Total generated Methane'].values/(self.param2['L0'].apply(lambda x: 1 if x <=0 else x) * self.param2['solid Content'].values)
        
### Methane collected            
        self.LFG['Total Methane collected']= self.Methan_gen_by_year.apply(lambda x: (x*self.LFG_Coll_Eff['average collection'].values/100).sum())  
        
        self.LFG['Collection Eff']= self.LFG['Total Methane collected'].values/self.LFG['Total generated Methane'].apply(lambda x: 1 if x <=0 else x) 

### Blower electricity use
        self.LFG['Blower electricity use']=( self.LFG['Total Methane collected']/self.Input.LF_gas['blwrPRRm3']['amount']) * (self.Input.LF_gas['blwrPerLoad']['amount'] /100) * (100/self.Input.LF_gas['blwrEff']['amount']) * 24 * 356.25
        #Adding Blower electricity use to LCI
        self.add_LCI('Electricity_consumption',self.LFG['Blower electricity use'],self.LCI)
### Methane combustion for Energy         
        def comb_frac(j):
            return(0 if not self.Input.LF_gas['enrgRecovered']['amount']==1 else \
                   0 if j <= self.Input.LF_gas['enrgOn']['amount'] else \
                   (100-self.Input.LF_gas['EnrgRecDownTime']['amount'])/100  if j <= self.Input.LF_gas['enrgOff1']['amount'] else 0)
        
        Time = pd.Series(np.arange(0,self.timescale))
        self.LFG['Total Methane combusted']=  self.Methan_gen_by_year.apply(lambda x: (x*self.LFG_Coll_Eff['average collection'].values/100 * Time.apply(comb_frac)).sum())
           
        self.LFG['Percent of Generated used for Energy']= self.LFG['Total Methane combusted'].values/self.LFG['Total generated Methane'].apply(lambda x: 1 if x <=0 else x)  * 100
     
        self.LFG['Percent of Collected used for Energy']= self.LFG['Total Methane combusted'].values/self.LFG['Total Methane collected'].apply(lambda x: 1 if x <=0 else x)  * 100

### Electricity generated
        self.LFG['Electricity generated'] = self.LFG['Total Methane combusted'] * self.Input.LFG_Comb['convEff']['amount']*self.CommonData.LHV['CH4']['amount'] /3.6
        #Adding the generated electricity to LCI
        self.add_LCI('Electricity_production' ,self.LFG['Electricity generated'],self.LCI)
      
### Methane Sent to Flare  (Includes downtime but not methane destruction efficiency)        
        self.LFG['Total Methane flared']= self.LFG['Total Methane collected']-self.LFG['Total Methane combusted']

### Methane Oxidized
        self.LFG['Total Methane oxidized'] = self.Methan_gen_by_year.apply(lambda x: (x*(1-self.LFG_Coll_Eff['average collection'].values/100) * self.LFG_Ox_Eff['average oxidation'].values/100).sum()) 

### Methane Emitted        
        self.LFG['Total Methane Emitted']=  self.LFG['Total generated Methane'] - self.LFG['Total Methane combusted'] * self.Input.LF_gas['EngineCombEff']['amount']/100 \
                                                        - self.LFG['Total Methane flared'] *self.Input.LF_gas['FlareCombEff']['amount']/100 - self.LFG['Total Methane oxidized']

        self.LFG['Percent of Generated Methane Emitted']= self.LFG['Total Methane Emitted'].values/self.LFG['Total generated Methane'].apply(lambda x: 1 if x <=0 else x)  * 100

### Mass of methane in uncollected biogas used to calculated the emissions         
        self.LFG['Total methane in uncollected biogas'] = self.LFG['Total generated Methane'] - self.LFG['Total Methane collected']

### Emission factor: Emission to the air from venting, flaring and combustion of biogas        
        Biogas_factor = self.gas_emission_factor['Concentration_ppmv']/(self.Input.LF_gas['ch4prop']['amount']*10**6)
        Vent_factor = Biogas_factor*(1-self.gas_emission_factor['Destruction_Eff_Vent']/100)*(1/self.CommonData.STP['mole_to_L']['amount'])*self.gas_emission_factor['MW']
        Flare_factor = Biogas_factor*(1-self.gas_emission_factor['Destruction_Eff_Flare']/100)*(1/self.CommonData.STP['mole_to_L']['amount'])*self.gas_emission_factor['MW']
        Comb_factor = Biogas_factor*(1-self.gas_emission_factor['Destruction_Eff_User_Defined']/100)*(1/self.CommonData.STP['mole_to_L']['amount'])*self.gas_emission_factor['MW']
        self.emission_to_air =self.LFG['Total methane in uncollected biogas'].apply(lambda x: x*Vent_factor) + self.LFG['Total Methane flared'].apply(lambda x: x*Flare_factor)+self.LFG['Total Methane combusted'].apply(lambda x: x*Comb_factor)
        self.emission_to_air.columns=self.gas_emission_factor['Exchange'] +' to '+ self.gas_emission_factor['Subcompartment']
        key1 = zip(self.emission_to_air.columns,self.gas_emission_factor['Biosphere_key'])
        self.key1=dict(key1) 

### Direct CO2 and Methane emissions, Calculated in the model        
        self.LFG['Mass of emitted methane']=self.LFG['Total Methane Emitted']*self.CommonData.STP['m3CH4_to_kg']['amount']
        
        self.LFG['Mass of CO2 generated with methane']=self.LFG['Total generated Methane']*(1/self.Input.LF_gas['ch4prop']['amount'])*(1-self.Input.LF_gas['ch4prop']['amount'])*self.CommonData.STP['m3CO2_to_kg']['amount']
        
        self.LFG['Mass of CO2 generated with methane combustion'] =  (self.LFG['Total Methane combusted']*self.Input.LF_gas['EngineCombEff']['amount']/100 + self.LFG['Total Methane flared']*self.Input.LF_gas['FlareCombEff']['amount']/100) \
                                                                        *1000*(1/self.CommonData.STP['mole_to_L']['amount'])*self.CommonData.MW['CO2']['amount']/1000
        
        self.LFG['Mass of CO2 generated with methane oxidation'] = self.LFG['Total Methane oxidized']*1000*(1/self.CommonData.STP['mole_to_L']['amount'])*self.CommonData.MW['CO2']['amount']/1000
        
        self.LFG['Mass of CO2 storage'] = -(1-self.Material_Properties['Moisture Content'][4:]/100)*self.Material_Properties['Carbon Storage Factor'][4:]*self.CommonData.MW['CO2']['amount']/self.CommonData.MW['C']['amount']
        
### Adding the CO2 emissions to 'emission_to_air' dict        
        if 'Carbon dioxide, non-fossil to unspecified' in self.emission_to_air.columns:
            self.emission_to_air['Carbon dioxide, non-fossil to unspecified'] += self.LFG['Mass of CO2 generated with methane']+self.LFG['Mass of CO2 generated with methane combustion']+self.LFG['Mass of CO2 generated with methane oxidation']
        else:
            self.emission_to_air['Carbon dioxide, non-fossil to unspecified'] = self.LFG['Mass of CO2 generated with methane']+self.LFG['Mass of CO2 generated with methane combustion']+self.LFG['Mass of CO2 generated with methane oxidation']
            self.key1['Carbon dioxide, non-fossil to unspecified']=('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')

### Adding the CO2 storage to 'emission_to_air' dict  
        if 'Carbon dioxide, from soil or biomass stock to unspecified' in self.emission_to_air.columns:
            self.emission_to_air['Carbon dioxide, from soil or biomass stock to unspecified'] += self.LFG['Mass of CO2 storage'] 
        else:
            self.emission_to_air['Carbon dioxide, from soil or biomass stock to unspecified'] = self.LFG['Mass of CO2 storage'] 
            self.key1['Carbon dioxide, from soil or biomass stock to unspecified']=('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6')   
            
### Adding the Methane emissions to 'emission_to_air' dict  
        if 'Methane, non-fossil to unspecified' in self.emission_to_air.columns:
            self.emission_to_air['Methane, non-fossil to unspecified'] += self.LFG['Mass of emitted methane']
        else:
            self.emission_to_air['Methane, non-fossil to unspecified'] = self.LFG['Mass of emitted methane'] 
            self.key1['Methane, non-fossil to unspecified']=('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8')          

            
# =============================================================================
#        
### LEACHATE
#
# =============================================================================
    def Leachate(self):
        self.param3=pd.DataFrame(index = np.arange(1,101)) # Leachate
        self.lcht_conc=pd.DataFrame(index = np.arange(1,101)) # Concentration of emissions in leachate
        self.sludge = pd.DataFrame(index = self.Index) # Generated sludge from Leachate treatment
### LEACHATE GENERATION, QUANTITY AND CONSTITUENTS
        self.param3['year'] = np.arange(1,101)
        self.param3['Annual Precipitation (mm)'] = 900
        self.param3['Percent of Precipitation that Becomes Leachate (%)'] = [20, 13.3, 6.6, 6.6, 6.6, 6.5, 6.5, 6.5, 6.5, 6.5]+[0.04 for i in range(90)]
        self.param3['fraction of Leachate that is Recirculated'] = 0
        self.param3['farction of Collected Leachate that is Sent to WWTP'] = 1
        self.param3['Leachate Collection Efficiency (%)']= self.param3['year'].apply(lambda x: self.Input.Leachate['LF_lcht_p']['amount'] if x<=self.Input.Leachate['LF_time3']['amount'] \
                                                           and x>=self.Input.Leachate['LF_time1']['amount'] else 0)
        
        LF_msw_acre = 115802 # Mg/ha 
### Mass balance of Leachate
        self.param3['Generated Leachate (m3/Mg MSW)'] = (self.param3['Annual Precipitation (mm)'].values/1000)*(self.param3['Percent of Precipitation that Becomes Leachate (%)'].values/100)*(10000/LF_msw_acre)
        self.param3['Collected Leachate (m3/Mg MSW)'] = self.param3['Generated Leachate (m3/Mg MSW)'].values * self.param3['Leachate Collection Efficiency (%)'].values
        self.param3['Recirculated Leachate (m3/Mg MSW)'] = self.param3['Generated Leachate (m3/Mg MSW)'].values * self.param3['fraction of Leachate that is Recirculated'].values
        self.param3['Treated Leachate (m3/Mg MSW)'] = self.param3['Collected Leachate (m3/Mg MSW)'].values * self.param3['farction of Collected Leachate that is Sent to WWTP'].values
        self.param3['Fugitive Leachate  (m3/Mg MSW)'] = self.param3['Generated Leachate (m3/Mg MSW)'].values - self.param3['Treated Leachate (m3/Mg MSW)'].values -self.param3['Recirculated Leachate (m3/Mg MSW)'].values

### COD and BOD slope
        self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'] = self.param3['year'].apply(lambda x:
                                                                                        (self.Input.BOD['LF_BOD_con2']['amount']-self.Input.BOD['LF_BOD_con1']['amount'])/self.Input.BOD['LF_BOD2']['amount'] if x <= self.Input.BOD['LF_BOD2']['amount'] else
                                                                                        (self.Input.BOD['LF_BOD_con4']['amount']-self.Input.BOD['LF_BOD_con3']['amount'])/(self.Input.BOD['LF_BOD4']['amount']-self.Input.BOD['LF_BOD2']['amount']) if x <= self.Input.BOD['LF_BOD4']['amount'] else
                                                                                        (self.Input.BOD['LF_BOD_con6']['amount']-self.Input.BOD['LF_BOD_con5']['amount'])/(self.Input.BOD['LF_BOD6']['amount']-self.Input.BOD['LF_BOD4']['amount']) if x <= self.Input.BOD['LF_BOD6']['amount'] else
                                                                                        0)
        self.param3['Slope of COD Concentration vs. Time (kg/L-yr)'] = self.param3['year'].apply(lambda x:
                                                                                        (self.Input.COD['LF_COD_con2']['amount']-self.Input.COD['LF_COD_con1']['amount'])/self.Input.COD['LF_COD2']['amount'] if x <= self.Input.COD['LF_COD2']['amount'] else
                                                                                        (self.Input.COD['LF_COD_con4']['amount']-self.Input.COD['LF_COD_con3']['amount'])/(self.Input.COD['LF_COD4']['amount']-self.Input.COD['LF_COD2']['amount']) if x <= self.Input.COD['LF_COD4']['amount'] else
                                                                                        (self.Input.COD['LF_COD_con6']['amount']-self.Input.COD['LF_COD_con5']['amount'])/(self.Input.COD['LF_COD6']['amount']-self.Input.COD['LF_COD4']['amount']) if x <= self.Input.COD['LF_COD6']['amount'] else
                                                                                        0)

### Concentration of other effluents in leachate  (kg/L) 
# Only COD and BOD concentrations are calculated, for the other ones, data is in the ('LF_Leachate_Coeff.xlsx')                                                                                         
        for i in self.lcht_coef.index:
            self.lcht_conc[self.lcht_coef['Emission'][i]] = self.lcht_coef['Concentrations (kg/L)'][i]

### Concentration of BOD and COD in leachate 
        self.lcht_conc['BOD5, Biological Oxygen Demand'] = self.param3['year'].apply(lambda x:
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'][x] * (-x) + self.Input.BOD['LF_BOD_con1']['amount']) if x <= self.Input.BOD['LF_BOD2']['amount'] else
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'][x] * (x-self.Input.BOD['LF_BOD2']['amount']) + self.Input.BOD['LF_BOD_con3']['amount']) if x <= self.Input.BOD['LF_BOD4']['amount'] else
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'][x] * (x-self.Input.BOD['LF_BOD4']['amount']) + self.Input.BOD['LF_BOD_con5']['amount']) if x <= self.Input.BOD['LF_BOD6']['amount'] else
                                                                                        0) 
        
        self.lcht_conc['COD, Chemical Oxygen Demand'] = self.param3['year'].apply(lambda x:
                                                                                        (self.param3['Slope of COD Concentration vs. Time (kg/L-yr)'][x] * (-x) + self.Input.COD['LF_COD_con1']['amount']) if x <= self.Input.COD['LF_COD2']['amount'] else
                                                                                        (self.param3['Slope of COD Concentration vs. Time (kg/L-yr)'][x] * (x-self.Input.COD['LF_COD2']['amount']) + self.Input.COD['LF_COD_con3']['amount']) if x <= self.Input.COD['LF_COD4']['amount'] else
                                                                                        (self.param3['Slope of COD Concentration vs. Time (kg/L-yr)'][x] * (x-self.Input.COD['LF_COD4']['amount']) + self.Input.COD['LF_COD_con5']['amount']) if x <= self.Input.COD['LF_COD6']['amount'] else
                                                                                        self.Input.COD['LF_COD_con7']['amount'])

### Fugitive Leachate Emissions (leaks through liner) (kg/Mg MSW)
        self.Fugitive_Leachate = self.lcht_conc.multiply(self.param3['Fugitive Leachate  (m3/Mg MSW)'],axis=0).sum()*1000

### Post-treatment effluent emissions (kg/Mg MSW)       
        self.Effluent = self.lcht_conc.multiply(self.param3['Treated Leachate (m3/Mg MSW)'],axis=0).multiply(1-self.lcht_coef['Removal Efficiency (%)'].values/100,axis=1).sum()*1000
        
        self.Surface_water_emission = self.lcht_Alloc[self.lcht_Alloc.columns[1:]].multiply(self.Effluent,axis=1)
        self.Surface_water_emission.index = self.Index
        key2=zip(self.Surface_water_emission.columns ,self.lcht_coef['Surface_water'])
        self.key2 = dict(key2)
        self.Ground_water_emission = self.lcht_Alloc[self.lcht_Alloc.columns[1:]].multiply(self.Fugitive_Leachate,axis=1)
        self.Ground_water_emission.index = self.Index
        key3=zip(self.Surface_water_emission.columns ,self.lcht_coef['Ground_water'])
        self.key3 = dict(key3)


### Electricity Consumption for Leachate Treatment
        BOD_removed = (sum(self.lcht_conc['BOD5, Biological Oxygen Demand'].values*self.param3['Treated Leachate (m3/Mg MSW)'].values)*1000-self.Effluent['BOD5, Biological Oxygen Demand'])
        BOD_elec = BOD_removed * self.Input.BOD['LF_lcht_ec']['amount']
        Pump_elec_per_litr = self.Input.lcht_pump['leachAirPerLeach']['amount'] *(1/self.Input.lcht_pump['leachCompPowReq']['amount'] )*(1/28.32)*(1/(60*24*365.25))*(self.Input.lcht_pump['leachCompLoad']['amount'] /100)*(100/self.Input.lcht_pump['leachEff']['amount'])*8766/1.341    
        Pump_elec = sum(self.param3['Collected Leachate (m3/Mg MSW)'].values * 1000 * Pump_elec_per_litr)
        self.Leachate_elec = self.lcht_Alloc['BOD5, Biological Oxygen Demand']*BOD_elec + Pump_elec
        #Adding Blower electricity use to LCI
        self.add_LCI('Electricity_consumption',self.Leachate_elec.values,self.LCI)

### List of metals in Leachate
        self.metals = ['Arsenic, ion','Barium','Cadmium, ion','Chromium, ion','Lead','Mercury','Selenium','Silver, ion']
        
### Calculating Slude generation and transport
        LF_sldg_BOD = self.Input.BOD['LF_sldg_per_BOD']['amount'] * BOD_removed 
        LF_sldg_PO4 = self.Effluent['Phosphate']*(self.Input.Leachate['LF_eff_PO4']['amount']/100)/((100-self.Input.Leachate['LF_eff_PO4']['amount'])/100)
        LF_sldg_mtls = sum(self.Effluent[self.metals])*(self.Input.Leachate['LF_eff_mtls']['amount']/100)/((100-self.Input.Leachate['LF_eff_mtls']['amount'])/100)
        LF_sldg_tss = self.Effluent['Suspended solids, unspecified']*(self.Input.Leachate['LF_eff_TSS']['amount']/100)/((100-self.Input.Leachate['LF_eff_TSS']['amount'])/100)
        
        self.sludge['sludge generated from BOD removal'] = self.lcht_Alloc['BOD5, Biological Oxygen Demand'].values * LF_sldg_BOD
        
        self.sludge['sludge generated from phosphate removal'] = self.lcht_Alloc['Phosphate'].values * LF_sldg_PO4
        
        self.sludge['sludge generated from metals removal'] = self.lcht_Alloc[self.metals].multiply((self.Effluent[self.metals])*(self.Input.Leachate['LF_eff_mtls']['amount']/100)/((100-self.Input.Leachate['LF_eff_mtls']['amount'])/100),axis=1).sum(axis=1).values
        
        self.sludge['sludge generated from suspended solids removal'] = self.lcht_Alloc['Suspended solids, unspecified'].values * LF_sldg_tss
        
        self.sludge['total sludge generated'] = self.sludge['sludge generated from BOD removal']+self.sludge['sludge generated from phosphate removal']+\
                                                self.sludge['sludge generated from metals removal']+self.sludge['sludge generated from suspended solids removal']
                                                
        self.sludge['Medium-Heavy Duty Transportation'] = self.sludge['total sludge generated']/1000 * self.Input.Leachate['dis_POTW']['amount']                            
        self.add_LCI('Internal_Process_Transportation_Medium_Duty_Diesel_Truck',self.sludge['Medium-Heavy Duty Transportation']*1000,self.LCI)
            
# =============================================================================
#
### Life-Cycle Costs
#
# =============================================================================
# =============================================================================
#     def cost(self):
# # minimum labor costs
#         LF_c43 = self.Input.LF['Num_labor']['amount']*self.Input.LF['D_per_w']['amount']*self.Input.LF['Hr_per_d']['amount']\
#                     *self.Input.LF['W_per_yr']['amount']*self.Input.LF['wage_hr']['amount']
# #depth of liner and leachate control system
#         LF_Dlls = (self.Input.LF['LF_Dspl']['amount']*self.Input.LF['LF_z4']['amount'])+\
#                     (self.Input.LF['LF_Dssl']['amount']*self.Input.LF['LF_z4']['amount']*self.Input.LF['LF_z6']['amount'])+\
#                     (self.Input.LF['LF_Dslc']['amount']*self.Input.LF['LF_z4']['amount'])+(self.Input.LF['LF_Dsl']['amount']*self.Input.LF['LF_z4']['amount'])       
# #height of waste below grade
#         LF_Hb = self.Input.LF['LF_De']['amount']-LF_Dlls
# 
# ### MAIN LINER CONSTRUCTION
# #soil available from excavation
#         LF_Vsl = self.Input.LF['LF_f10']['amount']*(1-self.Input.LF['LF_f2']['amount'])*self.Input.LF['']['amount']
# 
# =============================================================================


# =============================================================================
#
### Life-Cycle Inventory
#
# =============================================================================
    def Material_energy_use(self):
### Electricity Use        
        #Building electricity use
        bld_elec = 0.596  #kWh/Mg
        self.add_LCI('Electricity_consumption',bld_elec,self.LCI)
### Fuel
        #Diesel	
        dies_pc=2.342866	#L/Mg
        self.add_LCI('Equipment_Diesel',dies_pc,self.LCI)
        #Gasoline
        gaso_pc=0.000616	#L/Mg
        self.add_LCI('Equipment_Gasoline',gaso_pc,self.LCI)
### Transportation
        #Heavy duty truck transportation required
        HD_trans = 0.1409593	#Mg-km/Mg
        self.add_LCI('Internal_Process_Transportation_Heavy_Duty_Diesel_Truck',HD_trans*1000,self.LCI)
        #Medium duty transportation required
        MD_trans = 	2.1137375	#Mg-km/Mg
        self.add_LCI('Internal_Process_Transportation_Medium_Duty_Diesel_Truck',MD_trans*1000,self.LCI)
#Heavy duty truck transportation required
        HD_trans_empty  = 4.02741E-03	#Mg-km/Mg
        self.add_LCI('Empty_Return_Heavy_Duty_Diesel_Truck',HD_trans_empty*1000,self.LCI)
        #Medium duty transportation required
        MD_trans_empty = 8.80724E-02	#Mg-km/Mg
        self.add_LCI('Empty_Return_Medium_Duty_Diesel_Truck',MD_trans_empty*1000,self.LCI)
### Material Use
        #HDPE liner	
        op_HDPE_Liner = 4.69579E-03  #kg/Mg
        self.add_LCI('HDPE_Liner',op_HDPE_Liner,self.LCI)
        #HDPE cover	
        cl_HDPE_Liner=1.15879E-01 #kg/Mg
        self.add_LCI('HDPE_Liner',cl_HDPE_Liner,self.LCI)
        #Geotextile
        cl_GeoTxt=1.14786E-02 #kg/Mg
        self.add_LCI('Geotextile',cl_GeoTxt,self.LCI)
        #HDPE pipe	
        cl_HDPE_Pipe=1.3349E-03 #m/Mg
        self.add_LCI('HDPE_Pipe',cl_HDPE_Pipe,self.LCI)
        #PVC pipe	
        cl_PVC_Pipe=2.5680E-04	#m/Mg
        self.add_LCI('PVC_Pipe',cl_PVC_Pipe,self.LCI)
        #HDPE cover	
        pc_HDPE_Liner=3.8626E-04 #kg/Mg
        self.add_LCI('HDPE_Liner',pc_HDPE_Liner,self.LCI)
        #Geotextile	
        pc_GeoTxt=3.8262E-05 #kg/Mg
        self.add_LCI('Geotextile',pc_GeoTxt,self.LCI)


        self.key4 = {'Electricity_production':('Technosphere', 'Electricity_production'),     
                    'Electricity_consumption':('Technosphere', 'Electricity_consumption'),
                    'Equipment_Diesel':('Technosphere', 'Equipment_Diesel'),
                    'Equipment_Gasoline':('Technosphere', 'Equipment_Gasoline'),
                    'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck':('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck'),
                    'Internal_Process_Transportation_Medium_Duty_Diesel_Truck':('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck'),
                    'Empty_Return_Heavy_Duty_Diesel_Truck':('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck'),
                    'Empty_Return_Medium_Duty_Diesel_Truck':('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck'),
                    'HDPE_Liner':('Technosphere', 'HDPE_Liner'),
                    'Geotextile':('Technosphere', 'Geotextile'),
                    'HDPE_Pipe':('Technosphere', 'HDPE_Pipe'),
                    'PVC_Pipe':('Technosphere', 'PVC_Pipe')}



# =============================================================================
#
### Report
#
# =============================================================================
    def report(self):
### Output
        self.LF = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.LF["process name"] = 'LF'
        self.LF["Waste"] = Waste
        self.LF["Technosphere"] = Technosphere
        self.LF["Biosphere"] = Biosphere
        
        for x in [Waste,Technosphere, Biosphere]:
            for y in self.Index:
                x[y]={}
         
### Output Biosphere Database        
        for y in self.Index:
            # Emission to air    
            for x in self.key1:
                if 'biosphere3' in str(self.key1[x]):
                    Biosphere[y][self.key1[x]]= self.emission_to_air[x][y] 
            # Emission to Surface Water 
            for x in self.key2:
                if 'biosphere3' in str(self.key2[x]):
                    Biosphere[y][self.key2[x]]= self.Surface_water_emission[x][y]
            # Emission to Ground Water
            for x in self.key3:
                if 'biosphere3' in str(self.key3[x]):
                    Biosphere[y][self.key3[x]]= self.Ground_water_emission[x][y]
            # Technosphere
            for x in self.key4:
                Technosphere[y][self.key4[x]]= self.LCI[x][y]
        return(self.LF)

### Calc function _ Do all the calculations 
    def calc(self):
        self.Cal_LFG_Col_Ox()
        self.Cal_LFG()
        self.Leachate()
        self.Material_energy_use()

### setup for Monte Carlo simulation   
    def setup_MC(self,seed=None):
        self.Input.setup_MC(seed)

### Calculate based on the generated numbers   
    def MC_calc(self):      
        input_list = self.Input.gen_MC()
        self.calc()
        return(input_list)


# =============================================================================
# from time import time
# B=time()
# A= LF()
# for i in range (100):
#     A.calc()
#     A.report()
# print(time()-B)
# =============================================================================
  
