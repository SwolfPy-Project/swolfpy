# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:36:54 2019

@author: msmsa
"""
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group


# =============================================================================
# from Waste_DB import *
# Waste_DB = WasteDB()
# Initial = Exchange()
# Initial.add_exchange(("Collection_SF", 'SF_Collection'), 1, 'Mg', 'technosphere')
# Waste_DB.dbh.add_activity("Initial","Initial","Mg",Initial)
# Waste_DB.write() 
# 
# get_activity(("Waste",'25 : Fe')).new_exchange(input=('Material_Reprocessing', 'Material_Reprocessing-Ferrous_Cans'),\
#              amount=1,type="biosphere").save()
# 
# get_activity(("Waste",'24 : Al')).new_exchange(input=('Material_Reprocessing', 'Material_Reprocessing-Aluminum_Cans'),\
#              amount=1,type="biosphere").save()
# get_activity(("Waste",'30 : Mixed Glass')).new_exchange(input=('Material_Reprocessing', 'Material_Reprocessing-Mixed_Glass'),\
#              amount=1,type="biosphere").save()
# get_activity(("Waste",'10 : Mixed Paper')).new_exchange(input=('Material_Reprocessing', 'Material_Reprocessing-Mixed_Paper'),\
#              amount=1,type="biosphere").save()
# get_activity(("Waste",'3 : Bottom Ash')).new_exchange(input=('LF', 'Landfill-Bottom_Ash'),\
#              amount=1,type="biosphere").save()
# get_activity(("Waste",'4 : Fly Ash')).new_exchange(input=('LF', 'Landfill-Fly_Ash'),\
#              amount=1,type="biosphere").save()
# =============================================================================


projects.set_current('Base')

db = Database('Collection_SF')

project_data = [
        {'name': 'res_to_LF', 'amount': 0.5},
        {'name': 'percent_to_WTE','formula': '1 - res_to_LF'},
        {'name': 'rec_to_SS_MRF','amount': 1},
        {'name': 'moc_to_AD','amount': 0.5},
        {'name': 'moc_to_AC','formula': '1 - moc_to_AD'}
        ]
parameters.new_project_parameters(project_data)
for x in Database('Collection_SF'):
    parameters.add_exchanges_to_group("my group", x)
    
ActivityParameter.recalculate_exchanges("my group")

db = Database("Waste")
functional_unit = {db.get("Initial") : 1}
lca = LCA(functional_unit, ('IPCC_2007_SWOLF', 'climate change', 'GWP100yr')) 
lca.lci()
lca.lcia()
print ("Collection SF :", lca.score)

import matplotlib.pyplot as plt
fig, ((ax1),(ax2)) = plt.subplots(nrows=2, ncols=1,figsize=(20, 25))
# ===============================================================================================
from bw2analyzer import ContributionAnalysis
CA=ContributionAnalysis()
V=CA.annotated_top_processes(lca)

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
    
plt.rcParams["figure.figsize"] = (20,5)    
plt.rcParams.update({'font.size':16})
negative = []
positive=[]
dd.reverse()
for x in range(len(dd)):
    if dd[x][0]<0:
        negative.append(dd[x][0])
        if x ==0:
            ax1.barh("Activity",dd[x][0],height=0.1,left=0)
        else:
            ax1.barh("Activity",dd[x][0],height=0.1,left=sum(negative[:-1]))

dd.reverse()
for x in range(len(dd)):
    if dd[x][0]>0:
        positive.append(dd[x][0])
        if x ==0:
            ax1.barh("Activity",dd[x][0],height=0.1,left=0)
        else:
            ax1.barh("Activity",dd[x][0],height=0.1,left=sum(positive[:-1]))
            
    

ax1.legend([x[1] for x in dd],loc=3)
#ax1.title('Top Activities Contribution, CutOff = 0.05, Collection')

# ===============================================================================================
V=CA.annotated_top_emissions(lca)
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
        
negative = []
positive=[]
dd.reverse()
for x in range(len(dd)):
    if dd[x][0]<0:
        negative.append(dd[x][0])
        if x ==0:
            ax2.barh("Emissions",dd[x][0],height=0.1,left=0)
        else:
            ax2.barh("Emissions",dd[x][0],height=0.1,left=sum(negative[:-1]))
    else:
        positive.append(dd[x][0])
        if x ==0:
            ax2.barh("Emissions",dd[x][0],height=0.1,left=0)
        else:
            ax2.barh("Emissions",dd[x][0],height=0.1,left=sum(positive[:-1]))
            
    

ax2.legend([x[1] for x in dd],loc=3)
#ax2.title('Top Emisison Contribution, CutOff = 0.05, Collection')
