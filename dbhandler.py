from brightway2 import *

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
		
## Example##		
#a = Exchange()
#a.add_exchange(('ecoinvent 3.4 cutoff', 'f64cdcbe8d33b115b227231335e47b63'),1.0,'tkm','technosphere')
#a.add_exchange(('ecoinvent 3.4 cutoff', '8a4d020ef16489760b886f3c95aeaed1'),2.0,'tkm','technosphere')
#b = DatabaseHandler ('auto_test')
#b.add_activity('1234','transport', a, 'kg')

food_mass = 0.4
food_ch4_yield_per_Mg = 12

# Creating DB
dh = DatabaseHandler('auto_MSW')

#Creating activities
dh.add_activity ('1','Initial','Mg')
dh.add_activity ('2','Food Collection', 'Mg')
dh.add_activity ('3','Food Landfill', 'Mg')

#Creating exchanges
ex = Exchange()
ex.add_exchange((dh.get_db_name(), '2'), food_mass, 'Mg', 'technosphere')

ex2 = Exchange()
ex2.add_exchange((dh.get_db_name(), '3'), food_mass, 'Mg', 'technosphere')
ex2.add_exchange(('ecoinvent 3.4 cutoff', 'bfcd07940a319765aec1555ad12643f8'), 4, 'kg', 'technosphere')
ex2.add_exchange(('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'), 5, 'kg', 'biosphere')

ex3 = Exchange()
ex3.add_exchange(('ecoinvent 3.4 cutoff', 'bfcd07940a319765aec1555ad12643f8'), 2, 'kg', 'technosphere')
ex3.add_exchange(('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'), 4, 'kg', 'biosphere')
ex3.add_exchange(('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8'), food_mass*food_ch4_yield_per_Mg, 'kg', 'biosphere')

#Linking activities with exchanges
dh.add_exchanges('1', ex)
dh.add_exchanges('2', ex2)
dh.add_exchanges('3', ex3)

#Writing to DB
dh.write() 



		
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