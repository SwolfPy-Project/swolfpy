# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:21:53 2019

@author: msmsa
"""
from brightway2 import *
import time


class process_data():
    pass

    def __init__(self,dbname):
        Database(dbname).register()
        self.db = Database(dbname)
    
    def read(self,data):
        self.data = data
        A=time.time()
        for x in self.data['Biosphere'].keys():
            self.db.new_activity(code = x , name = x, location = "GLO", comment = " -- ", type = "process", unit = "Mg" ).save()
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
        
        
