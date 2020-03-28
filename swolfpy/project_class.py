# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:13:23 2019

@author: msmsa
"""

from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
from .process_model import *
from .Required_keys import *
import pandas as pd
import copy
from bw2analyzer import ContributionAnalysis
from .Parameters import *
from pathlib import Path

class project():
    """
    Project class creates a new project in Birghtway2.
    """
    def __init__ (self,project_name,CommonData,Treatment_processes,Distance,Collection_processes=None):
        """Create project object.            

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
        
        .. note:: Treatment processes and distance between them are required for creating a project. Collection processes are not need unless they are included in the system boundary.
        
        :Example:
        
        >>> # Treatment_processes:
        >>> # Include LF and WTE
        >>> from swolfpy.ProcessModels import CommonData
        >>> from swolfpy.ProcessModels import LF
        >>> from swolfpy.ProcessModels import WTE
        >>> common_data = CommonData.CommonData()
        >>> Treatment_processes = {}
        >>> Treatment_processes['LF']={'input_type':['RWC','Bottom_Ash','Fly_Ash','Other_Residual'],'model': LF.LF()}
        >>> Treatment_processes['WTE']={'input_type':['RWC','Other_Residual'],'model': WTE.WTE()}
        >>> # Distance            
        >>> from swolfpy.Distance import Distance
        >>> import pandas as pd
        >>> Processes = ['LF','WTE','SF_COl']
        >>> Data = pd.DataFrame([[None,20,20],[None,None,20],[None,None,None]],index=Processes,columns=Processes)
        >>> distance = Distance(Data=Data)
        >>> # Collection_processes:
        >>> # Ony include one single family sector wih residual waste collection
        >>> from swolfpy.ProcessModels import SF_collection
        >>> Collection_processes = {}
        >>> Collection_scheme_SF_COL={'RWC':{'Contribution':1,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
        >>> 'SSO_DryRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
        >>> 'REC_WetRes':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}},
        >>> 'MRDO':{'Contribution':0,'separate_col':{'SSR':0,'DSR':0,'MSR':0,'MSRDO':0,'SSYW':0,'SSYWDO':0}}} 
        >>> Collection_processes['SF_COl']={'input_type':[],'model': SF_collection.SF_Col('SF_COl',Collection_scheme_SF_COL,Treatment_processes=Treatment_processes,Distance=distance)}      
        >>> # project
        >>> from swolfpy import project_class
        >>> demo = project_class.project('demo',common_data,Treatment_processes,distance,Collection_processes)
        
        """
        self.project_name= project_name
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
        for i in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual','RDF','Wastewater','OCC','Mixed_Paper','ONP','OFF','Fiber_Other','PET',
                 'HDPE_Unsorted','HDPE_P','HDPE_T','PVC','LDPE_Film','Polypropylene','Polystyrene','Plastic_Other','Mixed_Plastic','Al','Fe','Cu','Brown_glass','Clear_glass',
                 'Green_glass','Mixed_Glass','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            self.waste_treatment[i]= self.find_destination(i) 
            
        self.process_model={}
   

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
        Check the `x` and return `0` if `x` is `nan`.
        
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
        #initiate biosphere database and LCIA methods
        bw2setup()
        
        #Checking the path for technosphere LCI data and writing the technophere database
        if path:
            self.technosphere_path = path
        else:
            self.technosphere_path = str(Path(__file__).parent)+'/Data/SWOLF_AccountMode_LCI DATA.csv'
        self.write_technosphere()
        
        #Deleting the old (expired) databases (if exist)
        xx= [x for x in databases]
        for x in xx:
            if x not in ['biosphere3','Technosphere']:
                del databases[x]
        
        #Initializing the databases
        for DB_name in self.Treatment_processes:
            if self.Treatment_processes[DB_name]['model'].Process_Type in ['Treatment','Collection']:
                Process_Model.init_DB(DB_name,self.CommonData.Index)
            elif self.Treatment_processes[DB_name]['model'].Process_Type == 'Reprocessing':
                Process_Model.init_DB(DB_name,self.CommonData.Reprocessing_Index)
                
        
        Database("waste").register()
        self.waste_BD = Database("waste")

    def write_technosphere(self):
        self.technosphere_data ={}
        self.technosphere_db_name='Technosphere'
        if self.technosphere_db_name in databases:
            del databases[self.technosphere_db_name]   

        outputdata1 = pd.read_csv(self.technosphere_path)
        
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
        print("""
####
++++++  Writing the {}
        """.format(self.technosphere_db_name))
        
        self.technosphere_db = Database(self.technosphere_db_name)
        self.technosphere_db.write(self.technosphere_data)
            
    def write_project(self):
        self.parameters={}
        self.parameters_list=[]
        self.act_include_param={}
        for j in self.Treatment_processes:
            (P,G)=self.import_database(j,self.waste_treatment)
            self.parameters[j]=P
            self.act_include_param[j]=G
            self.parameters_list+=P
                            
    def import_database(self,name,waste_treatment):
        self.process_model[name] = Process_Model(name,waste_treatment,self.Distance)
        self.Treatment_processes[name]['model'].calc()
        self.process_model[name].Report = self.Treatment_processes[name]['model'].report()
        
        if self.Treatment_processes[name]['model'].Process_Type in ['Treatment','Collection']:
            (P,G)=self.process_model[name].Write_DB(self.CommonData.Index)
        elif self.Treatment_processes[name]['model'].Process_Type == 'Reprocessing':
            (P,G)=self.process_model[name].Write_DB(self.CommonData.Reprocessing_Index)
            
        return((P,G))
    
    def report_parameters(self):
        """
        Reports the `parameters` in dictionary format.
        
        :return: dictionary include the processes as key and parameters in each process as values.
        :rtype: dict
        
        """
        return(self.parameters)
    
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
        """
        Update the `parameters` and their related exchanges based on the `new_param_data`.
        
        :param new_param_data: List of `parameters` (waste fractions) in the project with new values
        :type new_param_data: list
        
        .. note:: `parameters` are waste fractions which show what fraction of waste from one source go to different destinations, so sum of parameters from each source should be 1. (0<= `parameters` <=1)
        
        """
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
		