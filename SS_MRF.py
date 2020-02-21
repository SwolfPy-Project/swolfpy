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
    def __init__(self,input_data_path=None,CommonDataObjct=None):
        
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()
            
        self.InputData= SS_MRF_input(input_data_path)
        
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
        self.Assumed_Comp = pd.Series(self.InputData.Assumed_Comp,index=self.Index)

#%% Calc Function
    def calc(self):
        self.LCI_Waste = LCI(self.Index)
        self.LCI = LCI(self.Index)
        #self.LCC = LCI(self.Index)
            
        ### Initial mass
        self._Input = np.array(self.Assumed_Comp)

        ### Drum Feeder          
        self._DF_feed=Drum_Feeder(self._Input,self.InputData,self.LCI)

        ### Manual Sort 1 (Negative)  for separating the plastic film   
        self._MS1_rmnd,self._MS1_rmvd=Man_Sort1(self._DF_feed,self.process_data['Manual Sort 1 (Negative)'].values,self.InputData,self.LCI)
        #self._MS1_rmnd is not residual, it goes to vacuum

        ### Vacuum     
        self._Vac_rmnd,self._Vac_rmvd=Vacuum(self._MS1_rmvd,self.process_data['Vacuum'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('Other_Residual',self._Vac_rmnd)
        self.LCI_Waste.add('LDPE_Film',self._Vac_rmvd)
        
        ### Disc Screen 1: OCC separation
        self._DS1_rmnd,self._DS1_rmvd=DS1(self._MS1_rmnd,self.process_data['Disc Screen 1'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('OCC',self._DS1_rmvd)
        
        ### Disc Screen 2: Newspaper separation
        self._DS2_rmnd,self._DS2_rmvd=DS2(self._DS1_rmnd,self.process_data['Disc Screen 2'].values,self.InputData,self.LCI)        

        ### Manual Sort 2-DS2 (Negative)
        self._MS2_DS2_rmnd,self._MS2_DS2_rmvd=MS2_DS2(self._DS2_rmvd,self.process_data['Manual Sort 2-DS2 (Negative)'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('Other_Residual',self._MS2_DS2_rmvd)
        
        ### Disc Screen 3: Fiber separation
        self._DS3_rmnd,self._DS3_rmvd=DS3(self._DS2_rmnd,self.process_data['Disc Screen 3'].values,self.InputData,self.LCI)
        
        ### Manual Sort 2-DS3 (Negative)
        self._MS2_DS3_rmnd,self._MS2_DS3_rmvd=MS2_DS3(self._DS3_rmvd,self.process_data['Manual Sort 2-DS3 (Negative)'].values,self.InputData,self.LCI)   
        self.LCI_Waste.add('Other_Residual',self._MS2_DS3_rmvd)
        
        ### Secondary sort for mixed paper
        self._Mixed_Paper,self._ONP,self._OFF,self._Fiber_Other=Mixed_paper_separation(self._MS2_DS3_rmnd+self._MS2_DS2_rmnd,self.InputData)
        self.LCI_Waste.add('Mixed_Paper',self._Mixed_Paper)
        self.LCI_Waste.add('ONP',self._ONP)
        self.LCI_Waste.add('OFF',self._OFF)
        self.LCI_Waste.add('Fiber_Other',self._Fiber_Other)
        
        ### 1-Way Baler: product is baled OCC and mixed fiber
        self._Baler_1Way_Baled=Baler_1Way(self._DS1_rmvd,self._MS2_DS3_rmnd+self._MS2_DS2_rmnd,self.InputData,self.LCI)
        
        ### Glass Breaker Screen
        self._GBS_rmnd,self._GBS_rmvd=GBS(self._DS3_rmnd,self.process_data['Glass Breaker Screen'].values,self.InputData,self.LCI)
        
        ### Air Knife
        self._AK_rmnd,self._AK_rmvd=AK(self._GBS_rmvd,self.process_data['Air Knife'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('Other_Residual',self._AK_rmvd)
        
        ### Optical Glass
        self._OG_rmnd,self._OG_rmvd=OG(self._AK_rmnd,self.process_data['Optical Glass'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('Other_Residual',self._OG_rmnd)
        
        ### Manual Sort 3-G (Negative)
        self._MS3_G_rmnd,self._MS3_G_rmvd=MS3_G(self._OG_rmvd,self.process_data['Manual Sort 3-G (Negative)'].values,self.InputData,self.LCI)  
        self.LCI_Waste.add('Other_Residual',self._MS3_G_rmvd)
        
        ### Secondary sort glass
        self._Res_Glass,self._Brown_glass,self._Clear_glass,self._Green_glass,self._Mixed_Glass=Glass_type(self._MS3_G_rmnd,self.InputData)
        self.LCI_Waste.add('Other_Residual',self._Res_Glass)
        self.LCI_Waste.add('Brown_glass',self._Brown_glass)
        self.LCI_Waste.add('Clear_glass',self._Clear_glass)
        self.LCI_Waste.add('Green_glass',self._Green_glass)
        self.LCI_Waste.add('Mixed_Glass',self._Mixed_Glass)
        
        ### Optical PET
        self._OPET_rmnd,self._OPET_rmvd=OPET(self._GBS_rmnd,self.process_data['Optical PET'].values,self.InputData,self.LCI)           

        ### Manual Sort 4-PET (Negative)
        self._MS4_PET_rmnd,self._MS4_PET_rmvd=MS4_PET(self._OPET_rmvd,self.process_data['Manual Sort 4-PET (Negative)'].values,self.InputData,self.LCI) 
        self.LCI_Waste.add('Other_Residual',self._MS4_PET_rmvd)
        self.LCI_Waste.add('PET',self._MS4_PET_rmnd)

        ### Optical HDPE
        self._OHDPE_rmnd,self._OHDPE_rmvd=OHDPE(self._OPET_rmnd,self.process_data['Optical HDPE'].values,self.InputData,self.LCI)           

        ### Manual Sort 4-HDPE (Negative)
        self._MS4_HDPE_rmnd,self._MS4_HDPE_rmvd=MS4_HDPE(self._OHDPE_rmvd,self.process_data['Manual Sort 4-HDPE (Negative)'].values,self.InputData,self.LCI) 
        self.LCI_Waste.add('Other_Residual',self._MS4_HDPE_rmvd)
        
        ### HDPE sold by type?
        self._HDPE_Unsorted,self._HDPE_P,self._HDPE_T=HDPE_type(self._MS4_HDPE_rmnd,self.InputData)
        self.LCI_Waste.add('HDPE_Unsorted',self._HDPE_Unsorted)
        self.LCI_Waste.add('HDPE_P',self._HDPE_P)
        self.LCI_Waste.add('HDPE_T',self._HDPE_T)
        
        ### Magnet
        self._Magnet_rmnd,self._Magnet_rmvd=Magnet(self._OHDPE_rmnd,self.process_data['Magnet'].values,self.InputData,self.LCI)           

        ### Manual Sort 4-Fe (Negative)
        self._MS4_Fe_rmnd,self._MS4_Fe_rmvd=MS4_Fe(self._Magnet_rmvd,self.process_data['Manual Sort 4-Fe (Negative)'].values,self.InputData,self.LCI) 
        self.LCI_Waste.add('Other_Residual',self._MS4_Fe_rmvd)
        self.LCI_Waste.add('Fe',self._MS4_Fe_rmnd)
        
        ### Eddy Current Separator
        self._EDS_rmnd,self._EDS_rmvd=EDS(self._Magnet_rmnd,self.process_data['Eddy Current Separator'].values,self.InputData,self.LCI)           

        ### Manual Sort 4-Al (Negative)
        self._MS4_Al_rmnd,self._MS4_Al_rmvd=MS4_Al(self._EDS_rmvd,self.process_data['Manual Sort 4-Al (Negative)'].values,self.InputData,self.LCI) 
        self.LCI_Waste.add('Other_Residual',self._MS4_Al_rmvd)
        self.LCI_Waste.add('Al',self._MS4_Al_rmnd)
        
        ### Manual Sort 5 (Positive)
        self._MS5_rmnd,self._MS5_rmvd=MS5(self._EDS_rmnd,self.process_data['Manual Sort 5 (Positive)'].values,self.InputData,self.LCI)
        self.LCI_Waste.add('Other_Residual',self._MS5_rmnd)
        
        ### 2-Way Baler: product is baled plastics and metals (container) + Film
        self._Recovered_Container = self._MS4_PET_rmnd + self._MS4_HDPE_rmnd + self._MS4_Fe_rmnd + self._MS4_Al_rmnd + self._MS5_rmvd
        self._Baler_2Way_Baled=Baler_2Way(self._Recovered_Container+self._Vac_rmvd,self.InputData,self.LCI)
        
        ### Rolling_Stock
        Rolling_Stock(self._Input,self.InputData,self.LCI)

        ### Conveyor
        #Calculate the mass carried by conveyor
        self._Mass_toConveyor = 2*self._Input + self._DF_feed+\
                        (self._MS1_rmnd if self.InputData.Rec_material['OCC']['amount']>0 else 0)+\
                        (self._DS1_rmnd+self._DS2_rmvd+self._DS2_rmnd+self._DS3_rmvd if self.InputData.Rec_material['Non_OCC_Fiber']['amount']>0 else 0)+\
                        self._DS3_rmnd+\
                        (self._GBS_rmvd+self._AK_rmnd+self._OG_rmvd if self.InputData.Rec_material['Glass']['amount']>0 else 0)+\
                        (self._GBS_rmnd+self._OPET_rmvd if self.InputData.Rec_material['PET']['amount']>0 else 0)+\
                        (self._OPET_rmnd+self._OHDPE_rmvd if self.InputData.Rec_material['HDPE']['amount']>0 else 0)+\
                        (self._OHDPE_rmnd +self._Magnet_rmvd if self.InputData.Rec_material['Ferrous']['amount']>0 else 0)+\
                        (self._Magnet_rmnd+self._EDS_rmvd if self.InputData.Rec_material['Aluminous']['amount']>0 else 0)+ \
                        self._EDS_rmnd

        #conveyor
        Conveyor(self._Mass_toConveyor,self.InputData,self.LCI)        

        ### General Electricity
        Electricity(self._Input,self.InputData,self.LCI)
        
#%% Check Mass balance        
        ### Check mass balance:
        mass_out = self.LCI_Waste.LCI.sum(axis=1)
        for i in range(len(self.Index)):
            if abs(mass_out[i]-self._Input[i])>0.01:
                raise ValueError('*** Mass Balance Error *** \n Output mass is not equal to input mass!')
                
#%% Report    
    ### Report
    def report(self):
        ### Output
        self.SS_MRF = {}
        self.SS_MRF["process name"] = 'SS_MRF'
        
        # Waste
        #self.waste_DF = self.LCI_Waste.report(self._Input)
        #self.SS_MRF["Waste"] = self.waste_DF.transpose().to_dict()
        self.SS_MRF["Waste"] = self.LCI_Waste.report_T(self._Input).to_dict()
        
        # Technosphere
        #self.technosphere = self.LCI.report(self._Input)
        #self.SS_MRF["Technosphere"] = self.technosphere.transpose().to_dict()
        self.SS_MRF["Technosphere"] = self.LCI.report_T(self._Input).to_dict()
        
        # Biosphere
        Biosphere={}
        for y in self.Index:
            Biosphere[y]={}
        self.SS_MRF["Biosphere"] = Biosphere
        return(self.SS_MRF)

#%% Monte Carlo         
    ### setup for Monte Carlo simulation   
    def setup_MC(self,seed=None):
        self.InputData.setup_MC(seed)

    ### Calculate based on the generated numbers   
    def MC_calc(self):      
        input_list = self.InputData.gen_MC()
        self.calc()
        return(input_list)


# =============================================================================
# from time import time
# T1 = time()
# AA = SS_MRF()
# for i in range(100):
#     AA.calc()
#     AA.report()
# print('time ' ,time()-T1)
# =============================================================================






