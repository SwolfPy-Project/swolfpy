# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:45:04 2020

@author: msmsa
"""
import numpy as np
import pandas as pd
import os
from .LCA_matrix import LCA_matrix
import multiprocessing as mp
from brightway2 import LCA, projects

class Monte_Carlo(LCA_matrix):
    def __init__(self, functional_unit, method, project, process_models = None, process_model_names = None, common_data = None, parameters = None,seed = None):
        super().__init__(functional_unit, method, project)
        
        self.process_models = process_models
        self.process_model_names = process_model_names
        self.parameters = parameters
        self.common_data = common_data
        if seed:
            self.seed = seed
        else:
            self.seed = 0           
        
    def run(self, nproc, n):       
        pool_adapter = lambda x: x
        with pool_adapter(mp.Pool(processes=nproc)) as pool:
            res = pool.map(
                Monte_Carlo.worker,
                [
                    (self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed  + i, n//nproc)
                    for i in range(nproc)
                ]
            )
        self.results = [x for lst in res for x in lst]
        #res=Monte_Carlo.worker((self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed, n//nproc))
        #self.results = [x for lst in res for x in lst]

    @staticmethod
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
        return [Monte_Carlo.parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models=process_models, process_model_names=process_model_names, parameters=parameters, common_data=common_data, index =x) for x in range(n)]
    
    
    @staticmethod
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
                                raise KeyError('Exchange {} is calculated but not exist in LCA technosphere'.format(((key2),(process_name, material))))
                        else:
                            raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'.format(((key2),(process_name, material))))
                                
                for material,value in report_dict["Waste"].items():
                    for key2, value2 in value.items():
                        key2 = (process_name + "_product", material + '_' + key2)
                        if not np.isnan(value2):
                            if ((key2),(process_name, material)) in tech_matrix.keys():
                                if tech_matrix[((key2),(process_name, material))] != value2:
                                    tech_matrix[((key2),(process_name, material))] = value2
                            else:
                                raise KeyError('Exchange {} is calculated but not exist in LCA technosphere'.format(((key2),(process_name, material))))
                                
                        else:
                            raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'.format(((key2),(process_name, material))))
                            
                
                for material,value in report_dict["Biosphere"].items():
                    for key2, value2 in value.items():
                        if not np.isnan(value2):
                            if bio_matrix[((key2),(process_name, material))] != value2:
                                bio_matrix[((key2),(process_name, material))] = value2
                        else:
                            raise ValueError('Amount for Exchange {} is Nan. The amount should be number, check the calculations in the process model'.format(((key2),(process_name, material))))              
                i+=1
            
        if parameters:
            param_exchanges,params = parameters.MC_calc()
            uncertain_inputs += params
            for key, value in param_exchanges.items():
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
        return(os.getpid(),lca_results,uncertain_inputs)

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
