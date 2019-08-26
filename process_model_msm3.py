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
from Parameters import *
#elementary_flows =load_Elementary_flows("Elementary flows_EcoinventV3.csv")
#biosphere_keys = create_biosphere_key(elementary_flows)



class Process_Model():

    def __init__(self, process_name,waste_treatment):
        self.process_model_output = {}
        self.process_name = process_name
        self.DB_waste_name =self.process_name +'_product'
        
        self.waste_treatment=waste_treatment

        
        #Databases
        self.database_biosphere = Database("biosphere3")
        self.database_Waste = Database(self.DB_waste_name)
        ### ==========================
        self.database_Waste_technosphere = Database("Technosphere")
        ### ==========================
		
        self.uncertain_parameters = Parameters()
        
    
    def check_nan(self, x):  # replace zeros when there is no data ("nan")
        if str(x) == "nan":
            return 0
        return x
    
    def read_output_from_SWOLF (self, filepath):  #excel file
        if 'xlsx' in filepath:
            outputdata = pd.ExcelFile(filepath)
            data = outputdata.parse(header=None)
        else:
            data=pd.read_csv(filepath,header=None)
        waste = (data[np.arange(2,31).tolist()][8:69]).to_dict()
        technosphere = (data[[2]+np.arange(33,78).tolist()][8:69]).to_dict()
        biosphere =  (data[np.arange(0,63).tolist()][71:1824]).to_dict()
        
        # revising the waste dictionary. waste[key1][key2] , key1: waste fraction , key2: Waste_stream
        CC=[waste[i][8] for i in np.arange(2,31)]  # name of the prodcuts _ waste
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
        
        
        #### removing the zero emisisons
        
        
        
        
        self.process_model_output ["process name"] = self.process_name
        self.process_model_output ["Waste"] = waste
        self.process_model_output ["Technosphere"] = technosphere
        self.process_model_output ["Biosphere"] = biosphere
        return (self.process_model_output)
    
    
    def init_DB(self,Data_bsae_name):
        self.db_data ={}
        self.DB_name = Data_bsae_name
        for x in  MSW_Fractions:
            self.db_data[(self.DB_name,x)] ={}    # add activity to database
            self.db_data[(self.DB_name,x)]['name'] = self.DB_name+"_"+x
            self.db_data[(self.DB_name,x)]['unit'] = 'Mg'
            self.db_data[(self.DB_name,x)]['exchanges'] =[]
        db = Database(self.DB_name)
        db.write(self.db_data)
        
    
    def Write_DB (self,Data_bsae_name):
        self.db_data ={}
        self.db_waste_data={}
        self.DB_name = Data_bsae_name
        self.parameters=[]
        self.list_of_params=[]
        self.act_in_group =set()
        self.params_dict = dict()
        for x in  self.process_model_output ["Waste"].keys():
            self.db_data[(self.DB_name,x)] ={}    # add activity to database
            self.db_data[(self.DB_name,x)]['name'] = self.DB_name+"_"+x
            self.db_data[(self.DB_name,x)]['unit'] = 'Mg'
            self.db_data[(self.DB_name,x)]['exchanges'] =[]
            
            
            for key in self.process_model_output ["Waste"][x]:
                #if self.process_model_output ["Waste"][x][key] != 0:
                if True:
                    if key in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual',
                     'RDF','Al','Fe','Cu']:
                        ex = {}                        # add exchange to activities
                        ex['amount'] = self.process_model_output ["Waste"][x][key]
                        ex['input'] = (self.process_name+'_product' , x+'_'+key)
                        ex['type'] = 'technosphere'
                        ex['unit'] = 'Mg'
                        self.db_data[(self.DB_name,x)]['exchanges'].append(ex)
                        
                        self.db_waste_data[(self.DB_waste_name,x+'_'+key)] ={}    # add activity to Waste_database
                        self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['name'] = self.DB_waste_name+"_"+x+'_'+key
                        self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['unit'] = 'Mg'
                        self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'] =[]
                        self.act_in_group.add((self.DB_waste_name,x+'_'+key))
                        if key in ['Bottom_Ash','Fly_Ash']:
                            for p in self.waste_treatment[key]:
                                ex = {}                        # add exchange to activities
                                ex['amount'] = 0
                                ex['input'] = (p ,key)
                                ex['type'] = 'technosphere'
                                ex['unit'] = 'Mg'
                                ex['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p 
                                if "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p not in self.list_of_params:
                                    self.parameters.append({'name':"frac_of_"+key+'_from_'+self.DB_name+'_to_'+p ,'amount':0})
                                    self.list_of_params.append("frac_of_"+key+'_from_'+self.DB_name+'_to_'+p)
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p] = set()
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((p,key),(self.process_name+'_product' , x+'_'+key)))
                                    self.uncertain_parameters.add_parameter(key,self.DB_name,p)									
                                else:
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((p,key),(self.process_name+'_product' , x+'_'+key)))									
                                self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'].append(ex)
                        else:
                            for p in self.waste_treatment[key]:
                                ex = {}                        # add exchange to activities
                                ex['amount'] = 0
                                ex['input'] = (p ,x)
                                ex['type'] = 'technosphere'
                                ex['unit'] = 'Mg'
                                ex['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p
                                if "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p not in self.list_of_params:
                                    self.parameters.append({'name':"frac_of_"+key+'_from_'+self.DB_name+'_to_'+p ,'amount':0})
                                    self.list_of_params.append("frac_of_"+key+'_from_'+self.DB_name+'_to_'+p)
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p] = set()
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((p,x),(self.process_name+'_product' , x+'_'+key)))
                                    self.uncertain_parameters.add_parameter(key,self.DB_name,p)									
                                else:
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((p,x),(self.process_name+'_product' , x+'_'+key)))								
                                self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'].append(ex)
                            
                                
                    else:
                        ex = {}                        # add exchange to activities
                        ex['amount'] = self.process_model_output ["Waste"][x][key]
                        ex['input'] = (self.process_name+'_product' ,key)
                        ex['type'] = 'technosphere'
                        ex['unit'] = 'Mg'
                        self.db_data[(self.DB_name,x)]['exchanges'].append(ex)
                        
                        self.db_waste_data[(self.DB_waste_name,key)] ={}    # add activity to Waste_database
                        self.db_waste_data[(self.DB_waste_name,key)]['name'] = self.DB_waste_name+'_'+key
                        self.db_waste_data[(self.DB_waste_name,key)]['unit'] = 'Mg'
                        self.db_waste_data[(self.DB_waste_name,key)]['exchanges'] =[]
                        self.act_in_group.add((self.DB_waste_name,key))
                        
# =============================================================================
#                         for p in self.waste_treatment[key]:
#                             ex = {}                        # add exchange to activities
#                             ex['amount'] = 0
#                             ex['input'] = (p ,key)
#                             ex['type'] = 'technosphere'
#                             ex['unit'] = 'Mg'
#                             ex['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p
#                             self.db_waste_data[(self.DB_waste_name,key)]['exchanges'].append(ex)
# =============================================================================
                        
          
            for key in self.process_model_output ["Technosphere"][x]:
                #if self.process_model_output ["Technosphere"][x][key] != 0:
                if True:
                    ex = {}                        # add exchange to activities
                    ex['amount'] = self.process_model_output ["Technosphere"][x][key]
                    ex['input'] = key
                    ex['type'] = 'technosphere'
                    self.db_data[(self.DB_name,x)]['exchanges'].append(ex)
                    
            for key in self.process_model_output ["Biosphere"][x]:
                #if self.process_model_output ["Biosphere"][x][key] != 0:
                if True:
                    ex = {}                        # add exchange to activities
                    ex['amount'] = self.process_model_output ["Biosphere"][x][key]
                    ex['input'] = key
                    ex['type'] = 'biosphere'
                    ex['unit'] = 'kg'
                    self.db_data[(self.DB_name,x)]['exchanges'].append(ex)
                    

        self.database_Waste.write(self.db_waste_data)
        db = Database(self.DB_name)
        db.write(self.db_data)
        self.uncertain_parameters.set_params_dict(self.params_dict)
        return(self.parameters,self.act_in_group)
