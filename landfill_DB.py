from process_model import *
from full_system import *
from process_model_output import *
import material_properties

import time
import datetime


t3 = time.time()


if "LF" in databases:
    del databases["LF"]



a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')

SWOLF_data = a.read_output_from_SWOLF ("Landfill", "trad_landfill _BW2.xlsx")

tr = Treatment('Landfill') 
tr.import_from_SWOLF(SWOLF_data)

tr.write_output('test.csv')
print('Importing Full System')
fs = FullSystem('test.csv','database_TT_LF.csv')
print('Running Full System')
t1 = time.time()
fs.run_no_TT()
t2 = time.time()
print('Time to run full system: %0.1f secs' % (t2-t1))
print('Total time to run: %0.1f secs' % (t2-t3))


"""
print('Running LCA')

db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC 2007', 'climate change', 'GWP 100a')) 
lca.lci()
lca.lcia()
print(lca.score)
"""