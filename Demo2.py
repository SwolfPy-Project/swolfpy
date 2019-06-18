# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
from process_model_msm3 import *
import time
projects.set_current("msm5")


Treatment_processes = {}
Treatment_processes['AD']={'path':"AD_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}
Treatment_processes['SSMRF']={'path':"SS_MRF_BW2.csv",'input_type':['SSRC']}
Treatment_processes['WTE']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}



def init_database(name,waste_treatment):
    process = Process_Model(name,waste_treatment)
    process.init_DB(name)


def import_database(name,path,waste_treatment):
    process = Process_Model(name,waste_treatment)
    process_data = process.read_output_from_SWOLF(path)
    (P,G)=process.Write_DB(name)
    return((P,G))
    
  
xx= [x for x in databases]
for x in xx:
    if x not in ['biosphere3','ecoinvent_test','Technosphere']:
        del databases[x]
        
# MWC, RWC , SSRC ,DSRC , MSRC, LVC, MOC, WETC, DRYC, RDOC , YWDC , MSDC

LF
Other_Residual_destination=[]
Separated_Organics_destination=[]
Bottom_Ash_destination=[]
Fly_Ash_destination=[]
Al_destination=[]
Fe_destination=[]
MWC_destination=[]
RWC_destination=[]
MOC_destination=[]
SSRC_destination=[]
RDF_destination=[]
Rec_destination = ['REPROC']

for p in Treatment_processes:
    if 'Other_Residual' in Treatment_processes[p]['input_type']:
        Other_Residual_destination.append(p)
    if 'RDF' in Treatment_processes[p]['input_type']:
        RDF_destination.append(p)
    if 'Separated_Organics' in Treatment_processes[p]['input_type']:
        Separated_Organics_destination.append(p)
    if 'Bottom_Ash' in Treatment_processes[p]['input_type']:
        Bottom_Ash_destination.append(p)        
    if 'Fly_Ash' in Treatment_processes[p]['input_type']:
        Fly_Ash_destination.append(p)    
    if 'Al' in Treatment_processes[p]['input_type']:
        Al_destination.append(p)    
    if 'Fe' in Treatment_processes[p]['input_type']:
        Fe_destination.append(p)    
    if 'MWC' in Treatment_processes[p]['input_type']:
        MWC_destination.append(p)    
    if 'RWC' in Treatment_processes[p]['input_type']:
        RWC_destination.append(p)    
    if 'MOC' in Treatment_processes[p]['input_type']:
        MOC_destination.append(p)    
    if 'SSRC' in Treatment_processes[p]['input_type']:
        SSRC_destination.append(p)




waste_treatment['Wastewater']=[]

init_database("WTE",waste_treatment)
init_database("REPROC",waste_treatment)
init_database("LF",waste_treatment)
init_database("AD",waste_treatment)
init_database("COMP",waste_treatment)
init_database("SS_MRF",waste_treatment)


(P1,G1)=import_database("LF","trad_landfill _BW2.xlsx",waste_treatment)
(P2,G2)=import_database("WTE", "WTE_BW2.csv",waste_treatment)
(P3,G3)=import_database("REPROC", "Material_Reprocessing_BW2.csv",waste_treatment)
(P4,G4)=import_database("AD", "AD_BW2.csv",waste_treatment)
(P5,G5)=import_database("COMP", "Composting_BW2.csv",waste_treatment)
(P6,G6)=import_database("SS_MRF", "SS_MRF_BW2.csv",waste_treatment)






for x in G2:
    bw2.parameters.add_exchanges_to_group("WTE",x)









