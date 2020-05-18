# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:35:26 2020

@author: msmsa
"""
from .LCA_matrix import LCA_matrix
import numpy as np
from scipy.optimize import minimize
from random import random
import plotly.graph_objects as go
from plotly.offline import plot


class Optimization(LCA_matrix):
    """
    
    :param functional_unit: 
    :type functional_unit: dict
    :param method: 
    :type method: lsit
    :param project: 
    :type project: ``swolfpy.Project.Project``
    
    """
    def __init__(self,functional_unit, method, project):
        super().__init__(functional_unit, method)
        self.project = project
        
    ### Objective function    
    def _objective_function(self, x):
        """
        Use the new parameters (Waste fractions) to update the ``tech_matrix`` (``tech_param``)
        and reculate the LCA score.
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
        calculate the mass to the process from the `supply_array` matrix.
        """
        self._objective_function(x)
        
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
        """
        calculate the mass of the `emission` to biosphere from the `inventory`.
        """
        self._objective_function(x)
        inventory=self.biosphere_matrix*self.supply_array
        emission_amount = 0
        for i in range(len(inventory)):
            if emission == self.biosphere_dict[i]:
                emission_amount+=inventory[i]
        print(emission_amount)
        return emission_amount
    
    
    def _create_equality(self, N_param_Ingroup):
        """
        Check that the sum of parameters in each group should be one.
        """
        local_index = self.Param_index
        l = lambda x: sum([x[i] for i in range(local_index,local_index+N_param_Ingroup)]) -1 
        self.Param_index+=N_param_Ingroup
        return l
        
    def _create_inequality(self, key, limit, KeyType,ConstType):
        """
        
        :param key: process name, key for activtity in process or key for activity in biosphere
        :type key: str or tuple
        :param limit: 
        :type limit: float
        :param KeyType: ``"Process"``, ``"WasteToProcess"``, ``"Emission"``
        :type KeyType: str
        :param ConstType: ``"<="`` , ``">="``
        :type ConstType: str
        
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
            
    
    def _create_constraints(self):
        cons = list()
        group = dict()
        
        # Index for the parameters
        self.Param_index=0
        
        # Number of parameters in each group (from one source to different denstinations)
        for key in self.project.parameters.param_uncertainty_dict.keys():
            group[key] = len(self.project.parameters.param_uncertainty_dict[key])

        # Equal constraint (sum of the parameters in each group should be one)
        for vals in group.values():
            cons.append({'type':'eq', 'fun':self._create_equality(N_param_Ingroup=vals)})
            
        if self.constraints:
            for key in self.constraints.keys():
                cons.append({'type':'ineq', 'fun': self._create_inequality(key, self.constraints[key]['limit'], self.constraints[key]['KeyType'], self.constraints[key]['ConstType'])})
        return cons
    
    def optimize_parameters(self, constraints=None):
        """
        Call the ``scipy.optimize.minimize()`` to minimize the LCA score. \n
        ``constraints`` is python dictionary. \n 
        Constraint type can be ``'<='`` or ``'>='``. \n
        Three kind of constraints are defined as below: \n
        * **Process:** Constraint on the total mass to the processs. The ``'KeyType'`` should be ``'Process'`` (e.g., The capacity of the WTE). Examaple:
        
        >>> constraints = {}
        >>> # Use name the the process as key in dict
        >>> constraints['WTE'] = {'limit':100, 'KeyType':'Process','ConstType':"<="}
        
        * **WasteToProcess:** Constraint on the total mass of waste fraction to the processs. The ``'KeyType'`` should be ``'WasteToProcess'`` (e.g., Ban food waste from landfill). Examaple:
        
        >>> constraints = {}
        >>> # Use database key as key in dict
        >>> constraints[('LF','Food_Waste_Vegetable')] = {'limit':0, 'KeyType':'WasteToProcess','ConstType':"<="}
        
        * **Emission:** Constraint on the emissions. The ``'KeyType'`` should be ``'Emission'`` (e.g., CO2 emissions Cap). Examaple:
        
        >>> constraints = {}
        >>> # Use database key as key in dict
        >>> constraints[('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7')] = {'limit':100,'KeyType':'Emission','ConstType':"<="}
        
        """
        self.constraints=constraints
        self.magnitude = len(str(int(abs(self.score)))) 
        
        x0 = [i['amount'] for i in self.project.parameters_list] # initializing with the users initial solution
        #x0 = [1 for _ in self.project.parameters_list] #changing initial x0 to outside feasible region
        
        self.oldx=[0 for i in range(len(x0))]
        
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        self.cons = self._create_constraints()
        
        res = minimize(self._objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
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
            
    def multi_start_optimization(self, constraints=None, max_iter=30):
        self.constraints=constraints
        self.magnitude = len(str(int(abs(self.score)))) 
        
        global_min = 1E100
        
        self.cons = self._create_constraints()
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        
        for _ in range(max_iter):
            x0 = [random() for i in self.project.parameters_list] #initializing with the users initial solution
            self.oldx=[0 for i in range(len(x0))]
            res = minimize(self._objective_function, x0, method='SLSQP', bounds=bnds, constraints=self.cons)
            
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
    
    def plot_sankey(self,optimized_flow=True):
        """Plots a sankey diagram for the waste mass flows. \n
        Calls the ``plotly.graph_objs.Sankey`` to plot sankey. \n
        Calculates the mass flows by calling ``self.get_mass_flow()``. \n
        
        :param optimized_flow: If ``True``, it plots the sankey based on the optimized waste fractions. 
                                If ``False``, it plost the sankey based on the current waste fractions by calling ``self.project.parameters_list``.
        :type optimized_flow: bool
        
        """
        if optimized_flow:
            params = [i['amount'] for i in self.optimized_x]
        else:
            params = [i['amount'] for i in self.project.parameters_list]
            self.oldx=[0 for i in range(len(params))]
            self.magnitude = len(str(int(abs(self.score)))) 
   
        product = []
        index = 0
        for _,i in self.project.parameters.param_uncertainty_dict.items():
            for j in i:
                product.append((j[3],params[index]))
                index+=1
        
        label = self.project.parameters.nodes
        source = []
        target = []
        value = []
        label_link = []
        color = []
        for x in product:
            key,frac =  x
            source.append(label.index(key[0]))
            target.append(label.index(key[1]))
            label_link.append(key[2])
            color.append('rgba({},{},{}, 0.8)'.format(*np.random.randint(256, size=3))) 
            mass=0
            for m in self.project.CommonData.Index:
                mass += self.get_mass_flow((key[0]+'_product',m+'_'+key[2]),'WasteToProcess',params)
                mass += self.get_mass_flow((key[0]+'_product',key[2]),'WasteToProcess',params)
                
            value.append(np.round(mass*frac,3))
        
        print("""
              # Sankey Mass flows
              label= {}
              source= {}
              target= {}
              label_link= {}
              value= {}""".format(label,source,target,label_link,value))
        
        node = dict(pad = 20,
                    thickness = 20,
                    line = dict(color = "black", width = 0.5),
                    label = label,
                    color = "blue")
        
        link = dict(source = source, 
                    target = target,
                    value = value,
                    label = label_link,
                    color = color)
        
        # The other good option for the valueformat is ".3f". Yes
        plot(go.Figure(data=[go.Sankey( valueformat = ".3s",
                                             valuesuffix = "Mg",
                                             node = node,
                                             link = link)]))