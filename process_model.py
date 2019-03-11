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
		self.outputs['Biosphere'] = list()
		self.outputs['Technosphere'] = list()
		self.outputs['Waste'] = list()
		self.outputs['Initial'] = list()
		self.check_process_model()
		
	def check_process_model (self):
		for value in self.required_inputs:
			if value not in self.process_model_inputs:
				raise Exception ('Required input {} not available in Process Model inputs' .format(value))
	
	
	def check_outputs(self, db):
		if db not in ['Biosphere', 'Technosphere', 'Waste']:
			raise Exception ('{} not a Biosphere, Technosphere, Waste output' .format(db))
	
	
	def create_output(self, flow, material, db, code, amount):
		self.check_outputs(db)
		temp = list()
		temp.append(flow)
		temp.append(material)
		temp.append(db)
		temp.append(code)
		temp.append(amount)
		if flow == 'Initial':
			self.outputs[flow].append(temp)
		else:
			self.outputs[db].append(temp)
			
	
	def write_output(self, filename): 
		write = FileHandler()
		write.writeCSVList (filename,self.outputs['Initial'])
		write.appendCSVList (filename,self.outputs['Biosphere'])
		write.appendCSVList (filename,self.outputs['Technosphere'])
		write.appendCSVList (filename,self.outputs['Waste'])
		
				
class Collection(ProcessModel):
	
	def __init__ (self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties):
		ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties)
		

class Treatment(ProcessModel):

		def __init__ (self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties):
			ProcessModel.__init__(self, name, required_inputs, allowable_inputs, allowable_outputs, process_model_inputs, material_properties)

			
