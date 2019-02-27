from model2 import *
from usermodel import *
from file_handler import *


#this information will be read from file

types = ['SSMRF','WTE','Landfill','AD']
waste_in = [['aluminium','paper','glass'],['paper'],['*'],['yard waste']]
waste_out = [['alumium','glass'],[''],['aaa'],['bbb']]
model_file_type = ['Python', 'Excel']



model = Model2(types,waste_in,waste_out)

#allocates a list of user models. Each item on the list is an object. This information will be user input
user_inputs = []

model_file_path1 = 'AD3.gzip'
data_file_path1 = 'AD_input_data.csv'

outputs = ['elecProd','eq_life','elecCons']

csv_data = File_Handler()
csv_data.load_csv(data_file_path1)

a = UserModel('AD1','AD',model.get_waste_strm_in('AD'),model.get_waste_strm_out('AD'),model_file_type[1],model_file_path1,csv_data.data,outputs)
#b = UserModel('LF1','Landfill',model.get_waste_strm_in('Landfill'),model.get_waste_strm_out('Landfill').model_file_type[1])
#c = UserModel('WTE1','WTE',model.get_waste_strm_in('WTE'),model.get_waste_strm_out('WTE'),model_file_type[1])

#user_inputs.append(a)
#user_inputs.append(b)
#user_inputs.append(c)