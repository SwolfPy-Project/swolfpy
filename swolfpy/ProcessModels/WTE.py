# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:10:31 2019

@author: msmsa
"""
import numpy as np
import pandas as pd
#from WTE_Input_script import *
from .WTE_Input import *
from .CommonData import *
from stats_arrays import *
from pathlib import Path


class WTE:
    def __init__(self,input_data_path=None,CommonDataObjct=None):
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()
            
        self.Process_Type = 'Treatment'
        self.InputData= WTE_input(input_data_path)
        ### Read Material properties
        self.Material_Properties=pd.read_excel(Path(__file__).parent.parent/'Data/Material properties.xlsx',index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel(Path(__file__).parent.parent/'Data/Material properties - process modles.xlsx', sheet_name = 'WTE', index_col = 'Parameter')
        self.process_data.fillna(0,inplace=True)
        self.Index = self.CommonData.Index[1:]
        
    def calc(self):
        self.LCI_index = False

        ### Energy Calculations
        self.Energy_Calculations=pd.DataFrame(index = self.Index)
        
        #'MJ/kgww'
        self.Energy_Calculations['Energy_Loss_Due_to_Water'] = (-1) * self.Material_Properties['Moisture Content'][4:].values / 100 * self.CommonData.Evap_heat['Water_Evap_Heat']['amount'] 
        
        #'MJ/kgww'
        self.Energy_Calculations['Energy_Loss_Due_to_Ashes'] = (-1) *  self.process_data['Heat Lost via Ashes - Cp (J/g K)'][3:].values * \
                                                        self.process_data['Temperature Difference (K)'][3:].values /1000 * (self.Material_Properties['Ash Content'][4:].values/100 + \
                                                        self.Material_Properties['Volatile Solids'][4:].values/100*(1-self.process_data['Combustion Efficiency (% of VS)'][3:].values))\
                                                        * (100-self.Material_Properties['Moisture Content'][4:].values) /100

        #'MJ/kgww'
        self.Energy_Calculations['Energy_Produced'] = self.Material_Properties['Lower Heating Value'][4:].values * self.process_data['Combustion Efficiency (% of VS)'][3:].values * \
                                                (100-self.Material_Properties['Moisture Content'][4:].values)/100

        
        #'MJ/kgww'
        self.Energy_Calculations['Total_Energy_Produced'] = self.Energy_Calculations['Energy_Produced'].values + self.Energy_Calculations['Energy_Loss_Due_to_Ashes'].values + \
                                                       self.Energy_Calculations['Energy_Loss_Due_to_Water'].values

        # 'kWh/kgww'
        self.Energy_Calculations['Energy_Recovered_as_Electricity'] = self.Energy_Calculations['Total_Energy_Produced'].values * self.InputData.Elec_Prod_Eff['Net_Efficiency']['amount'] / 3.6
        
        # 'kWh/Mgww'
        self.Energy_Calculations['Net_Electricity_Use'] = self.Energy_Calculations['Energy_Recovered_as_Electricity'].values * (-1000)

        #'MJ/Mgww'
        self.Energy_Calculations['Heat_Recovered'] = self.Energy_Calculations['Total_Energy_Produced'].values * 1000 * self.InputData.Elec_Prod_Eff['Heat_prod_Eff']['amount']
            
        ### Combustion Emission
        self.Combustion_Emission = pd.DataFrame(index = self.Index)
        
        #'kg/kgww'
        self.Combustion_Emission['CO2_fossil'] = self.Material_Properties['Fossil Carbon Content'][4:].values / 100 * self.process_data['Combustion Efficiency (% of VS)'][3:].values\
                                            * (1-self.Material_Properties['Moisture Content'][4:].values/100) * (self.CommonData.MW['CO2']['amount'])/self.CommonData.MW['C']['amount']
        
        #'kg/kgww'
        self.Combustion_Emission['CO2_biogenic'] = self.Material_Properties['Biogenic Carbon Content'][4:].values / 100 * self.process_data['Combustion Efficiency (% of VS)'][3:].values\
                                            * (1-self.Material_Properties['Moisture Content'][4:].values/100) * (self.CommonData.MW['CO2']['amount'])/self.CommonData.MW['C']['amount']

        
        ### Stack metal emissions
        key1={'As':'Arsenic','Ba':'Barium','Cd':'Cadmium','Cr':'Chromium','Cu':'Copper','Hg':'Mercury','Ni':'Nickel','Pb':'Lead','Sb':'Antimony','Se':'Selenium','Zn':'Zinc'}
        for m in key1.keys():
            # 'kg/kgww'
            self.Combustion_Emission[m] = self.Material_Properties[key1[m]][4:].values / 100 * self.InputData.Stack_metal_emission[m]['amount'] * (1-self.Material_Properties['Moisture Content'][4:].values/100)

        
        ### mole content of input waste
        #'Moles per dry kg'
        self.Combustion_Emission['C_mole'] = (self.Material_Properties['Biogenic Carbon Content'][4:].values+self.Material_Properties['Fossil Carbon Content'][4:].values) / 100 \
                                        /self.CommonData.MW['C']['amount'] * 1000

        
        key2={'Hydrogen Content':('H','H_mole'),'Oxygen Content':('O','O_mole'),'Nitrogen Content':('N','N_mole'),'Chlorine':('Cl','Cl_mole'),\
              'Sulphur':('S','S_mole')}
        for m in key2.keys():
            #'Moles per dry kg'
            self.Combustion_Emission[key2[m][1]] = self.Material_Properties[m][4:].values / 100 /self.CommonData.MW[key2[m][0]]['amount'] * 1000

        
        self.Combustion_Emission['alpha'] = -0.699*self.Combustion_Emission['O_mole'].values+1.5*self.Combustion_Emission['C_mole'].values+0.35*self.Combustion_Emission['H_mole'].values-0.244* \
                                        self.Combustion_Emission['Cl_mole'].values+1.5*self.Combustion_Emission['S_mole'].values+0.53*self.Combustion_Emission['N_mole'].values

        
        #'mole/kgDryFlueGas'
        self.Combustion_Emission['Moles_per_dry_flue_gas'] = self.Combustion_Emission['O_mole'].values/2 + self.Combustion_Emission['alpha'].values*4.78-self.Combustion_Emission['H_mole'].values\
                                                        /4+5*self.Combustion_Emission['Cl_mole'].values/4+self.Combustion_Emission['N_mole'].values/2

        #'dscm FlueGas/kgww'   #Dry Standard Cubic meter
        self.Combustion_Emission['Flue_gas'] = self.Combustion_Emission['Moles_per_dry_flue_gas'].values * self.CommonData.STP['Density_Air']['amount']/ 1000 * (1-self.Material_Properties['Moisture Content'][4:].values/100)

            
        key3={'Stack_SO2':('Sulfur_dioxide',self.CommonData.MW['SO2']['amount']),'Stack_HCl':('HCl',self.CommonData.MW['HCl']['amount']),\
              'Stack_NOx':('NOx',self.CommonData.MW['NOx']['amount']),'Stack_CO':('CO',self.CommonData.MW['CO']['amount']),\
              'Stack_Methane':('Methane',self.CommonData.MW['CH4']['amount']),'Stack_Nitrous_Oxide':('Nitrous_Oxide',self.CommonData.MW['Nitrous_Oxide']['amount']),\
              'Stack_Ammonia':('Ammonia',self.CommonData.MW['Ammonia']['amount']),'Stack_Hydrocarbons':('Hydrocarbons',self.CommonData.MW['Hydrocarbons']['amount'])}
        for m in key3.keys():
            #'kg/kg ww'
            self.Combustion_Emission[m] = self.InputData.Stack_Gas_Conc_Non_metal[key3[m][0]]['amount']/10**6*key3[m][1]/1000 / (self.CommonData.STP['Density_Air']['amount'] / 1000) * self.Combustion_Emission['Flue_gas'].values

        #'kg/kg ww'
        self.Combustion_Emission['Stack_PM'] = self.InputData.Stack_Gas_Conc_Non_metal['PM']['amount']/10**6 * self.Combustion_Emission['Flue_gas'].values

        #'kg/kg ww'
        self.Combustion_Emission['Stack_Dioxins_Furans'] = self.InputData.Stack_Gas_Conc_Non_metal['Dioxins_Furans']['amount']/10**12 * self.Combustion_Emission['Flue_gas'].values
        
        ### Post_Combustion Solids
        self.Post_Combustion_Solids = pd.DataFrame(index = self.Index)
        
        #'kg/kg ww'
        self.Post_Combustion_Solids['Total_Post_Combustion_Solids']= self.Material_Properties['Ash Content'][4:].values/100 + (1-self.Material_Properties['Moisture Content'][4:].values/100)* \
                                                                self.Material_Properties['Volatile Solids'][4:].values*(1-self.process_data['Combustion Efficiency (% of VS)'][3:].values)

        #'kg/kg ww'
        self.Post_Combustion_Solids['Bottom_Ash_with_Metals']= (1-self.InputData.Metals_Recovery['Fly_ash_frac']['amount'])* self.Post_Combustion_Solids['Total_Post_Combustion_Solids'].values

        # 'kg/kg ww'
        self.Post_Combustion_Solids['Fly_Ash']= self.InputData.Metals_Recovery['Fly_ash_frac']['amount'] * self.Post_Combustion_Solids['Total_Post_Combustion_Solids'].values
        
        #'kg/kg ww'
        self.Post_Combustion_Solids['Ferrous_Recovery']= self.Material_Properties['Iron'][4:].values/100 *(1-self.Material_Properties['Moisture Content'][4:].values/100) * self.InputData.Metals_Recovery['Fe_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Fe that is Recoverable'][3:].values *(1-self.process_data['Fraction of Recoverable Fe Oxidized During Combustion'][3:].values)
                                                    
        #'kg/kg ww'    
        self.Post_Combustion_Solids['Aluminum_Recovery']= self.Material_Properties['Aluminum'][4:].values/100 *(1-self.Material_Properties['Moisture Content'][4:].values/100) * self.InputData.Metals_Recovery['Al_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Al that is Recoverable'][3:].values *(1-self.process_data['Fraction of Recoverable Al Oxidized During Combustion'][3:].values)
                                                    
        
        #'kg/kg ww'
        self.Post_Combustion_Solids['Copper_Recovery']= self.Material_Properties['Copper'][4:].values/100 *(1-self.Material_Properties['Moisture Content'][4:].values/100) * self.InputData.Metals_Recovery['Cu_Rec_Rate']['amount'] \
                                                    * self.process_data['Fraction of Cu that is Recoverable'][3:].values *(1-self.process_data['Fraction of Recoverable Cu Oxidized During Combustion'][3:].values)

            
        #'kg/kg ww'
        self.Post_Combustion_Solids['Bottom_Ash_without_Metals']= self.Post_Combustion_Solids['Bottom_Ash_with_Metals'].values - self.Post_Combustion_Solids['Ferrous_Recovery'].values-\
                                                                self.Post_Combustion_Solids['Aluminum_Recovery'].values - self.Post_Combustion_Solids['Copper_Recovery'].values
        
        ### metals in bottom ash and fly ash
        key4={"As":'Arsenic', "Ba":'Barium', "Cd":'Cadmium', "Cr":'Chromium', "Cu":'Copper', "Hg":'Mercury',\
               "Ni":'Nickel', "Pb":'Lead', "Sb":'Antimony', "Se":'Selenium', "Zn":'Zinc'}
        for m in key4.keys():
            #'kg/kg ww'
            self.Post_Combustion_Solids['Fly_ash_'+m] = self.Material_Properties[key4[m]][4:].values/100 * (1-self.Material_Properties['Moisture Content'][4:].values/100) * self.InputData.Fly_Ash_metal_emission[m]['amount']
        
        for m in key4.keys():    
            #'kg/kg ww'
            self.Post_Combustion_Solids['Bottom_ash_'+m] = self.Material_Properties[key4[m]][4:].values/100 * (1-self.Material_Properties['Moisture Content'][4:].values/100) * self.InputData.Bottom_Ash_metal_emission[m]['amount']
            
        ### APC_Consumption
        self.APC_Consumption = pd.DataFrame(index = self.Index)
        for x in ['lime','carbon','ammonia']:
            #'kg/Mg ww'
            self.APC_Consumption[x] = self.InputData.Material_Consumption[x]['amount']*1000
        		
		
    def setup_MC(self,seed=None):
        self.InputData.setup_MC(seed)
        self.InputData.create_uncertainty_from_inputs("WTE",self.process_data,seed)
		
    def MC_calc(self):      
        input_list = self.InputData.gen_MC()
        input_list2 = self.InputData.uncertainty_input_next()
        self.calc()
        return(input_list+input_list2)
		
    def report(self):
        ### Output
        self.WTE = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.WTE  ["process name"] = 'WTE'
        self.WTE  ["Waste"] = Waste
        self.WTE  ["Technosphere"] = Technosphere

        
        for x in [Waste,Technosphere]:
            for y in self.Index:
                x[y]={}
         
        ### Output Waste Database       
        for y in self.Index:
            Waste[y]['Bottom_Ash'] = self.Post_Combustion_Solids['Bottom_Ash_without_Metals'][y]
            
            Waste[y]['Fly_Ash'] = self.Post_Combustion_Solids['Fly_Ash'][y] + self.InputData.Material_Consumption['ammonia']['amount'] +\
            self.InputData.Material_Consumption['lime']['amount'] + self.InputData.Material_Consumption['carbon']['amount']
            
            Waste[y]['Al'] = self.Post_Combustion_Solids['Aluminum_Recovery'][y]
            
            Waste[y]['Fe'] = self.Post_Combustion_Solids['Ferrous_Recovery'][y]
            
            Waste[y]['Cu'] = self.Post_Combustion_Solids['Copper_Recovery'][y]
        
        ### Output Technospphere Database
            Technosphere[y][('Technosphere', 'Electricity_production')] = (-1) * self.Energy_Calculations['Net_Electricity_Use'][y]
            
            Technosphere[y][('Technosphere', 'Heat_Steam')] = self.Energy_Calculations['Heat_Recovered'][y]
            
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')] = self.InputData.Material_Consumption['ammonia']['amount'] * self.InputData.Material_Consumption['Distance_from_prod_fac']['amount'] + \
            self.InputData.Material_Consumption['lime']['amount'] * self.InputData.Material_Consumption['Distance_from_prod_fac']['amount'] + \
            self.InputData.Material_Consumption['carbon']['amount'] * self.InputData.Material_Consumption['Distance_from_prod_fac']['amount']
            
            Technosphere[y][('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck')]=(self.InputData.Material_Consumption['Distance_from_prod_fac']['amount'] * self.InputData.Material_Consumption['Empty_Return_Truck']['amount']  + \
            self.InputData.Material_Consumption['Distance_from_prod_fac']['amount'] * self.InputData.Material_Consumption['Empty_Return_Truck']['amount'] + \
            self.InputData.Material_Consumption['Distance_from_prod_fac']['amount'] * self.InputData.Material_Consumption['Empty_Return_Truck']['amount'])/23   # 23 is the heavy duty truck payload
            
            Technosphere[y][('Technosphere', 'lime_hydrated_loose_weight_RoW_lime_production')] = self.APC_Consumption['lime'][y]
            
            Technosphere[y][('Technosphere', 'ammonia_liquid_RoW_ammonia_production_steam_reforming_liquid')] = self.APC_Consumption['ammonia'][y]
            
            Technosphere[y][('Technosphere', 'charcoal_GLO_charcoal_production')] = self.APC_Consumption['carbon'][y]
            
        ### Output Biosphere Database
        bio_rename_dict={'Stack_Ammonia':('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014'),
              'Sb':('biosphere3', '77927dac-dea3-429d-a434-d5a71d92c4f7'),
              'As':('biosphere3', 'dc6dbdaa-9f13-43a8-8af5-6603688c6ad0'),
              'Ba':('biosphere3', '7e246e3a-5cff-43fc-a8e6-02d191424559'),
              'Cd':('biosphere3', '1c5a7322-9261-4d59-a692-adde6c12de92'),
              'CO2_fossil':('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'),
              'CO2_biogenic':('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7'),
              'Stack_CO':('biosphere3', 'ba2f3f82-c93a-47a5-822a-37ec97495275'),
              'Cr':('biosphere3', 'e142b577-e934-4085-9a07-3983d4d92afb'),
              'Cu':('biosphere3', 'ec8144d6-d123-43b1-9c17-a295422a0498'),
              'Stack_Nitrous_Oxide':('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98'),
              'Stack_Dioxins_Furans':('biosphere3', '082903e4-45d8-4078-94cb-736b15279277'),
              'Stack_Hydrocarbons':('biosphere3', 'f9abb851-8731-4c5b-b057-863996a1f94a'),
              'Stack_HCl':('biosphere3', 'c941d6d0-a56c-4e6c-95de-ac685635218d'),
              'Pb':('biosphere3', '8e123669-94d3-41d8-9480-a79211fe7c43'),
              'Hg':('biosphere3', '71234253-b3a7-4dfe-b166-a484ad15bee7'),
              'Stack_Methane':('biosphere3', 'b53d3744-3629-4219-be20-980865e54031'),
              'Ni':('biosphere3', 'a5506f4b-113f-4713-95c3-c819dde6e48b'),
              'Stack_NOx':('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457'),
              'Stack_PM':('biosphere3', '21e46cb8-6233-4c99-bac3-c41d2ab99498'),
              'Se':('biosphere3', '454c61fd-c52b-4a04-9731-f141bb7b5264'),
              'Stack_SO2':('biosphere3', 'fd7aa71c-508c-480d-81a6-8052aad92646'),
              'Zn':('biosphere3', '5ce378a0-b48d-471c-977d-79681521efde')}
        
        # report function rename the LCI dataframe, so we use the self.LCI_index to rename LCI only one time 
        # unless the we call the calc function
        if not self.LCI_index:
            self.Combustion_Emission=self.Combustion_Emission.rename(columns=bio_rename_dict)
            self.LCI_index = True
        
        self.Biosphere = (self.Combustion_Emission[bio_rename_dict.values()]*1000).transpose().to_dict()
        self.WTE["Biosphere"] = self.Biosphere
        return(self.WTE)


# =============================================================================
# from time import time
# A=WTE()
# A.calc() 
# B = time()
# for i in range(100):
#     A.calc() 
#     A.report()
# print(time()-B)
# =============================================================================



