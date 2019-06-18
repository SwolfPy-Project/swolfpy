# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:53:10 2019

@author: msmsa
"""

from project_class import *
Treatment_processes = {}
Treatment_processes['AD']={'path':"AD_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['LF1']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}
Treatment_processes['SSMRF']={'path':"SS_MRF_BW2.csv",'input_type':['SSRC']}
Treatment_processes['WTE']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE1']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}


mojtaba = project("demo4",Treatment_processes)
mojtaba.init_project('SWOLF_AccountMode_LCI DATA.csv')
mojtaba.write_project()
mojtaba.group_exchanges()