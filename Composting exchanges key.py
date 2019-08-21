# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:32:49 2019

@author: msardar2
"""

from brightway2 import *
projects.set_current('demo_5')
db=Database('COMP')
act = db.search('COMP_Yard_Trimmings_Leaves')[0]

for x in act.exchanges():
    print(get_activity(x.as_dict()['input']).key,get_activity(x.as_dict()['input']).as_dict()['name']\
  ,get_activity(x.as_dict()['input']).as_dict()['categories'] if 'categories' in get_activity(x.as_dict()['input']).as_dict().keys() else '' )




# =============================================================================
# ('COMP_product', 'Yard_Trimmings_Leaves_Other_Residual') COMP_product_Yard_Trimmings_Leaves_Other_Residual 
# ('Technosphere', 'Electricity_consumption') Electricity_consumption 
# ('Technosphere', 'Equipment_Diesel') Equipment_Diesel 
# ('Technosphere', 'Internal_Process_Transportation_Medium_Duty_Diesel_Truck') Internal_Process_Transportation_Medium_Duty_Diesel_Truck 
# ('Technosphere', 'Empty_Return_Medium_Duty_Diesel_Truck') Empty_Return_Medium_Duty_Diesel_Truck 
# ('Technosphere', 'Nitrogen_Fertilizer') Nitrogen_Fertilizer 
# ('Technosphere', 'Phosphorous_Fertilizer') Phosphorous_Fertilizer 
# ('Technosphere', 'Potassium_Fertilizer') Potassium_Fertilizer 
# ('Technosphere', 'Peat') Peat 
# ('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014') Ammonia ('air',)
# ('biosphere3', 'e4e9febc-07c1-403d-8d3a-6707bb4d96e6') Carbon dioxide, from soil or biomass stock ('air',)
# ('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7') Carbon dioxide, non-fossil ('air',)
# ('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98') Dinitrogen monoxide ('air',)
# ('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8') Methane, non-fossil ('air',)
# ('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457') Nitrogen oxides ('air',)
# ('biosphere3', 'd3260d0e-8203-4cbb-a45a-6a13131a5108') NMVOC, non-methane volatile organic compounds, unspecified origin ('air',)
# ('biosphere3', 'b9291c72-4b1d-4275-8068-4c707dc3ce33') Nitrate ('water', 'ground-')
# ('biosphere3', '7ce56135-2ca5-4fba-ad52-d62a34bfeb35') Nitrate ('water', 'surface water')
# =============================================================================




