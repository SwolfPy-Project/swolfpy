from brightway2 import *
from bw2data import query

class Exchange:

	def __init__(self):
		self.data = []
		
	def add_exchange (self, db_code, amount, unit, type):
		temp = dict()
		temp['input'] = db_code
		temp['amount'] = amount
		temp['unit'] = unit
		temp['type'] = type
		self.data.append(temp)
		
	def get_exchanges(self):
		return self.data
	
	def __repr__(self):
		string = str()
		for i in self.data:
			string =  string + str(i['input']) + ' - ' + str(i['amount']) + ' ' +str(i['unit']) + ', '  
		return string

class DatabaseHandler:

	def __init__(self, name):
		self.db = Database(name)
		self.db_name = name
		self.data = dict()
		
	def add_activity (self, id, name, unit, exchanges=[]):
		if not exchanges:
			self.data[(self.db_name, id)] = {"name": name, "exchanges": exchanges, "unit":unit}
		else:
			self.data[(self.db_name, id)] = {"name": name, "exchanges": exchanges.get_exchanges(), "unit":unit}
			
				
	def add_exchanges (self, id, exchanges):
		self.data[(self.db_name, id)]["exchanges"] = exchanges.get_exchanges()
	
	def write(self):
		self.db.write(self.data)
		
	def get(self, name):
		return self.db.get(name)
		
	def add_location(self, name, where):
		temp = self.db.get(name)
		temp['location'] = where
		temp.save()
		
	def add_categories(self, name, categories):
		temp = self.db.get(name)
		temp['categories'] = categories
		temp.save()
	
	def get_db_name(self):
		return self.db_name
		
	def get_all_activities(self, name):
		temp = Database(name)
		filter = query.Filter('name', 'notin', '')
		res = temp.query(filter)
		activities = list()
		for val in res.result.values():
			activities.append(val['name'])
		return activities
		


		
#example_data = {
#    ("example", "A"): {
#        "name": "A",
#        "exchanges": [{
#            "amount": 1.0,
#            "input": ("example", "B"),
#            "type": "technosphere"
#            }],
#        'unit': 'kilogram',
#        'location': 'here',
#        'categories': ("very", "interesting")
#        },
#    ("example", "B"): {
#        "name": "B",
#        "exchanges": [],
#        'unit': 'microgram',
#        'location': 'there',
#        'categories': ('quite', 'boring')
#        }
#    }


## DB METHODS ##
#random() - returns a random activity in the database
#get(*valid_exchange_tuple*) - returns an activity, but you must know the activity key
#load() - loads the whole database as a dictionary.
#make_searchable - allows searching of the database (by default, it is already searchable)
#search - search the database

# a = query.Filter("name", "has", "oil")
# bio = Database('biosphere3')
# bio.query(a)


#a = query.Filter("name", "is", "Oil, crude, in ground")
#b = bio.query(a)
#type(b.result)
#dict

#{('biosphere3', '88d06db9-59a1-4719-9174-afeb1fa4026a'): {'categories': ('natural resource',
#   'in ground'), 'code': '88d06db9-59a1-4719-9174-afeb1fa4026a', 'name': 'Oil, crude, in ground', 'database': 'biosphere3', 'unit': 'kilogram', 'type': 'natural resource', 'exchanges': []}}

   
#c = query.Filter("code", "is", "88d06db9-59a1-4719-9174-afeb1fa4026a")

#get_activity(('ecoinvent 3.2 cutoff', '3c76fc6ab34c7842c6be5fd74cfd1c18'))

#del databases[db.name]
  
##TABLE STRUCTURE##

#CREATE TABLE "activitydataset" (
#    "id" INTEGER NOT NULL PRIMARY KEY,
#    "data" BLOB NOT NULL,
#    "code" TEXT NOT NULL,
#    "database" TEXT NOT NULL,
#    "location" TEXT,
#    "name" TEXT,
#    "product" TEXT,
#    "type" TEXT
#)
#
#CREATE TABLE "exchangedataset" (
#    "id" INTEGER NOT NULL PRIMARY KEY,
#    "data" BLOB NOT NULL,
#    "input_code" TEXT NOT NULL,
#    "input_database" TEXT NOT NULL,
#    "output_code" TEXT NOT NULL,
#    "output_database" TEXT NOT NULL,
#    "type" TEXT NOT NULL
#)