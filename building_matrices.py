from brightway2 import *
from stats_arrays.random import MCRandomNumberGenerator
from bw2calc.utils import get_seed
import numpy as np
import time
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
from process_model_msm3 import *
import pandas as pd
from Required_keys import *
import copy
from bw2analyzer import ContributionAnalysis
from WTE import *
import sys
from multiprocessing import Queue
from multiprocessing import Pool
import multiprocessing as mp
import threading 
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
	project,fu,mt,A,tech_matrix,bio_matrix,n = args
	return [parallel_mc (project, fu, mt ,A, tech_matrix, bio_matrix) for x in range(n)]



def parallel_mc (project, functional_unit, method, A, tech_matrix, bio_matrix):
	projects.set_current(project, writable=False)
	lca = LCA(functional_unit, method)
	lca.lci()
	lca.lcia()
	A.MC_calc()
	a_dict = A.report()
	process_name = a_dict.pop("process name")
	for material,value in a_dict["Technosphere"].items():
		for key2, value2 in value.items():
			if value2!=0 and not np.isnan(value2):
				if tech_matrix[((key2),(process_name, material))] != value2:
					tech_matrix[((key2),(process_name, material))] = value2 
	
	for material,value in a_dict["Biosphere"].items():
		for key2, value2 in value.items():
			if value2!=0 and not np.isnan(value2):
				if bio_matrix[((key2),(process_name, material))] != value2:
					bio_matrix[((key2),(process_name, material))] = value2 
					
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
	def __init__(self, functional_unit, method, project):
		super(ParallelData, self).__init__(functional_unit, method)
		self.lci()
		self.lcia()
		self.fu = functional_unit
		self.mt = method
		self.pj = project
		
		
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
				
		
		A = WTE()
		A.setup_MC()
		
		lca_scores = list()
		#lca_scores.append(self.lca.score)
		t1 = time.time()
		#nproc = mp.cpu_count()
		nproc = 4
		n = 200
		

		
		with pool_adapter(mp.Pool(processes=nproc)) as pool:
			results = pool.map(
				worker,
				[
					(self.pj,self.fu,self.mt,A,tech_matrix, bio_matrix,n//nproc)
					for _ in range(nproc)
				]
			)
		self.res = [x for lst in results for x in lst]
		
		t2 = time.time()
		print('total time for %d runs: %0.1f secs. Using %d threads' % ((n, t2-t1, nproc)))
	

	
	
if __name__=='__main__':
	project = "demo_2"
	projects.set_current(project)
	db = Database("waste")
	functional_unit = {db.get("scenario1") : 1}
	method = ('IPCC 2007', 'climate change', 'GWP 100a')

	a = ParallelData(functional_unit, method, project) 
	
	from matplotlib.pylab import *
	hist(a.res, density=True, histtype="step")
	xlabel('(IPCC 2007, climate change, GWP 100a)')
	ylabel("Probability")
	
	
	
	


