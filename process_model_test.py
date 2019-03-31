from process_model import *
from full_system import *
from process_model_output import *
import material_properties


#def main ():
	# instantiate process model name, required_inputs, allowable_inputs, allowable_waste_outputs, allowable_bio_techno_outputs, process_model_inputs, material_properties
	
	
	#cl = Collection('test',['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c'],[material_properties.Yard_Trimmings_Branches.get_chemical_properties()])
	#tr = Treatment('test2',['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c'],'more material properties here')
	#
	#cl.create_output('Initial','Food','Waste','RWCS-RWC-WtE',0.5)
	#cl.create_output('Initial','Food','Waste','RWCS-RWC-WtE',0.6)
	#cl.create_output('RWCS-RWC-WtE','Food','Waste','RWCS-RWC-WtE',0.6)
	#cl.write_output('a.csv')
#del databases["Waste"]
a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')
SWOLF_data = a.read_output_from_SWOLF ("Landfill", "trad_landfill.xlsx")
tr = Treatment('Landfill',['a','b','c'],['a','b','c'],{},{},['a','b','c'],'more material properties here')
tr.import_from_SWOLF(SWOLF_data)
data = tr.get_output()
tr.write_output('test.csv')
print('Importing Full System')
fs = FullSystem('test.csv','database_TT2.csv')
print('Running Full System')
fs.run_no_TT_from_memory(data)

	#example to run full system
	#fs = FullSystem('a.csv','eco_invent_TT.csv','biosphere_TT.csv','database_TT.csv')
	#fs.run()

#if __name__ == '__main__':
#    main()
