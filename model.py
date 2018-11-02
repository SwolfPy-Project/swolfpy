class Model:
	def __init__(self, file_path):
		import csv
		with open(file_path, 'r') as f:
			reader = csv.reader(f)
			self.data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		f.close()
	
	def load_excel (self, excel_path):
		from koala.ExcelCompiler import ExcelCompiler
		c = ExcelCompiler(excel_path)
		self.sp = c.gen_graph() 
		
class Load_Model:
	def __init__(self, files):
		self.load = []
		import csv		
		for i in range(len(files)):
			self.load.append(Model(files[i]))
			
#for row in data:
#        print (row[0]) 
#        for val in row: 
#            print (val)