# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:35:26 2020

@author: msmsa
"""
from .LCA_matrix import LCA_matrix
import numpy as np
from scipy.optimize import minimize
from random import random

class Optimization(LCA_matrix):
    def __init__(self,functional_unit, method, project):
        super().__init__(functional_unit, method, project)
        
    ### Objective function    
    def objective_function(self, x):
        """
        Use the new parameters (Waste fractions) to update the tech_matrix (tech_param)
        and reculate the LCA score
        """
        if self.oldx != list(x): # Calculations are done only when the function get new x.
            param_exchanges=self.project.parameters.Param_exchanges(x)
            for key, value in param_exchanges.items():
                if key in self.tech_matrix:
                    self.tech_matrix[key] = value    
        
            tech = np.array(list(self.tech_matrix.values()), dtype=float)
            bio = np.array(list(self.bio_matrix.values()), dtype=float)
            
            self.rebuild_technosphere_matrix(tech)
            self.rebuild_biosphere_matrix(bio)
            self.lci_calculation()
            if self.lcia:
                self.lcia_calculation()
            
            self.oldx = list(x)
        return(self.score/10**self.magnitude)

    ### Mass to process
    def get_mass_flow(self, key, KeyType, x):
        """
        calculate the mass to the process from the supply_array matrix
        """
        self.objective_function(x)
        
        mass_flow=0
        if KeyType == 'WasteToProcess':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i]:
                    mass_flow += self.supply_array[i]
        
        elif KeyType == 'Process':
            for i in range(len(self.supply_array)):
                if key == self.activities_dict[i][0]:
                    mass_flow += self.supply_array[i]
        else:
            raise ValueError(""" KeyType for the get_mass_flow function is not defined correct.""")
        return mass_flow
        
    ### Emission flow in LCI
    def get_emission_amount(self, emission, x):
        self.objective_function(x)
        inventory=self.biosphere_matrix*self.supply_array
        emission_amount = 0
        for i in range(len(inventory)):
            if emission == self.biosphere_dict[i]:
                emission_amount+=inventory[i]
        return emission_amount
    
    
    def create_equality(self, N_param_Ingroup):
        """
        Check that the sum of parameters in each group should be one.
        """
        local_index = self.Param_index
        l = lambda x: sum([x[i] for i in range(local_index,local_index+N_param_Ingroup)]) -1 
        self.Param_index+=N_param_Ingroup
        return l
        
    def create_inequality(self, key, limit, KeyType,ConstType):
        """
        key: process name, key for activtity in process or key for activity in biosphere
        ConstType: <= , >=
        KeyType: Process,WasteToProcess,Emission
        """
        if ConstType not in ['<=','>=']:
            raise ValueError(" Constraint Type is not defined correct ") 
                        
        if KeyType == 'Process':
            if ConstType == '<=':
                l = lambda x: limit - self.get_mass_flow(key, KeyType, x) 
            else:
                l = lambda x: self.get_mass_flow(key, KeyType, x) - limit
            return l
            
        elif KeyType == 'WasteToProcess':
            if ConstType == '<=':
                l = lambda x: limit - self.get_mass_flow(key, KeyType, x)
            else:
                l = lambda x: self.get_mass_flow(key, KeyType, x) - limit
            return l

        elif KeyType == 'Emission': 
            if ConstType == '<=':
                l = lambda x: limit - self.get_emission_amount(key, x)
            else:
                l = lambda x: self.get_emission_amount(key, x) - limit
            return l
            
    
    def create_constraints(self):
        cons = list()
        group = dict()
        
        # Index for the parameters
        self.Param_index=0
        
        # Number of parameters in each group (from one source to different denstinations)
        for key in self.project.parameters.param_uncertainty_dict.keys():
            group[key] = len(self.project.parameters.param_uncertainty_dict[key])

        # Equal constraint (sum of the parameters in each group should be one)
        for vals in group.values():
            cons.append({'type':'eq', 'fun':self.create_equality(N_param_Ingroup=vals)})
            
        if self.constraints:
            for key in self.constraints.keys():
                cons.append({'type':'ineq', 'fun': self.create_inequality(key, self.constraints[key]['limit'], self.constraints[key]['KeyType'], self.constraints[key]['ConstType'])})
        return cons
    
    def optimize_parameters(self, project, constraints=None):
        self.constraints=constraints
        self.project = project
        self.magnitude = len(str(int(abs(self.score)))) 
        
        x0 = [i['amount'] for i in self.project.parameters_list] # initializing with the users initial solution
        #x0 = [1 for _ in self.project.parameters_list] #changing initial x0 to outside feasible region
        
        self.oldx=[0 for i in range(len(x0))]
        
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        self.cons = self.create_constraints()
        
        res = minimize(self.objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
        if res.success:
            self.success=True
            self.optimized_x=list()
            res.x=res.x.round(decimals=3)
            for i in range(len(self.project.parameters_list)):
                self.optimized_x.append({'name':self.project.parameters_list[i]['name'],'amount':res.x[i]})
            print(self.optimized_x)
            return res
        else:
            self.success=False
            print(res.message)
            return res
            
    def multi_start_optimization(self, project, constraints=None, max_iter=30):
        self.constraints=constraints
        self.project = project
        self.magnitude = len(str(int(abs(self.score)))) 
        
        global_min = 1E100
        
        self.cons = self.create_constraints()
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        
        for _ in range(max_iter):
            x0 = [random() for i in self.project.parameters_list] #initializing with the users initial solution
            self.oldx=[0 for i in range(len(x0))]
            res = minimize(self.objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
            
            if res.success:
                if res.fun < global_min:
                    res_global = res
                    global_min = res.fun
                    print(global_min)
        
        if res_global.success:
            self.success=True
            self.optimized_x=list()
            res_global.x=res_global.x.round(decimals=3)
            for i in range(len(self.project.parameters_list)):
                self.optimized_x.append({'name':self.project.parameters_list[i]['name'],'amount':res_global.x[i]})
            return res_global
        else:
            self.success=False
            print(res_global.message)
            return res_global
    
    def set_optimized_parameters_to_project(self):
        assert hasattr(self, "project"), "Must run optimize_parameters first"
        assert self.success, "Optimization has to be sucessful first"
        
        self.project.update_parameters(self.optimized_x)
    
# =============================================================================
#     def mass_to_process(self):
#         get_mass_flow(self, key, KeyType, x):
# =============================================================================