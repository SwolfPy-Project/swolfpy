######Using Database Handler and Translation Tables#####

from translation_table import *
from db_handler import *

ei = TranslationTable ('eco_invent_TT.csv')
bios = TranslationTable ('biosphere_TT.csv')
db_tt = TranslationTable('database_TT.csv')


food_mass = 0.4
food_ch4_yield_per_Mg = 12

# Creating DB
dbh = DatabaseHandler('auto_MSW2')

#Creating activities
dbh.add_activity ('1','Initial','Mg')
dbh.add_activity ('2','Food Collection', 'Mg')
dbh.add_activity ('3','Food Landfill', 'Mg')

#Creating exchanges
ex = Exchange()
ex.add_exchange((dbh.get_db_name(), '2'), food_mass, 'Mg', 'technosphere')

ex2 = Exchange()
ex2.add_exchange((dbh.get_db_name(), '3'), food_mass, 'Mg', 'technosphere')
ex2.add_exchange((db_tt.getVal('eco'), ei.getVal('market for diesel')), 4, 'kg', 'technosphere')
ex2.add_exchange((db_tt.getVal('biosp'), bios.getVal('C02')), 5, 'kg', 'biosphere')

ex3 = Exchange()
ex3.add_exchange((db_tt.getVal('eco'), ei.getVal('market for diesel')), 2, 'kg', 'technosphere')
ex3.add_exchange((db_tt.getVal('biosp'), bios.getVal('C02')), 4, 'kg', 'biosphere')
ex3.add_exchange((db_tt.getVal('biosp'), bios.getVal('CH4')), food_mass*food_ch4_yield_per_Mg, 'kg', 'biosphere')

#Linking activities with exchanges
#Note: we can reuse the same exchange object for different activities if needed
dbh.add_exchanges('1', ex)
dbh.add_exchanges('2', ex2)
dbh.add_exchanges('3', ex3)

#Writing to DB
dbh.write() 


