# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:10:43 2019

@author: msmsa
"""
from brightway2 import *
from db_handler import *
import pandas as pd

data=pd.read_csv('Collection_BW2.csv')

if "Collection_SF" in databases:
    Database("Collection_SF").delete()

db = Database("Collection_SF")


for i in range(60):
    for x in ['Residual_Collection', 'Single_Stream_Recycling','Yardwaste_SSO']:
        if data.at[i,x] != 0:
            db.new_activity(code = str("Collection_"+ data.at[i,'Waste_Fraction']+"_"+x) , name = str("Collection_"+ data.at[i,'Waste_Fraction']+"_"+x), location = "GLO", comment = " -- ", type = "process", unit = "Mg" ).save()
            


i=0
ex={}
for y in self.data['Biosphere'][x].keys():
if self.data['Biosphere'][x][y] != 0:
ex[i] = self.db.get(x).new_exchange(input=y,amount=self.data['Biosphere'][x][y],type="biosphere")
ex[i]['uncertainty type'],ex[i]['loc'], ex[i]['scale'] = 3, self.data['Biosphere'][x][y], 0.1* abs(self.data['Biosphere'][x][y])
i+=1
for y in self.data['Technosphere'][x].keys():
if self.data['Technosphere'][x][y] != 0:
ex[i] = self.db.get(x).new_exchange(input=y,amount=self.data['Technosphere'][x][y],type="technosphere")
ex[i]['uncertainty type'],ex[i]['loc'], ex[i]['scale'] = 3, self.data['Technosphere'][x][y], 0.1* abs(self.data['Technosphere'][x][y])
i+=1
#               for y in self.data['Waste'][x].keys():
#                   if self.data['Waste'][x][y] != 0:
#                       ex = self.db.get(x).new_exchange(input=y,amount=self.data['Waste'][x][y],type="Waste")
#                       ex['uncertainty type'],ex['loc'], ex['scale'] = 3, self.data['Waste'][x][y], 0.1* abs(self.data['Waste'][x][y])
#                       ex.save()
#                        i+=1
self.db.get(x).save()    
B=time.time()
print("Time =",B-A)    
