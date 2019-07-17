# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
Treatment_processes = {}
Treatment_processes['AD']={'path':"AD_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP1']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP2']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP3']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}
Treatment_processes['SSMRF']={'path':"SS_MRF_BW2.csv",'input_type':['SSRC']}
Treatment_processes['WTE']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE1']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE2']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE3']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}

mojtaba = project("demo_6",Treatment_processes)
mojtaba.init_project('SWOLF_AccountMode_LCI DATA.csv')
mojtaba.write_project()
mojtaba.group_exchanges()

gg=[{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0.25},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE1', 'amount': 0.25},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE2', 'amount': 0.25},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE3', 'amount': 0.25},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP1_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP1_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP1_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP1_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP1_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP2_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP2_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP2_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP2_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP2_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP3_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP3_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP3_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP3_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP3_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Bottom_Ash_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE1', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE2', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE3', 'amount': 0},
 {'name': 'frac_of_Fe_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Al_from_SSMRF_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE2_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE2_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE3_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE3_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE3_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE3_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE3_to_REPROC', 'amount': 1}]

mojtaba.update_parameters(gg)
scenario1 = {"WTE":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1},"WTE1":{"Yard_Trimmings_Grass":2,"Paper_Bags":2,"Mixed_Plastic":2},
             "WTE2":{"Yard_Trimmings_Grass":1,"Paper_Bags":0.1,"Mixed_Plastic":1},
             "WTE3":{"Yard_Trimmings_Grass":0.1,"Paper_Bags":1,"Mixed_Plastic":1},
             "COMP":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":7},"COMP1":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":5},
             "COMP2":{"Yard_Trimmings_Grass":9,"Yard_Trimmings_Leaves":6},"COMP3":{"Yard_Trimmings_Grass":3,"Yard_Trimmings_Leaves":1}}
mojtaba.process_start_scenario(scenario1,'scenario1')
mojtaba.Do_LCA("scenario1",('IPCC 2007', 'climate change', 'GWP 100a'),1)

scenario2 = {"WTE":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1,'Wood':1,'Office_Paper':2 ,'Magazines_':1, 'third_Class_Mail':3, 'Folding_Containers' : 2, 'Mixed_Paper' :1 },
             "WTE1":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1,'Wood':1,'Office_Paper':2 ,'Magazines_':1, 'third_Class_Mail':3, 'Folding_Containers' : 2, 'Mixed_Paper' :1 },
             "WTE2":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1,'Wood':1,'Office_Paper':2 ,'Magazines_':1, 'third_Class_Mail':3, 'Folding_Containers' : 2, 'Mixed_Paper' :1 },
             "WTE3":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1,'Wood':1,'Office_Paper':2 ,'Magazines_':1, 'third_Class_Mail':3, 'Folding_Containers' : 2, 'Mixed_Paper' :1 },
             "COMP":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":7},
             "COMP1":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":5},
             "COMP2":{"Yard_Trimmings_Grass":9,"Yard_Trimmings_Leaves":6},
             "COMP3":{"Yard_Trimmings_Grass":3,"Yard_Trimmings_Leaves":1}}
mojtaba.process_start_scenario(scenario2,'scenario2')
mojtaba.Do_LCA("scenario2",('IPCC 2007', 'climate change', 'GWP 100a'),1)



scenario3 = {"WTE":{'Yard_Trimmings_Leaves':1, 'Yard_Trimmings_Grass':1, 'Yard_Trimmings_Branches':1, 'Food_Waste_Vegetable':1, 'Food_Waste_Non_Vegetable':1,
                      'Wood':1, 'Wood_Other':1, 'Textiles':1, 'Rubber_Leather':1, 'Newsprint':1, 'Corr_Cardboard':1, 'Office_Paper':1, 'Magazines_':1, 'third_Class_Mail':1,
                      'Folding_Containers':1, 'Paper_Bags':1, 'Mixed_Paper':1, 'Paper_Non_recyclable':1, 'HDPE_Translucent_Containers':1, 'HDPE_Pigmented_Containers':1, 'PET_Containers':1,
                      'Plastic_Other_1_Polypropylene':1, 'Plastic_Other_2':1, 'Mixed_Plastic':1, 'Plastic_Film':1, 'Plastic_Non_Recyclable':1, 'Ferrous_Cans':1, 'Ferrous_Metal_Other':1,
                      'Aluminum_Cans':1, 'Aluminum_Foil':1, 'Aluminum_Other':1, 'Ferrous_Non_recyclable':1, 'Al_Non_recyclable':1, 'Glass_Brown':1, 'Glass_Green':1,
                      'Glass_Clear':1, 'Mixed_Glass':1, 'Glass_Non_recyclable':1, 'Misc_Organic':1, 'Misc_Inorganic':1, 'E_waste':1, 'Aerobic_Residual':1,
                      'Anaerobic_Residual':1, 'Bottom_Ash':1, 'Fly_Ash':1, 'Diapers_and_sanitary_products':1},
             "WTE1":{'Yard_Trimmings_Leaves':1, 'Yard_Trimmings_Grass':1, 'Yard_Trimmings_Branches':1, 'Food_Waste_Vegetable':1, 'Food_Waste_Non_Vegetable':1,
                      'Wood':1, 'Wood_Other':1, 'Textiles':1, 'Rubber_Leather':1, 'Newsprint':1, 'Corr_Cardboard':1, 'Office_Paper':1, 'Magazines_':1, 'third_Class_Mail':1,
                      'Folding_Containers':1, 'Paper_Bags':1, 'Mixed_Paper':1, 'Paper_Non_recyclable':1, 'HDPE_Translucent_Containers':1, 'HDPE_Pigmented_Containers':1, 'PET_Containers':1,
                      'Plastic_Other_1_Polypropylene':1, 'Plastic_Other_2':1, 'Mixed_Plastic':1, 'Plastic_Film':1, 'Plastic_Non_Recyclable':1, 'Ferrous_Cans':1, 'Ferrous_Metal_Other':1,
                      'Aluminum_Cans':1, 'Aluminum_Foil':1, 'Aluminum_Other':1, 'Ferrous_Non_recyclable':1, 'Al_Non_recyclable':1, 'Glass_Brown':1, 'Glass_Green':1,
                      'Glass_Clear':1, 'Mixed_Glass':1, 'Glass_Non_recyclable':1, 'Misc_Organic':1, 'Misc_Inorganic':1, 'E_waste':1, 'Aerobic_Residual':1,
                      'Anaerobic_Residual':1, 'Bottom_Ash':1, 'Fly_Ash':1, 'Diapers_and_sanitary_products':1},
             "WTE2":{'Yard_Trimmings_Leaves':1, 'Yard_Trimmings_Grass':1, 'Yard_Trimmings_Branches':1, 'Food_Waste_Vegetable':1, 'Food_Waste_Non_Vegetable':1,
                      'Wood':1, 'Wood_Other':1, 'Textiles':1, 'Rubber_Leather':1, 'Newsprint':1, 'Corr_Cardboard':1, 'Office_Paper':1, 'Magazines_':1, 'third_Class_Mail':1,
                      'Folding_Containers':1, 'Paper_Bags':1, 'Mixed_Paper':1, 'Paper_Non_recyclable':1, 'HDPE_Translucent_Containers':1, 'HDPE_Pigmented_Containers':1, 'PET_Containers':1,
                      'Plastic_Other_1_Polypropylene':1, 'Plastic_Other_2':1, 'Mixed_Plastic':1, 'Plastic_Film':1, 'Plastic_Non_Recyclable':1, 'Ferrous_Cans':1, 'Ferrous_Metal_Other':1,
                      'Aluminum_Cans':1, 'Aluminum_Foil':1, 'Aluminum_Other':1, 'Ferrous_Non_recyclable':1, 'Al_Non_recyclable':1, 'Glass_Brown':1, 'Glass_Green':1,
                      'Glass_Clear':1, 'Mixed_Glass':1, 'Glass_Non_recyclable':1, 'Misc_Organic':1, 'Misc_Inorganic':1, 'E_waste':1, 'Aerobic_Residual':1,
                      'Anaerobic_Residual':1, 'Bottom_Ash':1, 'Fly_Ash':1, 'Diapers_and_sanitary_products':1},
             "WTE3":{'Yard_Trimmings_Leaves':1, 'Yard_Trimmings_Grass':1, 'Yard_Trimmings_Branches':1, 'Food_Waste_Vegetable':1, 'Food_Waste_Non_Vegetable':1,
                      'Wood':1, 'Wood_Other':1, 'Textiles':1, 'Rubber_Leather':1, 'Newsprint':1, 'Corr_Cardboard':1, 'Office_Paper':1, 'Magazines_':1, 'third_Class_Mail':1,
                      'Folding_Containers':1, 'Paper_Bags':1, 'Mixed_Paper':1, 'Paper_Non_recyclable':1, 'HDPE_Translucent_Containers':1, 'HDPE_Pigmented_Containers':1, 'PET_Containers':1,
                      'Plastic_Other_1_Polypropylene':1, 'Plastic_Other_2':1, 'Mixed_Plastic':1, 'Plastic_Film':1, 'Plastic_Non_Recyclable':1, 'Ferrous_Cans':1, 'Ferrous_Metal_Other':1,
                      'Aluminum_Cans':1, 'Aluminum_Foil':1, 'Aluminum_Other':1, 'Ferrous_Non_recyclable':1, 'Al_Non_recyclable':1, 'Glass_Brown':1, 'Glass_Green':1,
                      'Glass_Clear':1, 'Mixed_Glass':1, 'Glass_Non_recyclable':1, 'Misc_Organic':1, 'Misc_Inorganic':1, 'E_waste':1, 'Aerobic_Residual':1,
                      'Anaerobic_Residual':1, 'Bottom_Ash':1, 'Fly_Ash':1, 'Diapers_and_sanitary_products':1},
             "COMP":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":7},
             "COMP1":{"Yard_Trimmings_Grass":2,"Yard_Trimmings_Leaves":5},
             "COMP2":{"Yard_Trimmings_Grass":9,"Yard_Trimmings_Leaves":6},
             "COMP3":{"Yard_Trimmings_Grass":3,"Yard_Trimmings_Leaves":1}}
mojtaba.process_start_scenario(scenario3,'scenario3')
mojtaba.Do_LCA("scenario3",('IPCC 2007', 'climate change', 'GWP 100a'),1)

















     
        
        
    





