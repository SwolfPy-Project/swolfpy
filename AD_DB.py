from process_model import *
from full_system import *
from process_model_output import *
import material_properties

import time
import datetime


t3 = time.time()


if "AD" in databases:
    del databases["AD"]

a = ProcessModelOutput()
a.create_waste_technosphere()
print('Importing SWOLF data')

SWOLF_data = a.read_output_from_SWOLF ("AD", "AD_BW2.csv")


tr = Treatment('AD') 
tr.import_from_SWOLF(SWOLF_data)
tr.write_output('AD_test.csv')

print('Importing Full System')
fs = FullSystem('AD_test.csv','database_TT_AD.csv')
print('Running Full System')
t1 = time.time()
fs.run_no_TT()
t2 = time.time()
print('Time to run full system: %0.1f secs' % (t2-t1))
print('Total time to run: %0.1f secs' % (t2-t3))