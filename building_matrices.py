from brightway2 import *
import numpy as np
from Required_keys import *
import multiprocessing as mp
import sys
from multiprocessing import Queue
from multiprocessing import Pool
from brightway2 import LCA
from bw2data import projects
import os
import pandas as pd
from scipy.optimize import minimize, rosen, rosen_der
from random import random

    
if sys.version_info < (3, 0):
    # multiprocessing.pool as a context manager not available in Python 2.7
    @contextmanager
    def pool_adapter(pool):
        try:
            yield pool
        finally:
            pool.terminate()
else:
    pool_adapter = lambda x: x


def worker(args):
    project, functional_unit, method, parameters, process_models, process_model_names, common_data, tech_matrix, bio_matrix, seed , n = args
    projects.set_current(project, writable=False)
    if common_data:
        common_data.setup_MC(seed)
    if process_models:
        for x in process_models:
            x.setup_MC(seed)
    if parameters:
        parameters.setup_MC(seed)
    lca = LCA(functional_unit, method[0])
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models=process_models, process_model_names=process_model_names, parameters=parameters, common_data=common_data, index =x) for x in range(n)]


def parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models = None, process_model_names = None, parameters = None, common_data = None, index =None):
    uncertain_inputs = list()
    
    if process_models:
        if common_data:
            uncertain_inputs += common_data.gen_MC()
            for process in process_models:
                process.CommonData = common_data
                uncertain_inputs += process.MC_calc()
        else:    
            for process in process_models:
                uncertain_inputs += process.MC_calc()
        
        i = 0
        for process_name in process_model_names:
            report_dict = process_models[i].report()
    
            for material,value in report_dict["Technosphere"].items():
                for key2, value2 in value.items():
                    if not np.isnan(value2):
                        if ((key2),(process_name, material)) in tech_matrix.keys():
                            if tech_matrix[((key2),(process_name, material))] != value2:
                                tech_matrix[((key2),(process_name, material))] = value2 
                        else:
                            print('**Warning** Exchange {} is calculated but not exist in LCA technosphere'.format(((key2),(process_name, material))))
                                
                            
            for material,value in report_dict["Waste"].items():
                for key2, value2 in value.items():
                    if key2 in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual',
                     'RDF','Al','Fe','Cu','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
                        key2 = (process_name + "_product", material + '_' + key2)
                    else:
                        key2 = (process_name + "_product", key2)
                    if not np.isnan(value2):
                        if tech_matrix[((key2),(process_name, material))] != value2:
                            tech_matrix[((key2),(process_name, material))] = value2
            
            for material,value in report_dict["Biosphere"].items():
                for key2, value2 in value.items():
                    if not np.isnan(value2):
                        if bio_matrix[((key2),(process_name, material))] != value2:
                            bio_matrix[((key2),(process_name, material))] = value2
            i+=1
        
    if parameters:
        matrix,params = parameters.MC_calc()
        uncertain_inputs += params
        for key, value in matrix.items():
            if key in tech_matrix:
                tech_matrix[key] = value    
    
    tech = np.array(list(tech_matrix.values()), dtype=float)
    bio = np.array(list(bio_matrix.values()), dtype=float)
    
    lca.rebuild_technosphere_matrix(tech)
    lca.rebuild_biosphere_matrix(bio)
    lca.lci_calculation()
    if lca.lcia:
        lca.lcia_calculation()

    lca_results = dict()
    lca_results[method[0]]=lca.score

    if len(method)>1:
        for i in range(1,len(method)):
            lca.switch_method(method[i])
            lca.lcia_calculation()
            lca_results[method[i]]=lca.score
        lca.switch_method(method[0])
    print(os.getpid(),index)
    return(os.getpid(),lca_results,uncertain_inputs,report_dict)
    
  

#%% Monte Carlo simulation

class ParallelData(LCA):
    def __init__(self, functional_unit, method, project, process_models = None, process_model_names = None, common_data = None, parameters = None,seed = None):
        super(ParallelData, self).__init__(functional_unit, method[0])
        self.lci()
        self.lcia()
        self.functional_unit = functional_unit
        self.method = method
        self.project = project
        self.process_models = process_models
        self.process_model_names = process_model_names
        self.parameters = parameters
        self.common_data = common_data
        self.seed = seed
        
        
        self.activities_dict,_,self.biosphere_dict = self.reverse_dict()
        
        """
        tech_matrix is dictionary include all the exhange as tuple (product,Feed) key and amount as value
        {(('LF', 'Aerobic_Residual'), ('SF1_product', 'Aerobic_Residual_MRDO')):0.8288506683507344}
        
        So we can update the tech_params by the keys
        """
        self.tech_matrix = dict()
        for i in self.tech_params:
            self.tech_matrix[(self.activities_dict[i[2]], self.activities_dict[i[3]])] = i[6]
        
        
        self.bio_matrix = dict()
        """
        bio_matrix is dictionary include all the exhange as tuple (product,Feed) key and amount as value
        {(('biosphere3', '0015ec22-72cb-4af1-8c7b-0ba0d041553c'), ('Technosphere', 'Boiler_Diesel')):6.12e-15}
        
        So we can update the bio_params by the keys
        """
        
        for i in self.bio_params:
            if (self.biosphere_dict[i[2]], self.activities_dict[i[3]]) not in self.bio_matrix.keys():
                self.bio_matrix[(self.biosphere_dict[i[2]], self.activities_dict[i[3]])] = i[6]
            else:
                self.bio_matrix[(str(self.biosphere_dict[i[2]]) + " - 1", self.activities_dict[i[3]])] = i[6]
                #print((str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]]))                
        
    def run(self, nproc, n):       
        with pool_adapter(mp.Pool(processes=nproc)) as pool:
            res = pool.map(
                worker,
                [
                    (self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed  + i, n//nproc)
                    for i in range(nproc)
                ]
            )
        self.results = [x for lst in res for x in lst]
        #res=worker((self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed, n//nproc))
        #self.results = [x for lst in res for x in lst]

    ### Export results
    def result_to_DF(self):
        output=pd.DataFrame()
        # Reporting the LCIA results; Create a column for each method
        for j in self.results[0][1].keys():
            output[j] = [self.results[i][1][j] for i in range(len(self.results))]
        # Reporting the input data    
        for j in range(len(self.results[0][2])):
                output[self.results[0][2][j][0]] = [self.results[i][2][j][1] for i in range(len(self.results))]
        return(output)

    def save_results(self,name):
        self.result_to_DF().to_pickle(name)



#%% Optimization
# =============================================================================
# =============================================================================
    ### Optimization of mass fractions
# =============================================================================
# =============================================================================
    ### Objective function    
    def objective_function(self, x):
        """
        Use the new parameters (Waste fractions) to update the tech_matrix (tech_param)
        and reculate the LCA score
        """
        if self.oldx != list(x): # Calculations are done only when the function get new x.
            matrix=self.project.unified_params.get_matrix(x)
            for key, value in matrix.items():
                if key in self.tech_matrix:
                    self.tech_matrix[key] = value    
        
            tech = np.array(list(self.tech_matrix.values()), dtype=float)
            bio = np.array(list(self.bio_matrix.values()), dtype=float)
            
            self.rebuild_technosphere_matrix(tech)
            self.rebuild_biosphere_matrix(bio)
            self.lci_calculation()
            if self.lcia:
                self.lcia_calculation()
            
            self.oldx = list(x)
        return(self.score/10**self.magnitude)

    ### Mass to process
    def get_mass_flow(self, key, KeyType, x):
        """
        calculate the mass to the process from the supply_array matrix
        """
        self.objective_function(x)
        
        mass_flow=0
        if KeyType == 'WasteToProcess':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i]:
                    mass_flow += self.supply_array[i]
        
        elif KeyType == 'Process':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i][0]:
                    mass_flow += self.supply_array[i]
        else:
            raise ValueError(""" KeyType for the get_mass_flow function is not defined correct.""")
        return mass_flow
        
    ### Emission flow in LCI
    def get_emission_amount(self, emission, x):
        self.objective_function(x)
        inventory=self.biosphere_matrix*self.supply_array
        emission_amount = 0
        for i in range(len(inventory)):
            if emission == self.biosphere_dict[i]:
                emission_amount+=inventory[i]
        return emission_amount
    
    
    def create_equality(self, N_param_Ingroup):
        """
        Check that the sum of parameters in each group should be one.
        """
        local_index = self.Param_index
        l = lambda x: sum([x[i] for i in range(local_index,local_index+N_param_Ingroup)]) -1 
        self.Param_index+=N_param_Ingroup
        return l
        
    def create_inequality(self, key, limit, KeyType,ConstType):
        """
        key: process name, key for activtity in process or key for activity in biosphere
        ConstType: <= , >=
        KeyType: Process,WasteToProcess,Emission
        """
        if ConstType not in ['<=','>=']:
            raise ValueError(" Constraint Type is not defined correct ") 
                        
        if KeyType == 'Process':
            if ConstType == '<=':
                l = lambda x: limit - self.get_mass_flow(key, KeyType, x) 
            else:
                l = lambda x: self.get_mass_flow(key, KeyType, x) - limit
            return l
            
        elif KeyType == 'WasteToProcess':
            if ConstType == '<=':
                l = lambda x: limit - self.get_mass_flow(key, KeyType, x)
            else:
                l = lambda x: self.get_mass_flow(key, KeyType, x) - limit
            return l

        elif KeyType == 'Emission': 
            if ConstType == '<=':
                l = lambda x: limit - self.get_emission_amount(key, x)
            else:
                l = lambda x: self.get_emission_amount(key, x) - limit
            return l
            
    
    def create_constraints(self):
        cons = list()
        group = dict()
        
        # Index for the parameters
        self.Param_index=0
        
        # Number of parameters in each group (from one source to different denstinations)
        for key in self.project.unified_params.param_uncertainty_dict.keys():
            group[key] = len(self.project.unified_params.param_uncertainty_dict[key])

        # Equal constraint (sum of the parameters in each group should be one)
        for vals in group.values():
            cons.append({'type':'eq', 'fun':self.create_equality(N_param_Ingroup=vals)})
            
        if self.constraints:
            for key in self.constraints.keys():
                cons.append({'type':'ineq', 'fun': self.create_inequality(key, self.constraints[key]['limit'], self.constraints[key]['KeyType'], self.constraints[key]['ConstType'])})
        return cons
    
    def optimize_parameters(self, project, constraints=None):
        self.constraints=constraints
        self.project = project
        self.magnitude = len(str(int(abs(self.score)))) 
        
        x0 = [i['amount'] for i in self.project.parameters_list] # initializing with the users initial solution
        #x0 = [1 for _ in self.project.parameters_list] #changing initial x0 to outside feasible region
        
        self.oldx=[0 for i in range(len(x0))]
        
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        self.cons = self.create_constraints()
        
        res = minimize(self.objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
        if res.success:
            self.success=True
            self.optimized_x=list()
            res.x=res.x.round(decimals=3)
            for i in range(len(self.project.parameters_list)):
                self.optimized_x.append({'name':self.project.parameters_list[i]['name'],'amount':res.x[i]})
            print(self.optimized_x)
            return res
        else:
            self.success=False
            print(res.message)
            return res
            
    def multi_start_optimization(self, project, constraints=None, max_iter=30):
        self.constraints=constraints
        self.project = project
        self.magnitude = len(str(int(abs(self.score)))) 
        
        global_min = 1E100
        
        self.cons = self.create_constraints()
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        
        for _ in range(max_iter):
            x0 = [random() for i in self.project.parameters_list] #initializing with the users initial solution
            self.oldx=[0 for i in range(len(x0))]
            res = minimize(self.objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
            
            if res.success:
                if res.fun < global_min:
                    res_global = res
                    global_min = res.fun
                    print(global_min)
        
        if res_global.success:
            self.success=True
            self.optimized_x=list()
            res_global.x=res_global.x.round(decimals=3)
            for i in range(len(self.project.parameters_list)):
                self.optimized_x.append({'name':self.project.parameters_list[i]['name'],'amount':res_global.x[i]})
            return res_global
        else:
            self.success=False
            print(res_global.message)
            return res_global
    
    def set_optimized_parameters_to_project(self):
        assert hasattr(self, "project"), "Must run optimize_parameters first"
        assert self.success, "Optimization has to be sucessful first"
        
        self.project.update_parameters(self.optimized_x)
    
# =============================================================================
#     def mass_to_process(self):
#         get_mass_flow(self, key, KeyType, x):
# =============================================================================
        
        
    
    

    
  

