# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:42:51 2019

@author: msmsa
"""
import pandas as pd
import numpy as np
from biosphere_key import *
from brightway2 import *
# Reading the keys 
from Required_keys import *
#elementary_flows =load_Elementary_flows("Elementary flows_EcoinventV3.csv")
#biosphere_keys = create_biosphere_key(elementary_flows)


class Process_Model():

    def __init__(self):
        self.process_model_output = {}
        #Databases
        self.database_biosphere = Database("biosphere3")
        self.database_Waste = Database("Waste")
        ### ==========================
        self.database_Waste_technosphere = Database("Technosphere")
        ### ==========================
        
    
    def check_nan(self, x):  # replace zeros when there is no data ("nan")
        if str(x) == "nan":
            return 0
        return x
    
    def read_output_from_SWOLF (self, process_name, filepath):  #excel file
        if 'xlsx' in filepath:
            outputdata = pd.ExcelFile(filepath)
            data = outputdata.parse(header=None)
        else:
            data=pd.read_csv(filepath,header=None)
        waste = (data[np.arange(2,31).tolist()][8:69]).to_dict()
        technosphere = (data[[2]+np.arange(33,78).tolist()][8:69]).to_dict()
        biosphere =  (data[np.arange(0,63).tolist()][71:1824]).to_dict()
        
        # revising the waste dictionary. waste[key1][key2] , key1: waste fraction , key2: Waste_stream
        CC=[("Waste",str(i) + "_"+waste[i][8]) for i in np.arange(2,31)]  # name of the prodcuts _ waste
        y=2
        for x in CC:
            waste[x]=waste.pop(y)
            y+=1   
            
        waste_fractions=[waste[[x for x in waste.keys()][0]][i] for i in np.arange(8,69)]  # name of the material fractions
        waste_fractions[0]="Product"
        DD=[x for x in waste.keys()]
        for x in DD:
            yy=8
            for tt in waste_fractions:
                waste[x][tt]=waste[x].pop(yy)
                yy+=1
            waste[x].pop('Product')
        waste.pop([x for x in waste.keys()][0])
    
        TT=[x for x in waste.keys()]  # new waste.keys that doesn't have ("2 : Waste Fractions")   
        VV={}
        for x in waste_fractions[1:]:
            VV[x] = {}
            for y in TT:
                VV[x][y] = float(self.check_nan(waste[y][x]))
        waste=VV
        
        
        # revising the technosphere dictionary. technosphere[key1][key2] , key1: waste fraction , key2: technosphere stream
        EE=[str(i) + " : "+technosphere[i][8] for i in ([2]+np.arange(33,78).tolist())]  # name of the prodcuts _ waste
        technosphere[EE[0]]=technosphere.pop(2)
        y=33
        for x in EE[1:]:
            technosphere[x]=technosphere.pop(y)
            y+=1
            
        FF=[x for x in technosphere.keys()]
        for x in FF:
            yy=8
            for tt in waste_fractions:
                technosphere[x][tt]=technosphere[x].pop(yy)
                yy+=1
                
        technosphere.pop([x for x in technosphere.keys()][0])
        
        i = 0
        DD=[x for x in technosphere.keys()]
        for x in DD:
            technosphere[technosphere_keys[i][0]] = technosphere.pop(x)
            technosphere[technosphere_keys[i][0]].pop('Product')
            i+=1
            
        CC= [x for x in technosphere.keys()]
        VV={}
        for x in waste_fractions[1:]:
            VV[x] = {}
            for y in CC:
                VV[x][y] = float(self.check_nan(technosphere[y][x]))
        technosphere=VV
        
        # revising the biosphere. biosphere[key1][key2] , key1: stream, key2: waste fraction
        l = 3
        for z in waste_fractions[1:]:
            biosphere[z] = biosphere.pop(l)
            l += 1
        biosphere.pop(0)
        biosphere.pop(1)
        biosphere.pop(2)
        
        for z in waste_fractions[1:]:
            biosphere[z].pop(71)
            pp=72
            nn=1
            for oo in biosphere_keys.values():
                biosphere[z][oo[0]]=float(self.check_nan(biosphere[z].pop(pp)))
                pp += 1   
        
        
        self.process_model_output ["process name"] = process_name
        self.process_model_output ["Waste"] = waste
        self.process_model_output ["Technosphere"] = technosphere
        self.process_model_output ["Biosphere"] = biosphere
        return (self.process_model_output)
    
    
    def Write_DB (self,Data_bsae_name):
        self.db_data ={}
        self.DB_name = Data_bsae_name
        for x in  self.process_model_output ["Waste"].keys():
            self.db_data[(self.DB_name,x)] ={}    # add activity to database
            self.db_data[(self.DB_name,x)]['name'] = self.DB_name+"_"+x
            self.db_data[(self.DB_name,x)]['unit'] = 'Mg'
            self.db_data[(self.DB_name,x)]['exchanges'] =[]
                    
        db = Database(self.DB_name)
        db.write(self.db_data)

    
def import_database(name,path):
    process = Process_Model()
    process_data = process.read_output_from_SWOLF(name,path)
    process.Write_DB(name)
    return()   
    

import_database("LF","trad_landfill _BW2.xlsx")
import_database("WTE", "WTE_BW2.csv")
import_database("REPROC", "Material_Reprocessing_BW2.csv")
import_database("AD", "AD_BW2.csv")
import_database("COMP", "Composting_BW2.csv")
import_database("SS_MRF", "SS_MRF_BW2.csv")