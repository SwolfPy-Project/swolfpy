from process_model import *
from full_system import *
import material_properties

# instantiate process model name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties:


cl = Collection('test',['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c'],[material_properties.Yard_Trimmings_Branches.get_chemical_properties()]

tr = Treatment('test2',['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c'],'material properties object here')

cl.create_output('Initial','Food','Waste','RWCS-RWC-WtE',0.5)
cl.create_output('Initial','Food','Waste','RWCS-RWC-WtE',0.6)
cl.create_output('RWCS-RWC-WtE','Food','Waste','RWCS-RWC-WtE',0.6)
cl.write_output('a.csv')

#example to run full system
#fs = FullSystem('a.csv','eco_invent_TT.csv','biosphere_TT.csv','database_TT.csv')
#fs.run()
