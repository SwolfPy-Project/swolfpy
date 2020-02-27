# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:14:31 2019

@author: msmsa
"""
from brightway2 import *
import pandas as pd
from biosphere_keys import *

def check_nan(x):  # replace zeros when there is no data ("nan")
    if str(x) == "nan":
        return 0
    return x

data ={}

database_name='Technosphere'

if database_name in databases:
    del databases[database_name]   
        
path ="SWOLF_AccountMode_LCI DATA.csv"
outputdata1 = pd.read_csv(path)
# activities
names = [x for x in outputdata1.columns][3:]

for x in names:
    data[(database_name,x)] ={}    # add activity to database
    data[(database_name,x)]['name'] = x
    data[(database_name,x)]['unit'] = check_nan(outputdata1[x][0])
    data[(database_name,x)]['exchanges'] =[]
    i=0
    for val in outputdata1[x][1:]:
        if float(check_nan(val)) != 0:
            ex = {}                        # add exchange to activities
            ex['amount'] = float(check_nan(val))
            ex['input'] = biosphere_keys[i][0]
            ex['type'] = 'biosphere'
            ex['unit'] = 'kg'
            data[(database_name,x)]['exchanges'].append(ex)
        i+=1

db = Database(database_name)
db.write(data)
