# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 18:44:04 2019

@author: msardar2
"""
from project_class import *
from building_matrices import *
from AD import *
from Composting import *
from brightway2 import *
from time import time

Treatment_processes = {}
Treatment_processes['AD']={'input_type':['MOC','Separated_Organics'],'model': AD()}
Treatment_processes['COMP']={'input_type':['MOC','Separated_Organics'], 'model': Comp()}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
   

project = "demo_5"
projects.set_current(project)
db = Database("waste")
functional_unit = {db.get("scenario1") : 1}
method = ('IPCC 2007', 'climate change', 'GWP 100a')



process_models = list()
process_model_names = list()
    
process_models.append(Treatment_processes['AD']['model'])
process_models.append(Treatment_processes['COMP']['model'])
process_model_names.append('AD')
process_model_names.append('COMP')


t1 = time()
n=40
a = ParallelData(functional_unit, method, project, process_models, process_model_names)
a.run(4,n)
t2=time()
print(n, 'runs in: ', t2-t1)
from matplotlib.pylab import *
hist(a.results, density=True, histtype="step")
xlabel('(IPCC 2007, climate change, GWP 100a)')
ylabel("Probability")