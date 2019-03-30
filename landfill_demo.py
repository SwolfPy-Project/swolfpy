from process_model import *
from full_system import *
from process_model_output import *
import material_properties






del databases["Waste"]
a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')
SWOLF_data = a.read_output_from_SWOLF ("Landfill", "trad_landfill.xlsx")
tr = Treatment('Landfill',['a','b','c'],['a','b','c'],{},{},['a','b','c'],'material properties here') 
tr.import_from_SWOLF(SWOLF_data)

tr.write_output('test.csv')
print('Importing Full System')
fs = FullSystem('test.csv','database_TT2.csv')
print('Running Full System')
fs.run_no_TT()
print('Running LCA')

db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC 2013', 'climate change', 'GWP 100a')) 
lca.lci()
lca.lcia()
lca.score