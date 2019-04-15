from db_handler import *
from translation_table import *
from file_handler import *

class FullSystem:

    def __init__(self, system_CSV, databaseTT):
    
        self.system_CSV = system_CSV
        self.databaseTT=databaseTT
        
    def run_no_TT(self):
        model = FileHandler()
        model.loadCSVList(self.system_CSV)
        
        db_tt = TranslationTable(self.databaseTT)
        
        #first DB in DB TT file should be the biosphere, next one should be technosphere DB
        db_map = dict()
        db_map['biosphere'] = list(db_tt.asDict().keys())[0]
        db_map['technosphere'] = list(db_tt.asDict().keys())[1]
        db_map['Waste'] = list(db_tt.asDict().keys())[2]
        
        bw2_databases = list()
        user_databases = list()
        
        for key, value in databases.items():
            bw2_databases.append(key)
        for key, value in db_tt.asDict().items():
            user_databases.append(value)
        
        create_db = set(user_databases) - set(bw2_databases) #only allows 1 user database creation
        
        if create_db is not None:
            dbh = DatabaseHandler(create_db.pop())
            
        for val in model.data:
            if val[0] == 'Initial':
                val[3] = val[3] + '-' + val[1]
                
            elif val[2]!=dbh.get_db_name():
                val[0] = val[0] + '-' + val[1]
                
            else:
                val[0] = val[0] + '-' + val[1]
                val[3] = val[3] + '-' + val[1]
            
            
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
                        
                    elif val[2] == db_map['biosphere']: #biosphere flow. 
                    
                        a = get_activity((db_tt.getVal(val[2]),val[3])) #to find corresponding unit
                        exchanges[activity].add_exchange((db_tt.getVal(val[2]),val[3]),float(val[4]),a.as_dict()['unit'],'biosphere')
                        
                        
                    elif val[2] == db_map['technosphere']: #technosphere flow. 
                    
                        a = get_activity((db_tt.getVal(val[2]),val[3])) #to find corresponding unit
                        exchanges[activity].add_exchange((db_tt.getVal(val[2]),val[3]),float(val[4]),a.as_dict()['unit'],'technosphere')

                    elif val[2] == db_map['Waste']: #technosphere flow. 
                        a = get_activity((db_tt.getVal(val[2]),val[3])) #to find corresponding unit
                        exchanges[activity].add_exchange((db_tt.getVal(val[2]),val[3]),float(val[4]),a.as_dict()['unit'],'technosphere')                    
        
        #Linking activities with exchanges
        for val in activities:
            dbh.add_exchanges(val, exchanges[val])
        
        #Writing to DB
        dbh.write() 
        
        
    def run(self, technosphereTT, biosphereTT):
    
        self.technosphereTT=technosphereTT
        self.biosphereTT=biosphereTT
        
        #loading model file
        model = FileHandler()
        model.loadCSVList(self.system_CSV)
        
        #loading translatin tables
        ei = TranslationTable (self.technosphereTT)
        bios = TranslationTable (self.biosphereTT)
        db_tt = TranslationTable(self.databaseTT)
        
        #first DB in DB TT file should be the biosphere, next one should be technosphere DB
        db_map = dict()
        db_map['biosphere'] = list(db_tt.asDict().keys())[0]
        db_map['technosphere'] = list(db_tt.asDict().keys())[1]
        
        
        #determine which DB to create from user DB list
        bw2_databases = list()
        user_databases = list()
        
        for key, value in databases.items():
            bw2_databases.append(key)
        for key, value in db_tt.asDict().items():
            user_databases.append(value)
        
        create_db = set(user_databases) - set(bw2_databases) #only allows 1 user database creation
        
        #creating DB handler
        dbh = DatabaseHandler(create_db.pop())
        
        #concatenating material names to activities
        for val in model.data:
            if val[0] == 'Initial':
                val[3] = val[3] + '-' + val[1]
                
            elif val[2]!=dbh.get_db_name():
                val[0] = val[0] + '-' + val[1]
                
            else:
                val[0] = val[0] + '-' + val[1]
                val[3] = val[3] + '-' + val[1]
            
            
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
                        
                    elif val[2] == db_map['biosphere']: #biosphere flow. 
                    
                        a = get_activity((db_tt.getVal(val[2]),bios.getVal(val[3]))) #to find corresponding unit
                        exchanges[activity].add_exchange((db_tt.getVal(val[2]),bios.getVal(val[3])),float(val[4]),a.as_dict()['unit'],'biosphere')
                        
                        
                    elif val[2] == db_map['technosphere']: #technosphere flow. 
                    
                        a = get_activity((db_tt.getVal(val[2]),ei.getVal(val[3]))) #to find corresponding unit
                        exchanges[activity].add_exchange((db_tt.getVal(val[2]),ei.getVal(val[3])),float(val[4]),a.as_dict()['unit'],'technosphere')
                    
        
        #Linking activities with exchanges
        for val in activities:
            dbh.add_exchanges(val, exchanges[val])
        
        #Writing to DB
        dbh.write() 
                
    
