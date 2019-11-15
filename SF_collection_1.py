# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from SF_collection_Input import *
from CommonData import *
from stats_arrays import *

class SF_Col:
    def __init__(self,Collection_scheme,Distance,Treatment_processes=None,Waste_gen_comp=None,sector_population=None, name=None):
### Importing the CommonData and Input data for SF_collection
        self.CommonData = CommonData()
        self.Input= SF_collection_Input()
        
        if name:
            self.name = name
        else:
            self.name =False
        
        if Treatment_processes:
            self.Treat_proc = Treatment_processes
        else:
            self.Treat_proc =False
            
            
### Read Material properties
        self.Material_Properties=pd.read_excel("Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)
        
### Read Material properties related to the process        
        self.process_data = pd.read_csv('SF_collection_Input-Material_dependent.csv',index_col = 'Materials')
        self.process_data.fillna(0,inplace=True)

### Read input data        
        self.col=pd.read_csv('SF_input_col.csv',index_col='Name',usecols=['Name','RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO'])
        self.col = self.col.transpose()

        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
                      'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
                      'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
                      'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
                      'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
                      'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
                      'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
                      'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
                      'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        self.col_schm = Collection_scheme
    def calc_composition(self):
        #Single Family Residential Waste Generation Rate (kg/household-week)
        g_res = 7*self.Input.Col['res_per_dwel']['amount']*self.Input.Col['res_gen']['amount']
        total_waste_gen = g_res * self.Input.Col['houses_res']['amount'] * 52 /1000

        
        #Check for Leave Vaccum
        self.process_data['LV'] = 0
        if self.Input.Col['Leaf_vacuum']['amount']==1:
            LV_gen = self.process_data.loc['Yard_Trimmings_Leaves','Comp']*self.Input.Col['res_gen']['amount'] * 365
            LV_col = self.Input.Col['Leaf_vacuum_amount']['amount']*1000/self.Input.Col['res_pop']['amount']
            self.process_data.loc['Yard_Trimmings_Leaves','LV'] = 1 if LV_gen <= LV_col else LV_col/LV_gen
            for j in ['RWC','SSO_DryRes','REC_WetRes','MRDO']:
                self.col_schm[j]['separate_col']['LV']=1 
        else:
            for j in ['RWC','SSO_DryRes','REC_WetRes','MRDO']:
                self.col_schm[j]['separate_col']['LV']=0
        self.col.loc['LV','Fr'] = self.Input.Col['LV_serv_times']['amount']/self.Input.Col['LV_serv_pd']['amount']
                

        # Total fraction where this service is offered        
        self.col_proc = {'RWC':self.col_schm['RWC']['Contribution'],
                        'SSO':self.col_schm['SSO_DryRes']['Contribution'],
                        'DryRes':self.col_schm['SSO_DryRes']['Contribution'],
                        'REC':self.col_schm['REC_WetRes']['Contribution'],
                        'WetRes':self.col_schm['REC_WetRes']['Contribution'],
                        'MRDO':self.col_schm['MRDO']['Contribution']}
        for i in ['LV','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']:
            self.col_proc[i] = sum([self.col_schm[j]['Contribution']*self.col_schm[j]['separate_col'][i] for j in ['RWC','SSO_DryRes','REC_WetRes','MRDO']])
            
        #Is this collection process offered? (1: in use, 0: not used)
        self.P_use = {}
        for j in self.col_proc.keys():
            self.P_use[j]= 1 if self.col_proc[j]>0 else 0
        
        #SWM Mass separated by collection process (Calculation)
        columns = ['RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']
        self.mass=pd.DataFrame(index =self.Index,columns=columns)
        
        for i in ['SSR','DSR','MSR','SSYW','SSO','REC','SSYWDO','MSRDO']:
            self.mass[i] = g_res * self.process_data[i] * self.process_data['Comp'] * self.P_use[i]
            self.mass.loc['Yard_Trimmings_Leaves',i] *= (1-self.process_data.loc['Yard_Trimmings_Leaves','LV'] )
        self.mass['LV'] = g_res * self.process_data['LV'] * self.process_data['Comp'] * self.P_use['LV']
        
        
        
        # Calculating the residual waste after separate collection
        for j in ['RWC','MRDO']:
            self.mass[j]= (g_res * self.process_data[j] * self.process_data['Comp'] - self.mass['SSR']*self.col_schm[j]['separate_col']['SSR'] - \
             self.mass['DSR']*self.col_schm[j]['separate_col']['DSR'] - self.mass['MSR']*self.col_schm[j]['separate_col']['MSR'] - \
             self.mass['LV']*self.col_schm[j]['separate_col']['LV'] - self.mass['SSYW']*self.col_schm[j]['separate_col']['SSYW'] -\
             self.mass['SSYWDO']*self.col_schm[j]['separate_col']['SSYWDO']-self.mass['MSRDO']*self.col_schm[j]['separate_col']['MSRDO'])* self.P_use[j]
        
        self.mass['DryRes']= (g_res * self.process_data['DryRes'] * self.process_data['Comp'] - self.mass['SSR']*self.col_schm['SSO_DryRes']['separate_col']['SSR'] - \
         self.mass['DSR']*self.col_schm['SSO_DryRes']['separate_col']['DSR'] - self.mass['MSR']*self.col_schm['SSO_DryRes']['separate_col']['MSR'] - \
         self.mass['LV']*self.col_schm['SSO_DryRes']['separate_col']['LV'] - self.mass['SSYW']*self.col_schm['SSO_DryRes']['separate_col']['SSYW'] -\
         self.mass['SSYWDO']*self.col_schm['SSO_DryRes']['separate_col']['SSYWDO']-self.mass['MSRDO']*self.col_schm['SSO_DryRes']['separate_col']['MSRDO']-\
         self.mass['SSO'])* self.P_use['DryRes']
                
        self.mass['WetRes']= (g_res * self.process_data['WetRes'] * self.process_data['Comp'] - self.mass['SSR']*self.col_schm['REC_WetRes']['separate_col']['SSR'] - \
         self.mass['DSR']*self.col_schm['REC_WetRes']['separate_col']['DSR'] - self.mass['MSR']*self.col_schm['REC_WetRes']['separate_col']['MSR'] - \
         self.mass['LV']*self.col_schm['REC_WetRes']['separate_col']['LV'] - self.mass['SSYW']*self.col_schm['REC_WetRes']['separate_col']['SSYW'] -\
         self.mass['SSYWDO']*self.col_schm['REC_WetRes']['separate_col']['SSYWDO']-self.mass['MSRDO']*self.col_schm['REC_WetRes']['separate_col']['MSRDO']-\
         self.mass['REC'])* self.P_use['WetRes']
        
 
        
        
        #Annual Mass Flows (Mg/yr)
        self.col_massflow=pd.DataFrame(index =self.Index)
        for i in ['RWC','SSR','DSR','MSR','MSRDO','LV','SSYW','SSYWDO','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            self.col_massflow[i]=self.mass[i] * self.Input.Col['houses_res']['amount'] * 52/1000 * self.col_proc[i]
        
        #Check generated mass = Collected mass
        tol_mass=self.mass.sum(axis=0)
        self.Mass_balance_Error = sum(self.col_massflow.sum())/total_waste_gen

        #Volume Composition of each collection process for each sector
        mass_to_cyd = self.process_data['Bulk_Density'].apply(lambda x: 1/x*1.30795 if x >0 else 0)
        for i in ['RWC','SSR','DSR','MSR','LV','SSYW','MRDO','SSYWDO','MSRDO']:
            vol = sum(self.mass[i]*mass_to_cyd)  # Unit kg/cyd
            if vol > 0 :
                self.col.loc[i,'den_c'] = sum(self.mass[i]*2.205/ vol)  # Unit lb/cyd
            else:
                self.col.loc[i,'den_c'] = 0
        for i,j in [('SSO','DryRes'),('REC','WetRes')]:
            vol = sum((self.mass[i]+self.mass[j])*mass_to_cyd)  # Unit kg/cyd
            if vol > 0 :
                self.col.loc[i,'den_c'] = sum((self.mass[i]+self.mass[j])*2.205/ vol)  # Unit lb/cyd
            else:
                self.col.loc[i,'den_c'] = 0
    

    def find_destination(self,product,Treatment_processes):
        destination={}
        for P in Treatment_processes:
            if product in Treatment_processes[P]['input_type']:
                destination[P] = Treatment_processes[P]['distance'][self.name]
        return(destination)
    
    ### calculating LCI and cost for different locations
    def calc_destin(self):
        if self.Treat_proc:
            self.dest = {}
            self.result_destination={}
            for i in ['RWC','SSR','DSR','MSR','MSRDO','LV','SSYW','SSYWDO','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
                self.dest[i]= self.find_destination(i,self.Treat_proc)
                self.result_destination[i] = {}
        
            # Number of times we need to run the collection
            n_run= max([len(self.dest[i]) for i in self.dest.keys()])
            
    
            for i in range(n_run):
                for j in self.dest.keys():
                    if len(self.dest[j]) > i:
                        self.col['Drf'][j] =self.dest[j][list(self.dest[j].keys())[i]]
                self.calc_lci()
                for j in self.dest.keys():
                    if len(self.dest[j]) > i:
                        self.result_destination[j][list(self.dest[j].keys())[i]] ={}
                        if self.output['FuelMg'][j] + self.output['FuelMg_dov'][j] !=0:
                            self.result_destination[j][list(self.dest[j].keys())[i]][('Technosphere', 'Equipment_Diesel')]=self.output['FuelMg'][j] + self.output['FuelMg_dov'][j]
                        if self.output['FuelMg_CNG'][j]!=0:
                            self.result_destination[j][list(self.dest[j].keys())[i]][('Technosphere', 'Equipment_CNG')]=self.output['FuelMg_CNG'][j]
                        if self.output['ElecMg'][j]!=0:
                            self.result_destination[j][list(self.dest[j].keys())[i]][('Technosphere', 'Electricity_consumption')]=self.output['ElecMg'][j]
        else:
            self.calc_lci()
            self.result_destination={}

        
    def calc_lci(self):
        #Selected compartment compaction density  (lb/yd3)
        #Override calculated density den_c and use an average assumed in-truck density
        self.col['d_msw']= self.col[['den_asmd','den_c']].apply(lambda x: x[0] if x[0]>0 else x[1],axis=1)
        
        #Between collection stops (miles/hour)
        self.col['Vbet'] = self.col['Dbtw']/( self.col['Tbtw']/60)
        #From collection route to facility (miles/hour)
        self.col['Vrf'] = self.col['Drf']/( self.col['Trf']/60)
        #From garage to route in the morning  (miles/hour)
        self.col['Vgr'] = self.col['Dgr']/( self.col['Tgr']/60)
        #From facility to garage (miles/hour)
        self.col['Vfg'] = self.col['Dfg']/( self.col['Tfg']/60)


        for i in ['RWC','SSR','DSR','MSR','LV','SSYW','MRDO','SSYWDO','MSRDO']:
            self.col.loc[i,'option_frac'] = self.col_proc[i]
            self.col.loc[i,'mass'] = sum(self.mass[i])
        # Revising mass of SSO_DryRes and REC_WetRec 
        for i,j in [('SSO','DryRes'),('REC','WetRes')]:
            self.col.loc[i,'mass'] = sum(self.mass[i] + self.mass[j])
        # Revising mass of LV collection - as it happens only in LV_serv_pd
        self.col.loc['LV','mass'] = self.col.loc['LV','mass']*52/self.Input.Col['LV_serv_pd']['amount']
            

### COLLECTION COSTS         
        # Collection use

            
        

### Calculations for collection vehicle activities
        #houses per trip (Volume limited) and (mass limited)
        for i in ['RWC','SSR','DSR','MSR','SSYW','SSO','REC','LV']:
            if not self.col.loc[i,'mass'] > 0:
                self.col.loc[i,'Ht_v']=0
                self.col.loc[i,'Ht_m']=0
            else:
                self.col.loc[i,'Ht_v']  = self.col.loc[i,'Ut']*self.col.loc[i,'Vt']*self.col.loc[i,'d_msw']*0.4536*self.col.loc[i,'Fr'] /self.col.loc[i,'mass']
                self.col.loc[i,'Ht_m']  = self.col.loc[i,'max_weight']*self.col.loc[i,'Fr']*1000 /  self.col.loc[i,'mass']                
            #households per trip (limited by mass or volume)
            if self.col.loc[i,'wt_lim'] == 1:
                self.col.loc[i,'Ht'] = min(self.col.loc[i,'Ht_v'],self.col.loc[i,'Ht_m'])
            else:
                self.col.loc[i,'Ht'] = self.col.loc[i,'Ht_v']
        

        #time per trip (min/trip) -- collection+travel+unload time
        self.col['Tc'] = self.col['Tbtw']*(self.col['Ht']/self.col['HS']-1)+self.col['TL']*self.col['Ht']/self.col['HS']+2*self.col['Trf']+self.col['S']

        #trips per day per vehicle (trip/day-vehicle)
        self.col['RD'] =  (self.col['WV']*60-(self.col['F1_']+self.col['F2_']+self.col['Tfg'])-0.5*(self.col['Trf']+self.col['S']))/self.col['Tc']
       
        #daily weight of refuse collected per vehicle (Mg/vehicle-day)
        self.col['RefD'] = self.col['Ht'] * self.col['mass']/self.col['Fr']/1000 * self.col['RD']
        
        #number of collection stops per day (stops/vehicle-day)
        for i in ['RWC','SSR','DSR','MSR','SSYW','SSO','REC','LV']:
            self.col['SD'] = self.col['Ht']*self.col['RD']/self.col['HS']

### Calculations for collection vehicle activities  (Drop off)
        for i in ['MRDO','SSYWDO','MSRDO']:
            #volume of recyclables deposited at drop-off site per week (cy/week-house)
            self.col.loc[i,'Ht'] = sum(self.mass[i])*self.Input.Col['houses_res']['amount']*self.col_proc[i]/0.4536 /self.col['d_msw'][i]
            
            #collection vehicle trips per week (trips/week)
            self.col.loc[i,'DO_trip_week'] =  self.col['Ht'][i] / (self.col['Vt'][i]*self.col['Ut'][i])
            
            #time per trip (min/trip) -- load+travel+unload time
            self.col.loc[i,'Tc'] = self.col['TL'][i]+2*self.col['Trf'][i]+self.col['S'][i]
                        
            #trips per day per vehicle (trip/day-vehicle)
            self.col.loc[i,'RD'] = (self.col['WV'][i]*60-(self.col['F1_'][i]+self.col['F2_'][i]+self.col['Tfg'][i]+self.col['Tgr'][i])+self.col['Trf'][i])/self.col['Tc'][i]





#daily weight of refuse collected per vehicle (tons/day-vehicle)
#number of collection stops per day (stops/vehicle-day) (1 stop per trip)











### Daily collection vehicle activity times        
        #loading time at collection stops (min/day-vehicle)
        self.col['LD'] = self.col['SD']*self.col['TL']
            
        #travel time between collection stops (min/day-vehicle)
        self.col['Tb'] = self.col['SD'].apply(lambda x: 0 if (x-1)<1 else x-1)*self.col['Tbtw']

        #travel time between route and disposal facility (min/day-vehicle)
        self.col['F_R'] = (2*self.col['RD']+0.5)*self.col['Trf']
        
        #unloading time at disposal facility (min/day-vehicle)
        self.col['UD'] = (self.col['RD']+0.5)*self.col['S']

### Daily fuel usage - Diesel
        for i in ['RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            if self.col.loc[i,'MPG_all'] != 0:
                #from garage to first collection route (gallons/day-vehicle)
                self.col.loc[i,'diesel_gr'] = self.col['Fract_Dies'][i] * self.col['Dgr'][i] /self.col['MPG_all'][i]
                #break time, if spent idling
                self.col.loc[i,'diesel_idl'] = 0
                #from first through last collection stop (gallons/day-vehicle)
                self.col.loc[i,'diesel_col'] = self.col['Fract_Dies'][i] * self.col['Dbtw'][i] * self.col['SD'][i] /self.col['MPG_all'][i]
                #between disposal facility and route (gallons/day-vehicle)
                self.col.loc[i,'diesel_rf'] = self.col['Fract_Dies'][i] * self.col['F_R'][i]/60 * self.col['Vrf'][i]  /self.col['MPG_all'][i]
                #unloading at disposal facility (gallons/day-vehicle)
                self.col.loc[i,'diesel_ud'] = 0
                #from disposal facility to garage (gallons/day-vehicle)
                self.col.loc[i,'diesel_fg'] = self.col['Fract_Dies'][i] * self.col['Dfg'][i] /self.col['MPG_all'][i]
            else:
                self.col.loc[i,'diesel_gr'] = self.col['Fract_Dies'][i] * self.col['Dgr'][i]*((1-self.col['fDgr'][i])/self.col['MPG_urban'][i]+self.col['fDgr'][i]/self.col['MPG_highway'][i])
                self.col.loc[i,'diesel_idl'] = self.col['Fract_Dies'][i] * (self.col['F1_'][i]*self.col['F1_idle'][i] + self.col['F2_'][i]*self.col['F2_idle'][i])/60 * self.col['GPH_idle_cv'][i]
                self.col.loc[i,'diesel_col'] = self.col['Fract_Dies'][i] * self.col['Dbtw'][i] * self.col['SD'][i] /self.col['MPG_collection'][i]
                self.col.loc[i,'diesel_rf'] = self.col['Fract_Dies'][i] * self.col['F_R'][i]/60 * self.col['Vrf'][i]  *((1-self.col['fDrd'][i])/self.col['MPG_urban'][i] + self.col['fDrd'][i]/self.col['MPG_highway'][i])
                self.col.loc[i,'diesel_ud'] = self.col['Fract_Dies'][i] * self.col['UD'][i] /60 * self.col['GPH_idle_cv'][i]
                self.col.loc[i,'diesel_fg'] = self.col['Fract_Dies'][i] * self.col['Dfg'][i] *((1-self.col['fDfg'][i])/self.col['MPG_urban'][i] + self.col['fDfg'][i]/self.col['MPG_highway'][i])

        self.col['FuelD'] = self.col['diesel_gr'] + self.col['diesel_idl'] + self.col['diesel_col'] + self.col['diesel_rf'] + self.col['diesel_ud'] + self.col['diesel_fg']
### Daily fuel usage - CNG - diesel gal equivalent
        for i in ['RWC','SSR','DSR','MSR','LV','SSYW','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            if self.col.loc[i,'MPG_all_CNG'] != 0:
                #from garage to first collection route (gallons/day-vehicle)
                self.col.loc[i,'CNG_gr'] = self.col['Fract_CNG'][i] * self.col['Dgr'][i] /self.col['MPG_all_CNG'][i]
                #break time, if spent idling
                self.col.loc[i,'CNG_idl'] = 0
                #from first through last collection stop (diesel gal equivalent/day-vehicle)
                self.col.loc[i,'CNG_col'] = self.col['Fract_CNG'][i] * self.col['Dbtw'][i] * self.col['SD'][i] /self.col['MPG_all_CNG'][i]
                #between disposal facility and route (diesel gal equivalent/day-vehicle)
                self.col.loc[i,'CNG_rf'] = self.col['Fract_CNG'][i] * self.col['F_R'][i]/60 * self.col['Vrf'][i]  /self.col['MPG_all_CNG'][i]
                #unloading at disposal facility (diesel gal equivalent/day-vehicle)
                self.col.loc[i,'CNG_ud'] = 0
                #from disposal facility to garage (diesel gal equivalent/day-vehicle)
                self.col.loc[i,'CNG_fg'] = self.col['Fract_CNG'][i] * self.col['Dfg'][i] /self.col['MPG_all_CNG'][i]
            else:
                self.col.loc[i,'CNG_gr'] = self.col['Fract_CNG'][i] * self.col['Dgr'][i]*((1-self.col['fDgr'][i])/self.col['MPG_urban_CNG'][i]+self.col['fDgr'][i]/self.col['MPG_hwy_CNG'][i])
                self.col.loc[i,'CNG_idl'] = self.col['Fract_CNG'][i] * (self.col['F1_'][i]*self.col['F1_idle'][i] + self.col['F2_'][i]*self.col['F2_idle'][i])/60 * self.col['GPH_idle_CNG'][i]
                self.col.loc[i,'CNG_col'] = self.col['Fract_CNG'][i] * self.col['Dbtw'][i] * self.col['SD'][i] /self.col['MPG_col_CNG'][i]
                self.col.loc[i,'CNG_rf'] = self.col['Fract_CNG'][i] * self.col['F_R'][i]/60 * self.col['Vrf'][i]  *((1-self.col['fDrd'][i])/self.col['MPG_urban_CNG'][i] + self.col['fDrd'][i]/self.col['MPG_hwy_CNG'][i])
                self.col.loc[i,'CNG_ud'] = self.col['Fract_CNG'][i] * self.col['UD'][i] /60 * self.col['GPH_idle_CNG'][i]
                self.col.loc[i,'CNG_fg'] = self.col['Fract_CNG'][i] * self.col['Dfg'][i] *((1-self.col['fDfg'][i])/self.col['MPG_urban_CNG'][i] + self.col['fDfg'][i]/self.col['MPG_hwy_CNG'][i])

        self.col['FuelD_CNG'] = self.col['CNG_gr'] + self.col['CNG_idl'] + self.col['CNG_col'] + self.col['CNG_rf'] + self.col['CNG_ud'] + self.col['CNG_fg']


###ENERGY CONSUMPTION
###Energy consumption by collection vehicles
        #total coll. vehicle fuel use per Mg of refuse (L/Mg)
        self.col['FuelMg'] = self.col[['FuelD','RefD']].apply(lambda x: 0 if x[1]==0 else x[0] *3.785 /x[1] , axis = 1)

        #total coll. vehicle CNG fuel use per Mg of refuse (diesel L equivalent/Mg)
        self.col['FuelMg_CNG'] = self.col[['FuelD_CNG','RefD']].apply(lambda x: 0 if x[1]==0 else x[0] *3.785 /x[1] , axis = 1)
        
###Energy consumption by drop-off vehicles
        for i in ['MRDO','SSYWDO','MSRDO']:
            #fuel usage per trip to drop-off site (gallons/trip)
            self.col.loc[i,'FuelT'] = self.P_use[i]*self.col['RTDdos'][i]*self.col['DED'][i]/self.col['dropoff_MPG'][i]
            
            #weight of refuse delivered per trip (kg/trip)
            self.col.loc[i,'RefT'] = sum(self.mass[i]) * self.col['Prtcp'][i] * 52 / (self.col['FREQdos'][i]*12)
            
            #total dropoff vehicle  fuel use per Mg of refuse (L/Mg)
            self.col.loc[i,'FuelMg_dov'] = 0 if self.col.loc[i,'RefT'] == 0 else self.col.loc[i,'FuelT'] * 3.785 / (self.col.loc[i,'RefT']/1000)
        
###Energy consumption by garage
        for i in ['RWC','SSR','DSR','MSR','MSRDO','LV','SSYW','SSYWDO','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            #daily electricity usage per vehicle  (kWh/vehicle-day)
            self.col.loc[i,'ElecD'] = self.P_use[i]*(self.col['grg_area'][i]*self.col['grg_enrg'][i]+self.col['off_area'][i]*self.col['off_enrg'][i])
        #electricity usage per Mg of refuse  (kWh/Mg)
        self.col['ElecMg'] = self.col[['ElecD','RefD']].apply(lambda x: 0 if x[1]==0 else x[0]/x[1] , axis = 1)
        
###Mass
        for i in ['RWC','SSR','DSR','MSR','MSRDO','LV','SSYW','SSYWDO','SSO','DryRes','REC','WetRes','MRDO','SSYWDO','MSRDO']:
            #total mass of refuse collected per year (Mg) 
            self.col.loc[i,'TotalMass'] =sum(self.col_massflow[i])

# =============================================================================
# =============================================================================
###      OUTPUT
# =============================================================================
# =============================================================================
        self.output = self.col[['TotalMass','FuelMg','FuelMg_CNG','ElecMg','FuelMg_dov']]
        self.output = self.output.fillna(0)
            

    def calc(self):
        self.calc_composition()
        self.calc_destin()
            
        
### setup for Monte Carlo simulation   
    def setup_MC(self,seed=None):
        self.Input.setup_MC(seed)

### Calculate based on the generated numbers   
    def MC_calc(self):      
        input_list = self.Input.gen_MC()
        self.calc()
        return(input_list)        


    def report(self):
### Output
        self.collection = {}
        Waste={}
        Technosphere={}
        Biosphere={}
        self.collection["process name"] = 'col' if not self.name else self.name
        self.collection["Waste"] = Waste
        self.collection["Technosphere"] = Technosphere
        self.collection["Biosphere"] = Biosphere
        self.collection['LCI'] = self.result_destination
        
        for x in [Waste,Technosphere, Biosphere]:
            for y in self.Index:
                x[y]={}
        
        for y in self.Index: 
            for x in self.col_massflow.columns:
                Waste[y][x]= self.col_massflow[x][y]
        return(self.collection)
         



Distance = {'Res':{'LF':20},
            'Rec':{'LF':20},
            'Organics':{'AD':20,'COMP':20}}


Collection_scheme = {'RWC':{'Contribution':0.2 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},
                    'SSO_DryRes':{'Contribution':0.2 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},
                    'REC_WetRes':{'Contribution':0 , 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}},                
                    'MRDO':{'Contribution':0.6, 
                            'separate_col':{'SSR':0,
                                            'DSR':0,
                                            'MSR':0,
                                            'MSRDO':0,
                                            'SSYW':0,
                                            'SSYWDO':0}}}


# =============================================================================
# Treatment_processes = {}
# Treatment_processes['AD']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':20},'model': AD()}
# Treatment_processes['COMP']={'input_type':['LV','SSYW','SSO','SSYWDO','Separated_Organics'],'distance':{'SF1':100}, 'model': Comp()}
# Treatment_processes['LF']={'input_type':['RWC','LV','DryRes','WetRes','MRDO','MSRDO','Bottom_Ash','Fly_Ash','Other_Residual'],'distance':{'SF1':20},'model': LF() }
# 
# 
# A= SF_Col(Collection_scheme,Distance,Treatment_processes=Treatment_processes,name='SF1')
# A.calc()
# AAA= A.col_massflow
# AAAA= A.output
# AAAAA=A.report()
# =============================================================================

# =============================================================================
# from time import time    
# A= SF_Col(Collection_scheme,Distance)
# B= time()
# for i in range(1000):
#     A.calc_composition()
#     A.
# print(time()-B)
# =============================================================================
