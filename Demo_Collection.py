# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
from building_matrices import *
from AD import *
from Composting import *
from WTE import *
from LF import *
from SF_collection_1 import *
from brightway2 import *
from CommonData import *
from time import time
import pickle
from SWOLF_method import *



Collection_scheme = {'RWC':{'Contribution':0.2 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},
                    'SSO_DryRes':{'Contribution':0.2 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},
                    'REC_WetRes':{'Contribution':0 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},                
                    'MRDO':{'Contribution':0.6, 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}}}

Treatment_processes = {}
Treatment_processes['AD']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':20},'model': AD()}
Treatment_processes['COMP']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':100}, 'model': Comp()}
Treatment_processes['LF']={'input_type':['RWC','LV','DryRes','WetRes','MRDO','MSRDO','Bottom_Ash','Fly_Ash','Other_Residual'],'distance':{'SF1':20},'model': LF() }

Distance_SF1 = {'Res':{'LF':20},
             'Rec':{'LF':20},
             'Organics':{'AD':20,'COMP':20}}

Collection_processes = {}
Collection_processes['SF1']={'input_type':[],'model': SF_Col(Collection_scheme,Distance_SF1,Treatment_processes=Treatment_processes,name='SF1')}

for j in Collection_processes.keys():
    Treatment_processes[j] = Collection_processes[j]
    



Project_name = "demo_collection"
demo = project(Project_name,Treatment_processes)
demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
demo.write_project()
demo.group_exchanges()
import_methods()

gg=[{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 1},
 {'name': 'frac_of_RWC_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_MSRDO_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_LV_from_SF1_to_AD', 'amount': 1},
 {'name': 'frac_of_LV_from_SF1_to_COMP', 'amount': 0},
 {'name': 'frac_of_LV_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_SSYW_from_SF1_to_AD', 'amount': 1},
 {'name': 'frac_of_SSYW_from_SF1_to_COMP', 'amount': 0},
 {'name': 'frac_of_SSYWDO_from_SF1_to_AD', 'amount': 1},
 {'name': 'frac_of_SSYWDO_from_SF1_to_COMP', 'amount': 0},
 {'name': 'frac_of_SSO_from_SF1_to_AD', 'amount': 1},
 {'name': 'frac_of_SSO_from_SF1_to_COMP', 'amount': 0},
 {'name': 'frac_of_DryRes_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_WetRes_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_MRDO_from_SF1_to_LF', 'amount': 1}]

demo.update_parameters(gg)

scenario4 = {"SF1":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario4,'scenario4')
demo.Do_LCA("scenario4",('SWOLF_IPCC','SWOLF'),1)


        





     
        
        
    





