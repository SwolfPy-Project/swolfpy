# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:18:42 2019

@author: msmsa
"""

from brightway2 import *

if True:
    if "BW2_Base" in projects:
        projects.delete_project('BW2_Base',delete_dir=True) # be sure to delete the directory also
    
    projects.create_project("BW2_Base")
    projects.set_current("BW2_Base")
    
    print ("\n", "######    Setup new project","     ######") 
    bw2setup()  # creating the methods
    
    print ("\n", "######    Importing ----->  SWOLF WASTE TECHNOSPHERE","     ######") 
    from process_model_output import *     # create the waste_technosphere


print ("\n", "######    Importing ----->  SWOLF METHODS","     ######" )
from SWOLF_method import *   # adding the methods
    

from Waste_DB import *
Waste_DB = WasteDB()
Waste_DB.write()         # create an empty waste Database

for j in ["WTE_DB", "landfill_DB"]:         # importing the processes' databases
    print ("\n", "######    Importing -----> ",j , "     ######" )
    exec("from %s import *" % j)
    
    

Bottom_ash = Exchange()
Bottom_ash.add_exchange(('LF', 'Landfill-Bottom Ash'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity('3 : Bottom Ash','3 : Bottom Ash',"Mg",Bottom_ash)
Fly_Ash = Exchange()
Fly_Ash.add_exchange(('LF', 'Landfill-Fly Ash'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity('4 : Fly Ash','4 : Fly Ash',"Mg",Fly_Ash)


Initial = Exchange()
Initial.add_exchange(('WTE', 'WTE-Yard Trimmings, Grass'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity("Initial","Initial","Mg",Initial)
Waste_DB.write() 


print ("\n", "######    Running the LCA      ######")
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print("grass Grass ", "IPCC 2007 SWOLF ",lca.score)


print ("\n", "######    Adding new initial     ######")

Initial2 = Exchange()
Initial2.add_exchange(('LF', 'Landfill-Yard Trimmings, Grass'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity("Initial2","Initial2","Mg",Initial2)
Bottom_ash = Exchange()
Bottom_ash.add_exchange(('LF', 'Landfill-Fly Ash'), 1, 'Mg', 'technosphere')
Waste_DB.dbh.add_activity('3 : Bottom Ash','3 : Bottom Ash',"Mg",Bottom_ash)
Waste_DB.write() 

print ("\n", "######    Running the LCA      ######")
db = Database("Waste")
functional_unit = {db.get("Initial2") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print("grass LF ", "IPCC 2007 SWOLF ",lca.score)


print ("\n", "######    Running the Comparative LCA with multi impact categories      ######")

list_functional_units = [{db.get("Initial"):1}, {db.get("Initial2"):1}]
list_methods = [('IPCC_2007_SWOLF', 'climate change', 'GWP100yr'),
                ('TRACI', 'environmental impact', 'acidification'),
                ('TRACI', 'environmental impact', 'ecotoxicity'),
                ('TRACI', 'environmental impact', 'eutrophication'),
                ('TRACI', 'environmental impact', 'ozone depletion')
                ]
calculation_setups['WTE_vs_LF']={'inv':list_functional_units, 'ia':list_methods}
calculation_setups['WTE_vs_LF']
lca = MultiLCA('WTE_vs_LF') 
lca.results
import pandas as pd
pd.DataFrame(index=['IPCC_2007_SWOLF','acidification','ecotoxicity','eutrophication','ozone depletion'], columns=["WTE", "LF"], data=lca.results.T)






print ("\n", "######    Creating new project _ new scenario with different waste DB or process DB     ######")
       
projects.copy_project("BW2_S1")
print("(name , number of DB, size(GB)) \n" , projects.report() )  



  

       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       