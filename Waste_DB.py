from db_handler import *

class WasteDB(object):

	def __init__(self):
		if "Waste" in databases:
			del databases["Waste"]
			
		self.dbh = DatabaseHandler('Waste')
		self.activities = ['Initial','3 : Bottom Ash','4 : Fly Ash','5 : Separated Organics','6 : Other Residual','7 : RDF','8 : Wastewater','9 : OCC','10 : Mixed Paper','11 : ONP','12 : OFF','13 : Other','14 : PET (#1)',
						'15 : HDPE-Unsorted (#2)','16 : HDPE-P (#2A)','17 : HDPE-T (#2B)','18 : PVC (#3)','19 : LDPE/Film ( #4)','20 : Polypropylene (#5)','21 : Polystyrene (#6)','22 : Other (#7)','23 : Mixed Plastic',
						'24 : Al','25 : Fe','26 : Cu','27 : Brown','28 : Clear','29 : Green','30 : Mixed Glass']

		for val in self.activities:
			self.dbh.add_activity(val,val,'Mg')
	
		self.exchanges = dict()

		for activity in self.activities:
			self.exchanges[activity] = Exchange()
	
	def get_activities(self, name):
		return self.dbh.get_all_activities(name)
	
	def write(self):
		self.dbh.write()



#data = {
#        
#("Waste", 'Initial'): {
#    "name": 'initial',
#    "exchanges": [{
#    "amount": 1.0,
#    "input": ('WTE', 'WTE-Yard Trimmings, Grass'),
#    "type": "technosphere"
#    }],
#       'unit': 'Mg',
#},
#        
#("Waste", '3 : Bottom Ash'): {
#    "name": '3 : Bottom Ash',
#    "exchanges": [{
#    "amount": 1.0,
#    "input": ('LF', 'Landfill-Bottom Ash'),
#    "type": "technosphere"
#    }],
#       'unit': 'Mg',
#},
#
#} ,

