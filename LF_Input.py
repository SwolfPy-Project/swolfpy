# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:08:08 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *
class LF_input:
    def __init__(self):
        pass

### Landfill Gas Parameters
        self.LF_gas = {                
                'actk':{'Name':'Landfill decay rate','amount':0.04,'unit':'1/yr','Reference':None},
                'initColTime':{'Name':'Time until initial gas collection','amount':2,'unit':'years','Reference':None},
                'initColEff':{'Name':'Initial gas collection efficiency','amount':50 ,'unit':'%','Reference':None},
                'cellFillTime':{'Name':'Cell fill time','amount':5 ,'unit':'years','Reference':None},  
                'intColEff':{'Name':'Gas collection efficiency under intermediate cover','amount':75 ,'unit':'%','Reference':None},  
                'incColTime':{'Name':'Time to increased gas collection efficiency','amount':15 ,'unit':'years','Reference':None},  
                'incColEff':{'Name':'Increased gas collection efficiency','amount':82.5 ,'unit':'%','Reference':None},  
                'timeToFinCover':{'Name':'Time from final waste placement to final cover','amount':1 ,'unit':'years','Reference':None},  
                'finColEff':{'Name':'Gas collection efficiency under final cover','amount':90 ,'unit':'%','Reference':None},  
                'enrgOn':{'Name':'Energy recovery cuton time','amount':5 ,'unit':'years','Reference':None},
                'enrgOff1':{'Name':'Energy recovery cutoff time','amount':52 ,'unit':'years','Reference':None},
                'flareOff':{'Name':'Flare cutoff time','amount':50 ,'unit':'Years','Reference':None},
                'enrgRecovered':{'Name':'Recover energy ','amount':1 ,'unit':'1/0','Reference':None},
                'EnrgRecDownTime':{'Name':'Energy recovery downtime ','amount': 3 ,'unit':'%','Reference':None},
                'FlareCombEff':{'Name':'Flare methane destruction efficiency','amount':99.9 ,'unit':'%','Reference':None},
                'EngineCombEff':{'Name':'Energy recovery destruction efficiency','amount':99 ,'unit':'%','Reference':None},
                'blwrPRR':{'Name':'Blower power rating requirement','amount':60.85 ,'unit':'scfm/hp','Reference':None},
                'blwrPRRm3':{'Name':'Blower power rating requirement','amount': 1215470.3 ,'unit':'m3/yr/kW','Reference':None},
                'blwrPerLoad':{'Name':'Blower load','amount':75 ,'unit':'%','Reference':None},
                'blwrEff':{'Name':'Blower efficiency','amount':90 ,'unit':'kW-out/kWh-in','Reference':None},
                'optime':{'Name':'Landfill Operation time','amount':20 ,'unit':'years','Reference':None}                
                }
        
### Oxidation Inputs
        self.Ox = {                
                'ox_nocol':{'Name':'Oxidation rate without collection','amount':10,'unit':'%','Reference':None},
                'ox_col':{'Name':'Oxidation rate with collection','amount':20,'unit':'%','Reference':None},
                'ox_fincov':{'Name':'Oxidation rate after final cover','amount':35 ,'unit':'%','Reference':None}
                }

### LFG combustion
        self.LFG_Comb = {'convEff':{'Name':'combustion eff','amount':0.365 ,'unit':None,'Reference':None}             
                        }

### Leachate
        self.Leachate = {
                        'dis_POTW':{'Name':'Distance to POTW','amount':40 ,'unit':'km','Reference':None}, 
                        'pay_leach':{'Name':'Actual payload of trucks delivering leachate','amount':35 ,'unit':'Mg','Reference':None}, 
                        'er_leach':{'Name':'Empty return of trucks delivering leachate','amount':1 ,'unit':None,'Reference':None}, 
                        'LF_lcht_p':{'Name':'Collection efficiency of leachate','amount':0.998 ,'unit':'fraction','Reference':None}, 
                        'LF_time1':{'Name':'time after waste placement that recirculation or treatment begins','amount':0 ,'unit':'years','Reference':None},  
                        'LF_time3':{'Name':'time after waste placement that leachate collection stops','amount':80 ,'unit':'years','Reference':None},
                        'LF_eff_BOD':{'Name':'BOD REMOVAL EFFICIENCY','amount':92.1 ,'unit':'%','Reference':None},
                        'LF_eff_COD':{'Name':'COD REMOVAL EFFICIENCY','amount':80 ,'unit':'%','Reference':None},
                        'LF_eff_NH3':{'Name':'NH3 REMOVAL EFFICIENCY','amount':21.6 ,'unit':'%','Reference':None},
                        'LF_eff_PO4':{'Name':'PO4 REMOVAL EFFICIENCY','amount':21.6 ,'unit':'%','Reference':None},
                        'LF_eff_TSS':{'Name':'TSS REMOVAL EFFICIENCY','amount':96 ,'unit':'%','Reference':None},
                        'LF_eff_mtls':{'Name':'metals REMOVAL EFFICIENCY','amount':85 ,'unit':'%','Reference':None},
                        'LF_eff_orgncs':{'Name':'trace organics REMOVAL EFFICIENCY','amount':0 ,'unit':'%','Reference':None}
                        }

### BOD
        self.BOD ={
                    'LF_BOD2':{'Name':'year period 1 ends','amount':1.5 ,'unit':'years','Reference':None},
                    'LF_BOD4':{'Name':'year period 2 ends','amount':10 ,'unit':'years','Reference':None},
                    'LF_BOD6':{'Name':'year period 3 ends','amount':50 ,'unit':'years','Reference':None},
                    'LF_BOD_con1':{'Name':'BOD starting concentration at period 1','amount':0.09992900727 ,'unit':'kg/L','Reference':None},
                    'LF_BOD_con3':{'Name':'BOD starting concentration at period 2','amount':0.09992900727 ,'unit':'kg/L','Reference':None},
                    'LF_BOD_con5':{'Name':'BOD starting concentration at period 3','amount':0.00999290073 ,'unit':'kg/L','Reference':None},
                    'LF_BOD_con2':{'Name':'BOD finish period 1','amount':0.09992900727 ,'unit':'kg/L','Reference':None},
                    'LF_BOD_con4':{'Name':'BOD finish period 2','amount':0.00999290073 ,'unit':'kg/L','Reference':None},
                    'LF_BOD_con6':{'Name':'BOD finish period 3','amount':0 ,'unit':'kg/L','Reference':None},
                    'LF_lcht_ec':{'Name':'electric energy consumption','amount':1.00107 ,'unit':'kWh / kg BOD removed','Reference':None},
                    'LF_sldg_per_BOD':{'Name':'sludge generated per BOD removed','amount':0.5 ,'unit':'kg sludge / kg BOD','Reference':None},
                    'LF_CO2_per_BOD':{'Name':'Mass CO2 (biomass) generated per mass BOD removed','amount':3.6 ,'unit':'kg CO2 / kg BOD ','Reference':None}
                }

### COD
        self.COD ={
                    'LF_COD2':{'Name':'Finish period 1','amount':1.5 ,'unit':'years','Reference':None},
                    'LF_COD4':{'Name':'Finish period 2','amount':10 ,'unit':'years','Reference':None},
                    'LF_COD6':{'Name':'Finish period 3','amount':50 ,'unit':'years','Reference':None},
                    'LF_COD_con1':{'Name':'COD start period 1','amount':0.012497117 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con3':{'Name':'COD start period 2','amount':0.012497117 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con5':{'Name':'COD start period 3','amount':0.000999769 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con7':{'Name':'COD start period 4','amount':9.99769E-05 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con2':{'Name':'COD finish period 1','amount':0.012497117 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con4':{'Name':'COD finish period 2','amount':0.003332165 ,'unit':'kg/L','Reference':None},
                    'LF_COD_con6':{'Name':'COD finish period 3','amount':9.99769E-05 ,'unit':'kg/L','Reference':None}
                }

### LEACHATE PUMPING
        self.lcht_pump = {
                        'leachAirPerLeach':{'Name':'Volume of free air required per volume of leachate pumped','amount':6 ,'unit':'STD L air/L leachate','Reference':None},
                        'leachCompPowReq':{'Name':'Compressor power requirements','amount':4 ,'unit':'cfm/hp','Reference':None},
                        'leachCompLoad':{'Name':'Compressor load percent','amount':75 ,'unit':'%','Reference':None},
                        'leachEff':{'Name':'Compressor motor efficiency','amount':90 ,'unit':'%','Reference':None}
                        }

### WASTE AND MATERIAL DENSITY
        self.density = {
                        'LF_d_msw':{'Name':'Compacted waste ','amount':890 ,'unit':'kg /m3','Reference':None},
                        'LF_d_soil':{'Name':'Soil and clay','amount':1840 ,'unit':'kg /m3','Reference':None},
                        'LF_d_HPDE':{'Name':'HDPE ','amount':954 ,'unit':'kg /m3','Reference':None},
                        'LF_d_revgen':{'Name':'Revenue generating cover','amount':1840 ,'unit':'kg /m3','Reference':None},
                        'LF_d_fuel':{'Name':'Diesel fuel ','amount':0.84 ,'unit':'kg/L','Reference':None},
                        'LF_d_gtx':{'Name':'Geotextiles','amount':94.50 ,'unit':'kg /m3','Reference':None},
                        'LF_d_sand':{'Name':'Sand','amount':1560 ,'unit':'kg /m3','Reference':None},
                        'LF_d_PVC':{'Name':'PVC','amount':1350 ,'unit':'kg /m3','Reference':None},
                        'LF_d_crt':{'Name':'Concrete','amount':2370 ,'unit':'kg /m3','Reference':None},
                        }

### Daily cover
        self.Daily_cover = {
                            'LF_p_HDPE1':{'Name':'Percent HDPE','amount':15 ,'unit':'%','Reference':None},
                            'LF_p_revgen':{'Name':'Percent revenue generating cover','amount':15 ,'unit':'%','Reference':None},
                            'LF_p_ncvr':{'Name':'Percent no daily cover','amount':0 ,'unit':'%','Reference':None},
                            'LF_p_cvr1':{'Name':'Percent volume used by daily cover','amount':10 ,'unit':'%','Reference':None},
                            'LF_t_HDPE':{'Name':'HDPE thickness ','amount':0.38 ,'unit':'mm','Reference':None},
                            'LF_a_HDPE':{'Name':'Area of HDPE ','amount':1000 ,'unit':'m2/ha','Reference':None},
                            'LF_fuel1':{'Name':'Total fuel use at a site with daily cover','amount':1.1679 ,'unit':'L/Mg','Reference':None},
                            'LF_fuel2':{'Name':'Fuel use at a site with no daily cover','amount':0.7925 ,'unit':'L/Mg','Reference':None},
                            'LF_hd1':{'Name':'HAUL DISTANCE_Fuel','amount':80 ,'unit':'km','Reference':None},
                            'LF_hd2':{'Name':'HAUL DISTANCE_Soil ','amount':16 ,'unit':'km','Reference':None},
                            'LF_hd3':{'Name':'HAUL DISTANCE_HDPE ','amount':400 ,'unit':'km','Reference':None},
                            'LF_er1':{'Name':'EMPTY RETURN_fuel','amount':1 ,'unit':None,'Reference':None},
                            'LF_er2':{'Name':'EMPTY RETURN_soil ','amount':1 ,'unit':None,'Reference':None},
                            'LF_er3':{'Name':'EMPTY RETURN_HDPE ','amount':1 ,'unit':None,'Reference':None},
                            'actpay_fuel':{'Name':'Actual payload of heavy duty fuel trucks','amount':35 ,'unit':'Mg','Reference':None},
                            'actpay_hdpe':{'Name':'Actual payload of heavy duty trucks hauling HDPE','amount':35 ,'unit':'Mg','Reference':None},
                            'actpay_soil':{'Name':'Actual payload of medium duty trucks hauling soil','amount':24 ,'unit':'Mg','Reference':None}
                            }

### Final cover _ Closure
        self.Final_cover = {
                            'LF_t_soil':{'Name':'Thickness of soil layer','amount':0.15 ,'unit':'m','Reference':None},
                            'LF_t_gtx':{'Name':'Thickness of geotextile layer','amount':1.5 ,'unit':'mm','Reference':None},
                            'LF_t_sand1':{'Name':'Thickness of first sand layer','amount':0.3 ,'unit':'m','Reference':None},
                            'LF_t_HDPE2':{'Name':'Thickness of HDPE layer','amount':1.5 ,'unit':'mm','Reference':None},
                            'LF_t_clay':{'Name':'Thickness of clay layer','amount':0.6 ,'unit':'m','Reference':None},
                            'LF_t_sand2':{'Name':'Thickness of second sand layer','amount':0 ,'unit':'m','Reference':None},
                            'LF_fuel8':{'Name':'FUEL USE DURING CLOSURE','amount':0.06673712 ,'unit':'L / Mg MSW','Reference':None},
                            'LF_hd5':{'Name':'Clay and soil','amount':8 ,'unit':'km','Reference':None},
                            'LF_hd6':{'Name':'Sand','amount':32 ,'unit':'km','Reference':None},
                            'LF_hd7':{'Name':'Geotextiles','amount':400 ,'unit':'km','Reference':None},
                            'LF_hd8':{'Name':'HDPE (Final Cover)','amount':400 ,'unit':'km','Reference':None},
                            'LF_hd9':{'Name':'HDPE (Non Final Cover)','amount':400 ,'unit':'km','Reference':None},
                            'LF_hd10':{'Name':'Fuel','amount':80 ,'unit':'km','Reference':None},
                            'LF_hd11':{'Name':'PVC','amount':400 ,'unit':'km','Reference':None},
                            'Heavy_er':{'Name':'Heavy duty truck empty return','amount':1 ,'unit':None,'Reference':None},
                            'Medium_er':{'Name':'Medium truck empty return','amount':1 ,'unit':None,'Reference':None},
                            'actpay_heavy':{'Name':'Heavy duty truck actual load','amount':35 ,'unit':'Mg','Reference':None},
                            'actpay_medium':{'Name':'Medium duty truck actual load','amount':24 ,'unit':'Mg','Reference':None}
                            }

### Gas Collection Pipe system
        self.Gas_Coll_pipe = {
                                'LF_gc_d_wells':{'Name':'Density of gas collection wells','amount':2.5 ,'unit':'wells/ha','Reference':None},
                                'LF_gc_d_HDPE':{'Name':'Linear density of HDPE pipe','amount':4.7 ,'unit':'kg/m','Reference':None},
                                'LF_gc_d_PVC':{'Name':'Linear density of PVC pipe','amount':3 ,'unit':'kg/m','Reference':None},
                                'LF_gc_l_wells':{'Name':'Average length of vertical wells','amount':13 ,'unit':'m','Reference':None},
                                'LF_gc_l_HDPE':{'Name':'Length of additional HDPE connection','amount':30 ,'unit':'m','Reference':None},
                                'LF_gc_HDPE':{'Name':'Amount HDPE','amount':0.008 ,'unit':'kg / Mg MSW','Reference':None},
                                'LF_gc_PVC':{'Name':'Amount PVC','amount':0.00405 ,'unit':'kg / Mg MSW','Reference':None}
                            }

### Post closure
        self.post_closure = {
                            'LF_n_pc':{'Name':'Post closure period','amount':30 ,'unit':'years','Reference':None},  
                            'LF_p_cvr':{'Name':'Percent of final cover replaced','amount':10 ,'unit':'%','Reference':None},  
                            'LF_fuel_12':{'Name':'Amount of fuel used per year for inspection','amount':0.00001668428 ,'unit':'L / year - Mg MSW','Reference':None},  
                            'LF_fuel_13':{'Name':'Amount of fuel used per year for mowing','amount':0.0000038373844 ,'unit':'L / year - Mg MSW','Reference':None},  
                            'Heavy_er':{'Name':'Heavy duty truck empty return','amount':1 ,'unit':None,'Reference':None},  
                            'Medium_er':{'Name':'Medium truck empty return','amount':1 ,'unit':None,'Reference':None},  
                            'actpay_heavy':{'Name':'Heavy duty truck actual load','amount':35 ,'unit':'Mg','Reference':None},
                            'actpay_medium':{'Name':'Medium duty truck actual load','amount':24 ,'unit':'Mg','Reference':None}
                            }             

        self.Input_list = {'Landfill Gas Parameters':self.LF_gas,'Oxidation Inputs':self.Ox ,'LFG combustion':self.LFG_Comb,
                           'Leachate':self.Leachate,'BOD':self.BOD,
                             'COD':self.COD,'LEACHATE PUMPING':self.lcht_pump,'WASTE AND MATERIAL DENSITY':self.density,
                             'Daily cover':self.Daily_cover,
                             'Final cover _ Closure':self.Final_cover,'Gas Collection Pipe system':self.Gas_Coll_pipe,
                             'Post closure':self.post_closure}

'''            
                        '':{'Name':'','amount': ,'unit':'','Reference':None},                    
'''


A= LF_input()
category=[]
Parameter=[]
Name=[]
amount=[]
unit=[]

for x in A.Input_list.keys():
    for y in  A.Input_list[x].keys():
        category.append(x)
        Parameter.append(y)
        Name.append(A.Input_list[x][y]['Name'])
        amount.append(A.Input_list[x][y]['amount'])
        unit.append(A.Input_list[x][y]['unit'])
AAA={'category':category,'Parameter':Parameter,'Name':Name,'amount':amount,'unit':unit}



    














