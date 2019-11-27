# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:23:49 2019

@author: msardar2
"""
import numpy as np
from copy import deepcopy

def add_LCI(Name,Flow,LCI):
    if Name in LCI.columns:
        LCI[Name] = Flow + LCI[Name].values
    else:
        LCI[Name] = Flow
        
### AD_Screan
def AD_screen(input,sep_eff, Material_Properties,LCI,flow_init):
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

    return(product,residual)


### AD_Add Water    
def add_water_AD(input,water_flow,Material_Properties,flow_init):
    product = deepcopy(flow_init)
    product.data['mass']=input.data['mass'].values + water_flow
    product.data['sol_cont'] = input.data['sol_cont'].values
    product.data['moist_cont'] = input.data['moist_cont'].values + water_flow
    product.data['vs_cont'] = input.data['vs_cont'].values
    product.data['ash_cont'] = input.data['ash_cont'].values
    #Nitrogen and carbon in the input stream
    product.data['C_cont'] = product.data['sol_cont'].values *  Material_Properties['Biogenic Carbon Content'].values/100
    product.data['N_cont'] = product.data['sol_cont'].values *  Material_Properties['Nitrogen Content'].values/100
    product.data['P_cont'] = product.data['sol_cont'].values *  Material_Properties['Phosphorus Content'].values/100
    product.data['K_cont'] = product.data['sol_cont'].values *  Material_Properties['Potassium Content'].values/100
    return(product)

### AD Reactor
def Reactor(input,CommonData,process_data,AD_input,Material_Properties,EmissionFactor_Engine,EmissionFactor_Flare ,LCI,flow_init):
    #Methane production
    CH4_prod_vol = input.data['sol_cont'].values / 1000 * Material_Properties['Methane Yield'].values * process_data['Percent of L0 reached'].values/100
    CH4_prod_mass_asC = CH4_prod_vol * CommonData.STP['m3CH4_to_kg']['amount']*CommonData.MW['C']['amount']/CommonData.MW['CH4']['amount']
    
    #Mehtane Balance
    CH4_fugitiv_mass_asC = CH4_prod_mass_asC * (1-AD_input.Biogas_gen['ad_collEff']['amount'])
    CH4_Energy_rec_asC = CH4_prod_mass_asC * AD_input.Biogas_gen['ad_collEff']['amount'] * (1-AD_input.Biogas_gen['ad_downTime']['amount'])
    CH4_Flare_asC = CH4_prod_mass_asC * AD_input.Biogas_gen['ad_collEff']['amount'] * AD_input.Biogas_gen['ad_downTime']['amount']
    CH4_unburn_AsC = CH4_Energy_rec_asC * (1-EmissionFactor_Engine['CH4_destruction']['amount']) + CH4_Flare_asC* (1-EmissionFactor_Flare['CH4_destruction']['amount'])
    CO2_from_CH4Comb = CH4_Energy_rec_asC * EmissionFactor_Engine['CH4_destruction']['amount'] + CH4_Flare_asC* EmissionFactor_Flare['CH4_destruction']['amount']
    
    #ENergy content
    CH4_Energy_EngCont = CH4_prod_vol * AD_input.Biogas_gen['ad_collEff']['amount'] * (1-AD_input.Biogas_gen['ad_downTime']['amount']) * AD_input.Biogas_gen['ad_ch4EngCont']['amount']
    CH4_Flare_EngCont = CH4_prod_vol * AD_input.Biogas_gen['ad_collEff']['amount'] * AD_input.Biogas_gen['ad_downTime']['amount'] * AD_input.Biogas_gen['ad_ch4EngCont']['amount']
    
    #Calculate emissions based on the energy content
    CO_Comb = (CH4_Energy_EngCont * EmissionFactor_Engine['CO']['amount'] + CH4_Flare_EngCont * EmissionFactor_Flare['CO']['amount'])/1000000
    NOx_Comb = (CH4_Energy_EngCont * EmissionFactor_Engine['NO2']['amount'] + CH4_Flare_EngCont * EmissionFactor_Flare['NO2']['amount'])/1000000
    SO2_Comb = (CH4_Energy_EngCont * EmissionFactor_Engine['SO2']['amount'] + CH4_Flare_EngCont * EmissionFactor_Flare['SO2']['amount'])/1000000
    NMVOCs_Comb = (CH4_Energy_EngCont * EmissionFactor_Engine['NMVOC']['amount'] + CH4_Flare_EngCont * EmissionFactor_Flare['NMVOC']['amount'])/1000000
    PM2_5_Comb = (CH4_Energy_EngCont * EmissionFactor_Engine['PM']['amount'] + CH4_Flare_EngCont * EmissionFactor_Flare['PM']['amount'])/1000000
    
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
    add_LCI(('Technosphere', 'Electricity_production'), Elec_prod ,LCI)
    
    #CO2 production
    CO2_prod_mass_asC = (BioGas_vol-CH4_prod_vol) * CommonData.STP['m3CO2_to_kg']['amount'] * CommonData.MW['C']['amount']/CommonData.MW['CO2']['amount']
    add_LCI('Carbon dioxide, non-fossil (in biogas)', CO2_prod_mass_asC * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
    
    #Water and Volatile solid in Biogas
    BioGas_VS = BioGas_mass * AD_input.Biogas_gen['perSolDec']['amount'] /100
    BioGas_Water = BioGas_mass - BioGas_VS
    
    #Product
    product = deepcopy(flow_init)
    product.data['vs_cont'] = input.data['vs_cont'].values - BioGas_VS
    product.data['ash_cont'] = input.data['ash_cont'].values
    product.data['sol_cont'] = product.data['vs_cont'].values + product.data['ash_cont']
    product.data['moist_cont'] = input.data['moist_cont'].values - BioGas_Water
    product.data['mass'] = product.data['moist_cont'].values + product.data['sol_cont'].values
    product.data['C_cont']= input.data['C_cont'].values - CO2_prod_mass_asC - CH4_prod_mass_asC
    product.data['N_cont']= input.data['N_cont'].values
    product.data['P_cont']= input.data['P_cont'].values
    product.data['K_cont']= input.data['K_cont'].values
    
    return(product)
    
### AD Dewater
def Dewater(input,CommonData,process_data,AD_input,Material_Properties,added_water,assumed_comp,LCI,flow_init):
    if AD_input.AD_operation['isDw']['amount']==1:
        # Calculating water removed
        liq_rem = (input.data['moist_cont'].values - AD_input.Dewater['ad_mcDigestate']['amount'] * input.data['mass'].values)/(1-AD_input.Dewater['ad_mcDigestate']['amount'])
        
        # Maximum water recirculate
        Recirculate_water_max = sum(added_water * assumed_comp) * AD_input.AD_operation['recircMax']['amount']
        
        #Liquid to reatment, new water, recirculate watersum(liq_rem * assumed_co
        total_liq_to_treatment = max(sum(liq_rem*assumed_comp) - Recirculate_water_max , 0 )
        liq_treatment_mass = total_liq_to_treatment * liq_rem / sum(liq_rem * assumed_comp)
        liq_treatment_vol = liq_treatment_mass/1000 /AD_input.Dig_prop['digliqdens']['amount']
        Recirulate_water_mass= (sum(liq_rem * assumed_comp) - total_liq_to_treatment) * liq_rem / sum(liq_rem * assumed_comp)
        New_water_mass= (sum(added_water * assumed_comp) - (sum(liq_rem * assumed_comp) - total_liq_to_treatment)) * liq_rem / sum(liq_rem * assumed_comp)
        
        #Product
        product = deepcopy(flow_init)
        product.data['vs_cont'] = input.data['vs_cont'].values
        product.data['ash_cont'] = input.data['ash_cont'].values
        product.data['sol_cont'] = input.data['sol_cont'].values
        product.data['moist_cont'] = input.data['moist_cont'].values - liq_rem
        product.data['mass'] = product.data['moist_cont'].values + product.data['sol_cont'].values
        product.data['C_cont']= input.data['C_cont'].values
        product.data['N_cont'] =  input.data['N_cont'].values * (1-liq_rem/input.data['moist_cont'].values * (100-AD_input.Dig_prop['perNSolid']['amount'])/100 )
        product.data['P_cont'] =  input.data['P_cont'].values * (1-liq_rem/input.data['moist_cont'].values * (100-AD_input.Dig_prop['perPSolid']['amount'])/100 )
        product.data['K_cont'] =  input.data['K_cont'].values * (1-liq_rem/input.data['moist_cont'].values * (100-AD_input.Dig_prop['perKSolid']['amount'])/100 )

        #Resource use
        Electricity = AD_input.Dewater['elec_dw']['amount'] * input.data['sol_cont'].values/1000
        add_LCI(('Technosphere', 'Electricity_consumption'), Electricity ,LCI)
        
        return(product,liq_rem,liq_treatment_vol)
        
    if AD_input.AD_operation['isDw']['amount'] !=1:
        #Product
        product = deepcopy(flow_init)
        product.data = input.data * 1

### AD_Mixing two flows
def AD_mix(input1,input2,Material_Properties,flow_init):
    product = deepcopy(flow_init)
    product.data['mass']=input1.data['mass'].values + input2.data['mass'].values
    product.data['sol_cont'] = input1.data['sol_cont'].values + input2.data['sol_cont'].values
    product.data['moist_cont'] = input1.data['moist_cont'].values + input2.data['moist_cont'].values
    product.data['vs_cont'] = input1.data['vs_cont'].values + input2.data['vs_cont'].values
    product.data['ash_cont'] = input1.data['ash_cont'].values + input2.data['ash_cont'].values
    product.data['C_cont'] = input1.data['C_cont'].values + input2.data['sol_cont'].values*Material_Properties['Biogenic Carbon Content'].values/100
    product.data['N_cont'] = input1.data['N_cont'].values + input2.data['sol_cont'].values*Material_Properties['Nitrogen Content'].values/100
    product.data['P_cont'] = input1.data['P_cont'].values+ input2.data['sol_cont'].values*Material_Properties['Phosphorus Content'].values/100
    product.data['K_cont'] = input1.data['K_cont'].values + input2.data['sol_cont'].values*Material_Properties['Potassium Content'].values/100
    return(product)

### AD Curing
def AD_curing(input,input_to_reactor,CommonData,process_data,AD_input,assumed_comp,Material_Properties,LCI,flow_init):
        if AD_input.AD_operation['isCured']['amount']==1:
            input.update(assumed_comp)
            #Calculate wood chips\screen rejects for moisture control
            Tot_WoodChips = (input.water-AD_input.Dig_prop['mcInitComp']['amount']*input.flow)\
            /(AD_input.Dig_prop['mcInitComp']['amount']-AD_input.Material_Properties['wcMC']['amount'])
            
            WC_SR = Tot_WoodChips * input.data['moist_cont'].values/input.water
            WC_SR_Water = WC_SR * AD_input.Material_Properties['wcMC']['amount']
            WC_SR_solid = WC_SR - WC_SR_Water
            
            #Carbon balance
            C_Remain = np.where(input.data['C_cont'].values/input_to_reactor.data['C_cont'].apply(lambda x: 1 if x<=0 else x ).values <= (1-process_data['Percent Carbon loss during curing'].values /100),
                             input.data['C_cont'].values,input_to_reactor.data['C_cont'].values * (1-process_data['Percent Carbon loss during curing'].values /100))
            C_loss = input.data['C_cont'].values - C_Remain
 
            C_loss_as_CH4 = AD_input.Curing_Bio['ad_pCasCH4']['amount'] * C_loss
            C_loss_as_CO2 = C_loss - C_loss_as_CH4
            
            add_LCI('Methane, non-fossil', C_loss_as_CH4 * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
            add_LCI('Carbon dioxide, non-fossil _ Curing', C_loss_as_CO2 * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
            
            #Nitrogen balance
            N_loss = input.data['N_cont'].values * process_data['Percent N emitted during composting'].values
            N_loss_as_N2O = N_loss * AD_input.Curing_Bio['ad_pNasN2O']['amount']
            N_loss_as_NH3 = N_loss * AD_input.Curing_Bio['ad_pNasNH3']['amount']
            
            add_LCI('Ammonia', N_loss_as_NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
            add_LCI('Dinitrogen monoxide', N_loss_as_N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
            
            #VOC emission
            VS_loss = AD_input.Curing_Bio['VSlossPerCloss']['amount'] * C_loss / CommonData.MW['C']['amount'] 
            VOC_emitted = VS_loss * process_data['VOC emissions during curing'].values/1000000
            add_LCI('NMVOC, non-methane volatile organic compounds, unspecified origin', VOC_emitted ,LCI)
            
            #Product
            product = deepcopy(flow_init)
            product.data['vs_cont'] = input.data['vs_cont'].values - VS_loss
            product.data['ash_cont'] = input.data['ash_cont'].values
            product.data['sol_cont'] = product.data['vs_cont'].values + product.data['ash_cont'].values
            
            product.data['C_cont']= input.data['C_cont'].values - C_loss
            product.data['N_cont']= input.data['N_cont'].values - N_loss
            product.data['P_cont']= input.data['P_cont'].values
            product.data['K_cont']= input.data['K_cont'].values
            
            #Water
            Water_curing =(WC_SR_Water - AD_input.Material_Properties['ad_mcFC']['amount'] * (WC_SR_Water + WC_SR_solid + product.data['sol_cont'].values) ) \
                            /(AD_input.Material_Properties['ad_mcFC']['amount']-1)
            
            #Product
            product.data['moist_cont'] = Water_curing
            product.data['mass'] = product.data['moist_cont'].values + product.data['sol_cont'].values
            
            #Resource use
            loder_dsl = input.data['mass'].values/1000 * AD_input.Loader['hpFEL']['amount'] * AD_input.Loader['mfFEL']['amount'] * AD_input.AD_operation['ophrsperday']['amount']  
            WC_shred_dsl = AD_input.shredding['Mtgp']['amount'] * AD_input.shredding['Mtgf']['amount'] * WC_SR / 1000
            Windrow_turner_dsl = (WC_SR + input.data['mass'].values)/1000* AD_input.Windrow_turn['Tcur']['amount']*AD_input.Windrow_turn['Mwta']['amount']\
                                    *AD_input.Windrow_turn['turnFreq']['amount'] * AD_input.Windrow_turn['Mwfa']['amount']
            
            add_LCI(('Technosphere', 'Equipment_Diesel'), loder_dsl ,LCI)
            add_LCI(('Technosphere', 'Equipment_Diesel'), WC_shred_dsl ,LCI)
            add_LCI(('Technosphere', 'Equipment_Diesel'), Windrow_turner_dsl ,LCI)
            
        return(product,WC_SR )

### AD Post_screen
def AD_Post_screen(input,input_WC_SR,AD_input,assumed_comp,Material_Properties,LCI,flow_init):
    product = deepcopy(flow_init)
    
    screan_out_mass = input_WC_SR * AD_input.Post_Screen['ad_scrEff_WC']['amount']
    
    Remain_WC = input_WC_SR - screan_out_mass
    Remain_WC_water = Remain_WC * AD_input.Material_Properties['wcMC']['amount']
    Remain_WC_solid = Remain_WC - Remain_WC_water
    Remain_WC_VS = Remain_WC_solid * AD_input.Material_Properties['wcVSC']['amount']
    Remain_WC_Ash = Remain_WC_solid - Remain_WC_VS
    
    #Product
    product = deepcopy(flow_init)
    product.data['vs_cont'] = input.data['vs_cont'].values +  Remain_WC_VS
    product.data['ash_cont'] = input.data['ash_cont'].values + Remain_WC_Ash
    product.data['sol_cont'] = input.data['sol_cont'].values + Remain_WC_solid
    product.data['moist_cont'] = input.data['moist_cont'].values + Remain_WC_water
    product.data['mass'] = product.data['moist_cont'].values + product.data['sol_cont'].values
    product.data['C_cont']= input.data['C_cont'].values   # Does not culculate the carbon in the WC
    product.data['N_cont']= input.data['N_cont'].values
    product.data['P_cont']= input.data['P_cont'].values
    product.data['K_cont']= input.data['K_cont'].values
    
    #Resource use
    Electricity = AD_input.Post_Screen['ad_engScreen']['amount'] * (input.data['mass'].values + input_WC_SR)
    add_LCI(('Technosphere', 'Electricity_consumption'), Electricity ,LCI)
    
    return(product)
    

def POTW (liq_treatment_vol,liq_rem,input_to_reactor,Dig_to_Curing,FinalCompost,index,AD_input,assumed_comp,Material_Properties,CommonData,LCI):
    #Allocation factor
    AF_total={}
    AF_total['COD'] = sum((1-Material_Properties['Moisture Content'].values/100) * assumed_comp * liq_treatment_vol * Material_Properties['Biogenic Carbon Content'].values/100 * 1000)
    AF_total['BOD'] = sum((1-Material_Properties['Moisture Content'].values/100) * assumed_comp * liq_treatment_vol * Material_Properties['Methane Yield'].values)
    AF_total['TSS'] = sum( assumed_comp * liq_treatment_vol )
    AF_total['Total_N']= sum( input_to_reactor.data['N_cont'].values * assumed_comp * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] ) 
    AF_total['Phosphate'] = sum((1-Material_Properties['Moisture Content'].values/100) * assumed_comp * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties['Phosphorus Content'].values/100*1000)
    
    for i in ['Iron','Copper','Cadmium','Arsenic','Mercury','Selenium','Chromium','Lead','Zinc','Barium','Silver']:
        AF_total[i] = sum((1-Material_Properties['Moisture Content'].values/100) * assumed_comp * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties[i].values/100 *1000)

    
    AF={}
    AF['COD'] = (1-Material_Properties['Moisture Content'].values/100) * liq_treatment_vol * Material_Properties['Biogenic Carbon Content'].values/100 * 1000 / AF_total['COD']
    AF['BOD'] = (1-Material_Properties['Moisture Content'].values/100) * liq_treatment_vol * Material_Properties['Methane Yield'].values / AF_total['BOD']
    AF['TSS'] = liq_treatment_vol/AF_total['TSS']
    AF['Total_N'] = input_to_reactor.data['N_cont'].values * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount']/AF_total['Total_N']
    AF['Phosphate'] = (1-Material_Properties['Moisture Content'].values/100) * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties['Phosphorus Content'].values/100 * 1000 / AF_total['Phosphate']
    
    for i in ['Iron','Copper','Cadmium','Arsenic','Mercury','Selenium','Chromium','Lead','Zinc','Barium','Silver']:
        if AF_total[i] == 0:
            AF[i]=0
        else:
            AF[i] = (1-Material_Properties['Moisture Content'].values/100) * FinalCompost.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] * Material_Properties[i].values/100 * 1000 / AF_total[i]
    
    #Emission from POTW
    Emission={}
    Emission['Total_N'] =  input_to_reactor.data['N_cont'].values * (100-AD_input.Dig_prop['perNSolid']['amount'])/100 * liq_rem/(Dig_to_Curing.data['moist_cont'].values+liq_rem) * (1-CommonData.WWT['n_rem']['amount']/100) 
    Emission['Phosphate'] = input_to_reactor.data['sol_cont'].values * Material_Properties['Phosphorus Content'].values/100 * (100-AD_input.Dig_prop['perPSolid']['amount'])/100 * liq_rem/(Dig_to_Curing.data['moist_cont'].values+liq_rem) *(94.97/30.97) * (1-CommonData.WWT['p_rem']['amount']/100) 
    
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
    add_LCI(('Technosphere', 'Internal_Process_Transportation_Heavy_Duty_Diesel_Truck'), AD_input.Digestate_treatment['ad_distPOTW']['amount'] * liq_treatment_vol * 1000 * AD_input.Dig_prop['digliqdens']['amount'] ,LCI)
    add_LCI(('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck'), liq_treatment_vol * AD_input.Dig_prop['digliqdens']['amount'] / AD_input.Digestate_treatment['payload_POTW']['amount']\
            * AD_input.Digestate_treatment['ad_distPOTW']['amount'] * AD_input.Digestate_treatment['ad_erPOTW']['amount'] ,LCI)
    
    add_LCI('Full_Total heavy duty truck tranport', AD_input.Digestate_treatment['wwtp_lf_dist']['amount'] * sludge_prod ,LCI)
    add_LCI(('Technosphere', 'Empty_Return_Heavy_Duty_Diesel_Truck'), AD_input.Digestate_treatment['wwtp_lf_dist']['amount'] * sludge_prod /1000\
            /AD_input.Digestate_treatment['payload_LFPOTW']['amount'] * AD_input.Digestate_treatment['er_wwtpLF']['amount']  ,LCI)
    
    add_LCI(('Technosphere', 'Electricity_consumption'), BOD_removed * CommonData.Leachate_treat['elecBOD']['amount'] ,LCI)


### Apply compost to Land _AD
def AD_compost_use(input,CommonData,process_data,Material_Properties,assumed_comp,AD_input,LCI):
    if AD_input.AD_operation['choice_BU']['amount'] == 1:
        # Carbon in final compost
        C_storage = input.data['C_cont'].values * AD_input.Soil_seq['perCStor']['amount']/100
        C_released = input.data['C_cont'].values - C_storage
        C_storage_hummus_formation = input.data['C_cont'].values * AD_input.Soil_seq['humFormFac']['amount']
        add_LCI('Carbon dioxide, non-fossil _ Land application', C_released * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Direct Carbon Storage and Humus Formation', -(C_storage+C_storage_hummus_formation) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        
        #Nitrogen in final compost
        input.data['N_cont'] = input.data['N_cont'].values * process_data['Percent NPK available as nutrient or emission (in addition to MFE)'].values/100
        input.data['P_cont'] = input.data['P_cont'].values * process_data['Percent NPK available as nutrient or emission (in addition to MFE)'].values/100
        input.data['K_cont'] = input.data['K_cont'].values * process_data['Percent NPK available as nutrient or emission (in addition to MFE)'].values/100
        
        N2O = input.data['N_cont'].values * AD_input.Land_app['perN2Oevap']['amount']/100 
        NH3 = input.data['N_cont'].values * AD_input.Land_app['perNasNH3fc']['amount']/100 * AD_input.Land_app['perNH3evap']['amount']/100
        NO3_GW = input.data['N_cont'].values * CommonData.Land_app['NO3leach']['amount'] 
        NO3_SW = input.data['N_cont'].values * CommonData.Land_app['NO3runoff']['amount'] 
        
        add_LCI('Dinitrogen monoxide', N2O * CommonData.MW['Nitrous_Oxide']['amount']/CommonData.MW['N']['amount']/2 ,LCI)
        add_LCI('Ammonia',NH3 * CommonData.MW['Ammonia']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (ground water)',NO3_GW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Nitrate (Surface water)',NO3_SW * CommonData.MW['Nitrate']['amount']/CommonData.MW['N']['amount'] ,LCI)
        
        
        if AD_input.AD_operation['fertOff']['amount'] == 1:
            # Nutrients availble in the final compost
            Navail = input.data['N_cont'].values * CommonData.Land_app['MFEN']['amount']
            Pavail = input.data['P_cont'].values * CommonData.Land_app['MFEP']['amount'] 
            Kavail = input.data['K_cont'].values * CommonData.Land_app['MFEK']['amount']
            
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
        
        if AD_input.AD_operation['peatOff']['amount'] == 1:
            Peat = input.data['mass'].values/AD_input.Material_Properties['ad_densFC']['amount'] * AD_input.Land_app['ad_densPeat']['amount'] / 1000 \
                    * AD_input.Land_app['ad_PeatSubFac']['amount'] * input.data['C_cont'].values/sum(input.data['C_cont'].values*assumed_comp)
            add_LCI(('Technosphere', 'Peat'), -Peat ,LCI)  
    
    if AD_input.AD_operation['choice_BU']['amount'] == 0:
        # Carbon in final compost
        Max_C_storage = (1-Material_Properties['Moisture Content'].values/100) * Material_Properties['Carbon Storage Factor'].values
        C_storage = np.where( input.data['C_cont'].values * AD_input.Soil_seq['percCStor_LF']['amount']/100 <= Max_C_storage,
                             input.data['C_cont'].values * AD_input.Soil_seq['percCStor_LF']['amount']/100,Max_C_storage)
        
        C_released = (input.data['C_cont'].values - C_storage)/2
        C_CH4 = (input.data['C_cont'].values - C_storage)/2
        C_CH4_Oxidized = C_CH4 * process_data['Percent of Generated Methane oxidized'].values/100
        C_CH4_Flared = C_CH4 * process_data['Percent of Generated Methane Flared'].values/100
        C_CH4_Emitted = C_CH4 * process_data['Percent of Generated Methane Emitted'].values/100
        C_CH4_EnergyRec = C_CH4 * process_data['Percent of Generated Methane used for Energy'].values/100
        C_CH4_Electricity = C_CH4_EnergyRec*CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount']*50/3.6 *0.36 # LHV of Methane: 50 MJ/kg
                
        add_LCI('Direct Carbon Storage and Humus Formation', -(C_storage) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Carbon dioxide, non-fossil _ Land application', (C_released+C_CH4_EnergyRec+C_CH4_Flared+C_CH4_Oxidized) * CommonData.MW['CO2']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI('Methane, non-fossil', C_CH4_Emitted * CommonData.MW['CH4']['amount']/CommonData.MW['C']['amount'] ,LCI)
        add_LCI(('Technosphere', 'Electricity_production'), C_CH4_Electricity ,LCI)
        
        #General emissions from LF
        add_LCI(('Technosphere', 'compost_to_LF'), input.data['mass'].values /1000 ,LCI)
        
        #Amomonium emission from LF (Calculated base on the ammomium/N_cont ratio in LF)
        NH4_GW= 0.0051/100 * input.data['N_cont'].values
        NH4_SW= 0.3597/100 * input.data['N_cont'].values
        add_LCI('Ammonium, ion (ground water)', NH4_GW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)
        add_LCI('Ammonium, ion (surface water)', NH4_SW * CommonData.MW['Ammonium']['amount']/CommonData.MW['N']['amount'] ,LCI)   
 