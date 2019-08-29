from brightway2 import *
import numpy as np
from Required_keys import *
from Composting import *
from AD import *
import multiprocessing as mp
import sys
from multiprocessing import Queue
from multiprocessing import Pool
from brightway2 import LCA
from bw2data import projects
import os

    
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
    project, functional_unit, method, process_models, process_model_names, common_data, tech_matrix, bio_matrix,seed ,n = args
    projects.set_current(project, writable=False)
    if common_data:
        common_data.setup_MC(seed)
    for x in process_models:
        x.setup_MC(seed)
    lca = LCA(functional_unit, method)
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models, process_model_names, common_data=common_data) for x in range(n)]

def worker2(args):
    project, functional_unit, method, param, tech_matrix, bio_matrix,seed ,n = args
    projects.set_current(project, writable=False)
    parameters.setup_MC(seed)
    lca = LCA(functional_unit, method)
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, parameters=param) for x in range(n)]

def worker3(args):
    project, functional_unit, method, parameters, process_models, process_model_names, common_data, tech_matrix, bio_matrix,seed, n = args
    projects.set_current(project, writable=False)
    if common_data:
        common_data.setup_MC(seed)
		
    for x in process_models:
        x.setup_MC(seed)		
    parameters.setup_MC(seed)
    
    lca = LCA(functional_unit, method)
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models, process_model_names, parameters, common_data) for x in range(n)]



def parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models = None, process_model_names = None, parameters = None, common_data = None):
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
                        if tech_matrix[((key2),(process_name, material))] != value2:
                            tech_matrix[((key2),(process_name, material))] = value2 
                            
            for material,value in report_dict["Waste"].items():
                for key2, value2 in value.items():
                    if key2 in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual','RDF','Al','Fe','Cu']:
                        key2 = (process_name + "_product",material+'_'+key2)
                    else:
                        key2 = (process_name + "_product",key2)
                    if not np.isnan(value2):
                        if tech_matrix[((key2),(process_name, material))] != value2:
                            tech_matrix[((key2),(process_name, material))] = value2
                            print(tech_matrix[((key2),(process_name, material))])
			
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
        if lca.weighting:
            lca.weighting_calculation()
    return(os.getpid(),lca.score,uncertain_inputs)
    
    


class ParallelData(LCA):
    def __init__(self, functional_unit, method, project, process_models = None, process_model_names = None, common_data = None, parameters = None,seed = None):
        super(ParallelData, self).__init__(functional_unit, method)
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
        
        
        activities_dict = dict(zip(self.activity_dict.values(),self.activity_dict.keys()))
        self.tech_matrix = dict()
        for i in self.tech_params:
            self.tech_matrix[(activities_dict[i[2]], activities_dict[i[3]])] = i[6]
        
        
        biosphere_dict = dict(zip(self.biosphere_dict.values(),self.biosphere_dict.keys()))
        self.bio_matrix = dict()
        biosphere_dict_names = dict()
        
        for i in self.bio_params:
            if (biosphere_dict[i[2]], activities_dict[i[3]]) not in self.bio_matrix.keys():
                self.bio_matrix[(biosphere_dict[i[2]], activities_dict[i[3]])] = i[6]
            else:
                self.bio_matrix[(str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]
                
        


    def run(self, nproc, n):       
        if self.process_models and not self.parameters:
            with pool_adapter(mp.Pool(processes=nproc)) as pool:
                res = pool.map(
                    worker,
                    [
                        (self.project, self.functional_unit, self.method, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix,self.seed + i, n//nproc)
                        for i in range(nproc)
                    ]
                )
            self.results = [x for lst in res for x in lst]

        elif self.parameters and not self.process_models:
			
            with pool_adapter(mp.Pool(processes=nproc)) as pool:
                    res = pool.map(
                    worker2,
                    [
                        (self.project, self.functional_unit, self.method, self.parameters, self.tech_matrix, self.bio_matrix,self.seed+i, n//nproc)
                        for i in range(nproc)
                    ]
                )
            self.results = [x for lst in res for x in lst]

        else:

            with pool_adapter(mp.Pool(processes=nproc)) as pool:
                res = pool.map(
                    worker3,
                    [
                        (self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix,self.seed + i, n//nproc)
                        for i in range(nproc)
                    ]
                )
            self.results = [x for lst in res for x in lst]     


    
   
if __name__=='__main__':
    pass
    
     
  

