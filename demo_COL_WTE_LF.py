from project_class import *
from WTE import *
from LF import *
from SF_collection_1 import *
from brightway2 import *
from CommonData import *
from time import time
import pickle
from SWOLF_method import *

Treatment_processes = {}

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


project_name = "demo_COL_WTE_LF"
method = [('SWOLF_IPCC','SWOLF')]
demo = project(project_name,Treatment_processes,Collection_processes)
demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
demo.write_project()
demo.group_exchanges()
import_methods()

flow_fractions=[{'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_RWC_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_RWC_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_MSRDO_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_LV_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_DryRes_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_DryRes_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_WetRes_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_WetRes_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_MRDO_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_MRDO_from_SF1_to_WTE', 'amount': 1}]
 
demo.update_parameters(flow_fractions)

scenario1 = {"SF1":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario1,'scenario1')
demo.Do_LCA("scenario1",method[0],1)



functional_unit = {("waste","scenario1") : 1}


from time import time
B= time()
from building_matrices import *
opt = ParallelData (functional_unit, method, project_name)
res=opt.optimize_parameters(demo, {'WTE':500}, {'77357947-ccc5-438e-9996-95e65e1e1bce':-100}) #'Nitrogen oxides' (kilogram, None, ('air', 'non-urban air or from high stacks')).
print(res)
print('Time for optimizing the flows: ', (time()-B))

opt.set_optimized_parameters_to_project()
demo.Do_LCA("scenario1",method[0],1)


