# -*- coding: utf-8 -*-
"""
Created on Wed May  8 20:35:43 2019

@author: msmsa
"""

from brightway2 import *
projects.set_current("MonteCarlo")
#bw2setup()


### Importing the data basse  
# Small version of ecoinvent is in our folder
Directory = "C:\\Users\\msmsa\\Google Drive\\Brightway2\\Laptop_BitBucket\\Small_Version_of_Ecoinvnet"
ecoinvent_test = SingleOutputEcospold2Importer(Directory,'ecoinvent_test')
ecoinvent_test.apply_strategies()
ecoinvent_test.statistics()
ecoinvent_test.write_database()

DB
Activity=DB.random()

IF = ('IPCC 2007', 'climate change', 'GWP 100a')

lca = LCA(demand={Activity: 1}, method=IF)
# Life cycle inventory
lca.lci()
# Life cycle impact assessment
lca.lcia()

print (lca.score)

mc = MonteCarloLCA({Activity: 1},('IPCC 2007', 'climate change', 'GWP 100a') )
mc_results = [mc() for x in range(500)]

from matplotlib.pylab import *
hist(mc_results, normed=True, histtype="step")
xlabel(methods[IF]["unit"])
ylabel("Probability")

##################
### check the montecarlo simulation in LF yard trimming branches
projects.set_current("BW2_S1")
db = Database('LF')
act=db.get("Landfill-Yard_Trimmings_Branches")

IF = ('IPCC 2007', 'climate change', 'GWP 100a')
lca = LCA(demand={act: 1}, method=IF)
# Life cycle inventory
lca.lci()
# Life cycle impact assessment
lca.lcia()

print("GWP of Landfill-Yard_Trimmings_Branches: " , lca.score)


for x in act.technosphere():
    x['uncertainty type'],x['loc'], x['scale'] = 3, x.amount, x.amount * 0.1
    x.save()
    
for x in act.biosphere():
    x['uncertainty type'],x['loc'], x['scale'] = 3, x.amount, abs(x.amount) * 0.1
    x.save()    

mc = MonteCarloLCA({act: 1},IF )
mc_results = [mc() for x in range(1000)]

print ("\n results from the Monte Carlo simulation \n")
from matplotlib.pylab import *
hist(mc_results, normed=True, histtype="step")
xlabel(methods[IF]["unit"])
ylabel("Probability")



################


    
    

