from db_handler import *
from translation_table import *
from file_handler import *


#issues: 1) no way of distinguishing biosphere and technosphere flows. 2) some exchanges are not fully connected. 
#Check if we should append the material name to the activity


#loading model file
model = FileHandler()
model.loadCSVList('full_system.csv')

#loading translatin tables
ei = TranslationTable ('eco_invent_TT.csv')
bios = TranslationTable ('biosphere_TT.csv')
db_tt = TranslationTable('database_TT.csv')

bw2_databases = list()
user_databases = list()

for key, value in databases.items():
	bw2_databases.append(key)
for key, value in db_tt.asDict().items():
	user_databases.append(value)

create_db = set(user_databases) - set(bw2_databases) #only allows 1 user database creation

dbh = DatabaseHandler(create_db.pop())
	
#getting all unique activities
activities = list()
for val in model.data:
	if val[0] not in activities:
		activities.append(val[0])

#creating all activities. Using Mg for all and using the same name as key
for val in activities:
	dbh.add_activity(val,val,'Mg')

#reading all exchanges. Each item of the dict will be an exchange Class
exchanges = dict()
for activity in activities:
	exchanges[activity] = Exchange()

for activity in activities:
	for val in model.data:
		if val[0] == activity:
			if val[2] == dbh.get_db_name(): #self loop
				exchanges[activity].add_exchange((db_tt.getVal(val[2]),val[3]),float(val[4]),'Mg','technosphere')
			elif val[2] == 'biosphere': #biosphere flow. We have to find a way to identify this
				a = get_activity((db_tt.getVal(val[2]),bios.getVal(val[3]))) #to find corresponding unit
				exchanges[activity].add_exchange((db_tt.getVal(val[2]),bios.getVal(val[3])),float(val[4]),a.as_dict()['unit'],'biosphere')
			elif val[2] == 'ecoinvent': #technosphere flow. We have to find a way to identify this
				a = get_activity((db_tt.getVal(val[2]),ei.getVal(val[3]))) #to find corresponding unit
				exchanges[activity].add_exchange((db_tt.getVal(val[2]),ei.getVal(val[3])),float(val[4]),a.as_dict()['unit'],'technosphere')
			

#Linking activities with exchanges
for val in activities:
	dbh.add_exchanges(val, exchanges[val])

#Writing to DB
dbh.write() 
			

	

