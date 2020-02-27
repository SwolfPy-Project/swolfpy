from project_class import *
from WTE import *
from LF import *
from SF_collection import *
from Distance import *
from brightway2 import *
from CommonData import *
from time import time
import pickle
from SWOLF_method import *

Treatment_processes = {}

Treatment_processes['LF']={'input_type':['RWC','LV','DryRes','WetRes','MRDO','MSRDO','Bottom_Ash','Fly_Ash','Other_Residual'],'model': LF() }
Treatment_processes['WTE']={'input_type':['RWC','DryRes','WetRes','MRDO','Other_Residual'],'model': WTE()}
Treatment_processes['WTE1']={'input_type':['RWC','DryRes','WetRes','MRDO','Other_Residual'],'model': WTE()}

Collection_scheme_SF1 = {'RWC':{'Contribution':1 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},
                    'SSO_DryRes':{'Contribution':0 , 
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
                    'MRDO':{'Contribution':0, 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}}}

distance = Distance(path='Distance.csv')

Collection_processes = {}
Collection_processes['SF1']={'input_type':[],'model': SF_Col('SF1',Collection_scheme_SF1,Treatment_processes=Treatment_processes,Distance=distance)}


project_name = "demo_COL_WTE_LF"
method = [('SWOLF_IPCC','SWOLF')]
demo = project(project_name,Treatment_processes,distance,Collection_processes)
demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
demo.write_project()
demo.group_exchanges()
import_methods()

flow_fractions=[{'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_RWC_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_RWC_from_SF1_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_RWC_from_SF1_to_WTE1', 'amount': 0.5},
 {'name': 'frac_of_MSRDO_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_LV_from_SF1_to_LF', 'amount': 1},
 {'name': 'frac_of_DryRes_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_DryRes_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_DryRes_from_SF1_to_WTE1', 'amount': 0},
 {'name': 'frac_of_WetRes_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_WetRes_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_WetRes_from_SF1_to_WTE1', 'amount': 0},
 {'name': 'frac_of_MRDO_from_SF1_to_LF', 'amount': 0},
 {'name': 'frac_of_MRDO_from_SF1_to_WTE', 'amount': 1},
 {'name': 'frac_of_MRDO_from_SF1_to_WTE1', 'amount': 0}]

 
demo.update_parameters(flow_fractions)

scenario2 = {"SF1":{"Yard_Trimmings_Branches":1}}
demo.process_start_scenario(scenario2,'scenario2')
demo.Do_LCA("scenario2",method[0],1)



functional_unit = {("waste","scenario2") : 1}

constraints = {'LF':{'limit':500, 'KeyType':'WasteToProcess','ConstType':'<='},
                'WTE1':{'limit':200, 'KeyType':'WasteToProcess','ConstType':'<='},
               'WTE':{'limit':10, 'KeyType':'Process','ConstType':'>='}
               }


constraints = {'LF':{'limit':600, 'KeyType':'Process','ConstType':'<='},
               'WTE':{'limit':200, 'KeyType':'Process','ConstType':'>='},
               'WTE1':{'limit':700, 'KeyType':'Process','ConstType':'>='}}



from time import time
B= time()
from building_matrices import *
opt = ParallelData(functional_unit, method, project_name)
#res=opt.optimize_parameters(demo)
#res=opt.optimize_parameters(demo,constraints)
res=opt.multi_start_optimization(demo, constraints=constraints, max_iter=30)
print(res)
print('Time for optimizing the flows: ', (time()-B))


x= res.x
for i in range(len(opt.cons)):
    print(opt.cons[i]['fun'](x))


opt.set_optimized_parameters_to_project()


lca = LCA({("waste","scenario2") : 1})
lca.lci()
A,B,C=lca.reverse_dict()
mass={'LF':0,'WTE':0,'WTE1':0}
for i in range(len(lca.supply_array)):
    if A[i][0] == 'LF':
        mass['LF']+=lca.supply_array[i]
    elif A[i][0] == 'WTE':
        mass['WTE']+=lca.supply_array[i]
    elif A[i][0] == 'WTE1':
        mass['WTE1']+=lca.supply_array[i]
print(mass)


    

demo.Do_LCA("scenario1",method[0],1)


