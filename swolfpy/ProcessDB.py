# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:42:51 2019

@author: msmsa
"""
import pandas as pd
import numpy as np
from brightway2 import *
from .Parameters import *


class ProcessDB():
    def __init__(self, process_name,waste_treatment,Distance=None):
        self.Report = {}
        self.P_Name = process_name
        self.P_Pr_Name =self.P_Name +'_product'
        self.Distance = Distance
        
        self.waste_treatment=waste_treatment

        #Databases
        self.database_biosphere = Database("biosphere3")
        self.database_Product = Database(self.P_Pr_Name)
        ### ==========================
        self.database_Waste_technosphere = Database("Technosphere")
        ### ==========================
        

    def check_nan(self, x):  # replace zeros when there is no data ("nan")
        if str(x) == "nan":
            return 0
        return x

    @staticmethod
    def init_DB(DB_name,waste_flows):
        db_data ={}
        for x in waste_flows:
            db_data[(DB_name,x)] ={}    # add activity to database
            db_data[(DB_name,x)]['name'] = DB_name+"_"+x
            db_data[(DB_name,x)]['unit'] = 'Mg/year'
            db_data[(DB_name,x)]['exchanges'] =[]
        
        print("""
              ####
              ++++++ Initializing the {}        
              """.format(DB_name))
        
        db = Database(DB_name)
        db.write(db_data)
        
    
    def Write_DB (self,waste_flows,parameters,Process_Type):
        """
        .. _Write_DB:
        
            
        """
        self.db_data ={}
        self.db_Pr_data={}
        self.parameters=[] # List of dictionaries ({'name':Formula ,'amount':0})
        self.list_of_params=[] # List of parameters name
        self.act_in_group =set()
        self.params_dict = dict()  # Dictionary that has set() include the key (input,act) for all the exchanges with parameters.
        self.uncertain_parameters = parameters
        
        for x in  waste_flows:    # x is waste fraction
            self.db_data[(self.P_Name,x)] ={}    # add activity to database
            self.db_data[(self.P_Name,x)]['name'] = self.P_Name+"_"+x
            if Process_Type == 'Collection':
                self.db_data[(self.P_Name,x)]['unit'] = '{} Mg/year'.format(np.round(sum(self.Report["Waste"][x].values()),decimals=2))
            else:
                self.db_data[(self.P_Name,x)]['unit'] = 'Mg/year'
            self.db_data[(self.P_Name,x)]['exchanges'] =[]

# =============================================================================
#                 if key in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual',
#                  'RDF','Al','Fe','Cu','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO',
#                  'OCC','Mixed_Paper','ONP','OFF','Fiber_Other','PET','HDPE_Unsorted','HDPE_P','HDPE_T','PVC','LDPE_Film',
#                  'Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic','Brown_glass','Clear_glass','Green_glass','Mixed_Glass']:
# =============================================================================

            for key in self.Report["Waste"][x]:
                
                ex = self.exchange((self.P_Pr_Name , x+'_'+key),'technosphere','Mg/year',self.Report["Waste"][x][key])
                self.db_data[(self.P_Name,x)]['exchanges'].append(ex)
                
                self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)] ={}    # add activity to Waste_database
                self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['name'] = self.P_Pr_Name+"_"+x+'_'+key
                self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['unit'] = 'Mg/year'
                self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'] =[]
                self.act_in_group.add((self.P_Pr_Name,x+'_'+key))
                
                #Streams that are not the same with their source.
                if key in ['Bottom_Ash','Fly_Ash',
                           'Al','Fe','Cu',
                           'OCC','Mixed_Paper','ONP','OFF','Fiber_Other',
                           'Brown_glass','Clear_glass','Green_glass','Mixed_Glass',
                           'PET','HDPE_Unsorted','HDPE_P','HDPE_T','PVC','LDPE_Film','Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic']:
                    #finding the destination
                    for p in self.waste_treatment[key]:
                        #adding exchange to waste processing
                        ex = self.exchange((p ,key),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p,Act=(self.P_Pr_Name,x+'_'+key),product=key)
                        self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex)
                        
                        #addin exchange for transportation between the process models
                        ex_trnp = self.exchange((self.P_Pr_Name ,self.P_Name+'_'+'to'+'_'+p),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p ,Act=(self.P_Pr_Name,x+'_'+key),product=key)
                        self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex_trnp)
                                   
                #Streams that are same with the source.
                elif key in ['Separated_Organics','Other_Residual','RDF']:  
                    #finding the destination
                    for p in self.waste_treatment[key]:
                        #adding exchange to waste processing
                        ex = self.exchange((p ,x),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p ,Act=(self.P_Pr_Name,x+'_'+key) ,product=key)                      
                        self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex)
                        
                        #addin exchange for transportation between the process models
                        ex_trnp = self.exchange((self.P_Pr_Name ,self.P_Name+'_'+'to'+'_'+p),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p ,Act=(self.P_Pr_Name,x+'_'+key) ,product=key)
                        self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex_trnp)
                
                #Collection streams. Transportation between the collection and treatment processes are calculate inside collection model.
                elif key in ['RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:            
                    #finding the destination
                    for p in self.waste_treatment[key]:
                        #adding exchange to waste processing
                        ex = self.exchange((p ,x),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p ,Act=(self.P_Pr_Name,x+'_'+key) ,product=key)                      
                        self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex)            
            
                        #addin exchange for transportation between the collection sector and treatment processs
                        if p in self.Report['LCI'][key].keys():
                            ex_trnp = self.exchange((self.P_Pr_Name ,key+'_'+'to'+'_'+p),'technosphere','Mg/year',0,Formula="frac_of_"+key+'_from_'+self.P_Name+'_to_'+p ,Act=(self.P_Pr_Name,x+'_'+key) ,product=key)
                            self.db_Pr_data[(self.P_Pr_Name,x+'_'+key)]['exchanges'].append(ex_trnp)
                        else:
                            raise ValueError('Inconsistent treatment processes in model and collection')
                                    
            
            ### Adding the technosphere exchnages to activities
            for key in self.Report["Technosphere"][x]:
                #if self.Report["Technosphere"][x][key] != 0:
                if True:
                    ex = self.exchange(key,'technosphere','Mg/year',self.Report["Technosphere"][x][key])                      
                    self.db_data[(self.P_Name,x)]['exchanges'].append(ex)
            
            ### Adding the biosphere exchnages       
            for key in self.Report["Biosphere"][x]:
                #if self.Report["Biosphere"][x][key] != 0:
                if True:
                    ex = self.exchange(key,'biosphere','kg',self.Report["Biosphere"][x][key])                     
                    self.db_data[(self.P_Name,x)]['exchanges'].append(ex)            
            
            
            ### Adding activity for transport between the collection and treatment processes
            if 'LCI' in self.Report.keys():
                for y in  self.Report["LCI"].keys():
                    for m in self.Report["LCI"][y].keys():
                        self.db_Pr_data[(self.P_Pr_Name,y+'_'+'to'+'_'+m)] ={}
                        self.db_Pr_data[(self.P_Pr_Name,y+'_'+'to'+'_'+m)]['name'] = 'LCI'+'_'+y+'to'+'_'+m
                        self.db_Pr_data[(self.P_Pr_Name,y+'_'+'to'+'_'+m)]['unit'] = 'Mg/year'
                        self.db_Pr_data[(self.P_Pr_Name,y+'_'+'to'+'_'+m)]['exchanges'] =[]
                        ### Adding exchage to transport activity between the collection and treatment processes
                        for n in self.Report["LCI"][y][m].keys():
                            ex = self.exchange(n,'technosphere','_',self.Report["LCI"][y][m][n])
                            self.db_Pr_data[(self.P_Pr_Name ,y+'_'+'to'+'_'+m)]['exchanges'].append(ex)
            
            ### Adding activity for transport between the treatment processes
            if len(self.db_Pr_data) > 0:  #check whether transportation is needed or not (if no waste is proudced, then no transportation is needed)           
                for p,q in self.Distance.Distance.keys():
                    if p == self.P_Name and p != q:
                        self.db_Pr_data[(self.P_Pr_Name,p+'_'+'to'+'_'+q)] ={}
                        self.db_Pr_data[(self.P_Pr_Name,p+'_'+'to'+'_'+q)]['name'] = 'LCI'+'_'+p+'_'+'to'+'_'+q
                        self.db_Pr_data[(self.P_Pr_Name,p+'_'+'to'+'_'+q)]['unit'] = 'Mg/year'
                        self.db_Pr_data[(self.P_Pr_Name,p+'_'+'to'+'_'+q)]['exchanges'] =[]
                        ### Adding exchage to transport activity between the treatment processes
                        ex = self.exchange(('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck'),'technosphere','Mg/year',1000 * self.Distance.Distance[(p,q)],Formula=None,Act=None,product=None)  # unit converion Mg to kg 
                        self.db_Pr_data[(self.P_Pr_Name,p+'_'+'to'+'_'+q)]['exchanges'].append(ex)
                    
### writing the databases
        if len(self.db_Pr_data) > 0:
            print("""
                  ####        
                  ++++++ Writing the {}   
                  """.format(self.P_Pr_Name))
    
            self.database_Product.write(self.db_Pr_data)
        
        print("""
              ####        
              ++++++ Writing the {}       
              """.format(self.P_Name))
        db = Database(self.P_Name)
        db.write(self.db_data)
        self.uncertain_parameters.params_dict.update(self.params_dict)
        return(self.parameters,self.act_in_group)


    def exchange(self,Input,Type,Unit,Amount,Formula=None,Act=None,product=None):
        """
        return exchange in a dictionary format
        """
        exchange={}
        exchange['amount'] = Amount
        exchange['input'] = Input
        exchange['type'] = Type
        exchange['unit'] = Unit
        
        if Formula:
            exchange['formula'] = Formula
            if Act == None or product == None:
                raise TypeError('swolfpy error: Act and product are not defined for formula(parameter): {}'.format(Formula)) 
            if Formula not in self.list_of_params:
                self.parameters.append({'name':Formula ,'amount':0})
                self.list_of_params.append(Formula)
                self.params_dict[Formula] = set()
                self.params_dict[Formula].add((Input,Act))
                self.uncertain_parameters.add_parameter(product,self.P_Name,Input[0],0) #add_parameter (self, product, process_model_from, process_model_to,value)							
            else:
                self.params_dict[Formula].add((Input,Act)) 
        
        return(exchange)      