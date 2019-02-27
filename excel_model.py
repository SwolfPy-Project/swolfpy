from koala.ExcelCompiler import ExcelCompiler
from koala import Spreadsheet
#!!Bug in Koala - does not accept sheet names with spaces!!
#!!Another Bug. When you set named ranges it will not calculate. Only will calculate when set to cell val (manually)!!

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
    
a = Excel_Model()
model_file_path1 = 'AD3.gzip'
data_file_path1 = 'AD_input_data.csv'

outputs = ['elecCons']
from file_handler import *
csv_data = File_Handler()
csv_data.load_csv(data_file_path1)
a.load_excel('AD_no_spaces.xlsx')
#a.load_binary('AD3.gzip')
a.set_named_range(csv_data.data)
a.read_named_range(outputs)