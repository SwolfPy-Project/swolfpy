# -*- coding: utf-8 -*-
"""
Created on Wed May  8 21:44:02 2019

@author: msmsa
"""
from brightway2 import *
projects.set_current("MonteCarlo")
Database("example").delete()

db = Database("example")

example_data = {
    ("example", "A"): {
        "code": "A",
        "name": "A",
        "categories": ["a category"],
        "type": "process",
        "unit": "kg",
        "exchanges": [{
            "amount": 1.0,
            "input": ("example", "B"),
            "uncertainty type": 3,
            "loc":1,
            "scale":.2,
            "type": "technosphere"
            }]
        },
    ("example", "B"): {
        "code": "B",
        "name": "B",
        "categories": ["another category"],
        "type": "process",
        "unit": "kg",
        "exchanges": [{
            "amount": 1.0,
            'input': ('biosphere3', 'f9749677-9c9f-4678-ab55-c607dfdc2cb9'),
            "uncertainty type": 0,
            "type": "biosphere"
            }]
        }
    }


       

db.write(example_data)
db.load()



IF = ('IPCC 2007', 'climate change', 'GWP 100a')

lca = LCA(demand={("example", "A"): 1}, method=IF)
# Life cycle inventory
lca.lci()
# Life cycle impact assessment
lca.lcia()

print (lca.score)

mc = MonteCarloLCA({("example", "A"): 1},('IPCC 2007', 'climate change', 'GWP 100a') )
mc_results = [mc() for x in range(10000)]

from matplotlib.pylab import *
hist(mc_results, normed=True, histtype="step")
xlabel(methods[IF]["unit"])
ylabel("Probability")




#db.get("AAA").delete()

### How to update a database
new_act=db.new_activity(code = "AAAA" , name = "BBB",location = "GLO", comment = " msm test",type = "process", unit = "kg" )
new_act.save()

new_ex = new_act.new_exchange(input=('biosphere3', 'f9749677-9c9f-4678-ab55-c607dfdc2cb9'), amount=1, type='biosphere', uncertainty_type = 3)
new_ex['uncertainty type'],new_ex['loc'], new_ex['scale'] = 3, 1, 0.25
new_ex.save()

#print([x for x in new_act.exchanges()])
#print([x for x in new_act.exchanges()][0].as_dict())



Activity = db.get("AAA")
mc = MonteCarloLCA({Activity: 1},('IPCC 2007', 'climate change', 'GWP 100a') )
mc_results = [mc() for x in range(1000)]

from matplotlib.pylab import *
hist(mc_results, normed=True, histtype="step")
xlabel(methods[IF]["unit"])
ylabel("Probability")



CC=[x for x in Activity.exchanges()][0]
CC.update(amount=6, loc = 6)
CC.save()

Activity = db.get("AAA")
mc = MonteCarloLCA({Activity: 1},('IPCC 2007', 'climate change', 'GWP 100a') )
mc_results = [mc() for x in range(1000)]

from matplotlib.pylab import *
hist(mc_results, normed=True, histtype="step")
xlabel(methods[IF]["unit"])
ylabel("Probability")


# ###########################
### uodate the LF database
projects.set_current("BW2_S1")
projects.copy_project('BW2_S2')


act=db.get("Landfill-Yard_Trimmings_Branches")
IF = ('IPCC 2007', 'climate change', 'GWP 100a')
lca = LCA(demand={act: 1}, method=IF)
# Life cycle inventory
lca.lci()
# Life cycle impact assessment
lca.lcia()

print("GWP of Landfill-Yard_Trimmings_Branches: " , lca.score)

import time
A=time.time()

db = Database("LF")
for x in db:
    for y in x.exchanges():
        y['amount'] = 1.01 * y.amount
        y.save()

B=time.time()
print("\n  time for updating the the Database: ", B-A)


IF = ('IPCC 2007', 'climate change', 'GWP 100a')
lca = LCA(demand={act: 1}, method=IF)
# Life cycle inventory
lca.lci()
# Life cycle impact assessment
lca.lcia()

print("GWP of Landfill-Yard_Trimmings_Branches: " , lca.score)

act=db.get("Landfill-Yard_Trimmings_Branches")
A=[x for x in act.exchanges()][0]['amount']


import time
A=time.time()

db = Database("LF")
for x in db:
    for y in x.exchanges():
        if random(1)[0] > 0.5:
            y['amount'] = 1.01 * y.amount
            y.save()

B=time.time()
print("\n  time for updating the the Database: ", B-A)




n=0
for x in db:
    for y in x.exchanges():
        n+=1
print(n)






