# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:10:43 2019

@author: msmsa
"""
from brightway2 import *

if "Collection_SF" in databases:
    del databases["Collection_SF"]

db = Database("Collection_SF")

data = {
("Collection_SF", 'Yard_Trimmings_Branches_res'): {
    "name": 'Yard_Trimmings_Branches_res',
    "exchanges": [
    {"amount": 0,
     "formula":"res_to_LF",
    "input": ('LF', 'Landfill-Yard_Trimmings_Branches'),
    "type": "technosphere"},
     
     {"amount": 0,
     "formula":"res_to_WTE",
    "input": ('WTE', 'WTE-Yard_Trimmings_Branches'),
    "type": "technosphere"},
     
    {"amount": 9.88,
    "input": ("Waste_technosphere", 'Collection_Diesel'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
},
    
("Collection_SF", 'Ferrous_Cans_rec'): {
    "name": 'Ferrous_Cans_rec',
    "exchanges": [
    {"amount": 0,
     "formula":"rec_to_SS_MRF",
    "input": ('SS_MRF', 'SS_MRF-Ferrous_Cans'),
    "type": "technosphere"},

    {"amount": 9.88,
    "input": ("Waste_technosphere", 'Collection_Diesel'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
},

("Collection_SF", 'Yard_Trimmings_Branches_moc'): {
    "name": 'Yard_Trimmings_Branches_moc',
    "exchanges": [
    {"amount": 9.88,
    "input": ("Waste_technosphere", 'Collection_Diesel'),
    "type": "technosphere"},
    {"amount": 0,
     "formula":"moc_to_AD",
    "input": ('AD', 'AD-Yard_Trimmings_Branches'),
    "type": "technosphere"},
    {"amount": 0,
     "formula":"moc_to_AC",
    "input": ('Composting', 'Composting-Yard_Trimmings_Branches'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
},    
    
("Collection_SF", 'SF_Collection'): {
    "name": 'SF_Collection',
    "exchanges": [
            
    {"amount": 1,
    "input": ("Collection_SF", 'Yard_Trimmings_Branches_res'),
    "type": "technosphere"},
         
     {"amount": 1,
    "input": ("Collection_SF", 'Yard_Trimmings_Branches_moc'),
    "type": "technosphere"},
         
     {"amount":0,
    "input": ("Collection_SF", 'Ferrous_Cans_rec'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
},
    
  }     
    
db.write(data)