# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:10:31 2019

@author: msmsa
"""
import numpy as np
import pandas as pd
from WTE_Input import *
from stats_arrays import *

class WTE:
    def __init__(self):
        self.WTE_input= WTE_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'WTE', index_col = 'Parameter')
        
        self.Index = ['Unit','Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
         'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines_', 'third_Class_Mail',
         'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers',
         'PET_Containers', 'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable',
         'Ferrous_Cans', 'Ferrous_Metal_Other', 'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable',
         'Glass_Brown', 'Glass_Green', 'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste',
         'Aerobic_Residual', 'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
         'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54', 'Waste_Fraction_55',
         'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        
        
    def calc(self):
        ### Energy Calculations
        self.Energy_Calculations=pd.DataFrame(index = self.Index)
        
        self.Energy_Calculations['Energy_Loss_Due_to_Water'] = (-1) * self.Material_Properties['Moisture Content'][4:] / 100 * self.WTE_input.Imported_data['Water_Evap_Heat']['amount']
        self.Energy_Calculations['Energy_Loss_Due_to_Water']['Unit'] = 'MJ/kgww'
        
        self.Energy_Calculations['Energy_Loss_Due_to_Ashes'] = (-1) *  self.process_data['Heat Lost via Ashes - Cp (J/g K)'][3:] * \
                                                        self.process_data['Temperature Difference (K)'][3:] /1000 * (self.Material_Properties['Ash Content'][4:]/100 + \
                                                        self.Material_Properties['Volatile Solids'][4:]/100*(1-self.process_data['Combustion Efficiency (% of VS)'][3:]))\
                                                        * (100-self.Material_Properties['Moisture Content'][4:]) /100
        self.Energy_Calculations['Energy_Loss_Due_to_Ashes']['Unit'] = 'MJ/kgww'
        
        self.Energy_Calculations['Energy_Produced'] = self.Material_Properties['Lower Heating Value'][4:] * self.process_data['Combustion Efficiency (% of VS)'][3:] * \
                                                (100-self.Material_Properties['Moisture Content'][4:])/100
        self.Energy_Calculations['Energy_Produced']['Unit'] = 'MJ/kgww'
        
        self.Energy_Calculations['Total_Energy_Produced'] = self.Energy_Calculations['Energy_Produced'][1:] + self.Energy_Calculations['Energy_Loss_Due_to_Ashes'][1:] + \
                                                       self.Energy_Calculations['Energy_Loss_Due_to_Water'][1:] 
        self.Energy_Calculations['Total_Energy_Produced']['Unit'] = 'MJ/kgww'
        
        self.Energy_Calculations['Energy_Recovered_as_Electricity'] = self.Energy_Calculations['Total_Energy_Produced'][1:] * self.WTE_input.Elec_Prod_Eff['Net_Efficiency']['amount'] / 3.6
        self.Energy_Calculations['Energy_Recovered_as_Electricity']['Unit'] = 'kWh/kgww'
        
        self.Energy_Calculations['Net_Electricity_Use'] = self.Energy_Calculations['Energy_Recovered_as_Electricity'][1:] * (-1000)
        self.Energy_Calculations['Net_Electricity_Use']['Unit'] = 'kWh/Mgww'
        
        self.Energy_Calculations['Heat_Recovered'] = self.Energy_Calculations['Total_Energy_Produced'][1:] * 1000 * self.WTE_input.Elec_Prod_Eff['Heat_prod_Eff']['amount']
        self.Energy_Calculations['Heat_Recovered']['Unit'] = 'MJ/Mgww'
            
          
        ### Combustion Emission
        self.Combustion_Emission = pd.DataFrame(index = self.Index)
        
        self.Combustion_Emission['CO2_fossil'] = self.Material_Properties['Fossil Carbon Content'][4:] / 100 * self.process_data['Combustion Efficiency (% of VS)']\
                                            * (1-self.Material_Properties['Moisture Content'][4:]/100) * (self.WTE_input.Imported_data['mw_C']['amount'] + 2*self.WTE_input.Imported_data['mw_O']['amount'])/self.WTE_input.Imported_data['mw_C']['amount']
        self.Combustion_Emission['CO2_fossil']['Unit'] = 'kg/kgww'
        
        self.Combustion_Emission['CO2_biogenic'] = self.Material_Properties['Biogenic Carbon Content'][4:] / 100 * self.process_data['Combustion Efficiency (% of VS)']\
                                            * (1-self.Material_Properties['Moisture Content'][4:]/100) * (self.WTE_input.Imported_data['mw_C']['amount'] + 2*self.WTE_input.Imported_data['mw_O']['amount'])/self.WTE_input.Imported_data['mw_C']['amount']
        self.Combustion_Emission['CO2_biogenic']['Unit'] = 'kg/kgww'
        
        ### Stack metal emissions
        key1={'As':'Arsenic','Ba':'Barium','Cd':'Cadmium','Cr':'Chromium','Cu':'Copper','Hg':'Mercury','Ni':'Nickel','Pb':'Lead','Sb':'Antimony','Se':'Selenium','Zn':'Zinc'}
        for m in key1.keys():
            self.Combustion_Emission[m] = self.Material_Properties[key1[m]][4:] / 100 * self.WTE_input.Stack_metal_emission[m]['amount'] * (1-self.Material_Properties['Moisture Content'][4:]/100)
            self.Combustion_Emission[m]['Unit'] = 'kg/kgww'
            
        ### mole content of input waste
        self.Combustion_Emission['C_mole'] = (self.Material_Properties['Biogenic Carbon Content'][4:]+self.Material_Properties['Fossil Carbon Content'][4:]) / 100 \
                                        /self.WTE_input.Imported_data['mw_C']['amount'] * 1000
        self.Combustion_Emission['C_mole']['Unit'] = 'Moles per dry kg'
        
        key2={'Hydrogen Content':('mw_H','H_mole'),'Oxygen Content':('mw_O','O_mole'),'Nitrogen Content':('mw_N','N_mole'),'Chlorine':('mw_Cl','Cl_mole'),\
              'Sulphur':('mw_S','S_mole')}
        for m in key2.keys():
            self.Combustion_Emission[key2[m][1]] = self.Material_Properties[m][4:] / 100 /self.WTE_input.Imported_data[key2[m][0]]['amount'] * 1000
            self.Combustion_Emission[key2[m][1]]['Unit'] = 'Moles per dry kg'
        
        self.Combustion_Emission['alpha'] = -0.699*self.Combustion_Emission['O_mole'][1:]+1.5*self.Combustion_Emission['C_mole'][1:]+0.35*self.Combustion_Emission['H_mole'][1:]-0.244* \
                                        self.Combustion_Emission['Cl_mole'][1:]+1.5*self.Combustion_Emission['S_mole'][1:]+0.53*self.Combustion_Emission['N_mole'][1:]
        self.Combustion_Emission['alpha']['unit'] = '_'
        
        self.Combustion_Emission['Moles_per_dry_flue_gas'] = self.Combustion_Emission['O_mole'][1:]/2 + self.Combustion_Emission['alpha'][1:]*4.78-self.Combustion_Emission['H_mole'][1:]\
                                                        /4+5*self.Combustion_Emission['Cl_mole'][1:]/4+self.Combustion_Emission['N_mole'][1:]/2
        self.Combustion_Emission['Moles_per_dry_flue_gas']['unit'] = 'mole/kgDryFlueGas'
        
        self.Combustion_Emission['Flue_gas'] = self.Combustion_Emission['Moles_per_dry_flue_gas'][1:] * self.WTE_input.Imported_data['Density_Air']['amount']/ 1000 * (1-self.Material_Properties['Moisture Content'][4:]/100)
        self.Combustion_Emission['Flue_gas']['unit'] = 'dscm FlueGas/kgww'   #Dry Standard Cubic meter
            
        key3={'Stack_SO2':('Sulfur_dioxide',self.WTE_input.Imported_data['mw_S']['amount']+2*self.WTE_input.Imported_data['mw_O']['amount']),'Stack_HCl':('HCl',self.WTE_input.Imported_data['mw_H']['amount']+self.WTE_input.Imported_data['mw_C']['amount']),\
              'Stack_NOx':('NOx',self.WTE_input.Imported_data['mw_N']['amount']+2*self.WTE_input.Imported_data['mw_O']['amount']),'Stack_CO':('CO',self.WTE_input.Imported_data['mw_C']['amount']+self.WTE_input.Imported_data['mw_O']['amount']),\
              'Stack_Methane':('Methane',self.WTE_input.Imported_data['mw_C']['amount']+4*self.WTE_input.Imported_data['mw_H']['amount']),'Stack_Nitrous_Oxide':('Nitrous_Oxide',2*self.WTE_input.Imported_data['mw_N']['amount']+self.WTE_input.Imported_data['mw_O']['amount']),\
              'Stack_Ammonia':('Ammonia',self.WTE_input.Imported_data['mw_N']['amount']+3*self.WTE_input.Imported_data['mw_H']['amount']),'Stack_Hydrocarbons':('Hydrocarbons',self.WTE_input.Imported_data['Hydrocarbons']['amount'])}
        for m in key3.keys():
            self.Combustion_Emission[m] = self.WTE_input.Stack_Gas_Conc_Non_metal[key3[m][0]]['amount']/10**6*key3[m][1]/1000 / (self.WTE_input.Imported_data['Density_Air']['amount'] / 1000) * self.Combustion_Emission['Flue_gas']
            self.Combustion_Emission[m]['Unit'] = 'kg/kg ww'
        
        self.Combustion_Emission['Stack_PM'] = self.WTE_input.Stack_Gas_Conc_Non_metal['PM']['amount']/10**6 * self.Combustion_Emission['Flue_gas']
        self.Combustion_Emission['Stack_PM']['Unit'] = 'kg/kg ww'
        
        self.Combustion_Emission['Stack_Dioxins_Furans'] = self.WTE_input.Stack_Gas_Conc_Non_metal['Dioxins_Furans']['amount']/10**12 * self.Combustion_Emission['Flue_gas']
        self.Combustion_Emission['Stack_Dioxins_Furans']['Unit'] = 'kg/kg ww'
        
        ### Post-Combustion Solids
        
        self.Post_Combustion_Solids = pd.DataFrame(index = self.Index)
        
        self.Post_Combustion_Solids['Total_Post_Combustion_Solids']= self.Material_Properties['Ash Content'][4:]/100 + (1-self.Material_Properties['Moisture Content'][4:]/100)* \
                                                                self.Material_Properties['Volatile Solids'][4:]*(1-self.process_data['Combustion Efficiency (% of VS)'][3:])
        self.Post_Combustion_Solids['Total_Post_Combustion_Solids']['Unit']= 'kg/kg ww'
        
        self.Post_Combustion_Solids['Bottom_Ash_with_Metals']= (1-self.WTE_input.Metals_Recovery['Fly_ash_frac']['amount'])* self.Post_Combustion_Solids['Total_Post_Combustion_Solids'][1:]
        self.Post_Combustion_Solids['Bottom_Ash_with_Metals']['Unit']= 'kg/kg ww'
        
        self.Post_Combustion_Solids['Fly_Ash']= self.WTE_input.Metals_Recovery['Fly_ash_frac']['amount'] * self.Post_Combustion_Solids['Total_Post_Combustion_Solids'][1:]
        self.Post_Combustion_Solids['Fly_Ash']['Unit']= 'kg/kg ww'
        
        self.Post_Combustion_Solids['Ferrous_Recovery']= self.Material_Properties['Iron'][4:]/100 *(1-self.Material_Properties['Moisture Content'][4:]/100) * self.WTE_input.Metals_Recovery['Fe_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Fe that is Recoverable'][3:] *(1-self.process_data['Fraction of Recoverable Fe Oxidized During Combustion'][3:])
        self.Post_Combustion_Solids['Ferrous_Recovery']['Unit']= 'kg/kg ww'
            
        self.Post_Combustion_Solids['Aluminum_Recovery']= self.Material_Properties['Aluminum'][4:]/100 *(1-self.Material_Properties['Moisture Content'][4:]/100) * self.WTE_input.Metals_Recovery['Al_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Al that is Recoverable'][3:] *(1-self.process_data['Fraction of Recoverable Al Oxidized During Combustion'][3:])
        self.Post_Combustion_Solids['Aluminum_Recovery']['Unit']= 'kg/kg ww'
        
        self.Post_Combustion_Solids['Copper_Recovery']= self.Material_Properties['Copper'][4:]/100 *(1-self.Material_Properties['Moisture Content'][4:]/100) * self.WTE_input.Metals_Recovery['Cu_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Cu that is Recoverable'][3:] *(1-self.process_data['Fraction of Recoverable Cu Oxidized During Combustion'][3:])
        self.Post_Combustion_Solids['Copper_Recovery']['Unit']= 'kg/kg ww'
            
        self.Post_Combustion_Solids['Bottom_Ash_without_Metals']= self.Post_Combustion_Solids['Bottom_Ash_with_Metals'][1:] - self.Post_Combustion_Solids['Ferrous_Recovery'][1:]-\
                                                                self.Post_Combustion_Solids['Aluminum_Recovery'] - self.Post_Combustion_Solids['Copper_Recovery']
        self.Post_Combustion_Solids['Bottom_Ash_without_Metals']['Unit']= 'kg/kg ww'
        
        ### metals in bottom ash and fly ash
        key4={"As":'Arsenic', "Ba":'Barium', "Cd":'Cadmium', "Cr":'Chromium', "Cu":'Copper', "Hg":'Mercury',\
               "Ni":'Nickel', "Pb":'Lead', "Sb":'Antimony', "Se":'Selenium', "Zn":'Zinc'}
        for m in key4.keys():
            self.Post_Combustion_Solids['Fly_ash_'+m] = self.Material_Properties[key4[m]][4:]/100 * (1-self.Material_Properties['Moisture Content'][4:]/100) * self.WTE_input.Fly_Ash_metal_emission[m]['amount']
            self.Post_Combustion_Solids['Fly_ash_'+m]['Unit'] = 'kg/kg ww'
        
        for m in key4.keys():    
            self.Post_Combustion_Solids['Bottom_ash_'+m] = self.Material_Properties[key4[m]][4:]/100 * (1-self.Material_Properties['Moisture Content'][4:]/100) * self.WTE_input.Bottom_Ash_metal_emission[m]['amount']
            self.Post_Combustion_Solids['Bottom_ash_'+m]['Unit'] = 'kg/kg ww'
        
    def setup_MC(self):
        self.WTE_input.setup_MC()
    def MC_calc(self):      
        self.WTE_input.gen_MC()
        self.calc()
    def report(self):
        ### Output
        self.WTE = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.WTE  ["process name"] = 'WTE'
        self.WTE  ["Waste"] = Waste
        self.WTE  ["Technosphere"] = Technosphere
        self.WTE  ["Biosphere"] = Biosphere
        
        for x in [Waste,Technosphere, Biosphere]:
            for y in self.Index[1:]:
                x[y]={}
         
        ### Output Waste Database       
        for y in self.Index[1:]:
            Waste[y]['Bottom_Ash'] = self.Post_Combustion_Solids['Bottom_Ash_without_Metals'][y]
            
            Waste[y]['Fly_Ash'] = self.Post_Combustion_Solids['Fly_Ash'][y] + self.WTE_input.Material_Consumption['ammonia']['amount'] +\
            self.WTE_input.Material_Consumption['lime']['amount'] + self.WTE_input.Material_Consumption['carbon']['amount']
            
            Waste[y]['Al'] = self.Post_Combustion_Solids['Aluminum_Recovery'][y]
            
            Waste[y]['Fe'] = self.Post_Combustion_Solids['Ferrous_Recovery'][y]
            
            Waste[y]['Cu'] = self.Post_Combustion_Solids['Copper_Recovery'][y]
        
        ### Output Technospphere Database
            Technosphere[y][('Technosphere', 'Electricity_production')] = self.Energy_Calculations['Net_Electricity_Use'][y]
            
            Technosphere[y][('Technosphere', 'Heat_Steam')] = self.Energy_Calculations['Heat_Recovered'][y]
            
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')] = self.WTE_input.Material_Consumption['ammonia']['amount'] * self.WTE_input.Material_Consumption['ammonia']['Distance_from_prod_fac'] + \
            self.WTE_input.Material_Consumption['lime']['amount'] * self.WTE_input.Material_Consumption['lime']['Distance_from_prod_fac'] + \
            self.WTE_input.Material_Consumption['carbon']['amount'] * self.WTE_input.Material_Consumption['carbon']['Distance_from_prod_fac']
            
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')]=self.WTE_input.Material_Consumption['ammonia']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['ammonia']['Empty_Return_Truck']  + \
            self.WTE_input.Material_Consumption['lime']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['lime']['Empty_Return_Truck'] + \
            self.WTE_input.Material_Consumption['carbon']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['carbon']['Empty_Return_Truck']
            
        ### Output Biosphere Database
        
        return(self.WTE)

    
































