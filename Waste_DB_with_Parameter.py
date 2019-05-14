# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:36:54 2019

@author: msmsa
"""
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group


projects.set_current('BW2_S1')




db = Database('Collection_SF')
act = db.get('Yard_Trimmings_Branches')



project_data = [
        {
    'name': 'percent_to_WTE',
    'amount': 0.5
},
{
    'name': 'percent_to_LF',
    'formula': '1 - percent_to_WTE',
} 
]
parameters.new_project_parameters(project_data)
parameters.add_exchanges_to_group("my group", act)
ActivityParameter.recalculate_exchanges("my group")


"""
from Waste_DB import *
Waste_DB = WasteDB()
Initial = Exchange()
Initial.add_exchange(("Collection_SF", 'SF_Collection'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity("Initial","Initial","Mg",Initial)
Waste_DB.write() 
"""


projects.set_current('BW2_S1')
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print ("WTE+ LF  :", lca.score)


project_data2 = [
    {'name': 'percent_to_WTE', 'amount': 0.5},
    {'name': 'percent_to_LF', 'formula': '1 - percent_to_WTE',} 
]


parameters.new_project_parameters(project_data2)
parameters.add_exchanges_to_group("my group", act)
ActivityParameter.recalculate_exchanges("my group")

projects.set_current('BW2_S1')
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print ("just WTE :",lca.score)


project_data3 = [
        {
    'name': 'percent_to_WTE',
    'amount': 0
},
{
    'name': 'percent_to_LF',
    'formula': '1 - percent_to_WTE',
} 
]
parameters.new_project_parameters(project_data3)
parameters.add_exchanges_to_group("my group", act)
ActivityParameter.recalculate_exchanges("my group")

projects.set_current('BW2_S1')
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print ("just LF :",lca.score)
