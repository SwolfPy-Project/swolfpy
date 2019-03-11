import csv
class FileHandler:
	def __init__(self):
		pass
			
	def setFileList(self,files):
		self.files=files
		
	def getFileList(self):
		return self.files
	


	def loadCSV (self, file_path): #só lê chave e valor
		with open(file_path, mode='r') as infile:
			next(infile) #skip header
			reader = csv.reader(infile)
			self.data = {rows[0]:(rows[1]) for rows in reader}
		infile.close()
		
	def loadCSVList (self, file_path):
		with open(file_path, mode='r') as infile:
			next(infile)
			reader = csv.reader(infile)
			self.data = list(list(rec) for rec in csv.reader(infile, delimiter=','))
		infile.close()

		

	def writeCSVList (self, file_path, data):
		csv.register_dialect('myDialect', delimiter = ',', lineterminator = '\n')
		with open(file_path, 'w', newline='') as outfile:
			outfile.write('Activity,Material,Database,Key,Amount\n') #header 		
			writer = csv.writer(outfile, dialect='myDialect')
			writer.writerows(data)
		outfile.close()
		
	def appendCSVList (self, file_path, data):
		csv.register_dialect('myDialect', delimiter = ',', lineterminator = '\n')
		with open(file_path, 'a', newline='') as outfile:	
			writer = csv.writer(outfile, dialect='myDialect')
			writer.writerows(data)
		outfile.close()
	
	
