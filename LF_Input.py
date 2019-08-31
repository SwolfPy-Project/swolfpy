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
                'initColEff':{'Name':'Initial gas collection efficiency','amount':50 ,'unit':'50','Reference':None},
                'cellFillTime':{'Name':'Cell fill time','amount':5 ,'unit':'years','Reference':None},  
                'intColEff':{'Name':'Gas collection efficiency under intermediate cover','amount':75 ,'unit':'%','Reference':None},  
                'incColTime':{'Name':'Time to increased gas collection efficiency','amount':15 ,'unit':'years','Reference':None},  
                'incColEff':{'Name':'Increased gas collection efficiency','amount':82.5 ,'unit':'%','Reference':None},  
                'timeToFinCover':{'Name':'Time from final waste placement to final cover','amount':1 ,'unit':'years','Reference':None},  
                'finColEff':{'Name':'Gas collection efficiency under final cover','amount':90 ,'unit':'%','Reference':None},  
                'enrgOn':{'Name':'Energy recovery cuton time','amount':5 ,'unit':'years','Reference':None},
                'enrgOff1':{'Name':'Energy recovery cutoff time','amount':52 ,'unit':'years','Reference':None},
                'flareOff':{'Name':'Flare cutoff time','amount':50 ,'unit':'Years','Reference':None},
                'enrgRecovered':{'Name':'Recover energy ','amount':True ,'unit':None,'Reference':None},
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
              
        
'''        
        
                        '':{'Name':'','amount': ,'unit':'','Reference':None},   
                        
'''