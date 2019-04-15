# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:03:36 2019

@author: msmsa
"""
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print("grass WTE ", "IPCC 2007 SWOLF ",lca.score)

"""Test"""