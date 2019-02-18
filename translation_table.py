from file_handler import *

class TranslationTable:
	def __init__(self, file_path):
		self.fh = FileHandler()
		self.fh.loadCSV(file_path)
		
	def getVal(self, key):
		return self.fh.data[key]
		
	
