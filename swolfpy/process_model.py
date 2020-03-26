# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:42:51 2019

@author: msmsa
"""
import pandas as pd
import numpy as np
from brightway2 import *
from .Required_keys import *
from .Parameters import *




class Process_Model():

    def __init__(self, process_name,waste_treatment,Distance=None):
        self.process_model_output = {}
        self.process_name = process_name
        self.DB_waste_name =self.process_name +'_product'
        self.Distance = Distance
        
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
        
        print("""
####
++++++ Initializing the {}        
        """.format(self.DB_name))
        
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
                if key in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual',
                 'RDF','Al','Fe','Cu','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO',
                 'OCC','Mixed_Paper','ONP','OFF','Fiber_Other','PET','HDPE_Unsorted','HDPE_P','HDPE_T','PVC','LDPE_Film',
                 'Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic','Brown_glass','Clear_glass','Green_glass','Mixed_Glass']:
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

                            
                            #Exchange for transportation between the process models
                            ex_trnp = {}                        # add exchange to activities _ related to transportation
                            ex_trnp['amount'] = 0
                            ex_trnp['input'] = (self.process_name+'_product' ,self.process_name+'_'+'to'+'_'+p)
                            ex_trnp['type'] = 'technosphere'
                            ex_trnp['unit'] = 'Mg'
                            ex_trnp['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p
                            self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((self.process_name+'_product' ,self.process_name+'_'+'to'+'_'+p),(self.process_name+'_product' , x+'_'+key)))
                            self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'].append(ex_trnp)                    
                                       
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
                            
                            if 'LCI' in self.process_model_output.keys():
                                if p in self.process_model_output['LCI'][key].keys():
                                    ex1 = {}                        # add exchange to activities
                                    ex1['amount'] = 0
                                    ex1['input'] = (self.process_name+'_product' ,key+'_'+'to'+'_'+p)
                                    ex1['type'] = 'technosphere'
                                    ex1['unit'] = 'Mg'
                                    ex1['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p
                                    self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((self.process_name+'_product' ,key+'_'+'to'+'_'+p),(self.process_name+'_product' , x+'_'+key)))
                                    self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'].append(ex1)
                            
                            #if key in ['Separated_Organics','Other_Residual','RDF','Al','Fe','Cu']:
                            if key not in ['Bottom_Ash','Fly_Ash','Wastewater','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
                                #Exchange for transportation between the process models
                                ex_trnp = {}                        # add exchange to activities _ related to transportation
                                ex_trnp['amount'] = 0
                                ex_trnp['input'] = (self.process_name+'_product' ,self.process_name+'_'+'to'+'_'+p)
                                ex_trnp['type'] = 'technosphere'
                                ex_trnp['unit'] = 'Mg'
                                ex_trnp['formula']= "frac_of_"+key+'_from_'+self.DB_name+'_to_'+p
                                self.params_dict["frac_of_"+key+'_from_'+self.DB_name+'_to_'+p].add(((self.process_name+'_product' ,self.process_name+'_'+'to'+'_'+p),(self.process_name+'_product' , x+'_'+key)))
                                self.db_waste_data[(self.DB_waste_name,x+'_'+key)]['exchanges'].append(ex_trnp)
                            
# =============================================================================
#                 elif key in ['Wastewater','OCC','Mixed_Paper','ONP','OFF','Fiber_Other','PET',
#                              'HDPE_Unsorted','HDPE_P','HDPE_T','PVC','LDPE_Film','Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic','Brown_glass','Clear_glass',
#                              'Green_glass','Mixed_Glass']:
# =============================================================================
                
                elif key in ['Wastewater']:
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
                
                else:
                    pass
                    
            if 'LCI' in self.process_model_output.keys():
                for y in  self.process_model_output ["LCI"].keys():
                    for m in self.process_model_output ["LCI"][y].keys():
                        self.db_waste_data[(self.DB_waste_name,y+'_'+'to'+'_'+m)] ={}    # add activity to Waste_database
                        self.db_waste_data[(self.DB_waste_name,y+'_'+'to'+'_'+m)]['name'] = 'LCI'+'_'+y+'to'+'_'+m
                        self.db_waste_data[(self.DB_waste_name,y+'_'+'to'+'_'+m)]['unit'] = 'Mg'
                        self.db_waste_data[(self.DB_waste_name,y+'_'+'to'+'_'+m)]['exchanges'] =[]
                        for n in self.process_model_output ["LCI"][y][m].keys():
                            ex = {}                        # add exchange to activities
                            ex['amount'] = self.process_model_output ["LCI"][y][m][n]
                            ex['input'] = n
                            ex['type'] = 'technosphere'
                            ex['unit'] = '_'
                            self.db_waste_data[(self.DB_waste_name ,y+'_'+'to'+'_'+m)]['exchanges'].append(ex)
            
            for p,q in self.Distance.Distance.keys():
                if p == self.DB_name and p != q:
                    self.db_waste_data[(self.DB_waste_name,p+'_'+'to'+'_'+q)] ={}
                    self.db_waste_data[(self.DB_waste_name,p+'_'+'to'+'_'+q)]['name'] = 'LCI'+'_'+p+'_'+'to'+'_'+q
                    self.db_waste_data[(self.DB_waste_name,p+'_'+'to'+'_'+q)]['unit'] = 'Mg'
                    self.db_waste_data[(self.DB_waste_name,p+'_'+'to'+'_'+q)]['exchanges'] =[]
                    #Adding the exchanges for transport between the process models
                    ex = {}                        
                    ex['amount'] = 1000 * self.Distance.Distance[(p,q)]    # unit converion Mg to kg
                    ex['input'] = ('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')
                    ex['type'] = 'technosphere'
                    ex['unit'] = 'Mg'
                    self.db_waste_data[(self.DB_waste_name,p+'_'+'to'+'_'+q)]['exchanges'].append(ex)
                    
                            
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
                    

        print("""
####        
++++++ Writing the {}   
        """.format(self.DB_waste_name))
        #print(self.db_waste_data)
        self.database_Waste.write(self.db_waste_data)
        
        print("""
####        
++++++ Writing the {}       
        """.format(self.DB_name))
        #print(self.db_data)
        db = Database(self.DB_name)
        db.write(self.db_data)
        self.uncertain_parameters.set_params_dict(self.params_dict)
        return(self.parameters,self.act_in_group)
