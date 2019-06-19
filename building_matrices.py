from brightway2 import *
from stats_arrays.random import MCRandomNumberGenerator
from bw2calc.utils import get_seed
import numpy as np
import time

db = Database("waste")
functional_unit = {db.get("scenario1") : 1}
lca = LCA(functional_unit, ('IPCC 2007', 'climate change', 'GWP 100a')) 
lca.lci()
lca.lcia()

activities_dict = dict(zip(lca.activity_dict.values(),lca.activity_dict.keys()))
tech_matrix = dict()
for i in lca.tech_params:
	tech_matrix[(activities_dict[i[2]], activities_dict[i[3]])] = i[6]


biosphere_dict = dict(zip(lca.biosphere_dict.values(),lca.biosphere_dict.keys()))
bio_matrix = dict()
biosphere_dict_names = dict()
#changing biosphere codes into names from biosphere 3 db
for key,val in biosphere_dict.items():
	biosphere_dict_names[key]=get_activity(val)

for i in lca.bio_params:
	if (biosphere_dict_names[i[2]], activities_dict[i[3]]) not in bio_matrix.keys():
		bio_matrix[(biosphere_dict_names[i[2]], activities_dict[i[3]])] = i[6]
	else: #duplicates...adds -1 and prints
		bio_matrix[(str(biosphere_dict_names[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]
		print(biosphere_dict_names[i[2]], activities_dict[i[3]])


#update bio_matrix and tech_matrix
# time test	
t1 = time.time()


for i in range(1000):
	tech = np.array(list(tech_matrix.values()), dtype=float)
	bio = np.array(list(bio_matrix.values()), dtype=float)
	#populate bio/tech array	
	
	
	
	lca.rebuild_technosphere_matrix(tech)
	lca.rebuild_biosphere_matrix(bio)
	lca.lci_calculation()
	if lca.lcia:
		lca.lcia_calculation()
		if lca.weighting:
			lca.weighting_calculation()
		print(lca.score)
			
t2 = time.time()
print('total time for 1000 runs: %0.1f secs' % (t2-t1))			