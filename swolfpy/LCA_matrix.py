# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:09:14 2020

@author: msmsa
"""
from brightway2 import LCA

class LCA_matrix(LCA):
    def __init__(self, functional_unit, method, project):
        """
        tech_matrix is dictionary include all the exhange as tuple (product,Feed) key and amount as value
        {(('LF', 'Aerobic_Residual'), ('SF1_product', 'Aerobic_Residual_MRDO')):0.8288506683507344}
               
        bio_matrix is dictionary include all the exhange as tuple (product,Feed) key and amount as value
        {(('biosphere3', '0015ec22-72cb-4af1-8c7b-0ba0d041553c'), ('Technosphere', 'Boiler_Diesel')):6.12e-15}
        
        So we can update the tech_params and bio_params by the keys      
        """
        super().__init__(functional_unit, method[0])
        self.lci()
        self.lcia()
        
        self.project = project
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