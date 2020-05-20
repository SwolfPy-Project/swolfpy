# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 19:20:43 2020

@author: msmsa
"""
import pandas as pd
from brightway2 import *
from swolfpy import *
from swolfpy_inputdata import *
from swolfpy_processmodels import *



technosphere = Technosphere('demo')
common_data = CommonData()
Treatment_processes = {}
Treatment_processes['LF']={'input_type':['RWC','Bottom_Ash','Fly_Ash','Other_Residual'],'model': LF()}
Treatment_processes['WTE']={'input_type':['RWC','Other_Residual'],'model': WTE()}

# Distance            
Processes = ['LF','WTE','SF_COl']
Data = pd.DataFrame([[None,20,20],[None,None,20],[None,None,None]],index=Processes,columns=Processes)
distance = Distance(Data=Data)

# Collection_processes:
Col_scheme=SF_Col.scheme()
Col_scheme['RWC']['Contribution'] = 1
Collection_processes={}
Collection_processes['SF_COl']={'input_type':[],'model': SF_Col('SF_COl',Col_scheme,Treatment_processes=Treatment_processes,Distance=distance)}      

# project
demo = Project('demo',common_data,Treatment_processes,distance,Collection_processes,technosphere)
demo.init_project()
demo.write_project()

demo.group_exchanges()

demo.update_parameters(demo.parameters.default_parameters_list())



# =============================================================================
# =============================================================================
#                              Monte Carlo analysis
# =============================================================================
# =============================================================================
### Monte Carlo analysis
projects.set_current('demo')
db = Database("SF_COl")
functional_unit = {db.get('Yard_Trimmings_Grass').key : 1}
method = [('IPCC 2007 (obsolete)', 'climate change', 'GWP 100a')]
project = 'demo'
process_models = []
process_model_names = []
process_models.append(Treatment_processes['SF_COl']['model'])
process_model_names.append('SF_COl')
MonteCarlo = Monte_Carlo(functional_unit, method, project, process_models = process_models, process_model_names = process_model_names, common_data = None, parameters = None,seed = None)
MonteCarlo.run(4,100)
res = MonteCarlo.result_to_DF()


### add uncertainty to process models
Treatment_processes['SF_COl']['model'].InputData.Col['res_gen'] = {'Name': 'Residential Generation rate',
                                                                     'amount': 1.3608,
                                                                     'unit': 'kg/person-day',
                                                                     'uncertainty_type': 3,
                                                                     'loc': 1.3608,
                                                                     'scale': 0.2,
                                                                     'shape': None,
                                                                     'minimum': None,
                                                                     'maximum': None,
                                                                     'Reference': None,
                                                                     'Comment': None}

MonteCarlo.run(4,100)
res = MonteCarlo.result_to_DF()

### add uncertainty to Common Data
demo.CommonData.Land_app['MFEN']={'Name': 'Nitrogen mineral fertilizer equivalent',
                                     'amount': 0.4,
                                     'unit': 'kg N/kg N applied',
                                     'uncertainty_type': 3,
                                     'loc': 0.6,
                                     'scale': 0.2,
                                     'shape': None,
                                     'minimum': None,
                                     'maximum': None,
                                     'Reference': None,
                                     'Comment': None}

MonteCarlo = Monte_Carlo(functional_unit, method, project, process_models = process_models, process_model_names = process_model_names, common_data = demo.CommonData, parameters = None,seed = None)
MonteCarlo.run(4,100)
res = MonteCarlo.result_to_DF()

### add uncertainty to parameters
demo.parameters.add_uncertainty('frac_of_RWC_from_SF_COl_to_LF', loc = 0.8, scale = 0.2, uncertainty_type = 3)
MonteCarlo = Monte_Carlo(functional_unit, method, project, process_models = None, process_model_names = None, common_data = None, parameters = demo.parameters,seed = None)
MonteCarlo.run(4,100)
res = MonteCarlo.result_to_DF()




# =============================================================================
# =============================================================================
#                              Optimization
# =============================================================================
# =============================================================================

### Optimizaiton
db = Database("SF_COl")
functional_unit = {db.get('Yard_Trimmings_Grass').key : 1}
method = [('IPCC 2007 (obsolete)', 'climate change', 'GWP 100a')]

from swolfpy import Optimization
Opt = Optimization(functional_unit, method,demo)

Opt.plot_sankey(optimized_flow=False)

Opt.optimize_parameters()
Opt.plot_sankey(optimized_flow=True)

Opt.multi_start_optimization()
Opt.plot_sankey(optimized_flow=True)

constraints = {}
constraints['WTE'] = {'limit':600, 'KeyType':'Process','ConstType':"<="}
Opt.optimize_parameters(constraints)
Opt.plot_sankey(optimized_flow=True)

constraints = {}
constraints[('WTE','Yard_Trimmings_Grass')] = {'limit':300, 'KeyType':'WasteToProcess','ConstType':"<="}
Opt.optimize_parameters(constraints)
Opt.plot_sankey(optimized_flow=True)

constraints = {}
constraints[('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')] = {'limit':290000,'KeyType':'Emission','ConstType':"<="}
Opt.optimize_parameters(constraints)
Opt.plot_sankey(optimized_flow=True)



