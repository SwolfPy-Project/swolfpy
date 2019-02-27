from file_handler import *
from excel_model import *

class UserModel:

	def __init__(self,name,type,waste_strm_in,waste_strm_out,model_file_type,model_file_path,inputs,outputs):
		self.name = name
		self.type = type
		self.waste_strm_in = waste_strm_in
		self.waste_strm_out = waste_strm_out
		self.model_file_type = model_file_type
		self.model_file_path = model_file_path
		
		
		if model_file_type == 'Excel':
			self.excel_model = Excel_Model()
			self.excel_model.load_binary(self.model_file_path)


			self.excel_model.set_named_range(inputs)
			self.calculated_outputs = self.excel_model.read_named_range(outputs)
			
	
	def set_waste_strm_in(self,list):
		self.waste_strm_in = list
		
	def set_waste_strm_out(self,list):
		self.waste_strm_out = list
	