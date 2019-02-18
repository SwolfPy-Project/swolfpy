from db_handler import *
## Example##		
#a = Exchange()
#a.add_exchange(('ecoinvent 3.4 cutoff', 'f64cdcbe8d33b115b227231335e47b63'),1.0,'tkm','technosphere')
#a.add_exchange(('ecoinvent 3.4 cutoff', '8a4d020ef16489760b886f3c95aeaed1'),2.0,'tkm','technosphere')
#b = DatabaseHandler ('auto_test')
#b.add_activity('1234','transport', a, 'kg')

food_mass = 0.4
food_ch4_yield_per_Mg = 12

# Creating DB
dbh = DatabaseHandler('auto_MSW')

#Creating activities
dbh.add_activity ('1','Initial','Mg')
dbh.add_activity ('2','Food Collection', 'Mg')
dbh.add_activity ('3','Food Landfill', 'Mg')

#Creating exchanges
ex = Exchange()
ex.add_exchange((dbh.get_db_name(), '2'), food_mass, 'Mg', 'technosphere')

ex2 = Exchange()
ex2.add_exchange((dbh.get_db_name(), '3'), food_mass, 'Mg', 'technosphere')
ex2.add_exchange(('ecoinvent 3.4 cutoff', 'bfcd07940a319765aec1555ad12643f8'), 4, 'kg', 'technosphere')
ex2.add_exchange(('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'), 5, 'kg', 'biosphere')

ex3 = Exchange()
ex3.add_exchange(('ecoinvent 3.4 cutoff', 'bfcd07940a319765aec1555ad12643f8'), 2, 'kg', 'technosphere')
ex3.add_exchange(('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'), 4, 'kg', 'biosphere')
ex3.add_exchange(('biosphere3', 'da1157e2-7593-4dfd-80dd-a3449b37a4d8'), food_mass*food_ch4_yield_per_Mg, 'kg', 'biosphere')

#Linking activities with exchanges
#Note: we can reuse the same exchange object for different activities if needed
dbh.add_exchanges('1', ex)
dbh.add_exchanges('2', ex2)
dbh.add_exchanges('3', ex3)

#Writing to DB
dbh.write() 


