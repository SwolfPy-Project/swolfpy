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




projects.set_current("demo_2")
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
#for key,val in biosphere_dict.items():
#    biosphere_dict_names[key]=get_activity(val)
#

for i in lca.bio_params:
    if (biosphere_dict[i[2]], activities_dict[i[3]]) not in bio_matrix.keys():
        bio_matrix[(biosphere_dict[i[2]], activities_dict[i[3]])] = i[6]
    else:
        bio_matrix[(str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]

#for i in lca.bio_params:
#    if (biosphere_dict_names[i[2]], activities_dict[i[3]]) not in bio_matrix.keys():
#        bio_matrix[(biosphere_dict_names[i[2]], activities_dict[i[3]])] = i[6]
#    else: #duplicates...adds -1 and prints
#        bio_matrix[(str(biosphere_dict_names[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]
#        # print(biosphere_dict_names[i[2]], activities_dict[i[3]])


A = WTE()
A.setup_MC()

a = Process_Model("WTE", {"WTE":1})
#b = Process_Model("LF", {"LF":1})

a.read_output_from_SWOLF("WTE_BW2.csv")
#b.read_output_from_SWOLF("trad_landfill _BW2.xlsx")

        
    
lca_scores = list()
lca_scores.append(lca.score)
t1 = time.time()


for i in range(200):
    #--WTE--
    #Technosphere
    #a.read_output_from_SWOLF("WTE_BW2.csv") #reloading from file...slow!
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
                    

    #Biosphere                
    '''for material,value in a.process_model_output['Biosphere'].items():
        for key2, value2 in value.items():
            if value2!=0:
                value2 *= 1+ np.random.rand()
                if bio_matrix[((key2),(a.process_name, material))] != value2:
                    bio_matrix[((key2),(a.process_name, material))] = value2                 
                    
                    
    #--LF--                
    #Technosphere
    b.read_output_from_SWOLF("trad_landfill _BW2.xlsx") #realoading from file...slow!
    for material,value in b.process_model_output['Technosphere'].items():
        for key2, value2 in value.items():
            if value2!=0:
                value2 *=1+ np.random.rand()
                if tech_matrix[((key2),(b.process_name, material))] != value2:
                    tech_matrix[((key2),(b.process_name, material))] = value2 
    
    #Biosphere                
    for material,value in b.process_model_output['Biosphere'].items():
        for key2, value2 in value.items():
            if value2!=0:
                value2 *= 1+ np.random.rand()
                if bio_matrix[((key2),(b.process_name, material))] != value2:
                    bio_matrix[((key2),(b.process_name, material))] = value2'''

    
    
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
    lca_scores.append(lca.score)
            
t2 = time.time()
print('total time for 200 runs: %0.1f secs' % (t2-t1))
#print(lca_scores)

#reading file 1000 runs 2450.1s - 2.45s/run
#not reading file 1000 runs in 54s - 0.054s/run

from matplotlib.pylab import *
hist(lca_scores, normed=True, histtype="step")
xlabel('(IPCC 2007, climate change, GWP 100a)')
ylabel("Probability")

