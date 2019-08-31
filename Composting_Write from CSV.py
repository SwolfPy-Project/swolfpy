from process_model import *
from full_system import *
from process_model_output import *
import material_properties

import time
import datetime


t3 = time.time()


if "Composting" in databases:
    del databases["Composting"]

a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')

SWOLF_data = a.read_output_from_SWOLF ("Composting", "Composting_BW2.csv")


tr = Treatment('Composting') 
tr.import_from_SWOLF(SWOLF_data)
tr.write_output('Composting_test.csv')

print('Importing Full System')
fs = FullSystem('Composting_test.csv','database_TT_Composting.csv')
print('Running Full System')
t1 = time.time()
fs.run_no_TT()
t2 = time.time()
print('Time to run full system: %0.1f secs' % (t2-t1))
print('Total time to run: %0.1f secs' % (t2-t3))