# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:09:14 2020

@author: msmsa
"""
from brightway2 import LCA

class LCA_matrix(LCA):
    """ 
    This class translate the ``row`` and ``col`` of the ``tech_param`` and ``bio_param`` to
    the acticity `key` in the Brightway2 database. \n
    Both the ``tech_param`` and ``bio_param`` has the ``dtype=[('input', '<u4'), ('output', '<u4'), 
    ('row', '<u4'), ('col', '<u4'), ('type', 'u1'), ('uncertainty_type', 'u1'), ('amount', '<f4'),
    ('loc', '<f4'), ('scale', '<f4'), ('shape', '<f4'), ('minimum', '<f4'), ('maximum', '<f4'),
    ('negative', '?')])`` data type. \n
    
    ``self.tech_matrix`` is a dictionary that includes all the technosphere and waste exhanges as tuple ``(product,Feed)`` key and amount as value:
    ``{(('LF', 'Aerobic_Residual'), ('SF1_product', 'Aerobic_Residual_MRDO')):0.828}``
           
    ``self.bio_matrix`` is a dictionary taht includes all the biosphere exhanges as tuple ``(product,Feed)`` `key` and amount as `value`
    ``{(('biosphere3', '0015ec22-72cb-4af1-8c7b-0ba0d041553c'), ('Technosphere', 'Boiler_Diesel')):6.12e-15}``
    
    So we can update the ``tech_params`` and ``bio_params`` by tuple keys that are consistant with the keys
    in the ``ProcessMolde.report()``. Check :ref:`Process models class <ProcessModel>` for more info.
    """
    def __init__(self, functional_unit, method):
        super().__init__(functional_unit, method[0])
        self.lci()
        self.lcia()
        
        self.functional_unit = functional_unit
        self.method = method

        self.activities_dict,_,self.biosphere_dict = self.reverse_dict()
        
        self.tech_matrix = dict()
        for i in self.tech_params:
            self.tech_matrix[(self.activities_dict[i[2]], self.activities_dict[i[3]])] = i[6]
        
        self.bio_matrix = dict()        
        for i in self.bio_params:
            if (self.biosphere_dict[i[2]], self.activities_dict[i[3]]) not in self.bio_matrix.keys():
                self.bio_matrix[(self.biosphere_dict[i[2]], self.activities_dict[i[3]])] = i[6]
            else:
                self.bio_matrix[(str(self.biosphere_dict[i[2]]) + " - 1", self.activities_dict[i[3]])] = i[6]
                #print((str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]]))