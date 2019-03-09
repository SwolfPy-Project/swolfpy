#required_inputs, allowable_inputs, allowable_outputs = list
#process_model_inputs = dict

from file_handler import *

class ProcessModel(object):

	def __init__ (self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties):
		self.name = name
		self.required_inputs = required_inputs
		self.allowable_inputs = allowable_inputs
		self.allowable_outputs = allowable_outputs
		self.process_model_inputs = process_model_inputs
		self.material_properties = material_properties
		self.outputs = dict()
		self.outputs['biosphere'] = list()
		self.outputs['technosphere'] = list()
		self.outputs['waste'] = list()
		self.outputs['initial'] = list()
		self.check()
		
	def check (self):
		for value in self.required_inputs:
			if value not in self.process_model_inputs:
				raise Exception ('Required input {} not available in Process Model inputs' .format(value))

	def create_output(self, filename): #still needs refinement
		write = FileHandler()
		temp_list = list()
		for key, value in self.outputs.items():
			temp_list.append(value)
		write.writeCSVList (filename,self.outputs.values())
		
				
class Collection(ProcessModel):
	
	def __init__ (self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties):
		ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties)
		

class Treatment(ProcessModel):

		def __init__ (self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties):
			ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties)

			
a = Collection('test',['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c'],'a')
a.create_output('a.csv')