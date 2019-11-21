# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
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



Treatment_processes = {}
Treatment_processes['AD']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':20},'model': AD()}
Treatment_processes['COMP']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':20}, 'model': Comp()}
Treatment_processes['LF']={'input_type':['RWC','LV','DryRes','WetRes','MRDO','MSRDO','Bottom_Ash','Fly_Ash','Other_Residual'],'distance':{'SF1':20},'model': LF() }
Treatment_processes['WTE']={'input_type':['RWC','DryRes','WetRes','MRDO','Other_Residual'],'distance':{'SF1':20},'model': WTE()}


Collection_scheme_SF1 = {'RWC':{'Contribution':0.2 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0.5,
                                            'SSYWDO':0.5}},
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

Collection_processes = {}
Collection_processes['SF1']={'input_type':[],'model': SF_Col(Collection_scheme_SF1,Treatment_processes=Treatment_processes,name='SF1')}


Project_name = "demo_collection_full"
demo = project(Project_name,Treatment_processes,Collection_processes)
demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
demo.write_project()
demo.group_exchanges()
import_methods()

flow_fractions = [{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 1},
             {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0},
             {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 1},
             {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0},
             {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount':1},
             {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
             {'name': 'frac_of_RWC_from_SF1_to_LF', 'amount': 0.5},
             {'name': 'frac_of_RWC_from_SF1_to_WTE', 'amount': 0.5},
             {'name': 'frac_of_MSRDO_from_SF1_to_LF', 'amount': 1},
             {'name': 'frac_of_LV_from_SF1_to_AD', 'amount': 0.5},
             {'name': 'frac_of_LV_from_SF1_to_COMP', 'amount': 0.5},
             {'name': 'frac_of_LV_from_SF1_to_LF', 'amount': 0},
             {'name': 'frac_of_SSYW_from_SF1_to_AD', 'amount': 0.5},
             {'name': 'frac_of_SSYW_from_SF1_to_COMP', 'amount': 0.5},
             {'name': 'frac_of_SSYWDO_from_SF1_to_AD', 'amount': 1},
             {'name': 'frac_of_SSYWDO_from_SF1_to_COMP', 'amount': 0},
             {'name': 'frac_of_SSO_from_SF1_to_AD', 'amount': 1},
             {'name': 'frac_of_SSO_from_SF1_to_COMP', 'amount': 0},
             {'name': 'frac_of_DryRes_from_SF1_to_LF', 'amount': 1},
             {'name': 'frac_of_DryRes_from_SF1_to_WTE', 'amount': 0},
             {'name': 'frac_of_WetRes_from_SF1_to_LF', 'amount': 1},
             {'name': 'frac_of_WetRes_from_SF1_to_WTE', 'amount': 0},
             {'name': 'frac_of_MRDO_from_SF1_to_LF', 'amount': 0.5},
             {'name': 'frac_of_MRDO_from_SF1_to_WTE', 'amount': 0.5}]

demo.update_parameters(flow_fractions)

scenario1 = {"SF1":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario1,'scenario1')
demo.Do_LCA("scenario1",('SWOLF_IPCC','SWOLF'),1)



functional_unit = {("waste","scenario1") : 1}
method = [('SWOLF_IPCC','SWOLF')]

from time import time
B= time()
from building_matrices import *
opt = ParallelData (functional_unit, method, Project_name)
res=opt.optimize_parameters(demo)
print(opt.objective_function(res['x']))
print(res)
print('Time for optimizing the flows: ', (time()-B))


x={}
for i in range(len(flow_fractions)):
    x[flow_fractions[i]['name']]=res[i]

    

scenario2 = {"AD":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario2,'scenario2')
demo.Do_LCA("scenario2",('SWOLF_IPCC','SWOLF'),1)

scenario3 = {"COMP":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario3,'scenario3')
demo.Do_LCA("scenario3",('SWOLF_IPCC','SWOLF'),1)  
    





     
        
        
    





