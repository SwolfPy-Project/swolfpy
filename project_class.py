# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:13:23 2019

@author: msmsa
"""

from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
from process_model_msm3 import *
import pandas as pd
from Required_keys import *
import copy
from bw2analyzer import ContributionAnalysis
from Parameters import *


class project():
    def __init__ (self,project_name,Treatment_processes):
        self.project_name= project_name
        self.Treatment_processes = Treatment_processes
        self.processes = [x for x in Treatment_processes.keys()]
        projects.set_current(self.project_name)
        
        self.waste_treatment = {}
        self.waste_treatment['Bottom_Ash']= self.find_destination('Bottom_Ash') 
        self.waste_treatment['Fly_Ash']= self.find_destination('Fly_Ash')
        self.waste_treatment['Separated_Organics']= self.find_destination('Separated_Organics')
        self.waste_treatment['Other_Residual']= self.find_destination('Other_Residual')
        self.waste_treatment['RDF']=self.find_destination('RDF')
        self.waste_treatment['Wastewater']= self.find_destination('Wastewater')
        self.waste_treatment['OCC']= self.find_destination('OCC')
        self.waste_treatment['Mixed_Paper']= self.find_destination('Mixed_Paper')
        self.waste_treatment['ONP']= self.find_destination('ONP')
        self.waste_treatment['OFF']= self.find_destination('OFF')
        self.waste_treatment['Fiber_Other']= self.find_destination('Fiber_Other')
        self.waste_treatment['PET']= self.find_destination('PET')
        self.waste_treatment['HDPE_Unsorted']= self.find_destination('HDPE_Unsorted')
        self.waste_treatment['HDPE_P']= self.find_destination('HDPE_P')
        self.waste_treatment['HDPE_T']= self.find_destination('HDPE_T')
        self.waste_treatment['PVC']= self.find_destination('PVC')
        self.waste_treatment['LDPE_Film']= self.find_destination('LDPE_Film')
        self.waste_treatment['Polypropylene']= self.find_destination('Polypropylene')
        self.waste_treatment['Polystyrene']= self.find_destination('Polystyrene')
        self.waste_treatment['Plastic_Other']= self.find_destination('Plastic_Other')
        self.waste_treatment[ 'Mixed_Plastic']= self.find_destination('Mixed_Plastic')
        self.waste_treatment['Al']= self.find_destination('Al')
        self.waste_treatment['Fe']= self.find_destination('Fe')
        self.waste_treatment['Cu']= self.find_destination('Cu')
        self.waste_treatment['Brown_glass']= self.find_destination('Brown_glass')
        self.waste_treatment['Clear_glass']= self.find_destination('Clear_glass')
        self.waste_treatment['Green_glass']= self.find_destination('Green_glass')
        self.waste_treatment['Mixed_Glass']= self.find_destination('Mixed_Glass')
        self.waste_treatment['MOC']= self.find_destination('MOC')
        self.waste_treatment['RWC']= self.find_destination('RWC')
        self.waste_treatment['SSRC']= self.find_destination('SSRC')
        self.waste_treatment['MWC']= self.find_destination('MWC')
        
        
        self.process_inputdata={}
        self.process_model={}
    
    def find_destination(self,product):
        destination=[]
        for P in self.Treatment_processes:
            if product in self.Treatment_processes[P]['input_type']:
                destination.append(P)
        return(destination)
   
    
    def check_nan(self,x):  # replace zeros when there is no data ("nan")
        if str(x) == "nan":
            return 0
        return x
    
    
    def init_project(self,path):
        bw2setup()
        self.technosphere_data ={}
        self.technosphere_db_name='Technosphere'
        if self.technosphere_db_name in databases:
            del databases[self.technosphere_db_name]   
        
        self.technosphere_path = path
        outputdata1 = pd.read_csv(path)
        # activities
        names = [x for x in outputdata1.columns][3:]
        for x in names:
            self.technosphere_data[(self.technosphere_db_name,x)] ={}    # add activity to database
            self.technosphere_data[(self.technosphere_db_name,x)]['name'] = x
            self.technosphere_data[(self.technosphere_db_name,x)]['unit'] = self.check_nan(outputdata1[x][0])
            self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'] =[]
            i=0
            for val in outputdata1[x][1:]:
                if float(self.check_nan(val)) != 0:
                    ex = {}                        # add exchange to activities
                    ex['amount'] = float(self.check_nan(val))
                    ex['input'] = biosphere_keys[i][0]
                    ex['type'] = 'biosphere'
                    ex['unit'] = 'kg'
                    self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'].append(ex)
                i+=1
        self.technosphere_db = Database(self.technosphere_db_name)
        self.technosphere_db.write(self.technosphere_data)
        
        xx= [x for x in databases]
        for x in xx:
            if x not in ['biosphere3','Technosphere']:
                del databases[x]
        
        for j in self.Treatment_processes:
            self.init_database(j,self.waste_treatment)
        
        Database("waste").register()
        self.waste_BD = Database("waste")
            

    def init_database(self,name,waste_treatment):
        process = Process_Model(name,waste_treatment)
        process.init_DB(name)
    
    def write_project(self):
        self.parameters={}
        self.parameters_list=[]
        self.act_include_param={}
        for j in self.Treatment_processes:
            if 'path' in self.Treatment_processes[j].keys():
                (P,G)=self.import_database(j,self.waste_treatment,self.Treatment_processes[j]['path'])
            else:
                (P,G)=self.import_database(j,self.waste_treatment)
            self.parameters[j]=P
            self.act_include_param[j]=G
            self.parameters_list+=P
                            
    def import_database(self,name,waste_treatment,path = None):
        self.process_model[name] = Process_Model(name,waste_treatment)
        if path:
            self.process_inputdata[name] = self.process_model[name].read_output_from_SWOLF(path)
        else:
            self.Treatment_processes[name]['model'].calc()
            self.process_inputdata[name] = self.Treatment_processes[name]['model'].report()
            self.process_model[name].process_model_output = self.Treatment_processes[name]['model'].report()
        (P,G)=self.process_model[name].Write_DB(name)
        return((P,G))
    
    def report_parameters(self):
        return(self.parameters)
    
    def report_parameters_list(self):
        return(self.parameters_list)
        
    def group_exchanges(self):
        for j in self.processes:
            if len(self.act_include_param[j]) > 0:
                for r in self.act_include_param[j]:
                    parameters.add_exchanges_to_group(j,r)
	
    def create_unified_params(self):
        unified_dict = dict()
        unified_dict2 = dict()
        for item in self.process_model.values():
            for key, value in item.uncertain_parameters.param_uncertainty_dict.items():
                unified_dict[key]=value
				
            for key, value in item.uncertain_parameters.params_dict.items():
                unified_dict2[key]=value
        self.unified_params = Parameters()
        self.unified_params.set_params_uncertainty_dict(unified_dict)
        self.unified_params.set_params_dict(unified_dict2)
        		
                    
    def update_parameters(self,new_param_data):
        self.create_unified_params()
        self.new_param_data=new_param_data
		
        for j in self.new_param_data:
            for k in self.parameters_list:
                if k['name'] == j['name']:
                    self.unified_params.update_values(j['name'],j['amount'])
					
        if self.unified_params.check_sum():
            for j in self.new_param_data:
                for k in self.parameters_list:
                    if k['name'] == j['name']:
                        k['amount']=j['amount']       
            parameters.new_project_parameters(self.new_param_data)
            for j in self.processes:
                if len(self.act_include_param[j]) > 0:
                    ActivityParameter.recalculate_exchanges(j)
					
        else:
            for j in self.new_param_data:
                for k in self.parameters_list:
                    if k['name'] == j['name']:
                        self.unified_params.update_values(k['name'],k['amount'])
		
			
		
                
    def process_start_scenario(self,input_dict,scenario_name):
        self.input_dict=input_dict
        self.scenario_name=scenario_name
        self.waste_BD.new_activity(code = self.scenario_name, name = self.scenario_name, type = "process", unit = "Mg" ).save()
        for P in self.input_dict:
            for y in self.input_dict[P]:
                if self.input_dict[P][y] != 0:
                    self.waste_BD.get(self.scenario_name).new_exchange(input=(P,y),amount=self.input_dict[P][y],type="technosphere").save()
        self.waste_BD.get(self.scenario_name).save()    

    def Do_LCA(self,scenario_name,impact_method,functioanl_unit):
        self.demand={(self.waste_BD.name,scenario_name):functioanl_unit}   
        self.lca= LCA(self.demand,impact_method)
        self.lca.lci()
        self.lca.lcia()
        print("lca socre= " , self.lca.score)
        self.CA=ContributionAnalysis()
        self.top_process= self.CA.annotated_top_processes(self.lca)    
        cc=[]
        for x in self.top_process:
            cc.append ([x[0],x[2]['name']])    
        cc.sort()
        
        CutOff= 0.05
        maxcc =abs(max(cc)[0]) 
        mincc= abs(min(cc)[0])
        import copy
        dd = list()
        i=0
        for x in cc:
            if abs(x[0])> CutOff * maxcc  or abs(x[0])> CutOff * mincc :
                dd.append(cc[i])
            i+=1
        import matplotlib.pyplot as plt
        plt.rcParams["figure.figsize"] = (20,5)    
        plt.rcParams.update({'font.size':16})
        negative = []
        positive=[]
        dd.reverse()
        for x in range(len(dd)):
            if dd[x][0]<0:
                negative.append(dd[x][0])
                if x ==0:
                    plt.barh("Activity",dd[x][0],height=0.1,left=0)
                else:
                    plt.barh("Activity",dd[x][0],height=0.1,left=sum(negative[:-1]))
        
        dd.reverse()
        for x in range(len(dd)):
            if dd[x][0]>0:
                positive.append(dd[x][0])
                if x ==0:
                    plt.barh("Activity",dd[x][0],height=0.1,left=0)
                else:
                    plt.barh("Activity",dd[x][0],height=0.1,left=sum(positive[:-1]))
                    
        plt.legend([x[1] for x in dd],loc=3)
        plt.title('Top Activities Contribution, CutOff = 0.05,'+scenario_name)
        

                
        

        
        

      

        
    