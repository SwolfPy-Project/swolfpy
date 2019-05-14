# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:03:36 2019

@author: msmsa
"""
from brightway2 import *

projects.set_current('BW2_S1')
db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()

from bw2analyzer import ContributionAnalysis
CA=ContributionAnalysis()
V=CA.annotated_top_emissions(lca)
"""
CA.annotated_top_emissions(lca,names = True)
Get list of most damaging processes in an LCA, sorted by ``abs(direct impact)``.
Returns a list of tuples: ``(lca score, supply, activity)``. If ``names`` is False, they returns the process key as the last element.
"""

cc=[]
for x in V:
    cc.append ([x[0],x[2]['name']])    
cc.sort()

CutOff= 0.05
maxcc =abs(max(cc)[0]) 
mincc= abs(min(cc)[0])
import copy
dd = list()
i=0
for x in cc:
    if abs(x[0])> CutOff * maxcc  or abs(x[0])> CutOff * mincc :
        dd.append(cc[i])
    i+=1
    
    
    
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,5)    
plt.rcParams.update({'font.size':16})
negative = []
positive=[]
dd.reverse()
for x in range(len(dd)):
    if dd[x][0]<0:
        negative.append(dd[x][0])
        if x ==0:
            plt.barh("Emissions",dd[x][0],height=0.1,left=0)
        else:
            plt.barh("Emissions",dd[x][0],height=0.1,left=sum(negative[:-1]))
    else:
        positive.append(dd[x][0])
        if x ==0:
            plt.barh("Emissions",dd[x][0],height=0.1,left=0)
        else:
            plt.barh("Emissions",dd[x][0],height=0.1,left=sum(positive[:-1]))
            
    

plt.legend([x[1] for x in dd],loc=3)
plt.title('Top Emisison Contribution, CutOff = 0.05, LF')

"""     #####################   Top acitivity  """

from bw2analyzer import ContributionAnalysis
CA=ContributionAnalysis()
V=CA.annotated_top_processes(lca)

"""
CA.annotated_top_emissions(lca,names = True)
Get list of most damaging processes in an LCA, sorted by ``abs(direct impact)``.
Returns a list of tuples: ``(lca score, supply, activity)``. If ``names`` is False, they returns the process key as the last element.
"""

cc=[]
for x in V:
    cc.append ([x[0],x[2]['name']])    
cc.sort()

CutOff= 0.05
maxcc =abs(max(cc)[0]) 
mincc= abs(min(cc)[0])
import copy
dd = list()
i=0
for x in cc:
    if abs(x[0])> CutOff * maxcc  or abs(x[0])> CutOff * mincc :
        dd.append(cc[i])
    i+=1
    
    
    
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,5)    
plt.rcParams.update({'font.size':16})
negative = []
positive=[]
dd.reverse()
for x in range(len(dd)):
    if dd[x][0]<0:
        negative.append(dd[x][0])
        if x ==0:
            plt.barh("Activity",dd[x][0],height=0.1,left=0)
        else:
            plt.barh("Activity",dd[x][0],height=0.1,left=sum(negative[:-1]))

dd.reverse()
for x in range(len(dd)):
    if dd[x][0]>0:
        positive.append(dd[x][0])
        if x ==0:
            plt.barh("Activity",dd[x][0],height=0.1,left=0)
        else:
            plt.barh("Activity",dd[x][0],height=0.1,left=sum(positive[:-1]))
            
    

plt.legend([x[1] for x in dd],loc=3)
plt.title('Top Activities Contribution, CutOff = 0.05,  0.5 WTE + LF')




lca.top_emissions()

lca.top_activities()


"""
from bw2calc import GraphTraversal
gt = GraphTraversal()
print(gt.calculate({db.get("Initial") : 1}, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')))

print (lca.activity_dict)



from bw2analyzer import SerializedLCAReport
functional_unit = {db.get("Initial") : 1}
slca = SerializedLCAReport(functional_unit, ('IPCC 2001', 'climate change', 'GWP 100a'),iterations = 10)
slca.calculate()
slca.write()

"""



