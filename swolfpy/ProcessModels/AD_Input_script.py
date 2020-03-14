# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:37:44 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from ..MC import *
class AD_input(MC):
    def __init__(self,input_data_path=None):
        if input_data_path:
            raise ValueError('Wrong input file, you cannot use input_data_path with input_script')

### Assumed Composition 
        self.Assumed_Comp = [0.1587847314,0.1199794853,0.1172076820,0.3296762444,0.0824190611,0.0065468408,0.0000264482,
                             0.0058447349,0.0006849813,0.0065073226,0.0191333727,0.0034644248,0.0010472311,0.0028584798,
                             0.0036027383,0.0027399253,0.0000264482,0.0385170270,0.0021076349,0.0038200882,0.0070342313,
                             0.0000264482,0.0000264482,0.0000264482,0.0103537562,0.0295859243,0.0015148626,0.0002897998,
                             0.0009484357,0.0012118900,0.0000264482,0.0000264482,0.0001317272,0.0143846079,0.0061648320,
                             0.0041098880,0.0000264482,0.0000264482,0.0000264482,0.0190635573,0.0,0.0,0.0,0.0,0.0,0.0,
                             0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]       


### Land application inputs
        self.Land_app = {
                'distLand':{"Name":"Distance to application site","amount":20,"unit":'km',"Reference":None},
                'erLand':{"Name":"Empty return from land application (0=no; 1=yes)","amount":1,"unit":'0/1',"Reference":None},
                'land_payload':{"Name":"Actual payload of truck used to haul soil amendment","amount":7.3,"unit":'Mg',"Reference":None},
                'ad_PeatSubFac':{"Name":"Volumetric peat replacement factor","amount":1,"unit":None,"Reference":'17'},
                'ad_densPeat':{"Name":"Density of peat","amount":200,"unit":'kg/m3',"Reference":'17'},
                'perN2Oevap':{"Name":"Percent of applied N evaporated as N2O","amount":1.5,"unit":'%',"Reference":'16'},
                'perNH3evap':{"Name":"Percent of Ammonia that evaporates","amount":15,"unit":'%',"Reference":'16'},
                'perNasNH3fc':{"Name":"Percent N that is Ammonia","amount":50,"unit":'%',"Reference":'16'},
                }

### Curing Biological Degradation
        self.Curing_Bio = {
                'ad_pCasCH4':{'Name':'Proportion of emitted C emitted as CH4','amount':0.017,'unit':None,'Referenc':'19'},
                'ad_pNasNH3':{'Name':'Proportion of emitted N emitted as NH3','amount':0.04,'unit':None,'Referenc':'26'},
                'ad_pNasN2O':{'Name':'Proportion of emitted N emitted as N2O','amount':0.004,'unit':None,'Referenc':'19'},
                'dmRed_Dig':{'Name':'VS reduction of digestate during curing','amount':0.3,'unit':None,'Referenc':'29'},
                'VSlossPerCloss':{'Name':'Mass of VS loss per mole of C loss','amount':12,'unit':'g/mol C','Referenc':None},
                }

### Curing Windrow Turning
        self.Windrow_turn = {
                'Tcur':{'Name':'Retention time in windrows','amount':21 ,'unit':'days','Referenc':None},
                'Mwta':{'Name':'Turning energy required per ton of compost','amount':0.24 ,'unit':'kWh/Mg','Referenc':None},
                'Mwfa':{'Name':'The fuel consumption of a windrow turner','amount':0.13 ,'unit':'L/kWh','Referenc':None},
                'turnFreq':{'Name':'Turning frequency','amount':0.43 ,'unit':'1/days','Referenc':None}
                }
        
        
### Facility Operation
        self.AD_operation = {
                'ad_lifetime':{'Name':'Facility economic lifetime','amount':20,'unit':'years','Referenc':None},
                'ophrsperday':{'Name':'Daily operating hours','amount':8,'unit':'hours','Referenc':None},
                'opdaysperyear':{'Name':'Annual operating days','amount':260,'unit':'days','Referenc':None},
                'retentionTime':{'Name':'Average retention time in reactor','amount':21,'unit':'days','Referenc':None},
                'recircMax':{'Name':'Maximum proportion of reactor water that can come from recirculation','amount':0.8,'unit':'fraction','Referenc':None},
                'isDw':{'Name':'Dewater digestate? (0=no; 1=yes)','amount':1,'unit':'0/1','Referenc':None},
                'isCured':{'Name':'Cure digestate solids stream? (0=no; 1=yes)','amount':1,'unit':'0/1','Referenc':None},
                'choice_BU':{'Name':'Digestate Beneficial Use (1) or No Beneficial Use (0)','amount':1,'unit':'0/1','Referenc':None},
                'peatOff':{'Name':'Digestate Beneficial Use offsets Peat (1 - Yes; 0 - No)','amount':1,'unit':'0/1','Referenc':None},
                'fertOff':{'Name':'Digestate Beneficial Use offsets Fertilizer (1 - Yes; 0 - No)','amount':1,'unit':'0/1','Referenc':None},
                }
### Biogas Generation and Use
        self.Biogas_gen = {
                'ad_ch4prop':{'Name':'Proportion of methane in collected biogas','amount':0.6,'unit':None,'Referenc':'28'},
                'ad_ch4stoich':{'Name':'Stoichiometric proportion of methane in produced biogas due to feedstock','amount':0.6,'unit':None,'Referenc':None},
                'ad_ch4EngCont':{'Name':'Methane energy content','amount':37.7,'unit':'MJ/m3','Referenc':None},
                'perLeak':{'Name':'Methane leakage','amount':3,'unit':'%','Referenc':'28'},
                'perSolDec':{'Name':'Percent of biogas mass from solid decomposition','amount':89,'unit':'%','Referenc':None,'Comment':'Average of cellulose (90%) and hemicellulose (88%)'},
                'ad_HeatRate':{'Name':'Heat rate for electrical energy generation','amount':9.86,'unit':'MJ/kWh','Referenc':'24'},
                'ad_collEff':{'Name':'Collection efficiency of biogas as proportion (0 to 1)','amount':0.97,'unit':None,'Referenc':None},
                'ad_downTime':{'Name':'Proportion of gas that is flared w/out electricity generation (0 to 1)','amount':0.03,'unit':None,'Referenc':None},
                }

### Biogas Combustion Emissions Factors
        self.emission_Flare = {  
                        'CH4_destruction':{'Name':'Methane destruction efficiency (0-1)','amount':0.999,'unit':None,'Referenc':None},
                        'CO':{'Name':'Carbon monoxide (CO)','amount':2.4,'unit':'g/GJ CH4 input','Referenc':None},
                        'NO2':{'Name':'Nitrogen oxides (as NO2)','amount':19.7,'unit':'g/GJ CH4 input','Referenc':None},
                        'SO2':{'Name':'Sulfur dioxide (SO2)','amount':23.3,'unit':'g/GJ CH4 input','Referenc':None},
                        'NMVOC':{'Name':'NMVOCs','amount':0,'unit':'g/GJ CH4 input','Referenc':None},
                        'PM':{'Name':'PM2.5','amount':36.9,'unit':'g/GJ CH4 input','Referenc':None},
                        }
        self.emission_Engine = {  
                        'CH4_destruction':{'Name':'Methane destruction efficiency (0-1)','amount':0.99,'unit':None,'Referenc':None},
                        'CO':{'Name':'Carbon monoxide (CO)','amount':273,'unit':'g/GJ CH4 input','Referenc':None},
                        'NO2':{'Name':'Nitrogen oxides (as NO2)','amount':540,'unit':'g/GJ CH4 input','Referenc':None},
                        'SO2':{'Name':'Sulfur dioxide (SO2)','amount':19.2,'unit':'g/GJ CH4 input','Referenc':None},
                        'NMVOC':{'Name':'NMVOCs','amount':105,'unit':'g/GJ CH4 input','Referenc':None},
                        'PM':{'Name':'PM2.5','amount':0.206,'unit':'g/GJ CH4 input','Referenc':None},
                            }

### Digestate Liquids Treatment
        self.Digestate_treatment = {
                'ad_distPOTW':{'Name':'Haul distance to treatment facility','amount':25 ,'unit':'km','Referenc':'15'},
                'ad_erPOTW':{'Name':'Empty return from treatment facility (1-Yes, 0-No)','amount':1 ,'unit':'0/1','Referenc':'15'},
                'payload_POTW':{'Name':'Actual payload of truck to treatment facility','amount':23 ,'unit':'Mg','Referenc':None},
                'er_wwtpLF':{'Name':'Empty return from LF to WWTP (1-Yes, 0-No)','amount':1 ,'unit':'0/1','Referenc':None},
                'payload_LFPOTW':{'Name':'Actual payload of truck to LF from WWTP','amount':23 ,'unit':'Mg','Referenc':None},
                'lchBODcont':{'Name':'BOD','amount':2.3 ,'unit':'kg/m3','Referenc':'28'},
                'lchCODcont':{'Name':'COD','amount':61.610 ,'unit':'kg/m3','Referenc':'31'},
                'lchTSScont':{'Name':'Total suspended solids','amount':1.450 ,'unit':'kg/m3','Referenc':'28'},
                'conc_totN':{'Name':'Total N','amount':1.350 ,'unit':'kg/m3','Referenc':'28'},
                'conc_Fe':{'Name':'Iron','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Cu':{'Name':'Copper','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Cd':{'Name':'Cadmium','amount':0.00003 ,'unit':'kg/m3','Referenc':39},
                'conc_As':{'Name':'Arsenic','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Hg':{'Name':'Mercury','amount':0.000026 ,'unit':'kg/m3','Referenc':39},
                'conc_P':{'Name':'Phosphate','amount':0.06 ,'unit':'kg/m3','Referenc':39},
                'conc_Se':{'Name':'Selenium','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Cr':{'Name':'Chromium','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Pb':{'Name':'Lead','amount':0.00261 ,'unit':'kg/m3','Referenc':39},
                'conc_Zn':{'Name':'Zinc','amount':0.0108 ,'unit':'kg/m3','Referenc':39},
                'conc_Ba':{'Name':'Barium','amount':0 ,'unit':'kg/m3','Referenc':None},
                'conc_Ag':{'Name':'Silver','amount':0 ,'unit':'kg/m3','Referenc':None},
                'wwtp_lf_dist':{'Name':'Distance from WWTP to landfill','amount':25 ,'unit':'km','Referenc':None}
                }
### Screening
        self.Post_Screen ={
                'ad_engScreen':{"Name":"Post-screen specific electricity consumption","amount":0.000882,"unit":'kWh/kg',"Reference":7},
                'ad_scrEff_WC':{"Name":"Proportion of wood chips remaining after post-screening","amount":0.75,"unit":'fraction',"Reference":None}
                }

### Material Properties
        self.Material_Properties ={
            'ad_mcReactor':{'Name':'Reactor moisture content','amount':0.92 ,'unit':'mass water/total mass','Referenc':20},
            'ad_mcFC':{'Name':'Finished compost moisture content','amount':0.45 ,'unit':'mass water/total mass','Referenc':None},
            'ad_densFC':{'Name':'Density of final compost','amount':700 ,'unit':'kg/m3','Referenc':2},
            'wcMC':{'Name':'Wood chip moisture content','amount':0.1586 ,'unit':'%','Referenc':None},
            'wcVSC':{'Name':'Wood chip VS content','amount':0.906 ,'unit':'%TS','Referenc':None}
            }
        
### Dewatering Parameters
        self.Dewater ={
            'elec_dw':{'Name':'Electricity Use','amount':75 ,'unit':'kWh/Mg TS throughput','Referenc':None},
            'ad_mcDigestate':{'Name':'Moisture Content of Solids Stream After Dewatering','amount':0.76 ,'unit':'mass water/total mass','Referenc':None}
            }

### Digestate Properties 
        self.Dig_prop = {
                'mcInitComp':{'Name':'Composting beginning moisture content (used to calculate wood chip requirements)','amount': 0.6,'unit':'mass water/total mass','Referenc':None},
                'digliqdens':{'Name':'Digestate Liquids Density','amount':1 ,'unit':'kg/L','Referenc':None},
                'perNSolid':{'Name':'Percent N to solids','amount':96 ,'unit':'%','Referenc':None},
                'perPSolid':{'Name':'Percent P to solids','amount':98.7 ,'unit':'%','Referenc':None},
                'perKSolid':{'Name':'Percent K to solids','amount':98.7 ,'unit':'%','Referenc':None}
                }

### Facility Energy Use
        self.Fac_Energy = {
        'Dsl_facility':{'Name':'Diesel fuel used by anaerobic digestion facility (not curing)','amount':0.3 ,'unit':'L/Mg','Referenc':28},
        'elec_preproc':{'Name':'Pre-processing Electricity Use','amount':9 ,'unit':'kWh/Mg','Referenc':28},
        'elec_facility':{'Name':'AD facility electricity use (excluding pre-process, dewatering, and curing)','amount':49 ,'unit':'kWh/Mg','Referenc':28}
                }  

### Front End Loader
        self.Loader = {
                'hpFEL':{"Name":"Front end loader use per facility capacity.","amount":0.168 ,"unit":'kW/Mgd',"Reference":'5'},
                'mfFEL':{"Name":"Front end loader specific fuel consumption.","amount":0.26 ,"unit":'L/kWh',"Reference":'6'}
                }

### Wood Chip Shredding
        self.shredding ={
                'Mtgp':{"Name":"Grinder power rating.","amount":10.6,"unit":'kWh/Mg',"Reference":'9'},
                'Mtgf':{"Name":"Grinder fuel consumption","amount":0.25,"unit":'L/kWh',"Reference":'9'}
                }

### Soil Sequestration
        self.Soil_seq ={
                'perCStor':{"Name":"Percent of carbon in finished compost remaining after 100 years","amount":10,"unit":'%',"Reference":'3'},
                'percCStor_LF':{"Name":"Percent of carbon in compost remaining after 100 years","amount":100,"unit":'%',"Reference":None},
                'humFormFac':{"Name":"100 year carbon storage from humus formation","amount":0,"unit":'kg-C/kg-C in compost',"Reference":'4'}
                }        
        
### Monte_carlo          
    def setup_MC(self,seed=None):
        self.Input_list = {'Land_app':self.Land_app,'Curing_Bio':self.Curing_Bio,'Windrow_turn':self.Windrow_turn,'AD_operation':self.AD_operation,'Biogas_gen':self.Biogas_gen,
                          'emission_Flare':self.emission_Flare, 'emission_Engine':self.emission_Engine,
                          'Digestate_treatment':self.Digestate_treatment,'Post_Screen':self.Post_Screen,'Material_Properties':self.Material_Properties,'Dewater':self.Dewater,
                          'Dig_prop':self.Dig_prop,'Fac_Energy':self.Fac_Energy, 'Loader':self.Loader,'shredding':self.shredding,'Soil_seq':self.Soil_seq}
        super().__init__(self.Input_list)
        super().setup_MC(seed)



#################################################################
#### Convering the input dictionaries to csv file
#################
# =============================================================================
# A= AD_input()
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

