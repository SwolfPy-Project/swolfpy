# -*- coding: utf-8 -*-
"""
@author: msmsa
"""
import numpy as np
import pandas as pd


class material:
    def __init__(self,name):
        self.name = name
        
    #physical properties
    
    def physical_properties (self,moistCont,ash,LHV):   # adding the physical properties
        self.moisCont = moistCont
        self.solidCont = (100 - moistCont )
        self.ash = ash
        self.vs = (100 - ash)
        self.LHV = LHV
    
    def get_physical_properties (self):   # return physical properties of material as dictionary
        return {"name":self.name , "Moisture cont.":self.moisCont, "Solid cont.":self.solidCont,\
        "Ash cont. % of TS": self.ash, "VS cont. % of TS": self.vs, "LHV MJ/dry kg":self.LHV}   
        
    def get_physical_properties_list (self):   # return physical properties of material as list
        return [self.moisCont, self.solidCont, self.ash, self.vs,self.LHV] 
        
    
    #chemical properties
    
    def chemical_properties (self,bio_C_c,fos_C_c,H_c,O_c,N_c,P_c,K_c,Fe_c,Cu_c,Cd_c,As_c,\
                             Hg_c,Se_c,Cr_c,Pb_c,Zn_c,Ba_c,Sb_c,Ni_c,Ag_c,Cl_c,S_c,Al_c):    # adding the chemical properties
        self.bio_C_c = bio_C_c 
        self.fos_C_c = fos_C_c
        self.H_c = H_c
        self.O_c = O_c
        self.N_c = N_c 
        self.P_c = P_c
        self.K_c = K_c
        self.Fe_c = Fe_c
        self.Cu_c = Cu_c
        self.Cd_c = Cd_c
        self.As_c = As_c
        self.Hg_c = Hg_c
        self.Se_c = Se_c
        self.Cr_c = Cr_c
        self.Pb_c = Pb_c
        self.Zn_c = Zn_c
        self.Ba_c = Ba_c
        self.Sb_c = Sb_c
        self.Ni_c = Ni_c 
        self.Ag_c = Ag_c
        self.Cl_c = Cl_c
        self.S_c = S_c
        self.Al_c = Al_c 
      

    def get_chemical_properties (self):   # return chemical properties of the material as dictionary
        return {"name":self.name , "bio_C_c % of TS":self.bio_C_c, "fos_C_c % of TS":self.fos_C_c, "H_c % of TS":self.H_c,
                "O_c % of TS":self.O_c, "N_c % of TS":self.N_c, "P_c % of TS":self.P_c,"K_c % of TS":self.K_c,
                "Fe_c % of TS":self.Fe_c, "Cu_c % of TS":self.Cu_c, "Cd_c % of TS":self.Cd_c, "As_c % of TS":self.As_c,
                "Hg_c % of TS":self.Hg_c, "Se_c % of TS":self.Se_c, "Cr_c % of TS":self.Cr_c, "Pb_c % of TS":self.Pb_c,
                "Zn_c % of TS":self.Zn_c, "Ba_c % of TS":self.Ba_c, "Sb_c % of TS":self.Sb_c, "Ni_c % of TS":self.Ni_c,
                "Ag_c % of TS":self.Ag_c, "Cl_c % of TS":self.Cl_c, "S_c % of TS":self.S_c, "Al_c % of TS":self.Al_c}   
        
    def get_chemical_properties_list (self):   # return chemical properties of the material as list
        return [ self.bio_C_c, self.fos_C_c, self.H_c, self.O_c, self.N_c, self.P_c,
                self.K_c, self.Fe_c, self.Cu_c, self.Cd_c, self.As_c, self.Hg_c, self.Se_c,
                self.Cr_c, self.Pb_c, self.Zn_c, self.Ba_c, self.Sb_c, self.Ni_c, self.Ag_c,
                self.Cl_c, self.S_c, self.Al_c]
        
    

def check_nan(x):  # replace zeros when there is no data ("nan")
    if str(x) == "nan":
        return 0
    return x


def load_material (file_path):  # read the xlsx file
    inputdata = pd.ExcelFile("SWMCommonData.xlsx")

    Mateiral_Properties = inputdata.parse(sheet_name="Material Properties",index_col="Materials")
    return Mateiral_Properties


Mateiral_Properties = load_material ("SWMCommonData.xlsx" )

# Creating the materials and importing the properties
for i in np.arange(4,49):
    exec("%s = %s" % (Mateiral_Properties.index[i],'material(Mateiral_Properties.index[i])'))
    
    exec("%s.physical_properties%s" % (Mateiral_Properties.index[i] ,\
                                     str((
                                    check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Moisture Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Ash Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Lower Heating Value'])
                                    ))))

    exec("%s.chemical_properties%s" % (Mateiral_Properties.index[i] , str((
                                    check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Biogenic Carbon Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Fossil Carbon Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Hydrogen Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Oxygen Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Nitrogen Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Phosphorus Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Potassium Content']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Iron']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Copper']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Cadmium']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Arsenic']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Mercury']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Selenium']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Chromium']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Lead']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Zinc']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Barium']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Antimony']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Nickel']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Silver']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Chlorine']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Sulphur']),
                                       check_nan(Mateiral_Properties.at[Mateiral_Properties.index[i],'Aluminum'])
                                    )))) 
                                        
   



