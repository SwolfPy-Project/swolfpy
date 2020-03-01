# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:51:44 2019

@author: msmsa
"""
import pandas as pd
import numpy as np
import brightway2 as bw2
database_biosphere = bw2.Database("biosphere3")


def load_Elementary_flows (file_path):  # read the xlsx file of process data
    elementary_flows = pd.read_csv(file_path)
    output={}
    for i in elementary_flows.index:
        output[i]={}
        for j in elementary_flows.columns:
            output[i][j] = elementary_flows.at[i,j]
    return output 

# new verison of ecoinvent use the 'natural resource' compartment instead of "Raw"
def category(x,y): # returns the category of each flow as tuple (Compartment,Subcompartment)
    if x == "Raw":
        x = 'natural resource'
    if y !='unspecified':
        return ((x.lower(),y))
    else:
        return ((x.lower(),))


def create_biosphere_key (elementary_flows):
    for x in elementary_flows:
        elementary_flows[x] = [elementary_flows[x]['Compartment'],elementary_flows[x]['Name'],elementary_flows[x]['Subcompartment']]
    # revising the biosphere flows' name that has change 
    for x in elementary_flows.values():
        if x[1] == 'Sulphur trioxide':
            x[1]= 'Sulfur trioxide'
        elif x[1] == 'Sulphur dioxide':
            x[1]= 'Sulfur dioxide'
        elif x[1] == 'Sulphur':
            x[1]= 'Sulfur'
        elif x[1] == 'Copper, Cu 0.38%, Au 9.7E-4%, Ag 9.7E-4%, Zn 0.63%, Pb 0.014%, in ore, in ground':
            x[1]= 'Copper, Cu 0.38%, in mixed ore, in ground'
        elif x[1] == 'Gold, Au 9.7E-4%, Ag 9.7E-4%, Zn 0.63%, Cu 0.38%, Pb 0.014%, in ore, in ground':
            x[1]= 'Gold, Au 9.7E-4%, in mixed ore, in ground'
        elif x[1] == 'Lead, Pb 0.014%, Au 9.7E-4%, Ag 9.7E-4%, Zn 0.63%, Cu 0.38%, in ore, in ground':
            x[1]= 'Lead, Pb 0.014%, in mixed ore, in ground' 
        elif x[1] == 'Silver, Ag 9.7E-4%, Au 9.7E-4%, Zn 0.63%, Cu 0.38%, Pb 0.014%, in ore, in ground':
            x[1]= 'Silver, Ag 9.7E-4%, in mixed ore, in ground'
        elif x[1] == 'Zinc, Zn 0.63%, Au 9.7E-4%, Ag 9.7E-4%, Cu 0.38%, Pb 0.014%, in ore, in ground':
            x[1]= 'Zinc, Zn 0.63%, in mixed ore, in ground' 

    #Database in the brightway2 has the search method, but it cannot find all the flows! 
    #So search is done with for loop which takes more time!
    biosphere_key = {}
    rr=0
    for ss in elementary_flows:
        biosphere_key[rr] = [x.key for x in database_biosphere if x["name"]==elementary_flows[rr][1] and category(elementary_flows[rr][0],\
                     elementary_flows[rr][2]) == x["categories"] and elementary_flows[rr][1] == x["name"]]
        rr+=1
    n=0    # number of elemantary flows without key in biosphere3 database 
    for cc in biosphere_key:
        if biosphere_key[cc] == []:
            n+=1
    print("number of elemantry flow without key: " , n)
    return biosphere_key

#test
#elementary_flows =load_Elementary_flows("Elementary flows_EcoinventV3.csv")
#biosphere_keys = create_biosphere_key(elementary_flows)


