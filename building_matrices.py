from brightway2 import *
import numpy as np
import time
from brightway2 import *
from Required_keys import *
from WTE import *
import multiprocessing as mp
import sys
from multiprocessing import Queue
from multiprocessing import Pool
from brightway2 import LCA
from bw2data import projects
    
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
    project, functional_unit, method,process_models, process_model_names, tech_matrix, bio_matrix, n = args
    projects.set_current(project, writable=False)
    lca = LCA(functional_unit, method)
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, process_models, process_model_names, tech_matrix, bio_matrix) for x in range(n)]



def parallel_mc (lca, project, functional_unit, method, process_models, process_model_names, tech_matrix, bio_matrix):

    for process in process_models:
        process.MC_calc()
    
    i = 0
    for process_name in process_model_names:
        report_dict = process_models[i].report()

        for material,value in report_dict["Technosphere"].items():
            for key2, value2 in value.items():
                if value2!=0 and not np.isnan(value2):
                    if tech_matrix[((key2),(process_name, material))] != value2:
                        tech_matrix[((key2),(process_name, material))] = value2 
		
        for material,value in report_dict["Biosphere"].items():
            for key2, value2 in value.items():
                if value2!=0 and not np.isnan(value2):
                    if bio_matrix[((key2),(process_name, material))] != value2:
                        bio_matrix[((key2),(process_name, material))] = value2
        i+=1
		
	
    tech = np.array(list(tech_matrix.values()), dtype=float)
    bio = np.array(list(bio_matrix.values()), dtype=float)
    
    lca.rebuild_technosphere_matrix(tech)
    lca.rebuild_biosphere_matrix(bio)
    lca.lci_calculation()
    if lca.lcia:
        lca.lcia_calculation()
        if lca.weighting:
            lca.weighting_calculation()

    return(lca.score)
    
    


class ParallelData(LCA):
    def __init__(self, functional_unit, method, project, process_models, process_model_names):
        super(ParallelData, self).__init__(functional_unit, method)
        self.lci()
        self.lcia()
        self.functional_unit = functional_unit
        self.method = method
        self.project = project
        self.process_models = process_models
        self.process_model_names = process_model_names
        
        
        activities_dict = dict(zip(self.activity_dict.values(),self.activity_dict.keys()))
        tech_matrix = dict()
        for i in self.tech_params:
            tech_matrix[(activities_dict[i[2]], activities_dict[i[3]])] = i[6]
        
        
        biosphere_dict = dict(zip(self.biosphere_dict.values(),self.biosphere_dict.keys()))
        bio_matrix = dict()
        biosphere_dict_names = dict()
        
        for i in self.bio_params:
            if (biosphere_dict[i[2]], activities_dict[i[3]]) not in bio_matrix.keys():
                bio_matrix[(biosphere_dict[i[2]], activities_dict[i[3]])] = i[6]
            else:
                bio_matrix[(str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]
                
        
        for x in self.process_models:
            x.setup_MC()

        

        t1 = time.time()
		#nproc = mp.cpu_count()
        nproc = 4
        n = 1000
        

        
        with pool_adapter(mp.Pool(processes=nproc)) as pool:
            res = pool.map(
                worker,
                [
                    (self.project, self.functional_unit, self.method, self.process_models, self.process_model_names, tech_matrix, bio_matrix, n//nproc)
                    for _ in range(nproc)
                ]
            )
        self.results = [x for lst in res for x in lst]
        
        t2 = time.time()
        print('total time for %d runs: %0.1f secs. Using %d threads and %d process model(s)' % ((n, t2-t1, nproc, len(self.process_models))))
    

    
    
if __name__=='__main__':
    project = "demo_5"
    projects.set_current(project)
    db = Database("waste")
    functional_unit = {db.get("scenario1") : 1}
    method = ('IPCC 2007', 'climate change', 'GWP 100a')
	
    process_models = list()
    process_model_names = list()
	
    process_models.append(WTE())
    process_models.append(WTE())
    process_models.append(WTE())
    process_models.append(WTE())
	
    process_model_names.append('WTE')
    process_model_names.append('WTE1')
    process_model_names.append('WTE2')
    process_model_names.append('WTE3')
	
    a = ParallelData(functional_unit, method, project, process_models, process_model_names) 
    
    from matplotlib.pylab import *
    hist(a.results, density=True, histtype="step")
    xlabel('(IPCC 2007, climate change, GWP 100a)')
    ylabel("Probability")
    
    
    


