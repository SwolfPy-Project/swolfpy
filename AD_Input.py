# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:37:44 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from stats_arrays import *
class AD_input:
    def __init__(self):
        pass

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
        
### Facility Operation
        self.AD_operation = {
                'ad_lifetime':{'Name':'Facility economic lifetime','amount':20,'unit':'years','Referenc':None},
                'ophrsperday':{'Name':'Daily operating hours','amount':8,'unit':'hours','Referenc':None},
                'opdaysperyear':{'Name':'Annual operating days','amount':260,'unit':'days','Referenc':None},
                'retentionTime':{'Name':'Average retention time in reactor','amount':21,'unit':'days','Referenc':None},
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
        self.emission_factor = {
             'Flare': {   
                        'CH4_destruction':{'Name':'Methane destruction efficiency (0-1)','amount':0.999,'unit':None,'Referenc':None},
                        'CO':{'Name':'Carbon monoxide (CO)','amount':2.4,'unit':'g/GJ CH4 input','Referenc':None},
                        'NO2':{'Name':'Nitrogen oxides (as NO2)','amount':19.7,'unit':'g/GJ CH4 input','Referenc':None},
                        'SO2':{'Name':'Sulfur dioxide (SO2)','amount':23.3,'unit':'g/GJ CH4 input','Referenc':None},
                        'NMVOC':{'Name':'NMVOCs','amount':0,'unit':'g/GJ CH4 input','Referenc':None},
                        'PM':{'Name':'PM2.5','amount':36.9,'unit':'g/GJ CH4 input','Referenc':None},
                    },
             'Engine': {   
                        'CH4_destruction':{'Name':'Methane destruction efficiency (0-1)','amount':0.99,'unit':None,'Referenc':None},
                        'CO':{'Name':'Carbon monoxide (CO)','amount':273,'unit':'g/GJ CH4 input','Referenc':None},
                        'NO2':{'Name':'Nitrogen oxides (as NO2)','amount':540,'unit':'g/GJ CH4 input','Referenc':None},
                        'SO2':{'Name':'Sulfur dioxide (SO2)','amount':19.2,'unit':'g/GJ CH4 input','Referenc':None},
                        'NMVOC':{'Name':'NMVOCs','amount':105,'unit':'g/GJ CH4 input','Referenc':None},
                        'PM':{'Name':'PM2.5','amount':0.206,'unit':'g/GJ CH4 input','Referenc':None},
                    } }

### Digestate Liquids Treatment
        self.Digestate_treatment = {
                'ad_distPOTW':{'Name':'Haul distance to treatment facility','amount':25 ,'unit':'km','Referenc':'15'},
                'ad_erPOTW':{'Name':'Empty return from treatment facility (1-Yes, 0-No)','amount':1 ,'unit':'0/1','Referenc':'15'},
                'payload_POTW':{'Name':'Actual payload of truck to treatment facility','amount':23 ,'unit':'Mg','Referenc':None},
                'er_wwtpLF':{'Name':'Empty return from LF to WWTP (1-Yes, 0-No)','amount':1 ,'unit':'0/1','Referenc':None},
                'payload_LFPOTW':{'Name':'Actual payload of truck to LF from WWTP','amount':23 ,'unit':'Mg','Referenc':None},
                'lchBODcont':{'Name':'BOD','amount':2300 ,'unit':'mg/L','Referenc':'28'},
                'lchCODcont':{'Name':'COD','amount':61610 ,'unit':'mg/L','Referenc':'31'},
                'lchTSScont':{'Name':'Total suspended solids','amount':1450 ,'unit':'mg/L','Referenc':'28'},
                'conc_totN':{'Name':'Total N','amount':1350 ,'unit':'mg/L','Referenc':'28'},
                'wwtp_lf_dist':{'Name':'Distance from WWTP to landfill','amount':25 ,'unit':'km','Referenc':None}
                }
             
"""        
        {
'':{'Name':'','amount': ,'unit':'','Referenc':None},
'':{'Name':'','amount': ,'unit':'','Referenc':None},
'':{'Name':'','amount': ,'unit':'','Referenc':None},
'':{'Name':'','amount': ,'unit':'','Referenc':None},
'':{'Name':'','amount': ,'unit':'','Referenc':None},
'':{'Name':'','amount': ,'unit':'','Referenc':None},
                }
        
"""