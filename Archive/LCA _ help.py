# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 21:58:52 2020

@author: msmsa
"""

from brightway2 import *
projects.set_current('PySWOLF')
db = Database('P1_LF')
db2 = Database('P2_WTE')
db3 = Database('Technosphere')
db4 = Database('biosphere3')


act1 = ('P1_LF','Yard_Trimmings_Grass')
act2= ('P2_WTE','Yard_Trimmings_Grass')


m1 = ('IPCC 2013', 'climate change', 'GTP 100a')
m2 = ('IPCC 2013', 'climate change', 'GTP 20a')
m3 = ('IPCC 2013', 'climate change', 'GWP 100a')


import numpy as np
import pandas as pd

dbnp = np.load(db.filepath_processed())
dbpd=pd.DataFrame(dbnp)

dbnp = np.load(db3.filepath_processed())
dbpd=pd.DataFrame(dbnp)

dbnp = np.load(db4.filepath_processed())
dbpd=pd.DataFrame(dbnp)


keysss=pd.Series(mapping)
AAA=pd.DataFrame(mapping)


myLCA = LCA({('P1_LF','Yard_Trimmings_Grass'):2},m1)
myLCA.lci()
myLCA.lcia()
print(myLCA.score)

myLCA_rev_act_dict, myLCA_rev_product_dict, myLCA_rev_bio_dict = myLCA.reverse_dict()



myLCA.technosphere_matrix
type(myLCA.technosphere_matrix)
print(myLCA.technosphere_matrix)
AAA=myLCA.technosphere_matrix.toarray()
myLCA_COO=myLCA.technosphere_matrix.tocoo()
names_of_my_inputs=[myLCA_rev_product_dict[i] for i in myLCA_COO.row]
myColumnAsDict = dict(zip(names_of_my_inputs,myLCA_COO.data))

myLCA.supply_array
myLCA.demand
myLCA.demand_array


import matplotlib.pyplot as plt
plt.spy(myLCA.technosphere_matrix)
plt.spy(myLCA.biosphere_matrix)


AAA=pd.DataFrame(myLCA.bio_params)


act_list=[{('P1_LF','Yard_Trimmings_Grass'):1},{('P2_WTE','Yard_Trimmings_Grass'):1}]


calculation_setups['msm'] = {'inv':act_list, 'ia':[m1,m2,m3]}
MyMultiLca=MultiLCA('msm')
MyMultiLca.results
MyMultiLca.results.shape










# =============================================================================
# =============================================================================
# =============================================================================
# # # scipy
# =============================================================================
# =============================================================================
# =============================================================================

# Constructing an empty matrix
from scipy.sparse import coo_matrix
AA = coo_matrix((3, 4), dtype=np.int8)
AA.toarray()



# Constructing a matrix using ijv format
row  = np.array([0, 3, 1, 0])
col  = np.array([0, 3, 1, 2])
data = np.array([4, 5, 7, 9])
coo_matrix((data, (row, col)), shape=(4, 4)).toarray()


# Constructing a matrix with duplicate indices
row  = np.array([0, 0, 1, 3, 1, 0, 0])
col  = np.array([0, 2, 1, 3, 1, 0, 0])
data = np.array([1, 1, 1, 1, 1, 1, 1])
coo = coo_matrix((data, (row, col)), shape=(4, 4))
coo.toarray()
AA=coo.tocsc()
print(AA)
AA.data


