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
from brightway2 import *
from CommonData import *
from time import time
import pickle
from SWOLF_method import *

if __name__=='__main__':
    
    Treatment_processes = {}
    Treatment_processes['LF']={'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual'], 'model':LF()}
    
    Project_name = "Demo_LF"
    demo = project(Project_name,Treatment_processes)
    demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
    demo.write_project()
    demo.group_exchanges()
    import_methods()
        
    #demo.update_parameters()
    scenario1 = {"LF":{"Wood":1}}
    demo.process_start_scenario(scenario1,'scenario1')
    
    
    demo.Do_LCA("scenario1",('SWOLF_IPCC','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_Acidification','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_Eutrophication','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_PhotochemicalSmog','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_HumanToxicity','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_Ecotoxicity','SWOLF'),1)
    demo.Do_LCA("scenario1",('SWOLF_CED','SWOLF'),1)

    
    
    
    project = "Demo_LF"
    projects.set_current(project)
    db = Database("waste")
    functional_unit = {db.get("scenario1") : 1}
    method = [('SWOLF_IPCC','SWOLF')]
    
    process_models = list()
    process_model_names = list()
        
    CommonData= CommonData()

    process_models.append(Treatment_processes['LF']['model'])
    process_model_names.append('LF')

    
    t1 = time()
    n=100
    a = ParallelData(functional_unit, method, project,process_models=process_models,process_model_names=process_model_names,common_data=CommonData,seed = 1)    
    a.run(4,n)
    t2=time()
    print(n, 'runs in: ', t2-t1)

### save results as Dataframe and pickle   
    AA=a.result_to_DF()
	
    demo.save(Project_name)	#saving project in a picle dump
	
### reloading file from pickle dump
    load=pickle.load(open(Project_name, "rb"))

    












     
        
        
    





