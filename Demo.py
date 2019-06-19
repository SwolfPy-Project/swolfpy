# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from brightway2 import *
from process_model_msm2 import *
import time
projects.set_current("Base_new")


def import_database(name,path,Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination):
    process = Process_Model(name,Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
    process_data = process.read_output_from_SWOLF(path)
    process.Write_DB(name)
    return()
  
# =============================================================================
# xx= [x for x in databases]
# for x in xx:
#     if x not in ['biosphere3','ecoinvent_test','Technosphere']:
#         del databases[x]
# =============================================================================
        
# MWC, RWC , SSRC ,DSRC , MSRC, LVC, MOC, WETC, DRYC, RDOC , YWDC , MSDC

Treatment_processes = {}
Treatment_processes['AD']={'path':["AD_BW2.csv"],'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':["Composting_BW2.csv"],'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':["trad_landfill _BW2.xlsx"],'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':["Material_Reprocessing_BW2.csv"],'input_type':['Al','Fe']}
Treatment_processes['SSMRF']={'path':["SS_MRF_BW2.csv"],'input_type':['SSRC']}
Treatment_processes['WTE']={'path':["WTE_BW2.csv"],'input_type':['MWC','RWC','Other_Residual']}

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




import_database("LF","trad_landfill _BW2.xlsx",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
import_database("WTE", "WTE_BW2.csv",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
import_database("REPROC", "Material_Reprocessing_BW2.csv",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
import_database("AD", "AD_BW2.csv",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
import_database("COMP", "Composting_BW2.csv",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
import_database("SS_MRF", "SS_MRF_BW2.csv",Bottom_Ash_destination,Other_Residual_destination,Fly_Ash_destination,Separated_Organics_destination,Al_destination,Fe_destination,RDF_destination)
