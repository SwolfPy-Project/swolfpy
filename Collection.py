# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:10:43 2019

@author: msmsa
"""
from brightway2 import *
from db_handler import *


if "Collection_SF" in databases:
    Database("Collection_SF").delete()

db = Database("Collection_SF")

data = {
("Collection_SF", 'Yard_Trimmings_Branches'): {
    "name": 'Yard Trimmings, Branches',
    "exchanges": [
    {"amount": 0,
     "formula":"percent_to_LF",
    "input": ('LF', 'Landfill-Yard_Trimmings_Branches'),
    "type": "technosphere"},
     
     {"amount": 0,
     "formula":"percent_to_WTE",
    "input": ('WTE', 'WTE-Yard_Trimmings_Branches'),
    "type": "technosphere"},
     
    {"amount": 9.88,
    "input": ("Waste_technosphere", 'Collection _Diesel  (per unit fuel)'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
},
("Collection_SF", 'SF_Collection'): {
    "name": 'SF_Collection',
    "exchanges": [
    {"amount": 1,
    "input": ("Collection_SF", 'Yard_Trimmings_Branches'),
    "type": "technosphere"}
    ],
       'unit': 'Mg',
}
  }     
db.write(data)