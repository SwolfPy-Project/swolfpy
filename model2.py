from typing import List

#type is a list ex. [SSMRF, LF, WTE] 
#waste_strm_in is a list of lists. elements at [0], corresponds to type [0] 
#waste_strm_out is a list of lists. elements at [0], corresponds to type [0]

class Model2:
	def __init__(self, type: List, waste_strm_in, waste_strm_out):
		self.type = type
		self.waste_strm_in = waste_strm_in
		self.waste_strm_out = waste_strm_out 
		
	def get_waste_strm_in (self, name):
		return self.waste_strm_in[self.type.index(name)]
		
	def get_waste_strm_out (self, name):
		return self.waste_strm_out[self.type.index(name)]	
	
	def get_type_index(self, name):
		return self.type.index(name)
	
	def get_type_name(self, index):
		return self.type[index]
	