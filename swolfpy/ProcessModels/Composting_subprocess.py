# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:06:06 2019

@author: msardar2
"""
from copy import deepcopy
import numpy as np

### Adding flows to LCI data frame
def add_LCI(Name,Flow,LCI):
    if Name in LCI.columns:
        LCI[Name] = Flow + LCI[Name].values
    else:
        LCI[Name] = Flow


def report_LCI(flow_name,LCI_datafram,waste_stream):
    if flow_name in LCI_datafram.columns:
        return(LCI_datafram[flow_name][waste_stream])
    else:
        return(0)
    
### Screan
def screen(input,sep_eff, Material_Properties,Op_param,LCI,flow_init):
    product = deepcopy(flow_init)
    residual = deepcopy(flow_init)
    
    residual.data['mass']=input.data['mass'].values * sep_eff
    residual.data['sol_cont'] = input.data['sol_cont'].values * sep_eff
    residual.data['moist_cont'] = input.data['moist_cont'].values * sep_eff
    residual.data['vs_cont'] = input.data['vs_cont'].values * sep_eff
    residual.data['ash_cont'] = input.data['ash_cont'].values * sep_eff
    
    product.data['mass']=input.data['mass'].values - residual.data['mass'].values
    product.data['sol_cont'] = input.data['sol_cont'].values - residual.data['sol_cont'].values
    product.data['moist_cont'] = input.data['moist_cont'].values - residual.data['moist_cont'].values
    product.data['vs_cont'] = input.data['vs_cont'].values - residual.data['vs_cont'].values
    product.data['ash_cont'] = input.data['ash_cont'].values - residual.data['ash_cont'].values
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['Mtr']['amount'] * input.data['mass'].values/1000  ,LCI) 

    return(product,residual)

### Shredding
def shredding(input,Material_Properties,Op_param,LCI,flow_init):
    product = deepcopy(flow_init)
    product.data = deepcopy(input.data)

    #Resource use    
    Shred_diesel = input.data['mass'].values / 1000 * Op_param['Mtgp']['amount'] * Op_param['Mtgf']['amount']                                   
    add_LCI(('Technosphere', 'Equipment_Diesel'),Shred_diesel,LCI) 
    
    return(product)

### Mixing two flows
def mix(input1,input2,Material_Properties,flow_init):
    product = deepcopy(flow_init)
    product.data['mass']=input1.data['mass'].values + input2.data['mass'].values
    product.data['sol_cont'] = input1.data['sol_cont'].values + input2.data['sol_cont'].values
    product.data['moist_cont'] = input1.data['moist_cont'].values + input2.data['moist_cont'].values
    product.data['vs_cont'] = input1.data['vs_cont'].values + input2.data['vs_cont'].values
    product.data['ash_cont'] = input1.data['ash_cont'].values + input2.data['ash_cont'].values
    return(product)

### Add Water    
def add_water(input,water_flow,Material_Properties,process_data,flow_init):
    product = deepcopy(flow_init)
    product.data['mass']=input.data['mass'].values + water_flow
    product.data['sol_cont'] = input.data['sol_cont'].values
    product.data['moist_cont'] = input.data['moist_cont'].values + water_flow
    product.data['vs_cont'] = input.data['vs_cont'].values 
    product.data['ash_cont'] = input.data['ash_cont'].values
    #Nitrogen and carbon in the input stream
    product.data['C_input'] = product.data['sol_cont'].values *  Material_Properties['Biogenic Carbon Content'].values/100 * process_data['Degrades'].values
    product.data['N_input'] = product.data['sol_cont'].values *  Material_Properties['Nitrogen Content'].values/100 * process_data['Degrades'].values
    return(product)

    
### Active Composting
def ac_comp(input,CommonData,process_data,Comp_input,Degradation_Parameters,Biological_Degredation,assumed_comp,Material_Properties,LCI,flow_init):
    #Degradation
    C_loss = input.data['C_input'].values * process_data['Percent C-loss during composting'].values/100 * Degradation_Parameters['acDegProp']['amount']/100
    N_loss = input.data['N_input'].values * process_data['Percent N-loss during composting'].values/100 * Degradation_Parameters['acDegProp']['amount']/100
    VS_loss = C_loss * process_data['Mass VS loss per mass C-loss'].values
    VOCs_loss = VS_loss * process_data['VOC emissions'].values / 1000000
    
    #Product
    product = deepcopy(flow_init)
    product.data['vs_cont'] = input.data['vs_cont'].values - VS_loss
    product.data['ash_cont'] = input.data['ash_cont'].values
    product.data['sol_cont'] = product.data['vs_cont'].values + product.data['ash_cont'].values
    product.data['C_cont']= input.data['C_input'].values - C_loss
    product.data['N_cont']= input.data['N_input'].values - N_loss
    
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
    water_after_ac = sum(product.data['sol_cont'].values * assumed_comp.values) * Degradation_Parameters['MCac']['amount'] / (1-Degradation_Parameters['MCac']['amount'])
    product.data['moist_cont'] = water_after_ac * input.data['moist_cont'].values/input.water
    product.data['mass']= product.data['sol_cont'].values + product.data['moist_cont'].values
    
    #Resource use
    Loader_diesel = Comp_input.Op_Param['Tdoh']['amount']*Comp_input.Loader['hpfel']['amount']*Comp_input.Loader['Mffel']['amount']
    Windrow_turner_diesel = Comp_input.Op_Param['Tact']['amount']*Comp_input.AC_Turning['Fta']['amount']* input.data['mass']/1000 * \
                                Comp_input.AC_Turning['Mwta']['amount'] * Comp_input.AC_Turning['Mwfa']['amount']                                     
    add_LCI(('Technosphere', 'Equipment_Diesel'), Windrow_turner_diesel+Loader_diesel ,LCI) 
    
    return(product)

### Post Screen
def post_screen(input,sep_eff, Material_Properties,Op_param,LCI,flow_init):
    product = deepcopy(flow_init)
    residual = deepcopy(flow_init)
    
    residual.data['mass']=input.data['mass'].values * sep_eff
    residual.data['sol_cont'] = input.data['sol_cont'].values * sep_eff
    residual.data['moist_cont'] = input.data['moist_cont'].values * sep_eff
    residual.data['vs_cont'] = input.data['vs_cont'].values * sep_eff
    residual.data['ash_cont'] = input.data['ash_cont'].values * sep_eff
    residual.data['C_cont'] = input.data['C_cont'].values * sep_eff
    residual.data['N_cont'] = input.data['N_cont'].values * sep_eff
    
    product.data['mass']=input.data['mass'].values - residual.data['mass'].values
    product.data['sol_cont'] = input.data['sol_cont'].values - residual.data['sol_cont'].values
    product.data['moist_cont'] = input.data['moist_cont'].values - residual.data['moist_cont'].values
    product.data['vs_cont'] = input.data['vs_cont'].values - residual.data['vs_cont'].values
    product.data['ash_cont'] = input.data['ash_cont'].values - residual.data['ash_cont'].values
    product.data['C_cont'] = input.data['C_cont'].values - residual.data['C_cont'].values
    product.data['N_cont'] = input.data['N_cont'].values- residual.data['N_cont'].values
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['Mtr']['amount'] * input.data['mass'].values/1000  ,LCI) 
    
    return(product,residual)
    

### Vaccuum
def vacuum(input,sep_eff, Material_Properties,Op_param,LCI,flow_init):
    product = deepcopy(flow_init)
    vacuumed = deepcopy(flow_init)
    
    vacuumed.data['mass']=input.data['mass'].values * sep_eff
    vacuumed.data['sol_cont'] = input.data['sol_cont'].values * sep_eff
    vacuumed.data['moist_cont'] = input.data['moist_cont'].values * sep_eff
    vacuumed.data['vs_cont'] = input.data['vs_cont'].values * sep_eff
    vacuumed.data['ash_cont'] = input.data['ash_cont'].values * sep_eff
    vacuumed.data['C_cont'] = input.data['C_cont'].values * sep_eff   
    vacuumed.data['N_cont'] = input.data['N_cont'].values * sep_eff        
    
    product.data['mass']=input.data['mass'].values - vacuumed.data['mass'].values
    product.data['sol_cont'] = input.data['sol_cont'].values - vacuumed.data['sol_cont'].values
    product.data['moist_cont'] = input.data['moist_cont'].values - vacuumed.data['moist_cont'].values
    product.data['vs_cont'] = input.data['vs_cont'].values - vacuumed.data['vs_cont'].values
    product.data['ash_cont'] = input.data['ash_cont'].values - vacuumed.data['ash_cont'].values
    product.data['C_cont'] = input.data['C_cont'].values- vacuumed.data['C_cont'].values
    product.data['N_cont'] = input.data['N_cont'].values - vacuumed.data['N_cont'].values
    
    #Resource use
    add_LCI(('Technosphere', 'Electricity_consumption'), Op_param['vacElecFac']['amount'] * input.data['mass'].values/1000  ,LCI)                                 
    add_LCI(('Technosphere', 'Equipment_Diesel'),Op_param['vacDiesFac']['amount'] * input.data['mass'].values/1000 ,LCI) 
    
    return(product,vacuumed)
        
### Curing
def curing(input,CommonData,process_data,Comp_input,Degradation_Parameters,Biological_Degredation,assumed_comp,Material_Properties,LCI,flow_init):
    #Degradation
    C_loss = input.data['C_cont'].values * process_data['Percent C-loss during composting'].values/100 * (100-Degradation_Parameters['acDegProp']['amount'])/100
    N_loss = input.data['N_cont'].values * process_data['Percent N-loss during composting'].values/100 * (100-Degradation_Parameters['acDegProp']['amount'])/100
    VS_loss = C_loss * process_data['Mass VS loss per mass C-loss'].values
    VOCs_loss = VS_loss * process_data['VOC emissions'].values / 1000000
    
    #Product
    product = deepcopy(flow_init)
    product.data['vs_cont'] = input.data['vs_cont'].values - VS_loss
    product.data['ash_cont'] = input.data['ash_cont'].values
    product.data['sol_cont'] = product.data['vs_cont'].values + product.data['ash_cont'].values
    product.data['C_cont']= input.data['C_cont'].values - C_loss
    product.data['N_cont']= input.data['N_cont'].values - N_loss
    
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
    water_after_cu = sum(product.data['sol_cont'].values * assumed_comp.values) * Degradation_Parameters['MCcu']['amount'] / (1-Degradation_Parameters['MCcu']['amount'])
    product.data['moist_cont'] = water_after_cu * input.data['moist_cont'].values/input.water
    product.data['mass']= product.data['sol_cont'].values + product.data['moist_cont'].values
    
    #Resource use
    Curing_diesel = Comp_input.Op_Param['Tcur']['amount']*Comp_input.Curing['Ftc']['amount']*Comp_input.AC_Turning['Mwta']['amount']*\
                    Comp_input.AC_Turning['Mwfa']['amount']*input.data['mass'].values/1000                                  
    add_LCI(('Technosphere', 'Equipment_Diesel'),Curing_diesel ,LCI) 
    
    return(product)

### Apply compost to Land
def compost_use(input,CommonData,process_data,Material_Properties,Biological_Degredation,Land_app,Fertilizer_offsest,Comp_input,LCI):
    if Fertilizer_offsest['choice_BU']['amount'] == 1:
        # Carbon in final compost
        C_storage = input.data['C_cont'].values * Biological_Degredation['percCStor']['amount']/100
        C_released = input.data['C_cont'].values - C_storage
        C_storage_hummus_formation = input.data['C_cont'].values * Biological_Degredation['humFormFac']['amount']
        add_LCI('Carbon dioxide, non-fossil', C_released * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil storage', -(C_storage+C_storage_hummus_formation) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        
        #Nitrogen in final compost
        N2O = input.data['N_cont'].values * Land_app['perN2Oevap']['amount']/100 
        NH3 = input.data['N_cont'].values * Land_app['perNasNH3fc']['amount']/100 * Land_app['perNH3evap']['amount']/100
        NO3_GW = input.data['N_cont'].values * CommonData.Land_app['NO3leach']['amount'] 
        FNO3_SW = input.data['N_cont'].values* CommonData.Land_app['NO3runoff']['amount'] 
        
        add_LCI('Dinitrogen monoxide', N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
        add_LCI('Ammonia',NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (ground water)',NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (Surface water)',FNO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        
        if Fertilizer_offsest['fertOff']['amount'] == 1:
            # Nutrients availble in the final compost
            Navail = input.data['N_cont'].values * CommonData.Land_app['MFEN']['amount'] * process_data['Degrades'].values
            Pavail = input.data['P_cont'].values * CommonData.Land_app['MFEP']['amount'] * process_data['Degrades'].values
            Kavail = input.data['K_cont'].values * CommonData.Land_app['MFEK']['amount'] * process_data['Degrades'].values
            
            # Diesel use for applying the compost
            Diesel_use = input.data['mass'].values /1000 * CommonData.Land_app['cmpLandDies']['amount']
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
            Peat = input.data['mass'].values/Comp_input.Material_Properties['densFC']['amount'] * Comp_input.Material_Properties['densPeat']['amount'] / 1000 \
                    * Comp_input.Material_Properties['PeatSubFac']['amount'] * input.data['C_cont'].values/sum(input.data['C_cont'].values*Comp_input.Assumed_Comp)
            add_LCI(('Technosphere', 'Peat'), -Peat ,LCI)  
    
    if Fertilizer_offsest['choice_BU']['amount'] == 0:
        # Carbon in final compost
        Max_C_storage = (1-Material_Properties['Moisture Content'].values/100) * Material_Properties['Carbon Storage Factor'].values
        C_storage = np.where( input.data['C_cont'].values * Biological_Degredation['percCStor_LF']['amount']/100 <= Max_C_storage,
                             input.data['C_cont'].values * Biological_Degredation['percCStor_LF']['amount']/100,Max_C_storage)
        
        C_released = (input.data['C_cont'].values - C_storage)/2
        C_CH4 = (input.data['C_cont'].values - C_storage)/2
        C_CH4_Oxidized = C_CH4 * process_data['Percent of Generated Methane oxidized'].values/100
        C_CH4_Flared = C_CH4 * process_data['Percent of Generated Methane Flared'].values/100
        C_CH4_Emitted = C_CH4 * process_data['Percent of Generated Methane Emitted'].values/100
        C_CH4_EnergyRec = C_CH4 * process_data['Percent of Generated Methane used for Energy'].values/100
        C_CH4_Electricity = C_CH4_EnergyRec*CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount']*50/3.6 * 0.36  # LHV of Methane: 50 MJ/kg
                
        add_LCI('Carbon dioxide, non-fossil storage', -(C_storage) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil', (C_released+C_CH4_EnergyRec+C_CH4_Flared+C_CH4_Oxidized) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Methane, non-fossil', C_CH4_Emitted * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI(('Technosphere', 'Electricity_consumption'), -C_CH4_Electricity ,LCI)
        
        #General emissions from LF
        add_LCI(('Technosphere', 'compost_to_LF'), input.data['mass'] /1000 ,LCI)
        
        #Amomonium emission from LF (Calculated base on the ammomium/N_cont ratio in LF)
        NH4_GW= 0.0051/100 * input.data['N_cont'].values
        NH4_SW= 0.3597/100 * input.data['N_cont'].values
        add_LCI('Ammonium, ion (ground water)', NH4_GW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Ammonium, ion (surface water)', NH4_SW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)
