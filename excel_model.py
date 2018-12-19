from koala.ExcelCompiler import ExcelCompiler
from koala import Spreadsheet
#!!Bug in Koala - does not accept sheet names with spaces!!

class Excel_Model:
	
	
	def __init__ (self):
		pass
		 			
	def load_excel(self, excel_path):
		c = ExcelCompiler(excel_path)
		self.sp = c.gen_graph()
		
	def set_val(self, cell, val):
		self.sp.set_value(cell,val)
	
	def eval(self, cell):
		return self.sp.evaluate(cell)
		
	def dump_binary(self, file):
		self.sp.dump(file)
	
	def load_binary(self, file):
		self.sp = Spreadsheet.load(file)
	
	def dump_reload(self, file):
		self.sp.dump(file)
		self.sp = Spreadsheet.load(file)
		
	def set_excel_formula(self, cell, formula):
		self.sp.set_formula(cell,formula)
		
	def clear_graph(self):
		import gc
		del self.sp
		gc.collect()
		

	def set_named_range(self, values):
		for key, value in values.items():
			self.set_val(key,value)

	def read_named_range(self, outputs):
		values = dict()
		for i in outputs:
			values[i] = self.eval(i)
		return values