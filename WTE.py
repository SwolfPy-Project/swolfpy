# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:10:31 2019

@author: msmsa
"""
import numpy as np
import pandas as pd
from WTE_Input import *
from CommonData import *
from stats_arrays import *



class WTE:
    def __init__(self):
        self.CommonData = CommonData()
        self.WTE_input= WTE_input()
        ### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        self.process_data=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'WTE', index_col = 'Parameter')
        self.process_data.fillna(0,inplace=True)
        self.Index = self.CommonData.Index

        
    def calc(self):

        ### Energy Calculations
        self.Energy_Calculations=pd.DataFrame(index = self.Index)
        
        self.Energy_Calculations['Energy_Loss_Due_to_Water'] = (-1) * self.Material_Properties['Moisture Content'][4:] / 100 * self.CommonData.Evap_heat['Water_Evap_Heat']['amount']
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
                                            * (1-self.Material_Properties['Moisture Content'][4:]/100) * (self.CommonData.MW['CO2']['amount'])/self.CommonData.MW['C']['amount']
        self.Combustion_Emission['CO2_fossil']['Unit'] = 'kg/kgww'
        
        self.Combustion_Emission['CO2_biogenic'] = self.Material_Properties['Biogenic Carbon Content'][4:] / 100 * self.process_data['Combustion Efficiency (% of VS)']\
                                            * (1-self.Material_Properties['Moisture Content'][4:]/100) * (self.CommonData.MW['CO2']['amount'])/self.CommonData.MW['C']['amount']
        self.Combustion_Emission['CO2_biogenic']['Unit'] = 'kg/kgww'
        
        ### Stack metal emissions
        key1={'As':'Arsenic','Ba':'Barium','Cd':'Cadmium','Cr':'Chromium','Cu':'Copper','Hg':'Mercury','Ni':'Nickel','Pb':'Lead','Sb':'Antimony','Se':'Selenium','Zn':'Zinc'}
        for m in key1.keys():
            self.Combustion_Emission[m] = self.Material_Properties[key1[m]][4:] / 100 * self.WTE_input.Stack_metal_emission[m]['amount'] * (1-self.Material_Properties['Moisture Content'][4:]/100)
            self.Combustion_Emission[m]['Unit'] = 'kg/kgww'
        
        ### mole content of input waste
        self.Combustion_Emission['C_mole'] = (self.Material_Properties['Biogenic Carbon Content'][4:]+self.Material_Properties['Fossil Carbon Content'][4:]) / 100 \
                                        /self.CommonData.MW['C']['amount'] * 1000
        self.Combustion_Emission['C_mole']['Unit'] = 'Moles per dry kg'
        
        key2={'Hydrogen Content':('H','H_mole'),'Oxygen Content':('O','O_mole'),'Nitrogen Content':('N','N_mole'),'Chlorine':('Cl','Cl_mole'),\
              'Sulphur':('S','S_mole')}
        for m in key2.keys():
            self.Combustion_Emission[key2[m][1]] = self.Material_Properties[m][4:] / 100 /self.CommonData.MW[key2[m][0]]['amount'] * 1000
            self.Combustion_Emission[key2[m][1]]['Unit'] = 'Moles per dry kg'
        
        self.Combustion_Emission['alpha'] = -0.699*self.Combustion_Emission['O_mole'][1:]+1.5*self.Combustion_Emission['C_mole'][1:]+0.35*self.Combustion_Emission['H_mole'][1:]-0.244* \
                                        self.Combustion_Emission['Cl_mole'][1:]+1.5*self.Combustion_Emission['S_mole'][1:]+0.53*self.Combustion_Emission['N_mole'][1:]
        self.Combustion_Emission['alpha']['unit'] = '_'
        
        self.Combustion_Emission['Moles_per_dry_flue_gas'] = self.Combustion_Emission['O_mole'][1:]/2 + self.Combustion_Emission['alpha'][1:]*4.78-self.Combustion_Emission['H_mole'][1:]\
                                                        /4+5*self.Combustion_Emission['Cl_mole'][1:]/4+self.Combustion_Emission['N_mole'][1:]/2
        self.Combustion_Emission['Moles_per_dry_flue_gas']['unit'] = 'mole/kgDryFlueGas'
        
        self.Combustion_Emission['Flue_gas'] = self.Combustion_Emission['Moles_per_dry_flue_gas'][1:] * self.CommonData.STP['Density_Air']['amount']/ 1000 * (1-self.Material_Properties['Moisture Content'][4:]/100)
        self.Combustion_Emission['Flue_gas']['unit'] = 'dscm FlueGas/kgww'   #Dry Standard Cubic meter
            
        key3={'Stack_SO2':('Sulfur_dioxide',self.CommonData.MW['SO2']['amount']),'Stack_HCl':('HCl',self.CommonData.MW['HCl']['amount']),\
              'Stack_NOx':('NOx',self.CommonData.MW['NOx']['amount']),'Stack_CO':('CO',self.CommonData.MW['CO']['amount']),\
              'Stack_Methane':('Methane',self.CommonData.MW['CH4']['amount']),'Stack_Nitrous_Oxide':('Nitrous_Oxide',self.CommonData.MW['Nitrous_Oxide']['amount']),\
              'Stack_Ammonia':('Ammonia',self.CommonData.MW['Ammonia']['amount']),'Stack_Hydrocarbons':('Hydrocarbons',self.CommonData.MW['Hydrocarbons']['amount'])}
        for m in key3.keys():
            self.Combustion_Emission[m] = self.WTE_input.Stack_Gas_Conc_Non_metal[key3[m][0]]['amount']/10**6*key3[m][1]/1000 / (self.CommonData.STP['Density_Air']['amount'] / 1000) * self.Combustion_Emission['Flue_gas']
            self.Combustion_Emission[m]['Unit'] = 'kg/kg ww'
        
        self.Combustion_Emission['Stack_PM'] = self.WTE_input.Stack_Gas_Conc_Non_metal['PM']['amount']/10**6 * self.Combustion_Emission['Flue_gas']
        self.Combustion_Emission['Stack_PM']['Unit'] = 'kg/kg ww'
        
        self.Combustion_Emission['Stack_Dioxins_Furans'] = self.WTE_input.Stack_Gas_Conc_Non_metal['Dioxins_Furans']['amount']/10**12 * self.Combustion_Emission['Flue_gas']
        self.Combustion_Emission['Stack_Dioxins_Furans']['Unit'] = 'kg/kg ww'
        
        
        ### Post_Combustion Solids
        
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
            
        ### APC_Consumption
        self.APC_Consumption = pd.DataFrame(index = self.Index)
        for x in ['lime','carbon','ammonia']:
            self.APC_Consumption[x] = self.WTE_input.Material_Consumption[x]['amount']*1000
            self.APC_Consumption.loc['Unit',x]= 'kg/Mg ww'
        

    def create_uncertainty_from_inputs(self,seed=None):
        self.process_data_1=pd.read_excel("Material properties - process modles.xlsx", sheet_name = 'WTE', index_col = 'Parameter')
        self.uncertain_dict = dict()
        cols = list(self.process_data_1)
        for col in range(0,len(cols),7):
            self.uncertain_dict[cols[col]] = list()
            for val in range(len(self.process_data[cols[col]][3:])):
                self.uncertain_dict[cols[col]].append(dict())
                if not np.isnan(self.process_data_1[cols[col+1]][3+val]):
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = int(self.process_data_1[cols[col+1]][3+val])
                    self.uncertain_dict[cols[col]][val]['loc'] = self.process_data_1[cols[col+2]][3+val]
                    self.uncertain_dict[cols[col]][val]['scale'] = self.process_data_1[cols[col+3]][3+val]
                    self.uncertain_dict[cols[col]][val]['shape'] = self.process_data_1[cols[col+4]][3+val]
                    self.uncertain_dict[cols[col]][val]['minimum'] = self.process_data_1[cols[col+5]][3+val]
                    self.uncertain_dict[cols[col]][val]['maximum'] = self.process_data_1[cols[col+6]][3+val]
                else:
                    self.uncertain_dict[cols[col]][val]['uncertainty_type'] = 1
							
        self.variables = dict()
        self.rng = dict()
        for key in self.uncertain_dict.keys():
            self.variables[key] = UncertaintyBase.from_dicts(*self.uncertain_dict[key])
            self.rng[key] = MCRandomNumberGenerator(self.variables[key],seed=seed)
		
    def uncertainty_input_next(self):
        data = dict()
        for key in self.rng.keys():
            data[key] = self.rng[key].next()
            for val in range(len(self.process_data[key][3:])):
                if not np.isnan(data[key][val]):			
                    self.process_data.at[(self.process_data_1.index.values[3+val]),key] = data[key][val]

		
		
    def setup_MC(self,seed=None):
        self.WTE_input.setup_MC(seed)
        self.create_uncertainty_from_inputs()
    def MC_calc(self):      
        input_list = self.WTE_input.gen_MC()
        self.uncertainty_input_next()
        self.calc()
        return(input_list)
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
            Technosphere[y][('Technosphere', 'Electricity_production')] = (-1) * self.Energy_Calculations['Net_Electricity_Use'][y]
            
            Technosphere[y][('Technosphere', 'Heat_Steam')] = self.Energy_Calculations['Heat_Recovered'][y]
            
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')] = self.WTE_input.Material_Consumption['ammonia']['amount'] * self.WTE_input.Material_Consumption['ammonia']['Distance_from_prod_fac'] + \
            self.WTE_input.Material_Consumption['lime']['amount'] * self.WTE_input.Material_Consumption['lime']['Distance_from_prod_fac'] + \
            self.WTE_input.Material_Consumption['carbon']['amount'] * self.WTE_input.Material_Consumption['carbon']['Distance_from_prod_fac']
            
            Technosphere[y][('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck')]=self.WTE_input.Material_Consumption['ammonia']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['ammonia']['Empty_Return_Truck']  + \
            self.WTE_input.Material_Consumption['lime']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['lime']['Empty_Return_Truck'] + \
            self.WTE_input.Material_Consumption['carbon']['Distance_from_prod_fac'] * self.WTE_input.Material_Consumption['carbon']['Empty_Return_Truck']
            
            Technosphere[y][('Technosphere', 'lime_hydrated_loose_weight_RoW_lime_production')] = self.APC_Consumption['lime'][y]
            
            Technosphere[y][('Technosphere', 'ammonia_liquid_RoW_ammonia_production_steam_reforming_liquid')] = self.APC_Consumption['ammonia'][y]
            
            Technosphere[y][('Technosphere', 'charcoal_GLO_charcoal_production')] = self.APC_Consumption['carbon'][y]
            
        ### Output Biosphere Database
            key5={'Ammonia':(('biosphere3', '87883a4e-1e3e-4c9d-90c0-f1bea36f8014'),'Stack_Ammonia'),
                  'Antimony':(('biosphere3', '77927dac-dea3-429d-a434-d5a71d92c4f7'),'Sb'),
                  'Arsenic':(('biosphere3', 'dc6dbdaa-9f13-43a8-8af5-6603688c6ad0'),'As'),
                  'Barium':(('biosphere3', '7e246e3a-5cff-43fc-a8e6-02d191424559'),'Ba'),
                  'Cadmium':(('biosphere3', '1c5a7322-9261-4d59-a692-adde6c12de92'),'Cd'),
                  'Carbon dioxide, fossil':(('biosphere3', '349b29d1-3e58-4c66-98b9-9d1a076efd2e'),'CO2_fossil'),
                  'Carbon dioxide, non-fossil':(('biosphere3', 'eba59fd6-f37e-41dc-9ca3-c7ea22d602c7'),'CO2_biogenic'),
                  'Carbon monoxide, fossil':(('biosphere3', 'ba2f3f82-c93a-47a5-822a-37ec97495275'),'Stack_CO'),
                  'Chromium':(('biosphere3', 'e142b577-e934-4085-9a07-3983d4d92afb'),'Cr'),
                  'Copper':(('biosphere3', 'ec8144d6-d123-43b1-9c17-a295422a0498'),'Cu'),
                  'Dinitrogen monoxide':(('biosphere3', '20185046-64bb-4c09-a8e7-e8a9e144ca98'),'Stack_Nitrous_Oxide'),
                  'Dioxins, measured as 2,3,7,8-tetrachlorodibenzo-p-dioxin':(('biosphere3', '082903e4-45d8-4078-94cb-736b15279277'),'Stack_Dioxins_Furans'),
                  'Hydrocarbons, unspecified':(('biosphere3', 'f9abb851-8731-4c5b-b057-863996a1f94a'),'Stack_Hydrocarbons'),
                  'Hydrogen chloride':(('biosphere3', 'c941d6d0-a56c-4e6c-95de-ac685635218d'),'Stack_HCl'),
                  'Lead':(('biosphere3', '8e123669-94d3-41d8-9480-a79211fe7c43'),'Pb'),
                  'Mercury':(('biosphere3', '71234253-b3a7-4dfe-b166-a484ad15bee7'),'Hg'),
                  'Methane':(('biosphere3', 'b53d3744-3629-4219-be20-980865e54031'),'Stack_Methane'),
                  'Nickel':(('biosphere3', 'a5506f4b-113f-4713-95c3-c819dde6e48b'),'Ni'),
                  'Nitrogen oxides':(('biosphere3', 'c1b91234-6f24-417b-8309-46111d09c457'),'Stack_NOx'),
                  'Particulates, < 2.5 um':(('biosphere3', '21e46cb8-6233-4c99-bac3-c41d2ab99498'),'Stack_PM'),
                  'Selenium':(('biosphere3', '454c61fd-c52b-4a04-9731-f141bb7b5264'),'Se'),
                  'Sulfur dioxide':(('biosphere3', 'fd7aa71c-508c-480d-81a6-8052aad92646'),'Stack_SO2'),
                  'Zinc':(('biosphere3', '5ce378a0-b48d-471c-977d-79681521efde'),'Zn')}
            for x in key5:
                Biosphere[y][key5[x][0]]= self.Combustion_Emission[key5[x][1]][y]
        
        return(self.WTE)






