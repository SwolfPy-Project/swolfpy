# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:10:12 2020

@author: msardar2
"""
import numpy as np
import pandas as pd
from SS_MRF_Input import *
from CommonData import *
from stats_arrays import *
from SS_MRF_subprocess import *

class SS_MRF:
    def __init__(self,input_data_path=None):
        self.CommonData = CommonData()
        self.SS_MRF_input= SS_MRF_input(input_data_path)
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'SS_MRF', index_col = 'Parameter')
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
        self.Assumed_Comp = pd.Series(self.SS_MRF_input.Assumed_Comp,index=self.Index)


    def calc(self):
### Initial mass 
         self._Input = np.array(self.Assumed_Comp)

### Drum Feeder          
         self._DF_res,self._DF_rmvd=Drum_Feeder(self._Input,self.process_data['Drum Feeder'].values)

### Manual Sort 1 (Negative)     
         self._DF_res,self._DF_rmvd=Man_Sort(self._Input,self.process_data['Drum Feeder'].values)





# =============================================================================
# Index(['Drum Feeder', 'Eddy Current Separator', 'Manual-ECS', 'Magnet',
#        'Manual-Magnet', 'Disc Screen 1', 'Manual-DS1', 'Disc Screen 2',
#        'Disc Screen 3', 'Manual-DS2', 'Manual-DS3', 'Vacuum', 'Manual-Vacuum',
#        'Optical HDPE', 'Manual-OSHDPE', 'Optical PET', 'Manual-OSPET',
#        'Manual Sort 1 (Negative)', 'Manual Sort 2-DS2 (Negative)',
#        'Manual Sort 2-DS3 (Negative)', 'Glass Breaker Screen', 'Air Knife',
#        'Optical Glass', 'Manual Sort 3-G (Negative)',
#        'Manual Sort 4-PET (Negative)', 'Manual Sort 4-HDPE (Negative)',
#        'Manual Sort 4-Fe (Negative)', 'Manual Sort 4-Al (Negative)',
#        'Manual Sort 5 (Positive)'],
#       dtype='object')
# =============================================================================


AA = SS_MRF()
AA.calc()
