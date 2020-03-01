# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:17:40 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from ..MC import *
class Composting_input(MC):
    def __init__(self,input_data_path=None):
        if input_data_path:
            raise ValueError('Wrong input file, you cannot use input_data_path with input_script')
    
### Assumed Composition 
        self.Assumed_Comp = [0.1915,0.1447,0.1414,0.3977,0.0221,0.0035,0.0000,0.0031,0.0004,0.0035,0.0102,0.0019,0.0006,0.0015,
                             0.0019,0.0015,0.0000,0.0206,0.0011,0.0020,0.0038,0.0000,0.0000,0.0000,0.0055,0.0158,0.0008,0.0002,
                             0.0005,0.0006,0.0000,0.0000,0.0001,0.0077,0.0033,0.0022,0.0000,0.0000,0.0000,0.0102,0.0000,0.0000,
                             0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000]


### Operating Parameters
        self.Op_Param = {
                'Taod':{"Name":"Annual operating days","amount":260,"unit":'days/year',"Reference":None},
                'Tdoh':{"Name":"Daily operating hours","amount":8,"unit":'hours/day',"Reference":None},
                'Tact':{"Name":"Active composting time","amount":70,"unit":'days',"Reference":None},
                'Tcur':{"Name":"Curing time","amount":30,"unit":'days',"Reference":None}
                }
        
### Substrate Parameters
        self.Sawdust = {
                        'Bulk_Density':{"Name":"Bulk Density","amount":240,"unit":"kg/m3","Reference":'25'},
                       'Moisture_Content':{"Name":"Moisture Content","amount":0.39,"unit":None,"Reference":'25'},
                       'Volatile Solids':{"Name":"Volatile Solids","amount":0.906,"unit":None,"Reference":'25'},
                       'C_Cont':{"Name":"C_Cont","amount":53.4,"unit":"%","Reference":'25'},
                       'N_Cont':{"Name":"N_Cont","amount":0.25,"unit":"%","Reference":'25'},
                       'Pre screen out proportion':{"Name":"Pre screen out proportion","amount":0.05,"unit":None,"Reference":'25'},
                       'Post screen out proportion':{"Name":"Post screen out proportion","amount":1,"unit":None,"Reference":'25'},
                       'Proportion Vacuumed Out':{"Name":"Proportion Vacuumed Out","amount":1,"unit":None,"Reference":'25'},
                       'C Emitted':{"Name":"C Emitted","amount":18,"unit":"%","Reference":'25'},
                       'VS loss per C loss':{"Name":"VS loss per C loss","amount":2,"unit":None,"Reference":'25'}
                       }
        
        self.Wood_Chips = {
                        'Bulk_Density':{"Name":"Bulk Density","amount":320,"unit":"kg/m3","Reference":'25'},
                        'Moisture_Content':{"Name":"Moisture Content","amount":0.5,"unit":None,"Reference":'25'},
                        'Volatile Solids':{"Name":"Volatile Solids","amount":0.906,"unit":None,"Reference":'25'}
                            }
        
        self.Screen_Rejects = {'Moisture_Content':{"Name":"Moisture Content","amount":0.2678,"unit":None,"Reference":'25'},
                               'Volatile Solids':{"Name":"Volatile Solids","amount":0.8825,"unit":None,"Reference":'25'},
                               'C_Cont':{"Name":"C_Cont","amount":48.1,"unit":"%","Reference":'25'},
                               'N_Cont':{"Name":"N_Cont","amount":0.1,"unit":"%","Reference":'25'},
                               'Pre screen out proportion':{"Name":"Pre screen out proportion","amount":0,"unit":None,"Reference":'25'},
                               'Post screen out proportion':{"Name":"Post screen out proportion","amount":90,"unit":None,"Reference":'25'},
                               'Proportion Vacuumed Out':{"Name":"Proportion Vacuumed Out","amount":1,"unit":None,"Reference":'25'}
                               }
        
### Degradation Parameters
        self.Degradation_Parameters={
                'CN':{"Name":"inimum CN target at beginning of active composting","amount":30,"unit":"kg C/kg N","Reference":None},
                'initMC':{"Name":"Minimum initial moisture content","amount":0.55,"unit":None,"Reference":None},
                'MCac':{"Name":"Moisture content after active composting","amount":0.5,"unit":None,"Reference":None},
                'MCcu':{"Name":"Moisture content after curing","amount":0.45,"unit":None,"Reference":None},
                'densfinComp':{"Name":"Final compost bulk density","amount":700,"unit":'kg/m3',"Reference":None},
                'acDegProp':{"Name":"Proportion of mass loss that occurs during active composting","amount":90,"unit":'%',"Reference":None},
                }

### Material Properties
        self.Material_Properties ={
            'densFC':{'Name':'Density of final compost','amount':700 ,'unit':'kg/m3','Referenc':None},
            'densPeat':{"Name":"Density of peat","amount":200,"unit":'kg/m3',"Reference":None},
            'PeatSubFac':{"Name":"Volumetric peat replacement factor","amount":1,"unit":None,"Reference":None}
            }

### Biological Degredation
        self.Biological_Degredation = {
                'pCasCH4':{"Name":"Proportion of emitted C emitted as CH4","amount":0.017,"unit":None,"Reference":'12'},
                'pNasNH3':{"Name":"Proportion of emitted N emitted as NH3","amount":0.04,"unit":None,"Reference":'31'},
                'pNasN2O':{"Name":"Proportion of emitted N emitted as N2O","amount":0.004,"unit":None,"Reference":'12'},
                'bfCH4re':{"Name":"Biofilter CH4 removal efficiency","amount":0.15,"unit":None,"Reference":'18'},
                'bfNH3re':{"Name":"Biofilter NH3 removal efficiency","amount":48,"unit":'%',"Reference":'18'},
                'bfN2Ore':{"Name":"Biofilter N2O removal efficiency","amount":0,"unit":'%',"Reference":'18'},
                'preNH3toNOx':{"Name":"Proportion of removed NH3 that becomes NOx","amount":1,"unit":None,"Reference":'18'},
                'preNH3toN2O':{"Name":"Proportion of removed NH3 that becomes Nitrous Oxide","amount":0,"unit":None,"Reference":'18'},
                'bfVOCre':{"Name":"Biofilter VOC removal efficiency","amount":18,"unit":'%',"Reference":'32'},
                'percCStor':{"Name":"Percent of carbon in compost remaining after 100 years","amount":10,"unit":'%',"Reference":'5'},
                'percCStor_LF':{"Name":"Percent of carbon in compost remaining after 100 years","amount":100,"unit":'%',"Reference":None},
                'humFormFac':{"Name":"100 year carbon storage from humus formation","amount":0,"unit":'kg-C/kg-C in Compost',"Reference":'6'}
                }
        
### Land application inputs
        self.Land_app = {
                'perN2Oevap':{"Name":"Percent of applied N evaporated as N2O","amount":1.5,"unit":'%',"Reference":'16'},
                'perNH3evap':{"Name":"Percent of Ammonia that evaporates","amount":15,"unit":'%',"Reference":'16'},
                'perNasNH3fc':{"Name":"Percent N that is Ammonia","amount":50,"unit":'%',"Reference":'16'},
                'distLand':{"Name":"Haul distance to land","amount":20,"unit":'km',"Reference":None},
                'land_payload':{"Name":"Actual payload of truck used to haul soil amendment","amount":7.3,"unit":'Mg',"Reference":None},
                }

### Odor Control System
        self.Odor_Cont = {
                'Moc':{"Name":"OC blower power required per air flow rate","amount":0,"unit":'kW/cmm',"Reference":'4'},
                'ocReqAF':{"Name":"Odor control air flow required","amount":0,"unit":'m3/Mgpd',"Reference":'19'}
                }
        
### Vacuum Cleaning System
        self.Vaccum_sys = {
                'vacDiesFac':{"Name":"Diesel use","amount":0.22,"unit":'L/Mg',"Reference":'8'},
                'vacElecFac':{"Name":"Vacuum electricity (diesel by default)","amount":0,"unit":'kWh/Mg',"Reference":None}
                }

### Screening
        self.Screen = {
                'Mtr':{"Name":"Energy required per weight of post-screened material","amount":0.9,"unit":'kWh/Mg',"Reference":'9'}
                }        
        
### Curing
        self.Curing = {
                'Ftc':{"Name":"Frequency of turning during curing phase","amount":0.14,"unit":'1/day',"Reference":'21,19,20'}
                }         
        
### Front End Loader
        self.Loader = {
                'hpfel':{"Name":"Front end loader energy required per weight flow of material","amount":0.336,"unit":'kW/Mgd',"Reference":'10'},
                'Mffel':{"Name":"Front end loader specific fuel consumption","amount":0.26,"unit":'L/kWh',"Reference":'16'}
                }          

### Office Area
        self.Office = {
                'Mta':{"Name":"Office Area required per ton per day of material","amount":1.7,"unit":'m2/Mgpd',"Reference":'10'},
                'Mea':{"Name":"Energy required to power an office","amount":290,"unit":'kWh/m2-yr',"Reference":'11'}
                }         
        
### Avoided Fertilizer Production Offsets
        self.Fertilizer_offset = {
                'choice_BU':{"Name":"Offset Beneficial Use of Compost? (0=no; 1=yes)","amount":1,"unit":None,"Reference":None},
                'peatOff':{"Name":"Soil amendment offset peat (1) or no (0)","amount":1,"unit":None,"Reference":None},
                'fertOff':{"Name":"Soil amendment offset fertilizer (1) or no (0)","amount":1,"unit":None,"Reference":None}
                }              
        
### Active Compost Force Aeration        
        self.AC_Aeration = {
                'Aeff':{"Name":"Motor efficiency","amount":0,"unit":'kW-in/kW-out',"Reference":'4'},
                'Bhp':{"Name":"Blower power","amount":0,"unit":'kW',"Reference":'19'},
                'Breq':{"Name":"Blowers required per dry mass compost.","amount":0,"unit":'1/Mg',"Reference":'16,20'},
                'blPropON':{"Name":"Proportion of the time that blowers are on","amount":0,"unit":None,"Reference":'20'}
                } 

### Active Compost Windrow Turning   
        
# =============================================================================
# =============================================================================
# # Mwta unit should be kWh/Mg.turn        
# =============================================================================
# =============================================================================
        
        self.AC_Turning = {
                'Mwta':{"Name":"Windrow turner power rating","amount":0.24,"unit":'kWh/Mg',"Reference":'3'},
                'Mwfa':{"Name":"The fuel consumption of a windrow turner","amount":0.127,"unit":'L/kWh',"Reference":'3'},
                'Fta':{"Name":"Turning frequency","amount":0.33,"unit":'1/days',"Reference":None}
                }   
        
### Waste Shredding
        self.Shredding = {
                'Mtgp':{"Name":"Grinder power rating.","amount":10.6,"unit":'kWh/Mg',"Reference":'3'},
                'Mtgf':{"Name":"Grinder fuel consumption","amount":0.25,"unit":'L/kWh',"Reference":'3'}
                }
        
### In-Vessel
        self.Vessel = {
                'Minv':{"Name":"Vessel energy use per weight of material","amount":0,"unit":'kWh/Mg',"Reference":'27'}
                }
        
### Monte_carlo          
    def setup_MC(self,seed=None):
        self.Input_list = {'Op_Param':self.Op_Param, 'Sawdust':self.Sawdust, 'Wood_Chips':self.Wood_Chips,
                'Screen_Rejects':self.Screen_Rejects, 'Degradation_Parameters':self.Degradation_Parameters,
                'Material_Properties':self.Material_Properties,'Biological_Degredation':self.Biological_Degredation, 'Land_app':self.Land_app, 'Odor_Cont':self.Odor_Cont,
                'Vaccum_sys':self.Vaccum_sys,'Screen':self.Screen,'Curing':self.Curing, 'Loader':self.Loader,
                'Office':self.Office,'Fertilizer_offset':self.Fertilizer_offset, 'AC_Aeration':self.AC_Aeration,
                'AC_Turning':self.AC_Turning,'Shredding':self.Shredding,'Vessel':self.Vessel}
        super().__init__(self.Input_list)
        super().setup_MC(seed)
#################################################################
#### Convering the input dictionaries to csv file
#################
# =============================================================================
# A= Composting_input()
# A.setup_MC()
# category=[]
# Parameter=[]
# Name=[]
# amount=[]
# unit=[]
# 
# for x in A.Input_list.keys():
#     for y in  A.Input_list[x].keys():
#         category.append(x)
#         Parameter.append(y)
#         Name.append(A.Input_list[x][y]['Name'])
#         amount.append(A.Input_list[x][y]['amount'])
#         unit.append(A.Input_list[x][y]['unit'])
# AAA={'category':category,'Parameter':Parameter,'Name':Name,'amount':amount,'unit':unit}
# =============================================================================
