# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
Treatment_processes = {}
Treatment_processes['AD']={'path':"AD_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}
Treatment_processes['SSMRF']={'path':"SS_MRF_BW2.csv",'input_type':['SSRC']}
Treatment_processes['WTE']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}


mojtaba = project("demo_2",Treatment_processes)
mojtaba.init_project('SWOLF_AccountMode_LCI DATA.csv')
mojtaba.write_project()
mojtaba.group_exchanges()

gg= [{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Bottom_Ash_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE', 'amount': 0},
 {'name': 'frac_of_Fe_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Al_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE_to_REPROC', 'amount': 1}]

mojtaba.update_parameters(gg)
scenario1 = {"LF":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1},"COMP":{"Yard_Trimmings_Grass":1,"Food_Waste_Vegetable":1}}
mojtaba.process_start_scenario(scenario1,'scenario1')
mojtaba.Do_LCA("scenario1",('IPCC 2007', 'climate change', 'GWP 100a'),1)

mojtaba.lca.activity_dict
mojtaba.lca.product_dict
mojtaba.lca.tech_params

for i, obj in enumerate(mojtaba.lca.tech_params):
    if obj['row'] == 0 and obj['col']==106:
        print(i)
        
        
    
mojtaba.lca.tech_params[982]['amount']=45
mojtaba.lca.rebuild_technosphere_matrix(mojtaba.lca.tech_params['amount'])
mojtaba.lca.lci_calculation()
mojtaba.lca.lcia()
mojtaba.lca.score


Database('biosphere3').search('Methane')[-4]
Database('biosphere3').search('Methane')[-4].key
mojtaba.lca.biosphere_dict[('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8')]

for i, obj in enumerate(mojtaba.lca.bio_params):
    if obj['row'] == 1053 and obj['col']==106:
        print(i)

mojtaba.lca.bio_params[1706]['amount']=24
mojtaba.lca.rebuild_biosphere_matrix(mojtaba.lca.bio_params['amount'])
mojtaba.lca.lci_calculation()
mojtaba.lca.lcia()
mojtaba.lca.score

import time
A=time.time()
for j, obj in enumerate(mojtaba.lca.bio_params):
    obj['amount']*=0.95
mojtaba.lca.rebuild_biosphere_matrix(mojtaba.lca.bio_params['amount'])
mojtaba.lca.lci_calculation()
mojtaba.lca.lcia()
mojtaba.lca.score
B= time.time()
print(A-B,mojtaba.lca.score )    
    



















scenario2 = {"COMP":{"Yard_Trimmings_Grass":1,"Food_Waste_Vegetable":1}}
mojtaba.process_start_scenario(scenario2,'scenario2')
mojtaba.Do_LCA("scenario2",('IPCC 2007', 'climate change', 'GWP 100a'),1)


gg= [{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Bottom_Ash_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE', 'amount': 0},
 {'name': 'frac_of_Fe_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Al_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE_to_REPROC', 'amount': 1}]
mojtaba.update_parameters(gg)
mojtaba.Do_LCA("scenario2",('IPCC 2007', 'climate change', 'GWP 100a'),1)

gg= [{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_LF', 'amount': 0.5},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE', 'amount': 0.5},
 {'name': 'frac_of_Bottom_Ash_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE', 'amount': 0},
 {'name': 'frac_of_Fe_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Al_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE_to_REPROC', 'amount': 1}]
mojtaba.update_parameters(gg)
mojtaba.Do_LCA("scenario2",('IPCC 2007', 'climate change', 'GWP 100a'),1)


        
        
        
        
        
        
        
        
    





