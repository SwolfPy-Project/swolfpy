# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:41:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd

### Flow
class flow:
    def __init__(self,Material_Properties):
        self.prop = Material_Properties
        self.Index = ['Yard_Trimmings_Leaves', 'Yard_Trimmings_Grass', 'Yard_Trimmings_Branches', 'Food_Waste_Vegetable', 'Food_Waste_Non_Vegetable',
              'Wood', 'Wood_Other', 'Textiles', 'Rubber_Leather', 'Newsprint', 'Corr_Cardboard', 'Office_Paper', 'Magazines', 'third_Class_Mail',
              'Folding_Containers', 'Paper_Bags', 'Mixed_Paper', 'Paper_Non_recyclable', 'HDPE_Translucent_Containers', 'HDPE_Pigmented_Containers', 'PET_Containers',
              'Plastic_Other_1_Polypropylene', 'Plastic_Other_2', 'Mixed_Plastic', 'Plastic_Film', 'Plastic_Non_Recyclable', 'Ferrous_Cans', 'Ferrous_Metal_Other',
              'Aluminum_Cans', 'Aluminum_Foil', 'Aluminum_Other', 'Ferrous_Non_recyclable', 'Al_Non_recyclable', 'Glass_Brown', 'Glass_Green',
              'Glass_Clear', 'Mixed_Glass', 'Glass_Non_recyclable', 'Misc_Organic', 'Misc_Inorganic', 'E_waste', 'Aerobic_Residual',
              'Anaerobic_Residual', 'Bottom_Ash', 'Fly_Ash', 'Diapers_and_sanitary_products', 'Waste_Fraction_47', 'Waste_Fraction_48',
              'Waste_Fraction_49', 'Waste_Fraction_50', 'Waste_Fraction_51', 'Waste_Fraction_52', 'Waste_Fraction_53', 'Waste_Fraction_54',
              'Waste_Fraction_55', 'Waste_Fraction_56', 'Waste_Fraction_57', 'Waste_Fraction_58', 'Waste_Fraction_59', 'Waste_Fraction_60']
        self.data = pd.DataFrame(index = self.Index,columns=['mass','sol_cont','moist_cont','vs_cont','ash_cont'])
### Update flow        
    def update(self,assumed_comp): 
        self.flow = sum(self.data['mass']*assumed_comp)
        self.water = sum(self.data['moist_cont']*assumed_comp)
        self.moist_cont = self.water / self.flow
        self.ash = sum(self.data['ash_cont']*assumed_comp)
        self.solid = sum(self.data['sol_cont']*assumed_comp)

### Create new flow
    def init_flow(self,massflows):
        self.data['mass']= massflows
        self.data['sol_cont'] = self.data['mass'] * (1-self.prop['Moisture Content']/100)
        self.data['moist_cont'] = self.data['mass'] * (self.prop['Moisture Content']/100)
        self.data['vs_cont'] = self.data['sol_cont'] * self.prop['Volatile Solids']/100
        self.data['ash_cont'] = self.data['sol_cont'] * self.prop['Ash Content']/100
    
###
def add_LCI(Name,Flow,LCI):
    if Name in LCI.columns:
        LCI[Name] += Flow
    else:
        LCI[Name] = Flow
            

### Screan
def screen(input,sep_eff, Material_Properties,Op_param,LCI):
    product = flow(Material_Properties)
    residual = flow(Material_Properties)
    
    residual.data['mass']=input.data['mass'] * sep_eff
    residual.data['sol_cont'] = input.data['sol_cont'] * sep_eff
    residual.data['moist_cont'] = input.data['moist_cont'] * sep_eff
    residual.data['vs_cont'] = input.data['vs_cont'] * sep_eff
    residual.data['ash_cont'] = input.data['ash_cont'] * sep_eff
    
    product.data['mass']=input.data['mass'] - residual.data['mass']
    product.data['sol_cont'] = input.data['sol_cont'] - residual.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] - residual.data['moist_cont']
    product.data['vs_cont'] = input.data['vs_cont'] - residual.data['vs_cont']
    product.data['ash_cont'] = input.data['ash_cont'] - residual.data['ash_cont']
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['Mtr']['amount'] * input.data['mass']/1000  ,LCI) 

    return(product,residual)

### Shredding
def shredding(input,Material_Properties,Op_param,LCI):
    product = flow(Material_Properties)
    product.data = input.data * 1

    #Resource use    
    Shred_diesel = input.data['mass'] / 1000 * Op_param['Mtgp']['amount'] * Op_param['Mtgf']['amount']                                   
    add_LCI(('Technosphere', 'Equipment_Diesel'),Shred_diesel,LCI) 
    
    return(product)

### Mixing two flows
def mix(input1,input2,Material_Properties):
    product = flow(Material_Properties)
    product.data['mass']=input1.data['mass'] + input2.data['mass']
    product.data['sol_cont'] = input1.data['sol_cont'] + input2.data['sol_cont']
    product.data['moist_cont'] = input1.data['moist_cont'] + input2.data['moist_cont']
    product.data['vs_cont'] = input1.data['vs_cont'] + input2.data['vs_cont']
    product.data['ash_cont'] = input1.data['ash_cont'] + input2.data['ash_cont']
    return(product)

### Add Water    
def add_water(input,water_flow,Material_Properties,process_data):
    product = flow(Material_Properties)
    product.data['mass']=input.data['mass'] + water_flow
    product.data['sol_cont'] = input.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] + water_flow
    product.data['vs_cont'] = input.data['vs_cont'] 
    product.data['ash_cont'] = input.data['ash_cont']
    #Nitrogen and carbon in the input stream
    product.data['C_input'] = product.data['sol_cont'] *  Material_Properties['Biogenic Carbon Content']/100 * process_data['Degrades']
    product.data['N_input'] = product.data['sol_cont'] *  Material_Properties['Nitrogen Content']/100 * process_data['Degrades']
    return(product)

    
### Active Composting
def ac_comp(input,CommonData,process_data,Comp_input,Degradation_Parameters,Biological_Degredation,assumed_comp,Material_Properties,LCI):
    #Degradation
    C_loss = input.data['C_input'] * process_data['Percent C-loss during composting']/100 * Degradation_Parameters['acDegProp']['amount']/100
    N_loss = input.data['N_input'] * process_data['Percent N-loss during composting']/100 * Degradation_Parameters['acDegProp']['amount']/100
    VS_loss = C_loss * process_data['Mass VS loss per mass C-loss']
    VOCs_loss = VS_loss * process_data['VOC emissions'] / 1000000
    
    #Product
    product = flow(Material_Properties)
    product.data['vs_cont'] = input.data['vs_cont'] - VS_loss
    product.data['ash_cont'] = input.data['ash_cont']
    product.data['sol_cont'] = product.data['vs_cont'] + product.data['ash_cont']
    product.data['C_cont']= input.data['C_input'] - C_loss
    product.data['N_cont']= input.data['N_input'] - N_loss
    
    #Off Gas
    C_loss_as_CH4 = C_loss * Biological_Degredation['pCasCH4']['amount'] 
    C_loss_as_CO2 = C_loss - C_loss_as_CH4
    add_LCI('Carbon dioxide, non-fossil', C_loss_as_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    N_loss_as_NH3 = N_loss * Biological_Degredation['pNasNH3']['amount'] 
    N_loss_as_N2O = N_loss * Biological_Degredation['pNasN2O']['amount'] 
    
    #Biofilter
    Biofilter_CH4 = C_loss_as_CH4 * (1-Biological_Degredation['bfCH4re']['amount'])
    Biofilter_CO2 = C_loss_as_CH4-Biofilter_CH4
    add_LCI('Methane, non-fossil',Biofilter_CH4 * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
    add_LCI('Carbon dioxide, non-fossil', Biofilter_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    Biofilter_NH3= N_loss_as_NH3 * (1-Biological_Degredation['bfNH3re']['amount']/100)
    Biofilter_N2O= N_loss_as_N2O * (1-Biological_Degredation['bfN2Ore']['amount']/100)
    Biofilter_NH3_to_N2O= (N_loss_as_NH3-Biofilter_NH3) * Biological_Degredation['preNH3toN2O']['amount'] 
    Biofilter_NH3_to_NOx= (N_loss_as_NH3-Biofilter_NH3) * Biological_Degredation['preNH3toNOx']['amount']
    Biofilter_VOCs = VOCs_loss  * (1-Biological_Degredation['bfVOCre']['amount']/100)
    
    add_LCI('Ammonia',Biofilter_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
    add_LCI('Dinitrogen monoxide',(Biofilter_N2O+Biofilter_NH3_to_N2O) * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
    add_LCI('Nitrogen oxides',Biofilter_NH3_to_NOx * CommonData.MW['NOx']['amount']/CommonData.MW['N']['amount'] ,LCI)
    add_LCI('VOCs emitted',Biofilter_VOCs ,LCI)
    
    # Caculating the moisture
    input.update(assumed_comp)
    water_after_ac = sum(product.data['sol_cont'] * assumed_comp) * Degradation_Parameters['MCac']['amount'] / (1-Degradation_Parameters['MCac']['amount'])
    product.data['moist_cont'] = water_after_ac * input.data['moist_cont']/input.water
    product.data['mass']= product.data['sol_cont'] + product.data['moist_cont']
    
    #Resource use
    Loader_diesel = Comp_input.Op_Param['Tdoh']['amount']*Comp_input.Loader['hpfel']['amount']*Comp_input.Loader['Mffel']['amount']
    Windrow_turner_diesel = Comp_input.Op_Param['Tact']['amount']*Comp_input.AC_Turning['Fta']['amount']* input.data['mass']/1000 * \
                                Comp_input.AC_Turning['Mwta']['amount'] * Comp_input.AC_Turning['Mwfa']['amount']                                     
    add_LCI(('Technosphere', 'Equipment_Diesel'), Windrow_turner_diesel+Loader_diesel ,LCI) 
    
    return(product)

### Post Screen
def post_screen(input,sep_eff, Material_Properties,Op_param,LCI):
    product = flow(Material_Properties)
    residual = flow(Material_Properties)
    
    residual.data['mass']=input.data['mass'] * sep_eff
    residual.data['sol_cont'] = input.data['sol_cont'] * sep_eff
    residual.data['moist_cont'] = input.data['moist_cont'] * sep_eff
    residual.data['vs_cont'] = input.data['vs_cont'] * sep_eff
    residual.data['ash_cont'] = input.data['ash_cont'] * sep_eff
    residual.data['C_cont'] = input.data['C_cont'] * sep_eff
    residual.data['N_cont'] = input.data['N_cont'] * sep_eff
    
    product.data['mass']=input.data['mass'] - residual.data['mass']
    product.data['sol_cont'] = input.data['sol_cont'] - residual.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] - residual.data['moist_cont']
    product.data['vs_cont'] = input.data['vs_cont'] - residual.data['vs_cont']
    product.data['ash_cont'] = input.data['ash_cont'] - residual.data['ash_cont']
    product.data['C_cont'] = input.data['C_cont'] - residual.data['C_cont']
    product.data['N_cont'] = input.data['N_cont'] - residual.data['N_cont']
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['Mtr']['amount'] * input.data['mass']/1000  ,LCI) 
    
    return(product,residual)
    

### Vaccuum
def vacuum(input,sep_eff, Material_Properties,Op_param,LCI):
    product = flow(Material_Properties)
    vacuumed = flow(Material_Properties)
    
    vacuumed.data['mass']=input.data['mass'] * sep_eff
    vacuumed.data['sol_cont'] = input.data['sol_cont'] * sep_eff
    vacuumed.data['moist_cont'] = input.data['moist_cont'] * sep_eff
    vacuumed.data['vs_cont'] = input.data['vs_cont'] * sep_eff
    vacuumed.data['ash_cont'] = input.data['ash_cont'] * sep_eff
    vacuumed.data['C_cont'] = input.data['C_cont'] * sep_eff   
    vacuumed.data['N_cont'] = input.data['N_cont'] * sep_eff        
    
    product.data['mass']=input.data['mass'] - vacuumed.data['mass']
    product.data['sol_cont'] = input.data['sol_cont'] - vacuumed.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] - vacuumed.data['moist_cont']
    product.data['vs_cont'] = input.data['vs_cont'] - vacuumed.data['vs_cont']
    product.data['ash_cont'] = input.data['ash_cont'] - vacuumed.data['ash_cont']
    product.data['C_cont'] = input.data['C_cont'] - vacuumed.data['C_cont']
    product.data['N_cont'] = input.data['N_cont'] - vacuumed.data['N_cont']
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['vacElecFac']['amount'] * input.data['mass']/1000  ,LCI)                                 
    add_LCI(('Technosphere', 'Equipment_Diesel'),Op_param['vacDiesFac']['amount'] * input.data['mass']/1000 ,LCI) 
    
    return(product,vacuumed)
        
### Curing
def curing(input,CommonData,process_data,Comp_input,Degradation_Parameters,Biological_Degredation,assumed_comp,Material_Properties,LCI):
    #Degradation
    C_loss = input.data['C_cont'] * process_data['Percent C-loss during composting']/100 * (100-Degradation_Parameters['acDegProp']['amount'])/100
    N_loss = input.data['N_cont'] * process_data['Percent N-loss during composting']/100 * (100-Degradation_Parameters['acDegProp']['amount'])/100
    VS_loss = C_loss * process_data['Mass VS loss per mass C-loss']
    VOCs_loss = VS_loss * process_data['VOC emissions'] / 1000000
    
    #Product
    product = flow(Material_Properties)
    product.data['vs_cont'] = input.data['vs_cont'] - VS_loss
    product.data['ash_cont'] = input.data['ash_cont']
    product.data['sol_cont'] = product.data['vs_cont'] + product.data['ash_cont']
    product.data['C_cont']= input.data['C_cont'] - C_loss
    product.data['N_cont']= input.data['N_cont'] - N_loss
    
    #Off Gas
    C_loss_as_CH4 = C_loss * Biological_Degredation['pCasCH4']['amount'] 
    C_loss_as_CO2 = C_loss - C_loss_as_CH4
    add_LCI('Carbon dioxide, non-fossil', C_loss_as_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    N_loss_as_NH3 = N_loss * Biological_Degredation['pNasNH3']['amount'] 
    N_loss_as_N2O = N_loss * Biological_Degredation['pNasN2O']['amount']     
    
    #Biofilter
    Biofilter_CH4 = C_loss_as_CH4 * (1-Biological_Degredation['bfCH4re']['amount'])
    Biofilter_CO2 = C_loss_as_CH4-Biofilter_CH4
    add_LCI('Methane, non-fossil',Biofilter_CH4 * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
    add_LCI('Carbon dioxide, non-fossil', Biofilter_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    Biofilter_NH3= N_loss_as_NH3 * (1-Biological_Degredation['bfNH3re']['amount']/100)
    Biofilter_N2O= N_loss_as_N2O * (1-Biological_Degredation['bfN2Ore']['amount']/100)
    Biofilter_NH3_to_N2O= (N_loss_as_NH3-Biofilter_NH3) * Biological_Degredation['preNH3toN2O']['amount'] 
    Biofilter_NH3_to_NOx= (N_loss_as_NH3-Biofilter_NH3) * Biological_Degredation['preNH3toNOx']['amount']
    Biofilter_VOCs = VOCs_loss  * (1-Biological_Degredation['bfVOCre']['amount']/100)
    
    add_LCI('Ammonia',Biofilter_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
    add_LCI('Dinitrogen monoxide',(Biofilter_N2O+Biofilter_NH3_to_N2O) * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
    add_LCI('Nitrogen oxides',Biofilter_NH3_to_NOx * CommonData.MW['NOx']['amount']/CommonData.MW['N']['amount'] ,LCI)
    add_LCI('VOCs emitted',Biofilter_VOCs ,LCI)

    # Caculating the moisture
    input.update(assumed_comp)
    water_after_cu = sum(product.data['sol_cont'] * assumed_comp) * Degradation_Parameters['MCcu']['amount'] / (1-Degradation_Parameters['MCcu']['amount'])
    product.data['moist_cont'] = water_after_cu * input.data['moist_cont']/input.water
    product.data['mass']= product.data['sol_cont'] + product.data['moist_cont']
    
    #Resource use
    Curing_diesel = Comp_input.Op_Param['Tcur']['amount']*Comp_input.Curing['Ftc']['amount']*Comp_input.AC_Turning['Mwta']['amount']*\
                    Comp_input.AC_Turning['Mwfa']['amount']*input.data['mass']/1000                                  
    add_LCI(('Technosphere', 'Equipment_Diesel'),Curing_diesel ,LCI) 
    
    return(product)

### Apply compost to Land
def compost_use(input,CommonData,process_data,Material_Properties,Biological_Degredation,Land_app,Fertilizer_offsest,LCI):
    if Fertilizer_offsest['choice_BU']['amount'] == 1:
        # Carbon in final compost
        C_storage = input.data['C_cont'] * Biological_Degredation['percCStor']['amount']/100
        C_released = input.data['C_cont'] - C_storage
        C_storage_hummus_formation = input.data['C_cont'] * Biological_Degredation['humFormFac']['amount']
        add_LCI('Carbon dioxide, non-fossil', C_released * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil storage', -(C_storage+C_storage_hummus_formation) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        
        #Nitrogen in final compost
        N2O = input.data['N_cont'] * Land_app['perN2Oevap']['amount']/100 
        NH3 = input.data['N_cont'] * Land_app['perNasNH3fc']['amount']/100 * Land_app['perNH3evap']['amount']/100
        NO3_GW = input.data['N_cont'] * CommonData.Land_app['NO3leach']['amount'] 
        FNO3_SW = input.data['N_cont'] * CommonData.Land_app['NO3runoff']['amount'] 
        
        add_LCI('Dinitrogen monoxide', N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
        add_LCI('Ammonia',NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (ground water)',NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (Surface water)',FNO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        
        if Fertilizer_offsest['fertOff']['amount'] == 1:
            # Nutrients availble in the final compost
            Navail = input.data['N_cont'] * CommonData.Land_app['MFEN']['amount'] * process_data['Degrades']
            Pavail = input.data['P_cont'] * CommonData.Land_app['MFEP']['amount'] * process_data['Degrades']
            Kavail = input.data['K_cont'] * CommonData.Land_app['MFEK']['amount'] * process_data['Degrades']
            
            # Diesel use for applying the compost
            Diesel_use = input.data['mass'] /1000 * CommonData.Land_app['cmpLandDies']['amount']
            add_LCI(('Technosphere', 'Equipment_Diesel'), Diesel_use ,LCI)
            
            # Offset from fertilizer
            Diesel_offset = -(Navail*CommonData.Land_app['DslAppN']['amount']+Pavail*CommonData.Land_app['DslAppP']['amount']+Kavail*CommonData.Land_app['DslAppK']['amount'])
            add_LCI(('Technosphere', 'Equipment_Diesel'), Diesel_offset ,LCI)
            add_LCI(('Technosphere', 'Nitrogen_Fertilizer'), -Navail ,LCI)
            add_LCI(('Technosphere', 'Phosphorous_Fertilizer'), -Pavail ,LCI)
            add_LCI(('Technosphere', 'Potassium_Fertilizer'), -Kavail ,LCI)
            
            # offset from applying fertilizer
            Fert_N2O = -Navail * CommonData.Land_app['fert_N2O']['amount']/100 
            Fert_NH3 = -Navail * CommonData.Land_app['fert_NH3']['amount']/100 * CommonData.Land_app['fert_NH3Evap']['amount']/100
            Fert_NO3_GW = -Navail * CommonData.Land_app['fert_NO3Leach']['amount'] /100
            Fert_NO3_SW = -Navail * CommonData.Land_app['fert_NO3Run']['amount'] / 100
            
            add_LCI('Dinitrogen monoxide', Fert_N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
            add_LCI('Ammonia',Fert_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Nitrate (ground water)',Fert_NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Nitrate (Surface water)',Fert_NO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        if Fertilizer_offsest['peatOff']['amount'] == 1:
            add_LCI(('Technosphere', 'Peat'), -input.data['mass']/1000,LCI)  
    
    if Fertilizer_offsest['choice_BU']['amount'] == 0:
        # Carbon in final compost
        Max_C_storage = (1-Material_Properties['Moisture Content']/100) * Material_Properties['Carbon Storage Factor']
        C_storage = np.where( input.data['C_cont'] * Biological_Degredation['percCStor_LF']['amount']/100 <= Max_C_storage,
                             input.data['C_cont'] * Biological_Degredation['percCStor_LF']['amount']/100,Max_C_storage)
        
        C_released = (input.data['C_cont'] - C_storage)/2
        C_CH4 = (input.data['C_cont'] - C_storage)/2
        C_CH4_Oxidized = C_CH4 * process_data['Percent of Generated Methane oxidized']/100
        C_CH4_Flared = C_CH4 * process_data['Percent of Generated Methane Flared']/100
        C_CH4_Emitted = C_CH4 * process_data['Percent of Generated Methane Emitted']/100
        C_CH4_EnergyRec = C_CH4 * process_data['Percent of Generated Methane used for Energy']/100
        C_CH4_Electricity = C_CH4_EnergyRec*CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount']*50/3.6  # LHV of Methane: 50 MJ/kg
                
        add_LCI('Carbon dioxide, non-fossil storage', -(C_storage) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil', (C_released+C_CH4_EnergyRec+C_CH4_Flared+C_CH4_Oxidized) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Methane, non-fossil', C_CH4_Emitted * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI(('Technosphere', 'Electricity_consumption'), -C_CH4_Electricity ,LCI)
        
        #General emissions from LF
        add_LCI(('Technosphere', 'compost_to_LF'), input.data['mass'] /1000 ,LCI)
        
        #Amomonium emission from LF (Calculated base on the ammomium/N_cont ratio in LF)
        NH4_GW= 0.0051/100 * input.data['N_cont']
        NH4_SW= 0.3597/100 * input.data['N_cont']
        add_LCI('Ammonium, ion (ground water)', NH4_GW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Ammonium, ion (surface water)', NH4_SW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)

### AD_Screan
def AD_screen(input,sep_eff, Material_Properties,LCI):
    product = flow(Material_Properties)
    residual = flow(Material_Properties)
    
    residual.data['mass']=input.data['mass'] * sep_eff
    residual.data['sol_cont'] = input.data['sol_cont'] * sep_eff
    residual.data['moist_cont'] = input.data['moist_cont'] * sep_eff
    residual.data['vs_cont'] = input.data['vs_cont'] * sep_eff
    residual.data['ash_cont'] = input.data['ash_cont'] * sep_eff
    
    product.data['mass']=input.data['mass'] - residual.data['mass']
    product.data['sol_cont'] = input.data['sol_cont'] - residual.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] - residual.data['moist_cont']
    product.data['vs_cont'] = input.data['vs_cont'] - residual.data['vs_cont']
    product.data['ash_cont'] = input.data['ash_cont'] - residual.data['ash_cont']

    return(product,residual)



### AD_Add Water    
def add_water_AD(input,water_flow,Material_Properties):
    product = flow(Material_Properties)
    product.data['mass']=input.data['mass'] + water_flow
    product.data['sol_cont'] = input.data['sol_cont']
    product.data['moist_cont'] = input.data['moist_cont'] + water_flow
    product.data['vs_cont'] = input.data['vs_cont'] 
    product.data['ash_cont'] = input.data['ash_cont']
    #Nitrogen and carbon in the input stream
    product.data['C_cont'] = product.data['sol_cont'] *  Material_Properties['Biogenic Carbon Content']/100
    product.data['N_cont'] = product.data['sol_cont'] *  Material_Properties['Nitrogen Content']/100
    product.data['P_cont'] = product.data['sol_cont'] *  Material_Properties['Phosphorus Content']/100
    product.data['K_cont'] = product.data['sol_cont'] *  Material_Properties['Potassium Content']/100
    return(product)

### AD Reactor
def Reactor(input,CommonData,process_data,AD_input,Material_Properties,EmissionFactor,LCI):
    #Methane production
    CH4_prod_vol = input.data['sol_cont'] / 1000 * Material_Properties['Methane Yield'] * process_data['Percent of L0 reached']/100
    CH4_prod_mass_asC = CH4_prod_vol * CommonData.STP['m3CH4_to_kg']['amount']*CommonData.MW['C']['amount']/CommonData.MW['CH4']['amount']
    
    #Mehtane Balance
    CH4_fugitiv_mass_asC = CH4_prod_mass_asC * (1-AD_input.Biogas_gen['ad_collEff']['amount'])
    CH4_Energy_rec_asC = CH4_prod_mass_asC * AD_input.Biogas_gen['ad_collEff']['amount'] * (1-AD_input.Biogas_gen['ad_downTime']['amount'])
    CH4_Flare_asC = CH4_prod_mass_asC * AD_input.Biogas_gen['ad_collEff']['amount'] * AD_input.Biogas_gen['ad_downTime']['amount']
    CH4_unburn_AsC = CH4_Energy_rec_asC * (1-EmissionFactor['Engine']['CH4_destruction']['amount']) + CH4_Flare_asC* (1-EmissionFactor['Flare']['CH4_destruction']['amount'])
    CO2_from_CH4Comb = CH4_Energy_rec_asC * EmissionFactor['Engine']['CH4_destruction']['amount'] + CH4_Flare_asC* EmissionFactor['Flare']['CH4_destruction']['amount']
    
    #ENergy content
    CH4_Energy_EngCont = CH4_prod_vol * AD_input.Biogas_gen['ad_collEff']['amount'] * (1-AD_input.Biogas_gen['ad_downTime']['amount']) * AD_input.Biogas_gen['ad_ch4EngCont']['amount']
    CH4_Flare_EngCont = CH4_prod_vol * AD_input.Biogas_gen['ad_collEff']['amount'] * AD_input.Biogas_gen['ad_downTime']['amount'] * AD_input.Biogas_gen['ad_ch4EngCont']['amount']
    
    #Calculate emissions based on the energy content
    CO_Comb = (CH4_Energy_EngCont * EmissionFactor['Engine']['CO']['amount'] + CH4_Flare_EngCont * EmissionFactor['Flare']['CO']['amount'])/1000000
    NOx_Comb = (CH4_Energy_EngCont * EmissionFactor['Engine']['NO2']['amount'] + CH4_Flare_EngCont * EmissionFactor['Flare']['NO2']['amount'])/1000000
    SO2_Comb = (CH4_Energy_EngCont * EmissionFactor['Engine']['SO2']['amount'] + CH4_Flare_EngCont * EmissionFactor['Flare']['SO2']['amount'])/1000000
    NMVOCs_Comb = (CH4_Energy_EngCont * EmissionFactor['Engine']['NMVOC']['amount'] + CH4_Flare_EngCont * EmissionFactor['Flare']['NMVOC']['amount'])/1000000
    PM2_5_Comb = (CH4_Energy_EngCont * EmissionFactor['Engine']['PM']['amount'] + CH4_Flare_EngCont * EmissionFactor['Flare']['PM']['amount'])/1000000
    
    add_LCI('Fugitive (Leaked) Methane', CH4_fugitiv_mass_asC * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
    add_LCI('Carbon dioxide, non-fossil from comubstion', CO2_from_CH4Comb * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    add_LCI('Methane, non-fossil (unburned)', CH4_unburn_AsC * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    add_LCI('Carbon monoxide (CO)', CO_Comb ,LCI)
    add_LCI('Nitrogen oxides (as NO2)', NOx_Comb ,LCI)
    add_LCI('Sulfur dioxide (SO2)', SO2_Comb ,LCI)
    add_LCI('NMVOCs', NMVOCs_Comb ,LCI)
    add_LCI('PM2.5', PM2_5_Comb ,LCI)
    
    #Biogas production
    BioGas_vol = CH4_prod_vol / AD_input.Biogas_gen['ad_ch4stoich']['amount']
    BioGas_mass = CH4_prod_vol * CommonData.STP['m3CH4_to_kg']['amount'] + (BioGas_vol-CH4_prod_vol) * CommonData.STP['m3CO2_to_kg']['amount']
    
    #Electricity production
    Elec_prod =  CH4_Energy_EngCont / AD_input.Biogas_gen['ad_HeatRate']['amount']
    add_LCI('Electricity Production', Elec_prod ,LCI)
    
    #CO2 production
    CO2_prod_mass_asC = (BioGas_vol-CH4_prod_vol) * CommonData.STP['m3CO2_to_kg']['amount'] * CommonData.MW['C']['amount']/CommonData.MW['CO2']['amount']
    add_LCI('Carbon dioxide, non-fossil (in biogas)', CO2_prod_mass_asC * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    #Water and Volatile solid in Biogas
    BioGas_VS = BioGas_mass * AD_input.Biogas_gen['perSolDec']['amount'] /100
    BioGas_Water = BioGas_mass - BioGas_VS
    
    #Product
    product = flow(Material_Properties)
    product.data['vs_cont'] = input.data['vs_cont'] - BioGas_VS
    product.data['ash_cont'] = input.data['ash_cont']
    product.data['sol_cont'] = product.data['vs_cont'] + product.data['ash_cont']
    product.data['moist_cont'] = input.data['moist_cont'] - BioGas_Water
    product.data['mass'] = product.data['moist_cont'] + product.data['sol_cont']
    product.data['C_cont']= input.data['C_cont'] - CO2_prod_mass_asC - CH4_prod_mass_asC
    product.data['N_cont']= input.data['N_cont']
    product.data['P_cont']= input.data['P_cont']
    product.data['K_cont']= input.data['K_cont']
    
    return(product)
    
### AD Dewater
def Dewater(input,CommonData,process_data,AD_input,Material_Properties,added_water,assumed_comp,LCI):
    if AD_input.AD_operation['isDw']['amount']==1:
        # Calculating water removed
        liq_rem = (input.data['moist_cont'] - AD_input.Dewater['ad_mcDigestate']['amount'] * input.data['mass'])/(1-AD_input.Dewater['ad_mcDigestate']['amount'])
        
        # Maximum water recirculate
        Recirculate_water_max = sum(added_water * assumed_comp) * AD_input.AD_operation['recircMax']['amount']
        
        #Liquid to reatment, new water, recirculate watersum(liq_rem * assumed_co
        total_liq_to_treatment = max(sum(liq_rem*assumed_comp) - Recirculate_water_max , 0 )
        liq_treatment_mass = total_liq_to_treatment * liq_rem / sum(liq_rem * assumed_comp)
        liq_treatment_vol = liq_treatment_mass/1000 /AD_input.Dig_prop['digliqdens']['amount']
        Recirulate_water_mass= (sum(liq_rem * assumed_comp) - total_liq_to_treatment) * liq_rem / sum(liq_rem * assumed_comp)
        New_water_mass= (sum(added_water * assumed_comp) - (sum(liq_rem * assumed_comp) - total_liq_to_treatment)) * liq_rem / sum(liq_rem * assumed_comp)
        
        #Product
        product = flow(Material_Properties)
        product.data['vs_cont'] = input.data['vs_cont']
        product.data['ash_cont'] = input.data['ash_cont']
        product.data['sol_cont'] = input.data['sol_cont']
        product.data['moist_cont'] = input.data['moist_cont'] - liq_rem
        product.data['mass'] = product.data['moist_cont'] + product.data['sol_cont']
        product.data['C_cont']= input.data['C_cont']
        product.data['N_cont'] =  input.data['N_cont'] * (1-liq_rem/input.data['moist_cont'] * (100-AD_input.Dig_prop['perNSolid']['amount'])/100 )
        product.data['P_cont'] =  input.data['P_cont'] * (1-liq_rem/input.data['moist_cont'] * (100-AD_input.Dig_prop['perPSolid']['amount'])/100 )
        product.data['K_cont'] =  input.data['K_cont'] * (1-liq_rem/input.data['moist_cont'] * (100-AD_input.Dig_prop['perKSolid']['amount'])/100 )

        #Resource use
        Electricity = AD_input.Dewater['elec_dw']['amount'] * input.data['sol_cont']/1000
        add_LCI('Electricity Use', Electricity ,LCI)
        
        return(product,liq_rem,liq_treatment_vol)
        
    if AD_input.AD_operation['isDw']['amount'] !=1:
        #Product
        product = flow(Material_Properties)
        product.data = input.data * 1

### AD_Mixing two flows
def AD_mix(input1,input2,Material_Properties):
    product = flow(Material_Properties)
    product.data['mass']=input1.data['mass'] + input2.data['mass']
    product.data['sol_cont'] = input1.data['sol_cont'] + input2.data['sol_cont']
    product.data['moist_cont'] = input1.data['moist_cont'] + input2.data['moist_cont']
    product.data['vs_cont'] = input1.data['vs_cont'] + input2.data['vs_cont']
    product.data['ash_cont'] = input1.data['ash_cont'] + input2.data['ash_cont']
    product.data['C_cont'] = input1.data['C_cont'] + input2.data['sol_cont']*Material_Properties['Biogenic Carbon Content']/100
    product.data['N_cont'] = input1.data['N_cont'] + input2.data['sol_cont']*Material_Properties['Nitrogen Content']/100
    product.data['P_cont'] = input1.data['P_cont'] + input2.data['sol_cont']*Material_Properties['Phosphorus Content']/100
    product.data['K_cont'] = input1.data['K_cont'] + input2.data['sol_cont']*Material_Properties['Potassium Content']/100
    return(product)

### AD Curing
def AD_curing(input,input_to_reactor,CommonData,process_data,AD_input,assumed_comp,Material_Properties,LCI):
        if AD_input.AD_operation['isCured']['amount']==1:
            input.update(assumed_comp)
            #Calculate wood chips\screen rejects for moisture control
            Tot_WoodChips = (input.water-AD_input.Dig_prop['mcInitComp']['amount']*input.flow)\
            /(AD_input.Dig_prop['mcInitComp']['amount']-AD_input.Material_Properties['wcMC']['amount'])
            
            WC_SR = Tot_WoodChips * input.data['moist_cont']/input.water
            WC_SR_Water = WC_SR * AD_input.Material_Properties['wcMC']['amount']
            WC_SR_solid = WC_SR - WC_SR_Water
            
            #Carbon balance
            C_Remain = np.where(input.data['C_cont']/input_to_reactor.data['C_cont'].apply(lambda x: 1 if x<=0 else x ) <= (1-process_data['Percent Carbon loss during curing'] /100),
                             input.data['C_cont'],input_to_reactor.data['C_cont'] * (1-process_data['Percent Carbon loss during curing'] /100))
            C_loss = input.data['C_cont'] - C_Remain
 
            C_loss_as_CH4 = AD_input.Curing_Bio['ad_pCasCH4']['amount'] * C_loss
            C_loss_as_CO2 = C_loss - C_loss_as_CH4
            
            add_LCI('Methane, non-fossil', C_loss_as_CH4 * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
            add_LCI('Carbon dioxide, non-fossil _ Curing', C_loss_as_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
            
            #Nitrogen balance
            N_loss = input.data['N_cont'] * process_data['Percent N emitted during composting']
            N_loss_as_N2O = N_loss * AD_input.Curing_Bio['ad_pNasN2O']['amount']
            N_loss_as_NH3 = N_loss * AD_input.Curing_Bio['ad_pNasNH3']['amount']
            
            add_LCI('Ammonia', N_loss_as_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Dinitrogen monoxide', N_loss_as_N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
            
            #VOC emission
            VS_loss = AD_input.Curing_Bio['VSlossPerCloss']['amount'] * C_loss / CommonData.MW['C']['amount'] 
            VOC_emitted = VS_loss * process_data['VOC emissions during curing']/1000000
            add_LCI('NMVOC, non-methane volatile organic compounds, unspecified origin', VOC_emitted ,LCI)
            
            #Product
            product = flow(Material_Properties)
            product.data['vs_cont'] = input.data['vs_cont'] - VS_loss
            product.data['ash_cont'] = input.data['ash_cont']
            product.data['sol_cont'] = product.data['vs_cont'] + product.data['ash_cont']
            
            product.data['C_cont']= input.data['C_cont'] - C_loss
            product.data['N_cont']= input.data['N_cont'] - N_loss
            product.data['P_cont']= input.data['P_cont']
            product.data['K_cont']= input.data['K_cont']
            
            #Water
            Water_curing =(WC_SR_Water - AD_input.Material_Properties['ad_mcFC']['amount'] * (WC_SR_Water + WC_SR_solid + product.data['sol_cont']) ) \
                            /(AD_input.Material_Properties['ad_mcFC']['amount']-1)
            
            #Product
            product.data['moist_cont'] = Water_curing
            product.data['mass'] = product.data['moist_cont'] + product.data['sol_cont']
            
            #Resource use
            loder_dsl = input.data['mass']/1000 * AD_input.Loader['hpFEL']['amount'] * AD_input.Loader['mfFEL']['amount'] * AD_input.AD_operation['ophrsperday']['amount']  
            WC_shred_dsl = AD_input.shredding['Mtgp']['amount'] * AD_input.shredding['Mtgf']['amount'] * WC_SR / 1000
            Windrow_turner_dsl = (WC_SR + input.data['mass'])/1000* AD_input.Windrow_turn['Tcur']['amount']*AD_input.Windrow_turn['Mwta']['amount']\
                                    *AD_input.Windrow_turn['turnFreq']['amount'] * AD_input.Windrow_turn['Mwfa']['amount']
            
            add_LCI('Diesel Total', loder_dsl ,LCI)
            add_LCI('Diesel Total', WC_shred_dsl ,LCI)
            add_LCI('Diesel Total', Windrow_turner_dsl ,LCI)
            
        return(product,WC_SR )

### AD Post_screen
def AD_Post_screen(input,input_WC_SR,AD_input,assumed_comp,Material_Properties,LCI):
    product = flow(Material_Properties)
    
    screan_out_mass = input_WC_SR * AD_input.Post_Screen['ad_scrEff_WC']['amount']
    
    Remain_WC = input_WC_SR - screan_out_mass
    Remain_WC_water = Remain_WC * AD_input.Material_Properties['wcMC']['amount']
    Remain_WC_solid = Remain_WC - Remain_WC_water
    Remain_WC_VS = Remain_WC_solid * AD_input.Material_Properties['wcVSC']['amount']
    Remain_WC_Ash = Remain_WC_solid - Remain_WC_VS
    
    #Product
    product = flow(Material_Properties)
    product.data['vs_cont'] = input.data['vs_cont'] +  Remain_WC_VS
    product.data['ash_cont'] = input.data['ash_cont'] + Remain_WC_Ash
    product.data['sol_cont'] = input.data['sol_cont'] + Remain_WC_solid
    product.data['moist_cont'] = input.data['moist_cont'] + Remain_WC_water
    product.data['mass'] = product.data['moist_cont'] + product.data['sol_cont']
    product.data['C_cont']= input.data['C_cont']   # Does not culculate the carbon in the WC
    product.data['N_cont']= input.data['N_cont'] 
    product.data['P_cont']= input.data['P_cont'] 
    product.data['K_cont']= input.data['K_cont'] 
    
    #Resource use
    Electricity = AD_input.Post_Screen['ad_engScreen']['amount'] * (input.data['mass'] + input_WC_SR)
    add_LCI('Electricity Use', Electricity ,LCI)
    
    return(product)
    

def POTW (liq_treatment_vol,liq_rem,input_to_reactor,Dig_to_Curing,FinalCompost,index,AD_input,assumed_comp,Material_Properties,CommonData,LCI):
    #Allocation factor
    AF_total={}
    AF_total['COD'] = sum((1-Material_Properties['Moisture Content']/100) * assumed_comp * liq_treatment_vol * Material_Properties['Biogenic Carbon Content']/100 * 1000)
    AF_total['BOD'] = sum((1-Material_Properties['Moisture Content']/100) * assumed_comp * liq_treatment_vol * Material_Properties['Methane Yield'])
    AF_total['TSS'] = sum( assumed_comp * liq_treatment_vol )
    AF_total['Total_N']= sum( input_to_reactor.data['N_cont'] * assumed_comp * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] ) 
    AF_total['Phosphate'] = sum((1-Material_Properties['Moisture Content']/100) * assumed_comp * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties['Phosphorus Content']/100*1000)
    
    for i in ['Iron','Copper','Cadmium','Arsenic','Mercury','Selenium','Chromium','Lead','Zinc','Barium','Silver']:
        AF_total[i] = sum((1-Material_Properties['Moisture Content']/100) * assumed_comp * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties[i]/100 *1000)

    
    AF={}
    AF['COD'] = (1-Material_Properties['Moisture Content']/100) * liq_treatment_vol * Material_Properties['Biogenic Carbon Content']/100 * 1000 / AF_total['COD']
    AF['BOD'] = (1-Material_Properties['Moisture Content']/100) * liq_treatment_vol * Material_Properties['Methane Yield'] / AF_total['BOD']
    AF['TSS'] = liq_treatment_vol/AF_total['TSS']
    AF['Total_N'] = input_to_reactor.data['N_cont'] * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount']/AF_total['Total_N']
    AF['Phosphate'] = (1-Material_Properties['Moisture Content']/100) * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties['Phosphorus Content']/100 * 1000 / AF_total['Phosphate']
    
    for i in ['Iron','Copper','Cadmium','Arsenic','Mercury','Selenium','Chromium','Lead','Zinc','Barium','Silver']:
        if AF_total[i] == 0:
            AF[i]=0
        else:
            AF[i] = (1-Material_Properties['Moisture Content']/100) * FinalCompost.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties[i]/100 * 1000 / AF_total[i]
    
    #Emission from POTW
    Emission={}
    Emission['Total_N'] =  input_to_reactor.data['N_cont'] * (100-AD_input.Dig_prop['perNSolid']['amount'])/100 * liq_rem/(Dig_to_Curing.data['moist_cont']+liq_rem) * (1-CommonData.WWT['n_rem']['amount']/100) 
    Emission['Phosphate'] = input_to_reactor.data['sol_cont'] * Material_Properties['Phosphorus Content']/100 * (100-AD_input.Dig_prop['perPSolid']['amount'])/100 * liq_rem/(Dig_to_Curing.data['moist_cont']+liq_rem) *(94.97/30.97) * (1-CommonData.WWT['p_rem']['amount']/100) 
    
    for i,j,k in [('COD','lchCODcont','cod_rem'),('BOD','lchBODcont','bod_rem'),('TSS','lchTSScont','tss_rem')\
                  ,('Iron','conc_Fe','metals_rem'),('Copper','conc_Cu','metals_rem'),('Cadmium','conc_Cd','metals_rem')\
                  ,('Arsenic','conc_As','metals_rem'),('Mercury','conc_Hg','metals_rem'),('Selenium','conc_Se','metals_rem')\
                  ,('Chromium','conc_Cr','metals_rem'),('Lead','conc_Pb','metals_rem'),('Zinc','conc_Zn','metals_rem')\
                  ,('Barium','conc_Ba','metals_rem'),('Silver','conc_Ag','metals_rem')]:
        Emission[i] = AD_input.Digestate_treatment[j]['amount'] * AF[i] * liq_treatment_vol * (1-CommonData.WWT[k]['amount']/100) 
    
    for i,j in [('COD','COD'),('BOD','BOD'),('TSS','Total suspended solids')\
                  ,('Iron','Iron'),('Copper','Copper'),('Cadmium','Cadmium')\
                  ,('Arsenic','Arsenic'),('Mercury','Mercury'),('Phosphate','Phosphate'),('Selenium','Selenium')\
                  ,('Chromium','Chromium'),('Lead','Lead'),('Zinc','Zinc')\
                  ,('Barium','Barium'),('Silver','Silver'),('Total_N','Total N')]:
        add_LCI(j, Emission[i] ,LCI)
    
    
    BOD_removed = AD_input.Digestate_treatment['lchBODcont']['amount'] * AF['BOD'] * liq_treatment_vol * CommonData.WWT['bod_rem']['amount']/100
    add_LCI('CO2-biogenic emissions from digested liquids treatment', BOD_removed * CommonData.Leachate_treat['co2bod']['amount'] ,LCI)
    
    #Sludge to LF
    sludge_prod = liq_treatment_vol * CommonData.Leachate_treat['sludgef']['amount'] # Unit kg
    
    #Resouce use
    add_LCI('Full_Total heavy duty truck tranport', AD_input.Digestate_treatment['ad_distPOTW']['amount'] * liq_treatment_vol * 1000 * AD_input.Dig_prop['digliqdens']['amount'] ,LCI)
    add_LCI('Empty_Total heavy duty truck empty return', liq_treatment_vol * AD_input.Dig_prop['digliqdens']['amount'] / AD_input.Digestate_treatment['payload_POTW']['amount']\
            * AD_input.Digestate_treatment['ad_distPOTW']['amount'] * AD_input.Digestate_treatment['ad_erPOTW']['amount'] ,LCI)
    
    add_LCI('Full_Total heavy duty truck tranport', AD_input.Digestate_treatment['wwtp_lf_dist']['amount'] * sludge_prod ,LCI)
    add_LCI('Empty_Total heavy duty truck empty return', AD_input.Digestate_treatment['wwtp_lf_dist']['amount'] * sludge_prod /1000\
            /AD_input.Digestate_treatment['payload_LFPOTW']['amount'] * AD_input.Digestate_treatment['er_wwtpLF']['amount']  ,LCI)
    
    add_LCI('Electricity Use', BOD_removed * CommonData.Leachate_treat['elecBOD']['amount'] ,LCI)


### Apply compost to Land _AD
def AD_compost_use(input,CommonData,process_data,Material_Properties,assumed_comp,AD_input,LCI):
    if AD_input.AD_operation['choice_BU']['amount'] == 1:
        # Carbon in final compost
        C_storage = input.data['C_cont'] * AD_input.Soil_seq['perCStor']['amount']/100
        C_released = input.data['C_cont'] - C_storage
        C_storage_hummus_formation = input.data['C_cont'] * AD_input.Soil_seq['humFormFac']['amount']
        add_LCI('Carbon dioxide, non-fossil _ Land application', C_released * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Direct Carbon Storage and Humus Formation', -(C_storage+C_storage_hummus_formation) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        
        #Nitrogen in final compost
        input.data['N_cont'] = input.data['N_cont'] * process_data['Percent NPK available as nutrient or emission (in addition to MFE)']/100
        input.data['P_cont'] = input.data['P_cont'] * process_data['Percent NPK available as nutrient or emission (in addition to MFE)']/100
        input.data['K_cont'] = input.data['K_cont'] * process_data['Percent NPK available as nutrient or emission (in addition to MFE)']/100
        
        N2O = input.data['N_cont'] * AD_input.Land_app['perN2Oevap']['amount']/100 
        NH3 = input.data['N_cont'] * AD_input.Land_app['perNasNH3fc']['amount']/100 * AD_input.Land_app['perNH3evap']['amount']/100
        NO3_GW = input.data['N_cont'] * CommonData.Land_app['NO3leach']['amount'] 
        NO3_SW = input.data['N_cont'] * CommonData.Land_app['NO3runoff']['amount'] 
        
        add_LCI('Dinitrogen monoxide', N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
        add_LCI('Ammonia',NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (ground water)',NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (Surface water)',NO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        
        if AD_input.AD_operation['fertOff']['amount'] == 1:
            # Nutrients availble in the final compost
            Navail = input.data['N_cont'] * CommonData.Land_app['MFEN']['amount']
            Pavail = input.data['P_cont'] * CommonData.Land_app['MFEP']['amount'] 
            Kavail = input.data['K_cont'] * CommonData.Land_app['MFEK']['amount']
            
            # Diesel use for applying the compost
            Diesel_use = input.data['mass'] /1000 * CommonData.Land_app['cmpLandDies']['amount']
            add_LCI('Diesel Total', Diesel_use ,LCI)
            
            # Offset from fertilizer
            Diesel_offset = -(Navail*CommonData.Land_app['DslAppN']['amount']+Pavail*CommonData.Land_app['DslAppP']['amount']+Kavail*CommonData.Land_app['DslAppK']['amount'])
            add_LCI('Diesel Total', Diesel_offset ,LCI)
            add_LCI('Nitrogen Mineral Fertilizer Equivalent mass to offset', -Navail ,LCI)
            add_LCI('Phosphorous Mineral Fertilizer Equivalent mass to offset', -Pavail ,LCI)
            add_LCI('Potassium Mineral Fertilizer Equivalent mass to offset', -Kavail ,LCI)
            
            # offset from applying fertilizer
            Fert_N2O = -Navail * CommonData.Land_app['fert_N2O']['amount']/100 
            Fert_NH3 = -Navail * CommonData.Land_app['fert_NH3']['amount']/100 * CommonData.Land_app['fert_NH3Evap']['amount']/100
            Fert_NO3_GW = -Navail * CommonData.Land_app['fert_NO3Leach']['amount'] /100
            Fert_NO3_SW = -Navail * CommonData.Land_app['fert_NO3Run']['amount'] / 100
            
            add_LCI('Dinitrogen monoxide', Fert_N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
            add_LCI('Ammonia',Fert_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Nitrate (ground water)',Fert_NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Nitrate (Surface water)',Fert_NO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        if AD_input.AD_operation['peatOff']['amount'] == 1:
            Peat = input.data['mass']/AD_input.Material_Properties['ad_densFC']['amount'] * AD_input.Land_app['ad_densPeat']['amount'] / 1000 \
                    * AD_input.Land_app['ad_PeatSubFac']['amount'] * input.data['C_cont']/sum(input.data['C_cont']*assumed_comp)
            add_LCI('Peat Equivalent mass to offset', -Peat ,LCI)  
    
    if AD_input.AD_operation['choice_BU']['amount'] == 0:
        # Carbon in final compost
        Max_C_storage = (1-Material_Properties['Moisture Content']/100) * Material_Properties['Carbon Storage Factor']
        C_storage = np.where( input.data['C_cont'] * AD_input.Soil_seq['percCStor_LF']['amount']/100 <= Max_C_storage,
                             input.data['C_cont'] * AD_input.Soil_seq['percCStor_LF']['amount']/100,Max_C_storage)
        
        C_released = (input.data['C_cont'] - C_storage)/2
        C_CH4 = (input.data['C_cont'] - C_storage)/2
        C_CH4_Oxidized = C_CH4 * process_data['Percent of Generated Methane oxidized']/100
        C_CH4_Flared = C_CH4 * process_data['Percent of Generated Methane Flared']/100
        C_CH4_Emitted = C_CH4 * process_data['Percent of Generated Methane Emitted']/100
        C_CH4_EnergyRec = C_CH4 * process_data['Percent of Generated Methane used for Energy']/100
        C_CH4_Electricity = C_CH4_EnergyRec*CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount']*50/3.6  # LHV of Methane: 50 MJ/kg
                
        add_LCI('Direct Carbon Storage and Humus Formation', -(C_storage) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil _ Land application', (C_released+C_CH4_EnergyRec+C_CH4_Flared+C_CH4_Oxidized) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Methane, non-fossil', C_CH4_Emitted * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Electricity Production', C_CH4_Electricity ,LCI)
        
        #General emissions from LF
        add_LCI('compost_to_LF', input.data['mass'] /1000 ,LCI)
        
        #Amomonium emission from LF (Calculated base on the ammomium/N_cont ratio in LF)
        NH4_GW= 0.0051/100 * input.data['N_cont']
        NH4_SW= 0.3597/100 * input.data['N_cont']
        add_LCI('Ammonium, ion (ground water)', NH4_GW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Ammonium, ion (surface water)', NH4_SW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)   
 