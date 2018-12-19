class File_Handler:
	def __init__(self):
		pass
			
	def setFileList(self,files):
		self.files=files
		
	def getFileList(self):
		return self.files
	
	#def load_csv(self, file_path):
	#	import csv
	#	with open(file_path, 'r') as f:
	#		reader = csv.reader(f)
	#		self.data = list(list(rec) for rec in csv.reader(f, delimiter=','))
	#	f.close()
	
	def load_csv (self, file_path): #só tá lendo chave e valor..não lê mais nada
		import csv
		with open(file_path, mode='r') as infile:
			next(infile) #skip header
			reader = csv.reader(infile)
			self.data = {rows[1]:float(rows[2]) for rows in reader}
		infile.close()