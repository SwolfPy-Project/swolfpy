# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:20:53 2019

@author: msmsa
"""

from brightway2 import *
projects.set_current('test')
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}


result = []
t3 = time.time()
for x in range(10):
    if "LF" in databases:    
        del databases["LF"]
    a = ProcessModelOutput()
    a.create_waste_technosphere()
    #print('Importing SWOLF data')

    SWOLF_data = a.read_output_from_SWOLF ("Landfill", "trad_landfill _BW2.xlsx")
    tr = Treatment('Landfill') 
    tr.import_from_SWOLF(SWOLF_data)

    tr.write_output('test.csv')
    fs = FullSystem('test.csv','database_TT_LF.csv')
    t1 = time.time()
    fs.run_no_TT()
    t2 = time.time()
    print('Time to run full system: %0.1f secs' % (t2-t1))
    print('Total time to run: %0.1f secs' % (t2-t3))
            
    lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
    lca.lci()
    lca.lcia()
    result.append(lca.score)