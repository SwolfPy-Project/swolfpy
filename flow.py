# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:41:44 2019

@author: msardar2
"""
import numpy as np
import pandas as pd

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
        
    def update(self,assumed_comp): 
        self.flow = sum(self.data['mass']*assumed_comp)
        self.water = sum(self.data['moist_cont']*assumed_comp)
        self.moist_cont = self.water / self.flow
        self.ash = sum(self.data['ash_cont']*assumed_comp)
        self.solid = sum(self.data['sol_cont']*assumed_comp)

    
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
