from process_model import *
from full_system import *
from process_model_output import *
import material_properties
import time
import datetime





#del databases["Waste"]
a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')
SWOLF_data = a.read_output_from_SWOLF ("Landfill", "trad_landfill.xlsx")
tr = Treatment('Landfill',['a','b','c'],['a','b','c'],{},{},['a','b','c'],'more material properties here')
tr.import_from_SWOLF(SWOLF_data)
data = tr.get_output()
tr.write_output('landfill.csv')

print('Importing Full System')
fs = FullSystem('landfill.csv','database_TT3.csv')
print('Running Full System')
t1 = time.time()
fs.run_no_TT_from_memory(data)
t2 = time.time()
print('Time to run full system: %0.1f secs' % (t2-t1))
#
#
#
#
#db = Database("Waste")
#functional_unit = {db.get("Initial") : 1}
#lca = LCA(functional_unit, ('IPCC 2013', 'climate change', 'GWP 100a')) 
#lca.lci()
#lca.lcia()
#lca.score