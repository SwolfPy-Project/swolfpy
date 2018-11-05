from model2 import *
from usermodel import *

types = ['SSMRF','WTE','Landfill']
waste_in = [['aluminium','paper','glass'],['paper'],['*']]
waste_out = [['alumium','glass'],[''],['poop']]
model = Model2(types,waste_in,waste_out)

user_inputs = []
a = UserModel('MRF1','SSMRF',model.get_waste_strm_in('SSMRF'),model.get_waste_strm_out('SSMRF'))
b = UserModel('LF1','Landfill',model.get_waste_strm_in('Landfill'),model.get_waste_strm_out('Landfill'))
c = UserModel('WTE1','WTE',model.get_waste_strm_in('WTE'),model.get_waste_strm_out('WTE'))

user_inputs.append(a)
user_inputs.append(b)
user_inputs.append(c)