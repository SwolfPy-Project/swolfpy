# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
from building_matrices import *
from AD import *
from Composting import *
from WTE import *
from brightway2 import *
from CommonData import *
from time import time

if __name__=='__main__':
    
    Treatment_processes = {}
    Treatment_processes['AD']={'input_type':['MOC','Separated_Organics'],'model': AD()}
    Treatment_processes['COMP']={'input_type':['MOC','Separated_Organics'], 'model': Comp()}
    Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
#    Treatment_processes['WTE']={'model':WTE(),'input_type':['MWC','RWC','Other_Residual','RDF']}
#    Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
#                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
#                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}  
    
    demo = project("Organic_Analysis",Treatment_processes)
    demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
    demo.write_project()
    demo.group_exchanges()
    
    gg=[{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0},
 {'name': 'frac_of_Bottom_Ash_from_LF_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_LF_to_LF', 'amount': 1},
 {'name': 'frac_of_Separated_Organics_from_LF_to_AD', 'amount': 1},
 {'name': 'frac_of_Separated_Organics_from_LF_to_COMP', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_LF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_LF_to_WTE', 'amount': 0},
 {'name': 'frac_of_RDF_from_LF_to_WTE', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1}]
    
    demo.update_parameters(gg)
    scenario1 = {"AD":{"Yard_Trimmings_Grass":1},"COMP":{"Yard_Trimmings_Grass":2,"Paper_Bags":2,"Mixed_Plastic":2},'WTE':{"Yard_Trimmings_Grass":1}}
    demo.process_start_scenario(scenario1,'scenario1')
    
    
    demo.Do_LCA("scenario1",('IPCC 2007', 'climate change', 'GWP 100a'),1)
    
    
    Treatment_processes['AD']['model'].AD_input.Curing_Bio = {
            'ad_pCasCH4':{'Name':'Proportion of emitted C emitted as CH4','amount':0.017,'unit':None,'Referenc':'19',
                          'uncertainty_type':3,'loc':0.017,'scale':0.004},
            'ad_pNasNH3':{'Name':'Proportion of emitted N emitted as NH3','amount':0.04,'unit':None,'Referenc':'26'},
            'ad_pNasN2O':{'Name':'Proportion of emitted N emitted as N2O','amount':0.004,'unit':None,'Referenc':'19'},
            'dmRed_Dig':{'Name':'VS reduction of digestate during curing','amount':0.3,'unit':None,'Referenc':'29'},
            'VSlossPerCloss':{'Name':'Mass of VS loss per mole of C loss','amount':12,'unit':'g/mol C','Referenc':None},
            }              
    Treatment_processes['COMP']['model'].Comp_input.Biological_Degredation = {
                'pCasCH4':{"Name":"Proportion of emitted C emitted as CH4","amount":0.017,"unit":None,"Reference":'12',
                           'uncertainty_type':3,'loc':0.017,'scale':0.004},
                'pNasNH3':{"Name":"Proportion of emitted N emitted as NH3","amount":0.04,"unit":None,"Reference":'31'},
                'pNasN2O':{"Name":"Proportion of emitted N emitted as N2O","amount":0.004,"unit":None,"Reference":'12'},
                'bfCH4re':{"Name":"Biofilter CH4 removal efficiency","amount":0.15,"unit":None,"Reference":'18'},
                'bfNH3re':{"Name":"Biofilter NH3 removal efficiency","amount":48,"unit":'%',"Reference":'18'},
                'bfN2Ore':{"Name":"Biofilter N2O removal efficiency","amount":0,"unit":'%',"Reference":'18'},
                'preNH3toNOx':{"Name":"Proportion of removed NH3 that becomes NOx","amount":1,"unit":None,"Reference":'18'},
                'preNH3toN2O':{"Name":"Proportion of removed NH3 that becomes Nitrous Oxide","amount":0,"unit":None,"Reference":'18'},
                'bfVOCre':{"Name":"Biofilter VOC removal efficiency","amount":18,"unit":'%',"Reference":'32'},
                'percCStor':{"Name":"Percent of carbon in compost remaining after 100 years","amount":10,"unit":'%',"Reference":'5'},
                'percCStor_LF':{"Name":"Percent of carbon in compost remaining after 100 years","amount":100,"unit":'%',"Reference":None},
                'humFormFac':{"Name":"100 year carbon storage from humus formation","amount":0,"unit":'kg-C/kg-C in Compost',"Reference":'6'}
                }
                    
    demo.unified_params.add_uncertainty('frac_of_Other_Residual_from_AD_to_LF', loc = 0.8, scale = 0.3, uncertainty_type = 7,minimum=0,maximum=2)
    demo.unified_params.add_uncertainty('frac_of_Other_Residual_from_AD_to_WTE', loc = 0.8, scale = 0.3, uncertainty_type = 7,minimum=0,maximum=2)
    
    Treatment_processes['AD']['model'].AD_input.AD_operation = {
                'ad_lifetime':{'Name':'Facility economic lifetime','amount':20,'unit':'years','Referenc':None},
                'ophrsperday':{'Name':'Daily operating hours','amount':8,'unit':'hours','Referenc':None},
                'opdaysperyear':{'Name':'Annual operating days','amount':260,'unit':'days','Referenc':None},
                'retentionTime':{'Name':'Average retention time in reactor','amount':21,'unit':'days','Referenc':None},
                'recircMax':{'Name':'Maximum proportion of reactor water that can come from recirculation','amount':0.8,'unit':'fraction','Referenc':None},
                'isDw':{'Name':'Dewater digestate? (0=no; 1=yes)','amount':1,'unit':'0/1','Referenc':None},
                'isCured':{'Name':'Cure digestate solids stream? (0=no; 1=yes)','amount':1,'unit':'0/1','Referenc':None},
                'choice_BU':{'Name':'Digestate Beneficial Use (1) or No Beneficial Use (0)','amount':0,'unit':'0/1','Referenc':None,
                             'uncertainty_type':7,'minimum':0,'maximum':2},
                'peatOff':{'Name':'Digestate Beneficial Use offsets Peat (1 - Yes; 0 - No)','amount':1,'unit':'0/1','Referenc':None,
                           'uncertainty_type':7,'minimum':0,'maximum':2},
                'fertOff':{'Name':'Digestate Beneficial Use offsets Fertilizer (1 - Yes; 0 - No)','amount':1,'unit':'0/1','Referenc':None},
                }
    
    
    
    
    from time import time
    project = "Organic_Analysis"
    projects.set_current(project)
    db = Database("waste")
    functional_unit = {db.get("scenario1") : 1}
    method = ('IPCC 2007', 'climate change', 'GWP 100a')
    
    
    CommonData = CommonData()
    process_models = list()
    process_model_names = list()
        
    CommonData.Land_app = {
                'cmpLandDies':{"Name":"Compost application diesel use","amount":0.8,"unit":'L/Mg compost',"Reference":None,
                               'uncertainty_type':3,'loc':0.8,'scale':0.2},
                'NO3runoff':{"Name":"Nitrogen runoff to surface water","amount":0.14,"unit":'kg N/kg N applied',"Reference":None},
                'NO3leach':{"Name":"Nitrogen leaching to ground water","amount":0.135,"unit":'kg N/kg N applied',"Reference":'23'},
                'MFEN':{"Name":"Nitrogen mineral fertilizer equivalent","amount":0.4,"unit":'kg N/kg N applied',"Reference":None},
                'MFEP':{"Name":"Phosphorus mineral fertilizer equivalent","amount":1,"unit":'kg N/kg N applied',"Reference":None},         
                'MFEK':{"Name":"Potassium mineral fertilizer equivalent","amount":1,"unit":'kg N/kg N applied',"Reference":None},
                'DslAppN':{"Name":"Fertilizer - Diesel fuel for application per kg N","amount":0.00229 ,"unit":'L/kg',"Reference":None},
                'DslAppP':{"Name":"Fertilizer - Diesel fuel for application per kg P","amount":0.00186 ,"unit":'L/kg',"Reference":None},
                'DslAppK':{"Name":"Fertilizer - Diesel fuel for application per kg K","amount":0.00125 ,"unit":'L/kg',"Reference":None},
                'fert_NO3Run':{"Name":"Fertilizer - Nitrate runoff to surface water","amount":10 ,"unit":'%',"Reference":None},
                'fert_NO3Leach':{"Name":"Fertilizer - Nitrate leaching to ground water","amount":10 ,"unit":'%',"Reference":None},
                'fert_N2O':{"Name":"Fertilizer - N released as N2O","amount":2.3 ,"unit":'%',"Reference":None},
                'fert_NH3':{"Name":"Fertilizer - N as NH3","amount":50 ,"unit":'%',"Reference":None},
                'fert_NH3Evap':{"Name":"Fertilizer - NH3 evaporated","amount":5 ,"unit":'%',"Reference":None}
                        }


    process_models.append(Treatment_processes['AD']['model'])
    process_model_names.append('AD')
# =============================================================================
#     process_models.append(Treatment_processes['COMP']['model'])
#     process_model_names.append('COMP')
#     process_models.append(Treatment_processes['WTE']['model'])
#     process_model_names.append('WTE')
# =============================================================================
    
    t1 = time()
    n=100
    #a = ParallelData(functional_unit, method, project,process_models=process_models,process_model_names=process_model_names)
    a = ParallelData(functional_unit, method, project,process_models=process_models,process_model_names=process_model_names,parameters=demo.unified_params,common_data=CommonData,seed = 1)
    #a = ParallelData(functional_unit, method, project,parameters=demo.unified_params)
    
    a.run(4,n)
    t2=time()
    print(n, 'runs in: ', t2-t1)
# =============================================================================
#     from matplotlib.pylab import *
#     hist(a.results, density=True, histtype="step")
#     xlabel('(IPCC 2007, climate change, GWP 100a)')
#     ylabel("Probability")
# =============================================================================
    













     
        
        
    





