# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:04:55 2020

@author: msmsa
"""

from swolfpy.ProcessModels import Reprocessing
from brightway2 import *
projects.set_current('demo')
AA=Reprocessing.REPROC()
AAA=AA.report()


flow= 'Office_Paper'
A_param= []
A_value = []
A_name = []
A_unit = []
for x in ['Waste']:
    for y in AAA[x][flow].keys():
        A_param.append(y)
        A_value.append(AAA[x][flow][y])
        

A_param= []
A_value = []
A_name = []
A_unit = []
for x in ['Technosphere','Biosphere']:
    for y in AAA[x][flow].keys():
        A_param.append(y)
        CC=get_activity(y).as_dict()
        if 'categories' in CC.keys():
            A_name.append(CC['name']+' '+str(CC['categories']))
        else:
            A_name.append(CC['name'])
        
        A_value.append(AAA[x][flow][y])
        A_unit.append(CC['unit'])
        