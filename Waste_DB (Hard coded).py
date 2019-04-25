# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:10:43 2019

@author: msmsa
"""
from brightway2 import *
projects.set_current("BW2_Base")
del databases["Waste"]

db = Database("Waste")

data = {
        
("Waste", 'Initial'): {
    "name": 'initial',
    "location":'RNA',
    "exchanges": [{
    "amount": 1.0,
    "input": ('WTE', 'WTE-Yard Trimmings, Grass'),
     'uncertainty type': 4,
     "minimum":0.5,
     "maximum":1.5,
              'scale without pedigree': 0.1414213562373095,
                           'scale': 0.2,
                           'pedigree': {
                               'completeness': 5,
                               'further technological correlation': 1,
                               'geographical correlation': 5,
                               'reliability': 4,
                               'temporal correlation': 3
                           },
    "type": "technosphere"
    }],
       'unit': 'Mg',
},
        
("Waste", '3 : Bottom Ash'): {
    "name": '3 : Bottom Ash',
    "exchanges": [{
    "amount": 1.0,
    "input": ('LF', 'Landfill-Bottom Ash'),
    "type": "technosphere"
    }],
       'unit': 'Mg',
},
        
("Waste", '4 : Fly Ash'): {
    "name": '4 : Fly Ash',
    "exchanges": [{
    "amount": 1.0,
    "input": ('LF', 'Landfill-Fly Ash'),
    "type": "technosphere"
    }],
    'unit': 'Mg',
},
            
("Waste", '5 : Separated Organics'): {
    "name": '5 : Separated Organics',
    "exchanges": [],
       'unit': 'Mg',
    } ,

("Waste", '6 : Other Residual'): {
    "name": '6 : Other Residual',
    "exchanges": [],
       'unit': 'Mg',
} ,
            
("Waste", '7 : RDF'): {
    "name": '7 : RDF',
    "exchanges": [],
       'unit': 'Mg',
    } ,
("Waste", '8 : Wastewater'): {
    "name": '8 : Wastewater',
    "exchanges": [],
       'unit': 'Mg',
} ,
            
("Waste", '9 : OCC'): {
    "name": '9 : OCC',
    "exchanges": [],
       'unit': 'Mg',
    } ,
    
("Waste", '10 : Mixed Paper'): {
    "name": '10 : Mixed Paper',
    "exchanges": [],
       'unit': 'Mg',
} ,
            
("Waste", '11 : ONP'): {
    "name": '11 : ONP',
    "exchanges": [],
       'unit': 'Mg',
    } ,
("Waste", '12 : OFF'): {
    "name": '12 : OFF',
    "exchanges": [],
       'unit': 'Mg',
} ,
            
("Waste", '13 : Other'): {
    "name": '13 : Other',
    "exchanges": [],
       'unit': 'Mg',
    } ,
        
("Waste", '14 : PET (#1)'): {
    "name": '14 : PET (#1)',
    "exchanges": [],
       'unit': 'Mg',
} ,
            
("Waste", '15 : HDPE-Unsorted (#2)'): {
    "name": '15 : HDPE-Unsorted (#2)',
    "exchanges": [],
       'unit': 'Mg',
    } ,

("Waste",  '16 : HDPE-P (#2A)'): {
    "name":  '16 : HDPE-P (#2A)',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '17 : HDPE-T (#2B)'): {
    "name":  '17 : HDPE-T (#2B)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '18 : PVC (#3)'): {
    "name":  '18 : PVC (#3)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '19 : LDPE/Film ( #4)'): {
    "name":  '19 : LDPE/Film ( #4)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '20 : Polypropylene (#5)'): {
    "name":  '20 : Polypropylene (#5)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '21 : Polystyrene (#6)'): {
    "name":  '21 : Polystyrene (#6)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '22 : Other (#7)'): {
    "name":  '22 : Other (#7)',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '23 : Mixed Plastic'): {
    "name":  '23 : Mixed Plastic',
    "exchanges": [],
       'unit': 'Mg',
} ,


("Waste",  '24 : Al'): {
    "name":  '24 : Al',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '25 : Fe'): {
    "name":  '25 : Fe',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '26 : Cu'): {
    "name":   '26 : Cu',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '27 : Brown'): {
    "name":  '27 : Brown',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '28 : Clear'): {
    "name":  '28 : Clear',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '29 : Green'): {
    "name":  '29 : Green',
    "exchanges": [],
       'unit': 'Mg',
} ,

("Waste",  '30 : Mixed Glass'): {
    "name":  '30 : Mixed Glass',
    "exchanges": [],
       'unit': 'Mg',
}      
    }
         
db.write(data)
