# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:25:05 2019

@author: msardar2
"""
import pandas as pd
import numpy as np
from ..MC import *

class WTE_input(MC):
    def __init__(self):
        ### WTE Economic Input Parameters
        self.Economic_parameters = {
                "WTE_lifetime":{"Name":"WTE Lifetime","amount":20,"unit":"years","Reference":None},
                "WTE_capacity_factor":{"Name":"WTE Capacity Factor","amount":0.91,"unit":None,"Reference":None},
                "Unit_WTE_capital_cost":{"Name":"Unit WTE Capital Cost","amount":520,"unit":"$/design tons per year","Reference":None},
                "Unit_WTE_O_M_cost":{"Name":"Unit WTE O&M Cost","amount":40,"unit":"$/Mg processed","Reference":None},
                "CF_I":{"Name":"Combustor Interest Rate","amount":0.05,"unit":None,"Reference":None}
                }
        
        ### Electricity Production Efficiency
        self.Elec_Prod_Eff = {
                "Gross_Efficiency":{"Name":"Gross Efficiency","amount":0.27,"unit":None,"Reference":None},
                "Net_Efficiency":{"Name":"Net Efficiency","amount":0.24,"unit":None,"Reference":None},
                "Heat_prod_Eff":{"Name":"Heat Production Efficiency","amount":0,"unit":None,"Reference":None}
                }
        
        ### Non-Metal Emissions at WTE Facility (Stack_Gas_Concentration)
        self.Stack_Gas_Conc_Non_metal ={
                "Sulfur_dioxide":{"Name":"Sulfur dioxide","amount":2,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "HCl":{"Name":"HCl","amount":2,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "NOx":{"Name":"NOx","amount":35,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "CO":{"Name":"CO","amount":20,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "PM":{"Name":"PM","amount":1.5,"unit":"mg/dscm  @ 7% oxygen, dry","Reference":None},
                "Dioxins_Furans":{"Name":"Dioxins / Furans","amount":1.5,"unit":"ng/dscm  @ 7% oxygen, dry","Reference":None},
                "Methane":{"Name":"Methane","amount":1.1,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "Nitrous_Oxide":{"Name":"Nitrous Oxide","amount":1.3,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "Ammonia":{"Name":"Ammonia","amount":2,"unit":"ppmv @ 7% oxygen, dry","Reference":None},
                "Hydrocarbons":{"Name":"Hydrocarbons","amount":1,"unit":"ppmv @ 7% oxygen, dry","Reference":None}
                }
        
        ### Metal Emissions at WTE Facility (Fraction in stack)
        self.Stack_metal_emission = {
                "As":{"Name":"As","amount":0.00012,"unit":None,"Reference":None},
                "Ba":{"Name":"Ba","amount":0,"unit":None,"Reference":None},
                "Cd":{"Name":"Cd","amount":0.00006,"unit":None,"Reference":None},
                "Cr":{"Name":"Cr","amount":0.00039,"unit":None,"Reference":None},
                "Cu":{"Name":"Cu","amount":0.00003,"unit":None,"Reference":None},
                "Hg":{"Name":"Hg","amount":0.00748,"unit":None,"Reference":None},
                "Ni":{"Name":"Ni","amount":0.00033,"unit":None,"Reference":None},
                "Pb":{"Name":"Pb","amount":0.00001,"unit":None,"Reference":None},
                "Sb":{"Name":"Sb","amount":0.00119,"unit":None,"Reference":None},
                "Se":{"Name":"Se","amount":0,"unit":None,"Reference":None},
                "Zn":{"Name":"Zn","amount":0,"unit":None,"Reference":None}
                }
        
        ### Metal Emissions at WTE Facility (Fraction in fly ash)
        self.Fly_Ash_metal_emission = {
                "As":{"Name":"As","amount":0.5892,"unit":None,"Reference":None},
                "Ba":{"Name":"Ba","amount":0,"unit":None,"Reference":None},
                "Cd":{"Name":"Cd","amount":0.8813,"unit":None,"Reference":None},
                "Cr":{"Name":"Cr","amount":0.1677,"unit":None,"Reference":None},
                "Cu":{"Name":"Cu","amount":0.0753,"unit":None,"Reference":None},
                "Hg":{"Name":"Hg","amount":0.9625,"unit":None,"Reference":None},
                "Ni":{"Name":"Ni","amount":0.1256,"unit":None,"Reference":None},
                "Pb":{"Name":"Pb","amount":0.5129,"unit":None,"Reference":None},
                "Sb":{"Name":"Sb","amount":0.5984,"unit":None,"Reference":None},
                "Se":{"Name":"Se","amount":0,"unit":None,"Reference":None},
                "Zn":{"Name":"Zn","amount":0.4818,"unit":None,"Reference":None}
                }
        
        ### Metal Emissions at WTE Facility (Fraction in bottom ash)
        self.Bottom_Ash_metal_emission = {
                "As":{"Name":"As","amount":0.41068,"unit":None,"Reference":None},
                "Ba":{"Name":"Ba","amount":1,"unit":None,"Reference":None},
                "Cd":{"Name":"Cd","amount":0.11864,"unit":None,"Reference":None},
                "Cr":{"Name":"Cr","amount":0.83191,"unit":None,"Reference":None},
                "Cu":{"Name":"Cu","amount":0.92647,"unit":None,"Reference":None},
                "Hg":{"Name":"Hg","amount":0.03002,"unit":None,"Reference":None},
                "Ni":{"Name":"Ni","amount":0.87407,"unit":None,"Reference":None},
                "Pb":{"Name":"Pb","amount":0.48709,"unit":None,"Reference":None},
                "Sb":{"Name":"Sb","amount":0.40041,"unit":None,"Reference":None},
                "Se":{"Name":"Se","amount":1,"unit":None,"Reference":None},
                "Zn":{"Name":"Zn","amount":0.5182,"unit":None,"Reference":None}
                }
        
        
        ### Metals Recovery
        self.Metals_Recovery={
        "Fe_Rec_Rate":{'Name':'Ferrous Recovery Rate from Bottom Ash','amount':0.9,"unit":None,"Reference":None}, 
        "Al_Rec_Rate":{'Name':'Aluminum Recovery Rate from Bottom Ash','amount':0.65,"unit":None,"Reference":None}, 
        "Cu_Rec_Rate":{'Name':'Copper Recovery Rate from Bottom Ash','amount':0.65,"unit":None,"Reference":None}, 
        "Fly_ash_frac":{'Name':'Fraction of Ash that Becomes Fly Ash','amount':0.05,"unit":None,"Reference":None}
                }
        
        ### Material Consumption
        self.Material_Consumption ={
        "lime":{'Name':'Mg lime/Mg MSW','amount':0.012,"unit":'Mg/Mgww',"Reference":None}, 
        "ammonia":{'Name':'Mg ammonia/Mg MSW','amount':0.0004,"unit":'Mg/Mgww',"Reference":None},
        "carbon":{'Name':'Mg carbon/Mg MSW','amount':0.0006,"unit":'Mg/Mgww',"Reference":None},
        "Distance_from_prod_fac":{'Name':'Distance_from_prod_fac','amount':100,"unit":'km',"Reference":None},
        "Empty_Return_Truck":{'Name':"Empty_Return_Truck",'amount':1,"unit":None,"Reference":None}
                }
        
### Monte_carlo          
    def setup_MC(self,seed=None):
        self.Input_list = {'Economic_parameters':self.Economic_parameters, 'Elec_Prod_Eff':self.Elec_Prod_Eff,'Stack_Gas_Conc_Non_metal':self.Stack_Gas_Conc_Non_metal,
                           'Stack_metal_emission':self.Stack_metal_emission, 'Fly_Ash_metal_emission':self.Fly_Ash_metal_emission,
                           'Bottom_Ash_metal_emission':self.Bottom_Ash_metal_emission,'Metals_Recovery':self.Metals_Recovery,
                           'Material_Consumption':self.Material_Consumption}
        super(WTE_input,self).__init__(self.Input_list )
        super().setup_MC(seed)    



#################################################################
#### Convering the input dictionaries to csv file
#################
A= WTE_input()
A.setup_MC()
category=[]
Parameter=[]
Name=[]
amount=[]
unit=[]

for x in A.Input_list.keys():
    for y in  A.Input_list[x].keys():
        category.append(x)
        Parameter.append(y)
        Name.append(A.Input_list[x][y]['Name'])
        amount.append(A.Input_list[x][y]['amount'])
        unit.append(A.Input_list[x][y]['unit'])
AAA={'category':category,'Parameter':Parameter,'Name':Name,'amount':amount,'unit':unit}
