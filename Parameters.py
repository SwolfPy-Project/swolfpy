from project_class import *

class Parameters():
	def __init__ (self):
		self.param_uncertainty_dict = dict()
		self.params_dict = dict()
	
	def add_parameter (self, waste_stream, process_model_from, process_model_to):
		long_name = 'frac_of_' + waste_stream + '_from_' + process_model_from + '_to_' + process_model_to
		key = waste_stream + process_model_from
		if key not in self.param_uncertainty_dict.keys():
			self.param_uncertainty_dict[key] = list()
			self.param_uncertainty_dict[key].append([process_model_to, 0.0, long_name])
		else:
			self.param_uncertainty_dict[key].append([process_model_to, 0.0, long_name])
			
	def update_values (self, long_name, val):
		for items in self.param_uncertainty_dict.values():
			for list_item in items:
				if list_item[2] == long_name:
					list_item[1] = val

		
	def check_sum(self):
		sum = 0
		flag = 1
		for item in self.param_uncertainty_dict.values():
			for list_item in item:
				sum += list_item[1]
				if sum != 1:
					print("sum is %d and not equal to 1!" %(sum))
					for i in item:
						print ("%s : %f" % (i[2],i[1]))
					sum = 0
					flag = 0
					break
			sum = 0
		return flag
			
		
	def set_params_dict(self, params_dict):
		self.params_dict = params_dict