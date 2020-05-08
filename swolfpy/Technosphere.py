# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:18:40 2020

@author: msmsa
"""
from brightway2 import *
import bw2io
import numpy as np
import pandas as pd
from .Required_keys import biosphere_keys
from pathlib import Path
from .SWOLF_method import import_methods
from swolfpy_inputdata import Technosphere_Input

class Technosphere:
    def __init__(self,project_name,LCI_path=None,LCI_Reference_path=None,Ecospold2_Path=None):
        self.project_name = project_name
        self.technosphere_db_name='Technosphere' 
        self.user_tech_name = 'User_Technosphere'
        
        self.InputData = Technosphere_Input(LCI_path,LCI_Reference_path,Ecospold2_Path)
        self.LCI_swolfpy_data = self.InputData.LCI_swolfpy_data
        self.LCI_reference = self.InputData.LCI_reference
        self.Ecospold2_Path = self.InputData.Ecospold2_Path
        
    def Create_Technosphere(self):
        projects.set_current(self.project_name)
        bw2setup()
        db=Database('biosphere3')
        if len(db.search('capital cost'))==0:
            db.new_activity(code='Capital_Cost', name="Capital Cost",unit='USD', categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Operational_Cost', name="Operational Cost", unit='USD',categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Utility_Cost', name="Utility Cost",unit='USD', categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Fuel_Cost', name="Fuel Cost",unit='USD', categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Electricity_Cost', name="Electricity Cost", unit='USD', categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Transportation_Cost', name="Transportation Cost", unit='USD',categories=('economic',), type='economic',location='US').save()
            db.new_activity(code='Material_Cost', name="Material Cost",unit='USD', categories=('economic',), type='economic',location='US').save()
        
        # adding swolf methods
        import_methods()
                    
        #Deleting the old (expired) databases (if exist)
        xx= [x for x in databases]
        for x in xx:
            if x not in ['biosphere3']:
                del databases[x]
        if self.LCI_reference['Reference_activity_id'].count()>0:
            self.Write_user_technospher()
            db = Database(self.user_tech_name)
            self.user_tech_keys={}
            for x in db:
                self.user_tech_keys[x.as_dict()['activity']] = x.key
        self.write_technosphere()
    
    def Write_user_technospher(self):
        """
        Creates the user technosphere database
        """
        self.user_tech=bw2io.importers.SingleOutputEcospold2Importer(dirpath=self.Ecospold2_Path,db_name=self.user_tech_name)
        self.user_tech.apply_strategies()
        stats=self.user_tech.statistics()
        if stats[2]>0:
            raise KeyError('There is {} unlink flows in the user defined technosphere (ecospold files). Make sure you are using the LCI ecosplod'.format(stats[2]))
        print("""
                ####
                ++++++  Writing the {}
                """.format(self.user_tech_name))
        self.user_tech.write_database()


    def write_technosphere(self):
        """
        Creates the swolfpy technosphere database
        """
        self.technosphere_data ={}
        # activities
        names = [x for x in self.LCI_swolfpy_data.columns][3:]
        for x in names:
            self.technosphere_data[(self.technosphere_db_name,x)] ={}    # add activity to database
            self.technosphere_data[(self.technosphere_db_name,x)]['name'] = x
            self.technosphere_data[(self.technosphere_db_name,x)]['unit'] = (lambda y: 'NA' if pd.isnull(y) else y)(self.LCI_swolfpy_data[x][0])
            self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'] =[]
            if pd.isnull(self.LCI_reference['Reference_activity_id'][x]):
                i=0
                for val in self.LCI_swolfpy_data[x][1:]:
                    if float(self.check_nan(val)) != 0:
                        ex = {}                        # add exchange to activities
                        ex['amount'] = float(self.check_nan(val))
                        ex['input'] = biosphere_keys[i][0]
                        ex['type'] = 'biosphere'
                        ex['unit'] = 'kg'
                        self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'].append(ex)
                    i+=1
            else:
                ex = {}                        # add exchange to activities
                ex['amount'] = 1
                ex['input'] = self.user_tech_keys[self.LCI_reference['Reference_activity_id'][x]]
                ex['type'] = 'technosphere'
                ex['unit'] = self.LCI_reference['Unit'][x]
                self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'].append(ex)
            
            if not pd.isnull(self.LCI_reference['Cost_key'][x]):        # adding the cost to technosphere
                ex = {}                        # add exchange to activities
                ex['amount'] = self.check_nan(self.LCI_reference['Cost'][x])
                ex['input'] = ('biosphere3',self.LCI_reference['Cost_key'][x]) 
                ex['type'] = 'biosphere'
                ex['unit'] = self.LCI_reference['Cost_Unit'][x]
                self.technosphere_data[(self.technosphere_db_name,x)]['exchanges'].append(ex)
                
        print("""
                ####
                ++++++  Writing the {}
                """.format(self.technosphere_db_name))
        self.technosphere_db = Database(self.technosphere_db_name)
        self.technosphere_db.write(self.technosphere_data)
        # replace zeros when there is no data ("nan")
    
    def check_nan(self,x):  
        """
        Check the `x` and return `0` if `x` is `nan`.
        
        """
        if str(x) == "nan":
            return 0
        return x