# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:13:23 2019

@author: msmsa
"""
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
from .ProcessDB import *
from .Required_keys import *
import pandas as pd
import copy
from bw2analyzer import ContributionAnalysis
from .Parameters import *
from .Technosphere import Technosphere
from pathlib import Path

class Project():
    """
    Project class creates a new project in Birghtway2.
    
    :param project_name: Name for the project
    :type project_name: str
    
    :param CommonData: CommonData object
    :type CommonData: class: `swolfpy.ProcessMoldes.CommonData`
    
    :param Treatment_processes: Dictionary for treatment processes include their input type and model.
    :type Treatment_processes: dict
    
    :param Distance: Distance object.
    :type Distance: class: `swolfpy.Distance.Distance`
    
    
    :param Collection_processes: Dictionary for collection processes include their input type and model. Input type for the collection process is empty list ``[]`` as they don't accept waste from other processes.
    :type Collection_processes: dict, optional
    
    .. note:: Treatment processes and distance between them are required for creating a project. Collection processes are not required unless they are included in the system boundary.
    
    :Create sample project:
    
    Step 1: Create CommonData and Treatment_processes dict with LF and WTE:
        
    >>> from swolfpy_inputdata import CommonData
    >>> from swolfpy_processmodels import LF
    >>> from swolfpy_processmodels import WTE
    >>> common_data = CommonData()
    >>> Treatment_processes = {}
    >>> Treatment_processes['LF']={'input_type':['RWC','Bottom_Ash','Fly_Ash','Other_Residual'],'model': LF()}
    >>> Treatment_processes['WTE']={'input_type':['RWC','Other_Residual'],'model': WTE()}

    Step 2: Create Distance object:
        
    >>> from swolfpy_processmodels import Distance
    >>> import pandas as pd
    >>> Processes = ['LF','WTE','SF_COl']
    >>> Data = pd.DataFrame([[None,20,20],[None,None,20],[None,None,None]],index=Processes,columns=Processes)
    >>> distance = Distance(Data=Data)
    
    Step 3: Create Collection_processes dict with one single family sector which only has residual waste collection:
        
    >>> from swolfpy_processmodels import SF_Col
    >>> Collection_processes = {}
    >>> Collection_scheme_SF_COL={'RWC':{'Contribution':1,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'SSO_DryRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'REC_WetRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
    >>> 'MRDO':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}}} 
    >>> Collection_processes['SF_COl']={'input_type':[],'model': SF_Col('SF_COl',Collection_scheme_SF_COL,
    >>>                                 Treatment_processes=Treatment_processes,Distance=distance)}      
    
    Step 4: Create project:
        
    >>> from swolfpy import Project
    >>> demo = Project('demo',common_data,Treatment_processes,distance,Collection_processes)
    >>> demo.init_project()
    >>> demo.write_project()
    >>> demo.group_exchanges()
    >>> demo.parameters.default_parameters_list()
        [{'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 1.0},
         {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 1.0},
         {'name': 'frac_of_RWC_from_SF_COl_to_LF', 'amount': 0.5},
         {'name': 'frac_of_RWC_from_SF_COl_to_WTE', 'amount': 0.5}]
    >>> demo.update_parameters(demo.parameters.default_parameters_list())
    """
    def __init__ (self,project_name,CommonData,Treatment_processes,Distance,Collection_processes=None,Technosphere_obj=None):        
        if Technosphere_obj:
            self.Technosphere = Technosphere_obj
            self.project_name = self.Technosphere.project_name
            if self.project_name != project_name:
                raise Warning('The project name should be same with the name selected for creating the technosphere')
        else:
            self.project_name = project_name
            self.Technosphere = Technosphere(self.project_name)
            
        self.CommonData =  CommonData  
        self.Treatment_processes = Treatment_processes
        self.Collection_processes = Collection_processes
        self.Distance = Distance
        if self.Collection_processes:
            for j in self.Collection_processes.keys():
                self.Treatment_processes[j] = self.Collection_processes[j]
    
        self.processes = [x for x in Treatment_processes.keys()]
        projects.set_current(self.project_name)
        
        self.waste_treatment = {}
        for i in self.CommonData.All_Waste_Pr_Index:
            self.waste_treatment[i]= self.find_destination(i) 
            
        self.process_model={}
        
        # Creating swolfpy parameter class
        self.parameters = Parameters(self.Treatment_processes)
   

    def find_destination(self,product):
        """
        Find the processes that can treat the `product`. This function check the `input_type` in the `Treatment_processes` dictionary.
        
        :param product: Waste product e.g., RWC, Fly_Ash, Separated_Organics, Other_Residual
        :type product: str
        
        :return: A list of the discovered processes in the `Treatment_processes` dictionary that can treat the `product`
        :rtype: list
        
        """
        destination=[]
        for P in self.Treatment_processes:
            if product in self.Treatment_processes[P]['input_type']:
                destination.append(P)
        return(destination)
   
    # replace zeros when there is no data ("nan")
    def check_nan(self,x):  
        """
        Check the `x` and return 0 if `x` is `nan`.
        
        """
        if str(x) == "nan":
            return 0
        return x
    
    
    def init_project(self,path=None):
        """
        This function initialize a `project` in Brightway2 by creating the `biosphere3` database and importing the impact assesment methods.
        Note: If the `project` already exists, it will delete all the databases except 'biosphere3'. `Technosphere` database is written from the 
        `SWOLF_AccountMode_LCI DATA.csv` in the `Data` folder unless user select new file with it's `path`.
        
        This function create an empty database for each process as a placeholder, so the model can browse these databases in 
        the next step (writing project) and create exchanges between them.
        
        :param path: Path to the `csv` file that includes the LCI data for technosphere flows
        :type path: str, optional 
        
        """
        self.Technosphere.Create_Technosphere()
        
        #Initializing the databases
        for DB_name in self.Treatment_processes:
            if self.Treatment_processes[DB_name]['model'].Process_Type in ['Treatment','Collection']:
                ProcessDB.init_DB(DB_name,self.CommonData.Index)
            elif self.Treatment_processes[DB_name]['model'].Process_Type == 'Reprocessing':
                ProcessDB.init_DB(DB_name,self.CommonData.Reprocessing_Index)
                
        
        Database("waste").register()
        self.waste_BD = Database("waste")
                    
    def write_project(self):
        self.parameters_dict={}
        self.parameters_list=[]
        self.act_include_param={}
        for j in self.Treatment_processes:
            (P,G)=self.import_database(j)
            self.parameters_dict[j]=P
            self.act_include_param[j]=G
            self.parameters_list+=P
                            
    def import_database(self,name):
        self.process_model[name] = ProcessDB(name,self.waste_treatment,self.Distance)
        self.Treatment_processes[name]['model'].calc()
        self.process_model[name].Report = self.Treatment_processes[name]['model'].report()
        
        if self.Treatment_processes[name]['model'].Process_Type in ['Treatment','Collection']:
            (P,G)=self.process_model[name].Write_DB(self.CommonData.Index,self.parameters,self.Treatment_processes[name]['model'].Process_Type)
        elif self.Treatment_processes[name]['model'].Process_Type == 'Reprocessing':
            (P,G)=self.process_model[name].Write_DB(self.CommonData.Reprocessing_Index,self.parameters,self.Treatment_processes[name]['model'].Process_Type)
            
        return((P,G))
    
    def report_parameters(self):
        """
        Reports the `parameters` in dictionary format.
        
        :return: dictionary include the processes as key and parameters in each process as values.
        :rtype: dict
        
        """
        return(self.parameters_dict)
    
    def report_parameters_list(self):
        """
        Reports the `parameters` in list format.        

        :return: List of `parameters` (waste fractions) in the project
        :rtype: list
        
        """
        return(self.parameters_list)
        
    def group_exchanges(self):
        """
        Create a group for each `parameter` and add the exchanges that include this `parameter` to this group. As a results, model know to 
        update the values in those exchanges when the `parameter` is updated.
        
        """
        for j in self.processes:
            print("""
                  Grouping the exchanges with parameters in Database {}
                  """.format(j))
            if len(self.act_include_param[j]) > 0:
                for r in self.act_include_param[j]:
                    parameters.add_exchanges_to_group(j,r)
        		
                    
    def update_parameters(self,new_param_data):
        """
        Update the `parameters` and their related exchanges based on the `new_param_data`.
        
        :param new_param_data: List of `parameters` (waste fractions) in the project with new values
        :type new_param_data: list
        
        .. note:: `parameters` are waste fractions which show what fraction of waste from one source go to different destinations, so sum of parameters from each source should be 1. (0<= `parameters` <=1)
        
        """
        self.new_param_data=new_param_data
		
        for j in self.new_param_data:
            for k in self.parameters_list:
                if k['name'] == j['name']:
                    self.parameters.update_values(j['name'],j['amount'])
					
        if self.parameters.check_sum():
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
                        self.parameters.update_values(k['name'],k['amount'])
		
                
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
        lca= LCA(self.demand,impact_method)
        lca.lci()
        lca.lcia()
        print("lca socre= " , lca.score)
        CA=ContributionAnalysis()
        top_process= CA.annotated_top_processes(lca)    
        cc=[]
        for x in top_process:
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
        lgnd = list()
        for x in range(len(dd)):
            if dd[x][0]<0:
                negative.append(dd[x][0])
                if x ==0:
                    plt.barh("Activity",dd[x][0],height=0.1,left=0)
                else:
                    plt.barh("Activity",dd[x][0],height=0.1,left=sum(negative[:-1]))
                lgnd.append(dd[x][1])
        
        dd.reverse()
        for x in range(len(dd)):
            if dd[x][0]>0:
                positive.append(dd[x][0])
                if x ==0:
                    plt.barh("Activity",dd[x][0],height=0.1,left=0)
                else:
                    plt.barh("Activity",dd[x][0],height=0.1,left=sum(positive[:-1]))
                lgnd.append(dd[x][1])
                    
        plt.legend(lgnd,loc=3)
        plt.title('Top Activities Contribution, CutOff = 0.05,'+scenario_name)
        
    def save(self,filename):
        import pickle
        pickle.dump(self, open(filename, "wb"))
		