class UserModel:

	def __init__(self,name,type,waste_strm_in,waste_strm_out):
		self.name = name
		self.type = type
		self.waste_strm_in = waste_strm_in
		self.waste_strm_out = waste_strm_out
	
	def set_waste_strm_in(self,list):
		self.waste_strm_in = list
		
	def set_waste_strm_out(self,list):
		self.waste_strm_out = list
	