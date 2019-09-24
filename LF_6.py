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

class LF:
    def __init__(self):
        self.CommonData = CommonData()
        self.Input= LF_input()
### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.gas_emission_factor=pd.read_excel("LF_Gas_emission_factors.xlsx",index_col = 'Biosphere_key')
        self.gas_emission_factor.fillna('',inplace=True)
        self.lcht_coef = pd.read_excel('LF_Leachate_Coeff.xlsx')
        self.lcht_coef.fillna(0,inplace=True)
        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
                      'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
                      'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
                      'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
                      'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
                      'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
                      'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
                      'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
                      'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        #self.Assumed_Comp = pd.Series(self.AD_Input.Assumed_Comp,index=self.Index)
        #self.SD=pd.read_excel('LF_stat.xlsx', index_col = 'Index')

        self.n = self.Input.LF_gas['optime']['amount']+1
        self.timescale = 101
        
        self.param1=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)])  # Parameters for LF operation (timing for LFG collection)
        self.param2=pd.DataFrame(index = self.Index) # LFG generation parameter
        self.param3=pd.DataFrame(index = np.arange(1,101))
        self.LFG = pd.DataFrame(index = self.Index)
        
        self.Methane_gen=pd.DataFrame(index = self.Index) # Methane generation
        self.Methane_Col=pd.DataFrame(index = self.Index) # Methane collected
        self.Methane_Comb=pd.DataFrame(index = self.Index) # Methane combustion for Energy
        self.Methane_Flare=pd.DataFrame(index = self.Index) # Methane Sent to Flare
        self.Methane_Ox=pd.DataFrame(index = self.Index) # Methane Oxidized
        self.Methane_Emitted=pd.DataFrame(index = self.Index) # Methane Emitted
        
    
    def Cal_LFG_Col_Ox(self):

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

    def Cal_LFG(self):

### LFG generation parameter
        self.param2['k'] = (self.Material_Properties['Lab Decay Rate'][4:]/156) * (self.Input.LF_gas['actk']['amount']/0.04)

        
        self.param2['L0'] = self.Material_Properties['Methane Yield'][4:]

        
        self.param2['solid Content'] = 1 - self.Material_Properties['Moisture Content'][4:]/100


### Methane generation                
        self.Methan_gen_by_year = (self.param2['L0']*self.param2['solid Content']* \
                                   (np.e**(-self.param2['k']*np.array(np.arange(0,self.timescale)))-
                                    np.e**(-self.param2['k']*np.array(np.arange(1,self.timescale+1))))
                                                    )        
        self.LFG['Total generated Methane']= self.Methan_gen_by_year.apply(lambda x: x.sum())                                                       
        
        self.LFG['Fraction of L0 Generated']=  self.LFG['Total generated Methane'].values/(self.param2['L0'].apply(lambda x: 1 if x <=0 else x) * self.param2['solid Content'].values)
        
### Methane collected            
        self.LFG['Total Methane collected']= self.Methan_gen_by_year.apply(lambda x: (x*self.LFG_Coll_Eff['average collection'].values/100).sum())  
        
        self.LFG['Collection Eff']= self.LFG['Total Methane collected'].values/self.LFG['Total generated Methane'].apply(lambda x: 1 if x <=0 else x) 

### Blower electricity use
        self.LFG['Blower electricity use']=( self.LFG['Total Methane collected']/self.Input.LF_gas['blwrPRRm3']['amount']) * (self.Input.LF_gas['blwrPerLoad']['amount'] /100) * (100/self.Input.LF_gas['blwrEff']['amount']) * 24 * 356.25

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
      
### Methane Sent to Flare  (Includes downtime but not methane destruction efficiency)        
        self.LFG['Total Methane flared']= self.LFG['Total Methane collected']-self.LFG['Total Methane combusted']

### Methane Oxidized
        self.LFG['Total Methane oxidized'] = self.Methan_gen_by_year.apply(lambda x: (x*(1-self.LFG_Coll_Eff['average collection'].values/100) * self.LFG_Ox_Eff['average oxidation'].values/100).sum()) 

### Methane Emitted        
        self.LFG['Total Methane Emitted']=  self.LFG['Total generated Methane'] - self.LFG['Total Methane combusted'] * self.Input.LF_gas['EngineCombEff']['amount']/100 \
                                                        - self.LFG['Total Methane flared'] *self.Input.LF_gas['FlareCombEff']['amount']/100 - self.LFG['Total Methane oxidized']

        self.LFG['Percent of Generated Methane Emitted']= self.LFG['Total Methane Emitted'].values/self.LFG['Total generated Methane'].apply(lambda x: 1 if x <=0 else x)  * 100


# =============================================================================
### LEACHATE
# =============================================================================

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
        self.param3['Concentrations of BOD5, Biological Oxygen Demand'] = self.param3['year'].apply(lambda x:
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'] * (-x) + self.Input.BOD['LF_BOD_con1']['amount']) if x <= self.Input.BOD['LF_BOD2']['amount'] else
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'] * (x-self.Input.BOD['LF_BOD2']['amount']) + self.Input.BOD['LF_BOD_con3']['amount']) if x <= self.Input.BOD['LF_BOD4']['amount'] else
                                                                                        (self.param3['Slope of BOD Concentration vs. Time (kg/L-yr)'] * (x-self.Input.BOD['LF_BOD4']['amount']) + self.Input.BOD['LF_BOD_con5']['amount']) if x <= self.Input.BOD['LF_BOD6']['amount'] else
                                                                                        0) 
        
        #self.param3['Concentrations of COD, Chemical Oxygen Demand'] = 
        

# =============================================================================
### Life-Cycle Costs
# =============================================================================

# minimum labor costs
        LF_c43 = self.Input.LF['Num_labor']['amount']*self.Input.LF['D_per_w']['amount']*self.Input.LF['Hr_per_d']['amount']\
                    *self.Input.LF['W_per_yr']['amount']*self.Input.LF['wage_hr']['amount']
#depth of liner and leachate control system
        LF_Dlls = (self.Input.LF['LF_Dspl']['amount']*self.Input.LF['LF_z4']['amount'])+\
                    (self.Input.LF['LF_Dssl']['amount']*self.Input.LF['LF_z4']['amount']*self.Input.LF['LF_z6']['amount'])+\
                    (self.Input.LF['LF_Dslc']['amount']*self.Input.LF['LF_z4']['amount'])+(self.Input.LF['LF_Dsl']['amount']*self.Input.LF['LF_z4']['amount'])       
#height of waste below grade
        LF_Hb = self.Input.LF['LF_De']['amount']-LF_Dlls

#self.Input.LF['']['amount']








# =============================================================================
### Operation
# =============================================================================

#LF_v_msw = =(self.Input.eco_param['Input_flow']['amount']*self.Input.eco_param['facLife']['amount']*self.Input.eco_param['annOpDays']['amount'] \
#             *1000*10000)/(LF_Wdv*LF_Ldv*self.Input.density['LF_d_msw']['amount'])





A= LF()
A.Cal_LFG_Col_Ox()
A.Cal_LFG() 
AAAA=A.LFG  

# =============================================================================
# from time import time
# B=time()
# A= LF()
# for i in range (100):
#     A.Cal_LFG_Col_Ox()
#     A.Cal_LFG()
# print(time()-B)
# =============================================================================
  
"""
Index(['abbreviation', 'Moisture Content', 'Volatile Solids', 'Ash Content',
       'Lower Heating Value', 'Methane Yield', 'Lab Decay Rate',
       'Bulk Density', 'Carbon Storage Factor', 'Biogenic Carbon Content',
       'Ultimate Biogenic C Converted to Biogas', 'Fossil Carbon Content',
       'Hydrogen Content', 'Oxygen Content', 'Nitrogen Content',
       'Phosphorus Content', 'Potassium Content', 'Iron', 'Copper', 'Cadmium',
       'Arsenic', 'Mercury', 'Selenium', 'Chromium', 'Lead', 'Zinc', 'Barium',
       'Antimony', 'Nickel', 'Silver', 'Chlorine', 'Sulphur', 'Aluminum',
       'Methane Yield.1'],
      dtype='object')
"""