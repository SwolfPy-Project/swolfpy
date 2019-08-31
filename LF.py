# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:07:56 2019

@author: msardar2
"""
import numpy as np
import pandas as pd
from LF_Input import *
from CommonData import *
from stats_arrays import *

class LF:
    def __init__(self):
        self.CommonData = CommonData()
        self.LF_input= LF_input()
### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.Index = ['Unit','Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
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
                ### Mass Flows
        self.n = self.LF_input.LF_gas['optime']['amount']+1
        self.timescale = 101
        self.Mass_flows=pd.DataFrame(index = self.Index)
    
    def Cal_LFG_Col_Ox(self):

### Parameters for LF operation (timing for LFG collection)
        self.param1=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)])
        self.param1['Time to initial collection'] = [max(self.LF_input.LF_gas['initColTime']['amount']-np.mod(i,self.LF_input.LF_gas['cellFillTime']['amount']),0) \
                                                             for i in np.arange(0,self.n)]
        self.param1['Time to interim cover'] = [self.LF_input.LF_gas['cellFillTime']['amount'] - np.mod(i,self.LF_input.LF_gas['cellFillTime']['amount']) \
                                                     for i in np.arange(0,self.n)]
        self.param1['Time to long term cover'] = [self.LF_input.LF_gas['incColTime']['amount'] - np.mod(i,self.LF_input.LF_gas['cellFillTime']['amount']) \
                                             for i in np.arange(0,self.n,1)]
        
        
### How long is energy on
        self.enrgOff = self.LF_input.LF_gas['enrgOff1']['amount'] if self.LF_input.LF_gas['enrgRecovered']['amount'] else 0

### Collection efficiency   
        self.LFG_Coll_Eff=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)])            
        for j in np.arange(0,self.timescale):
            self.LFG_Coll_Eff['Collection ' + str(j) + ' Years Since Waste Burial'] = [
                                                                      None if i>self.LF_input.LF_gas['optime']['amount'] else
                                                                      0 if(i+j)>=(max(self.enrgOff,self.LF_input.LF_gas['flareOff']['amount'])) else
                                                                      self.LF_input.LF_gas['finColEff']['amount'] if (i+j)>=(self.LF_input.LF_gas['timeToFinCover']['amount']+self.LF_input.LF_gas['optime']['amount']) else
                                                                      self.LF_input.LF_gas['incColEff']['amount'] if j>=self.param1['Time to long term cover']['Waste buried in Year '+str(i)] else
                                                                      self.LF_input.LF_gas['intColEff']['amount'] if j>=self.param1['Time to interim cover']['Waste buried in Year '+str(i)] else
                                                                      self.LF_input.LF_gas['initColEff']['amount'] if j>=self.param1['Time to initial collection']['Waste buried in Year '+str(i)] else
                                                                      0 for i in np.arange(0,self.n)
                                                                      ]
            
### Oxidation
        self.LFG_Ox_Eff=pd.DataFrame(index = ['Waste buried in Year '+str(i) for i in np.arange(0,self.n)])
        for j in np.arange(0,self.timescale):
            self.LFG_Ox_Eff['Oxidation ' + str(j) + ' Years Since Waste Burial'] = [
                                                                      None if i>self.LF_input.LF_gas['optime']['amount'] else
                                                                      self.LF_input.Ox['ox_fincov']['amount'] if(i+j)>=(max(self.enrgOff,self.LF_input.LF_gas['flareOff']['amount'])) else
                                                                      self.LF_input.Ox['ox_nocol']['amount'] if self.LFG_Coll_Eff['Collection ' + str(j) + ' Years Since Waste Burial']['Waste buried in Year '+str(i)] <self.LF_input.LF_gas['incColEff']['amount'] else
                                                                      self.LF_input.Ox['ox_col']['amount']  for i in np.arange(0,self.n)]
                                                                         
            
### calculating average collection and oxdiation            
        self.LFG_Coll_Eff = self.LFG_Coll_Eff.transpose()
        self.LFG_Ox_Eff = self.LFG_Ox_Eff.transpose()
        self.LFG_Coll_Eff['average collection']= self.LFG_Coll_Eff.sum(axis=1)/(self.n) 
        self.LFG_Ox_Eff['average oxidation']= self.LFG_Ox_Eff.sum(axis=1)/(self.n) 

    def Cal_LFG(self):

### LFG generation parameter
        self.param2=pd.DataFrame(index = self.Index)
        self.param2['k'] = (self.Material_Properties['Lab Decay Rate'][4:]/156) * (self.LF_input.LF_gas['actk']['amount']/0.04)
        self.param2.loc ['Unit','k'] = '1/yr'
        
        self.param2['L0'] = self.Material_Properties['Methane Yield'][4:]
        self.param2.loc ['Unit','L0'] = 'm3/dry Mg'
        
        self.param2['solid Content'] = 1 - self.Material_Properties['Moisture Content'][4:]/100
        self.param2.loc ['Unit','solid Content'] = 'Fraction'

### Methane generation        
        self.Methane_gen=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_gen['Methane generated at year: ' + str(j)]= self.param2['L0'][1:]*self.param2['solid Content'][1:]*(np.e**(-self.param2['k'][1:]*j)-np.e**(-self.param2['k'][1:]*(j+1))) 
            self.Methane_gen.loc ['Unit','Methane generated at year: ' + str(j)] = 'm3/Mg'
        
        self.Methane_gen['Total generated Methane']= self.Methane_gen.sum(axis=1)                                                       
        self.Methane_gen.loc ['Unit','Total generated Methane'] = 'm3/Mg'
        
        self.Methane_gen['Fraction of L0 Generated']=  self.Methane_gen['Total generated Methane'][1:]/(self.param2['L0'][1:].apply(lambda x: 1 if x <=0 else x) * self.param2['solid Content'][1:])
        self.Methane_gen.loc ['Unit','Fraction of L0 Generated'] = 'Fraction'
        

        
### Methane collected
        self.Methane_Col=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_Col['Methane collected at year: ' + str(j)]= self.Methane_gen['Methane generated at year: ' + str(j)][1:] * self.LFG_Coll_Eff['average collection']['Collection ' + str(j) + ' Years Since Waste Burial']/100
            self.Methane_Col.loc ['Unit','Methane collected at year: ' + str(j)] = 'm3/Mg'
            
        self.Methane_Col['Total Methane collected']= self.Methane_Col.sum(axis=1)
        self.Methane_Col.loc ['Unit','Total Methane collected'] = 'm3/Mg'
        
        self.Methane_Col['Collection Eff']= self.Methane_Col['Total Methane collected'][1:]/self.Methane_gen['Total generated Methane'][1:].apply(lambda x: 1 if x <=0 else x) 
        self.Methane_Col.loc ['Unit','Collection Eff'] = 'Fraction'

### Methane combustion for Energy         
        self.Methane_Comb=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_Comb['Methane combusted at year: ' + str(j)]= [ 'm3/Mg' if i == 'Unit' else
                                                                         0 if not self.LF_input.LF_gas['enrgRecovered']['amount'] else
                                                                         0 if j <= self.LF_input.LF_gas['enrgOn']['amount'] else
                                                                         self.Methane_Col['Methane collected at year: ' + str(j)][i]*(100-self.LF_input.LF_gas['EnrgRecDownTime']['amount'])/100  if j <= self.LF_input.LF_gas['enrgOff1']['amount'] else
                                                                         0 for i in self.Index]
            
        self.Methane_Comb['Total Methane combusted']= self.Methane_Comb.sum(axis=1)
        self.Methane_Comb.loc ['Unit','Total Methane combusted'] = 'm3/Mg'
        
        self.Methane_Comb['Percent of Generated used for Energy']= self.Methane_Comb['Total Methane combusted'][1:]/self.Methane_gen['Total generated Methane'][1:].apply(lambda x: 1 if x <=0 else x)  * 100
        self.Methane_Comb.loc ['Unit','Percent of Generated used for Energy'] = '%'        
        
        self.Methane_Comb['Percent of Collected used for Energy']= self.Methane_Comb['Total Methane combusted'][1:]/self.Methane_Col['Total Methane collected'][1:].apply(lambda x: 1 if x <=0 else x)  * 100
        self.Methane_Comb.loc ['Unit','Percent of Collected used for Energy'] = '%'        
        
### Methane Sent to Flare  (Includes downtime but not methane destruction efficiency)        
        self.Methane_Flare=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_Flare['Methane Flared at year: ' + str(j)]= self.Methane_Col['Methane collected at year: ' + str(j)][1:]-self.Methane_Comb['Methane combusted at year: ' + str(j)][1:]
            self.Methane_Flare.loc ['Unit','Methane Flared at year: ' + str(j)] = 'm3/Mg'        
        
        self.Methane_Flare['Total Methane flared']= self.Methane_Flare.sum(axis=1)
        self.Methane_Flare.loc ['Unit','Total Methane flared'] = 'm3/Mg'

### Methane Oxidized
        self.Methane_Ox=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_Ox['Methane oxidized at year: ' + str(j)]= (self.Methane_gen['Methane generated at year: ' + str(j)][1:]-self.Methane_Col['Methane collected at year: ' + str(j)][1:])\
                                                                    *self.LFG_Ox_Eff['average oxidation']['Oxidation ' + str(j) + ' Years Since Waste Burial']/100
            self.Methane_Ox.loc ['Unit','Methane oxidized at year: ' + str(j)] = 'm3/Mg'
        
        self.Methane_Ox['Total Methane oxidized']= self.Methane_Ox.sum(axis=1)
        self.Methane_Ox.loc ['Unit','Total Methane oxidized'] = 'm3/Mg'

### Methane Emitted
        self.Methane_Emitted=pd.DataFrame(index = self.Index)
        for j in np.arange(0,self.timescale):
            self.Methane_Emitted['Methane Emitted at year: ' + str(j)]= self.Methane_gen['Methane generated at year: ' + str(j)][1:] \
                                                                        -self.Methane_Comb['Methane combusted at year: ' + str(j)][1:]*self.LF_input.LF_gas['EngineCombEff']['amount']/100 \
                                                                        -self.Methane_Flare['Methane Flared at year: ' + str(j)][1:]*self.LF_input.LF_gas['FlareCombEff']['amount']/100 \
                                                                        -self.Methane_Ox['Methane oxidized at year: ' + str(j)][1:]
            self.Methane_Emitted.loc ['Unit','Methane Emitted at year: ' + str(j)] = 'm3/Mg'
        
        self.Methane_Emitted['Total Methane Emitted']= self.Methane_Emitted.sum(axis=1)
        self.Methane_Emitted.loc ['Unit','Total Methane Emitted'] = 'm3/Mg'

        self.Methane_Emitted['Percent of Generated Methane Emitted']= self.Methane_Emitted['Total Methane Emitted'][1:]/self.Methane_gen['Total generated Methane'][1:].apply(lambda x: 1 if x <=0 else x)  * 100
        self.Methane_Emitted.loc ['Unit','Percent of Generated Methane Emitted'] = '%'
        
    
    
A= LF()
A.Cal_LFG_Col_Ox()
A.Cal_LFG()
C = A.LFG_Coll_Eff
CC= A.param1
CCC= A.LFG_Ox_Eff
CCCC= A.param2
CCCCC=A.Methane_gen
CCCCCC=A.Methane_Col
CCCCCCC=A.Methane_Comb
B=A.Methane_Flare
BB=A.Methane_Ox
BBB=A.Methane_Emitted


from time import time
B=time()
A= LF()
for i in range (100):
    A.Cal_LFG_Col_Ox()
    A.Cal_LFG()
print(time()-B)
  
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