# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:44:09 2020

@author: msardar2
"""
from PySide2 import QtCore, QtGui, QtWidgets
from Table_from_pandas import *
import os
import PySWOLF
import sys
from brightway2 import *
import importlib  #to import moduls with string name
import pandas as pd
from Distance import *
from project_class import *
from building_matrices import *
from brightway2 import *
from Distance import *
from Required_keys import *
import numpy as np
import pickle
from copy import deepcopy
import ast






class MyQtApp(PySWOLF.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp,self).__init__()
        self.setupUi(self)
        
        self.PySWOLF.setCurrentWidget(self.Basic)
        
        
        ### Initial main window (set Disable and Enabled)
        self.Start.setEnabled(True)
        self.PySWOLF.setCurrentWidget(self.Start)
        self.Basic.setDisabled(True)
        self.Define_SWM.setDisabled(True)
        self.Load_Project.setDisabled(True)
        self.Create_Scenario.setDisabled(True)
        self.LCA_tab.setDisabled(True)
        self.MC_tab.setDisabled(True)
        self.Opt_tab.setDisabled(True)
        self.Treatment_process.setDisabled(True)
        self.Collection_process.setDisabled(True)
        self.Network.setDisabled(True)
        
        ### Start tab
        #Radio bottoms
        self.Start_def_process.setChecked(True)
        self.Start_user_process.clicked.connect(lambda: self.Start_def_process.setChecked(not(self.Start_user_process.isChecked())))
        self.Start_def_process.clicked.connect(lambda: self.Start_user_process.setChecked(not(self.Start_def_process.isChecked())))
        
        #bottoms connection
        self.Start_new_project.clicked.connect(self.Start_new_project_func)
        self.Start_load_project.clicked.connect(self.Start_load_project_func)
        
        
        self.Distance_table.setDisabled(True)
        
        self.Importing_processes()
        
        self.Define_Treatment_Processes()

        self.Create_Treat_prc_dict.clicked.connect(self.Create_Treatment_process_dict)
        
        #Import distance data
        self.Create_Distance.clicked.connect(self.Create_Distance_Table)
        
        #Create system and write project
        self.write_project.clicked.connect(self.write_project_func)
        
        #Load parameters
        self.Load_params.clicked.connect(self.load_params_func)
        
        
        #Update the parameters
        self.update_param.clicked.connect(self.update_network_parameters)
        
        #Create new scenario
        self.Start_new_sen.clicked.connect(self.Create_scenario_func)
        
    
        #Load project tab
        self.load_project_tab()
        
        
        ### Init progess Bar
        self.progressBar_write_project.setMinimum(0)
        self.progressBar_write_project.setMaximum(100)
        self.progressBar_write_project.setValue(0)
        
        
        
        ### Menu
        self.actionSave.triggered.connect(self.save)
        ### Exit
        self.actionExit.triggered.connect(sys.exit)
        
      
    
        



    @QtCore.Slot()  #Change tab: go to the process models or Define SWM system based on the user input
    def Start_new_project_func(self):
        if self.Start_def_process.isChecked():
            self.PySWOLF.setCurrentWidget(self.Define_SWM)
            self.Define_SWM.setEnabled(True)
            self.Import_Process_models_func()
            self._Collection_processes = {}
            self._Treatment_processes = {}
            
            
        else:
            self.PySWOLF.setCurrentWidget(self.Basic)
            self.Basic.setEnabled(True)
                
            
        


    @QtCore.Slot()  #Change tab and import process models
    def Start_load_project_func(self):
        self.PySWOLF.setCurrentWidget(self.Load_Project)
        self.Load_Project.setEnabled(True)      
        
        
        
    
    
    def Importing_processes(self):
        self.init_process_toolbox.setCurrentWidget(self.Landfill)
        # Landfill
        self.helper(self.IT_Default,self.IT_UserDefine,self.IT_BR,self.IT_FName)
        # Waste_to_Energy (WTE)
        self.helper(self.IT_Default_2,self.IT_UserDefine_2,self.IT_BR_2,self.IT_FName_2)
        # Anaerobic Digestion (AD)
        self.helper(self.IT_Default_3,self.IT_UserDefine_3,self.IT_BR_3,self.IT_FName_3)
        # Aerobic Composting (COMP)
        self.helper(self.IT_Default_4,self.IT_UserDefine_4,self.IT_BR_4,self.IT_FName_4)
        # Single Stream Material Facility (SS_MRF)
        self.helper(self.IT_Default_5,self.IT_UserDefine_5,self.IT_BR_5,self.IT_FName_5)
        
        
        # Single Family Collection (SF_Collection)
        self.helper(self.IT_Default_col,self.IT_UserDefine_col,self.IT_BR_col,self.IT_FName_col)
        
        # Multi-Family Collection (MF_Collection)
        self.helper(self.IT_Default_col_2,self.IT_UserDefine_col_2,self.IT_BR_col_2,self.IT_FName_col_2)
        
        # Commercial Collection (COM_Collection)
        self.helper(self.IT_Default_col_3,self.IT_UserDefine_col_3,self.IT_BR_col_3,self.IT_FName_col_3)
        
        
        
        
        
        #Defualt LF input Type
        self.IT_RWC.setChecked(True)
        self.IT_DryRes.setChecked(True)
        self.IT_WetRes.setChecked(True)
        self.IT_MRDO.setChecked(True)
        self.IT_Bottom_Ash.setChecked(True)
        self.IT_Fly_Ash.setChecked(True)
        self.IT_Other_Residual.setChecked(True)
        
        #Defualt WTE input Type
        self.IT_RWC_2.setChecked(True)
        self.IT_DryRes_2.setChecked(True)
        self.IT_WetRes_2.setChecked(True)
        self.IT_MRDO_2.setChecked(True)
        self.IT_Other_Residual_2.setChecked(True)
        
        #Defualt AD input Type
        self.IT_SSO_3.setChecked(True)
        self.IT_SSYW_3.setChecked(True)
        self.IT_SSYWDO_3.setChecked(True)
        self.IT_Separated_Organics_3.setChecked(True)
        
        #Defualt Composting input Type
        self.IT_SSO_4.setChecked(True)
        self.IT_SSYW_4.setChecked(True)
        self.IT_SSYWDO_4.setChecked(True)
        self.IT_Separated_Organics_4.setChecked(True)
        
        
        #Connect the PushButton [ImportProcessModels]
        self.ImportProcessModels.clicked.connect(self.Import_Process_models_func)
        


    # Check to ethier select Default or User Defined option
    def helper(self,IT_Default,IT_UserDefine,IT_BR,IT_FName):
        IT_Default.setChecked(True)
        IT_UserDefine.clicked.connect(lambda: IT_Default.setChecked(not(IT_UserDefine.isChecked())))
        IT_Default.clicked.connect(lambda: IT_UserDefine.setChecked(not(IT_Default.isChecked())))
        IT_BR.clicked.connect(self.select_file(IT_FName,"Python (*.py)"))
    
    def Define_Treatment_Processes(self):
        self._Plist = ['...','LF','WTE','Composting','AD']
        # Fill the Qcomobox for selecting process and Browsing the input file
        for z,x,y in [(self.P1,self.P1_BrInput,self.P1_Name),(self.P2,self.P2_BrInput,self.P2_Name),(self.P3,self.P3_BrInput,self.P3_Name),
                     (self.P4,self.P4_BrInput,self.P4_Name),(self.P5,self.P5_BrInput,self.P5_Name),(self.P6,self.P6_BrInput,self.P6_Name),
                     (self.P7,self.P7_BrInput,self.P7_Name),(self.P8,self.P8_BrInput,self.P8_Name),(self.P9,self.P9_BrInput,self.P9_Name),
                     (self.P10,self.P10_BrInput,self.P10_Name)]:
            z.addItems(self._Plist)
            z.currentTextChanged.connect(self.set_process_name(y,z))
            x.clicked.connect(self.select_file(y,"CSV (*.csv)"))
      
        
        
    @QtCore.Slot()    
    def set_process_name(self,name_place,process):
        def set_name_helper(name):
            if name !='...':
                full_name = process.objectName()+"_"+name
            else:
                full_name = ''
            name_place.setText(full_name)
        return(set_name_helper)
        
        

        
        
    
    @QtCore.Slot()
    def Create_Treatment_process_dict(self):
        for x,y,m,z in [(self.P1.currentText(),self.P1_Name.text(),self.P1_InputName.text(),self.P1_Input_Def.isChecked()),(self.P2.currentText(),self.P2_Name.text(),self.P2_InputName.text(),self.P2_Input_Def.isChecked()),
                    (self.P3.currentText(),self.P3_Name.text(),self.P3_InputName.text(),self.P3_Input_Def.isChecked()),(self.P4.currentText(),self.P4_Name.text(),self.P4_InputName.text(),self.P4_Input_Def.isChecked()),
                    (self.P5.currentText(),self.P5_Name.text(),self.P5_InputName.text(),self.P5_Input_Def.isChecked()),(self.P6.currentText(),self.P6_Name.text(),self.P6_InputName.text(),self.P6_Input_Def.isChecked()),
                    (self.P7.currentText(),self.P7_Name.text(),self.P7_InputName.text(),self.P7_Input_Def.isChecked()),(self.P8.currentText(),self.P8_Name.text(),self.P8_InputName.text(),self.P8_Input_Def.isChecked()),
                    (self.P9.currentText(),self.P9_Name.text(),self.P9_InputName.text(),self.P9_Input_Def.isChecked()),(self.P10.currentText(),self.P10_Name.text(),self.P10_InputName.text(),self.P10_Input_Def.isChecked())]:
            if x == 'LF':
                self._Treatment_processes[y]={}
                if z:
                    self._Treatment_processes[y]['model'] = LF.LF(input_data_path=m)
                else:
                    self._Treatment_processes[y]['model'] = LF.LF()
                self._Treatment_processes[y]['input_type']=self.LF_input_type

            elif x == 'WTE':
                self._Treatment_processes[y]={}
                if z:
                    self._Treatment_processes[y]['model'] = WTE.WTE(input_data_path=m)
                else:
                    self._Treatment_processes[y]['model'] = WTE.WTE()
                self._Treatment_processes[y]['input_type']=self.WTE_input_type

            elif x == 'AD':
                self._Treatment_processes[y]={}
                if z:
                    self._Treatment_processes[y]['model'] = AD.AD(input_data_path=m)
                else:
                    self._Treatment_processes[y]['model'] = AD.AD()
                self._Treatment_processes[y]['input_type']=self.AD_input_type

            elif x == 'Composting':
                self._Treatment_processes[y]={}
                if z:
                    self._Treatment_processes[y]['model'] = COMP.Comp(input_data_path=m)
                else:
                    self._Treatment_processes[y]['model'] = COMP.Comp()
                self._Treatment_processes[y]['input_type']=self.COMP_input_type
        
        #Does include collection
        self.isCollection = QtWidgets.QMessageBox()
        self.isCollection.setIcon(self.isCollection.Icon.Question)
        self.isCollection.setText('System Boundary')
        self.isCollection.setInformativeText('Is the model include collection process?')
        Yes=self.isCollection.addButton(self.isCollection.Yes)
        No=self.isCollection.addButton(self.isCollection.No)
        self.isCollection.exec()
        if self.isCollection.clickedButton()==Yes:
            self.Define_SWM_1.setCurrentWidget(self.Collection_process)
            self.Collection.setCurrentWidget(self.Col1_tab)
            self.Collection_process.setEnabled(True)
            self.init_collection()
        elif self.isCollection.clickedButton()==No:
            self.Define_SWM_1.setCurrentWidget(self.Network)
            self.Collection_process.setDisabled(True)
            self.Network.setEnabled(True)
        
        print(self._Treatment_processes)



            
    

    @QtCore.Slot()  #Change tab and import process models
    def Import_Process_models_func(self):
        self.PySWOLF.setCurrentWidget(self.Define_SWM)
        self.Define_SWM.setEnabled(True)
        self.Define_SWM_1.setCurrentWidget(self.Treatment_process)
        self.Treatment_process.setEnabled(True)
        
        global LF, WTE, AD, COMP, SF_Col
        
        #Import LF
        if self.IT_Default.isChecked():
            LF=importlib.import_module('LF')
        elif self.IT_UserDefine.isChecked():
            LF=importlib.import_module(self.IT_FName.text()[:-3])
        
        #Import WTE
        if self.IT_Default_2.isChecked():
            WTE=importlib.import_module('WTE')
        elif self.IT_UserDefine_2.isChecked():
            WTE=importlib.import_module(self.IT_FName_2.text()[:-3])

        #Import AD
        if self.IT_Default_3.isChecked():
            AD=importlib.import_module('AD')
        elif self.IT_UserDefine_3.isChecked():
            AD=importlib.import_module(self.IT_FName_3.text()[:-3])
            
        #Import COMP
        if self.IT_Default_4.isChecked():
            COMP=importlib.import_module('Composting')
        elif self.IT_UserDefine_4.isChecked():
            COMP=importlib.import_module(self.IT_FName_4.text()[:-3])

        
        #Import SF_Collection
        if self.IT_Default_col.isChecked():
            SF_Col=importlib.import_module('SF_collection')
        elif self.IT_UserDefine_col.isChecked():
            SF_Col=importlib.import_module(self.IT_FName_col.text()[:-3])
            


        self.LF_input_type = []
        for x in [self.IT_RWC,self.IT_SSO,self.IT_DryRes,self.IT_REC,self.IT_WetRes,self.IT_MRDO,self.IT_SSR,
                  self.IT_DSR,self.IT_MSR,self.IT_MSRDO,self.IT_SSYW,self.IT_SSYWDO,self.IT_Bottom_Ash,self.IT_Fly_Ash,
                  self.IT_Other_Residual,self.IT_Separated_Organics,self.IT_OCC,self.IT_Mixed_Paper,self.IT_ONP,
                  self.IT_OFF,self.IT_Fiber_Other,self.IT_PET,self.IT_HDPE_Unsorted,self.IT_HDPE_P,self.IT_HDPE_T,
                  self.IT_Polystyrene,self.IT_Plastic_Other,self.IT_Mixed_Plastic,self.IT_Brown_glass,self.IT_Clear_glass,
                  self.IT_Green_glass,self.IT_Mixed_Glass,self.IT_PVC,self.IT_LDPE_Film,self.IT_Polypropylene]:
            self.helper_1(x,self.LF_input_type)
        
        self.WTE_input_type = []
        for x in [self.IT_RWC_2,self.IT_SSO_2,self.IT_DryRes_2,self.IT_REC_2,self.IT_WetRes_2,self.IT_MRDO_2,self.IT_SSR_2,
                  self.IT_DSR_2,self.IT_MSR_2,self.IT_MSRDO_2,self.IT_SSYW_2,self.IT_SSYWDO_2,self.IT_Bottom_Ash_2,self.IT_Fly_Ash_2,
                  self.IT_Other_Residual_2,self.IT_Separated_Organics_2,self.IT_OCC_2,self.IT_Mixed_Paper_2,self.IT_ONP_2,
                  self.IT_OFF_2,self.IT_Fiber_Other_2,self.IT_PET_2,self.IT_HDPE_Unsorted_2,self.IT_HDPE_P_2,self.IT_HDPE_T_2,
                  self.IT_Polystyrene_2,self.IT_Plastic_Other_2,self.IT_Mixed_Plastic_2,self.IT_Brown_glass_2,self.IT_Clear_glass_2,
                  self.IT_Green_glass_2,self.IT_Mixed_Glass_2,self.IT_PVC_2,self.IT_LDPE_Film_2,self.IT_Polypropylene_2]:
            self.helper_1(x,self.WTE_input_type)

        self.AD_input_type = []
        for x in [self.IT_RWC_3,self.IT_SSO_3,self.IT_DryRes_3,self.IT_REC_3,self.IT_WetRes_3,self.IT_MRDO_3,self.IT_SSR_3,
                  self.IT_DSR_3,self.IT_MSR_3,self.IT_MSRDO_3,self.IT_SSYW_3,self.IT_SSYWDO_3,self.IT_Bottom_Ash_3,self.IT_Fly_Ash_3,
                  self.IT_Other_Residual_3,self.IT_Separated_Organics_3,self.IT_OCC_3,self.IT_Mixed_Paper_3,self.IT_ONP_3,
                  self.IT_OFF_3,self.IT_Fiber_Other_3,self.IT_PET_3,self.IT_HDPE_Unsorted_3,self.IT_HDPE_P_3,self.IT_HDPE_T_3,
                  self.IT_Polystyrene_3,self.IT_Plastic_Other_3,self.IT_Mixed_Plastic_3,self.IT_Brown_glass_3,self.IT_Clear_glass_3,
                  self.IT_Green_glass_3,self.IT_Mixed_Glass_3,self.IT_PVC_3,self.IT_LDPE_Film_3,self.IT_Polypropylene_3]:
            self.helper_1(x,self.AD_input_type)

        self.COMP_input_type = []
        for x in [self.IT_RWC_4,self.IT_SSO_4,self.IT_DryRes_4,self.IT_REC_4,self.IT_WetRes_4,self.IT_MRDO_4,self.IT_SSR_4,
                  self.IT_DSR_4,self.IT_MSR_4,self.IT_MSRDO_4,self.IT_SSYW_4,self.IT_SSYWDO_4,self.IT_Bottom_Ash_4,self.IT_Fly_Ash_4,
                  self.IT_Other_Residual_4,self.IT_Separated_Organics_4,self.IT_OCC_4,self.IT_Mixed_Paper_4,self.IT_ONP_4,
                  self.IT_OFF_4,self.IT_Fiber_Other_4,self.IT_PET_4,self.IT_HDPE_Unsorted_4,self.IT_HDPE_P_4,self.IT_HDPE_T_4,
                  self.IT_Polystyrene_4,self.IT_Plastic_Other_4,self.IT_Mixed_Plastic_4,self.IT_Brown_glass_4,self.IT_Clear_glass_4,
                  self.IT_Green_glass_4,self.IT_Mixed_Glass_4,self.IT_PVC_4,self.IT_LDPE_Film_4,self.IT_Polypropylene_4]:
            self.helper_1(x,self.COMP_input_type)

    # add the checked QCheckBoxes to the list
    def helper_1(self,x,List_of_input_type):
        if x.isChecked():
            List_of_input_type.append(x.text())
            
        

    
    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def select_file(self, LineEdit,Filter):
        self.fileDialog = QtWidgets.QFileDialog()
        def edit_line():
            wdr_path = str(os.getcwd()).replace('\\','/')
            file_name = str(self.fileDialog.getOpenFileName(filter=Filter)[0]).split('/')[-1]
            LineEdit.setText(file_name)
        return(edit_line)







    def init_collection(self):
        self._col_list = ['...','SF_Colllection','MF_Colllection','COM_Colllection']
        self.Col.addItems(self._col_list)
        self.Col_2.addItems(self._col_list)
        self.Col_3.addItems(self._col_list)
        self.Col_4.addItems(self._col_list)
        self.Col_5.addItems(self._col_list)
        self.Col.activated.connect(self.create_col_scheme(self.Sch_Col,self.Col))
        self.Col_2.activated.connect(self.create_col_scheme(self.Sch_Col_2,self.Col_2))
        self.Col_3.activated.connect(self.create_col_scheme(self.Sch_Col_3,self.Col_3))
        self.Col_4.activated.connect(self.create_col_scheme(self.Sch_Col_4,self.Col_4))
        self.Col_5.activated.connect(self.create_col_scheme(self.Sch_Col_5,self.Col_5))
        
        collection_1_scheme_pd = pd.DataFrame(columns=['Index','RWC','SSO_DryRes','REC_WetRes','MRDO'])
        collection_1_scheme_pd['Index']=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']
        collection_1_scheme_pd.iloc[0]=['Contribution',0,0,0,0]
        self.collection_1_scheme_model = Table_modeifed_collection_schm(collection_1_scheme_pd)
        self.Sch_Col.setModel(self.collection_1_scheme_model)
        self.Sch_Col.resizeColumnsToContents()
        self.Sch_Col.setDisabled(True)
        
        collection_2_scheme_pd = pd.DataFrame(columns=['Index','RWC','SSO_DryRes','REC_WetRes','MRDO'])
        collection_2_scheme_pd['Index']=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']
        collection_2_scheme_pd.iloc[0]=['Contribution',0,0,0,0]
        self.collection_2_scheme_model = Table_modeifed_collection_schm(collection_2_scheme_pd)
        self.Sch_Col_2.setModel(self.collection_2_scheme_model)
        self.Sch_Col_2.resizeColumnsToContents()
        self.Sch_Col_2.setDisabled(True)

        collection_3_scheme_pd = pd.DataFrame(columns=['Index','RWC','SSO_DryRes','REC_WetRes','MRDO'])
        collection_3_scheme_pd['Index']=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']
        collection_3_scheme_pd.iloc[0]=['Contribution',0,0,0,0]
        self.collection_3_scheme_model = Table_modeifed_collection_schm(collection_3_scheme_pd)
        self.Sch_Col_3.setModel(self.collection_3_scheme_model)
        self.Sch_Col_3.resizeColumnsToContents()
        self.Sch_Col_3.setDisabled(True)

        collection_4_scheme_pd = pd.DataFrame(columns=['Index','RWC','SSO_DryRes','REC_WetRes','MRDO'])
        collection_4_scheme_pd['Index']=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']
        collection_4_scheme_pd.iloc[0]=['Contribution',0,0,0,0]
        self.collection_4_scheme_model = Table_modeifed_collection_schm(collection_4_scheme_pd)
        self.Sch_Col_4.setModel(self.collection_4_scheme_model)
        self.Sch_Col_4.resizeColumnsToContents()
        self.Sch_Col_4.setDisabled(True)

        collection_5_scheme_pd = pd.DataFrame(columns=['Index','RWC','SSO_DryRes','REC_WetRes','MRDO'])
        collection_5_scheme_pd['Index']=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']
        collection_5_scheme_pd.iloc[0]=['Contribution',0,0,0,0]
        self.collection_5_scheme_model = Table_modeifed_collection_schm(collection_5_scheme_pd)
        self.Sch_Col_5.setModel(self.collection_5_scheme_model)
        self.Sch_Col_5.resizeColumnsToContents()
        self.Sch_Col_5.setDisabled(True)        
        
        self.Create_treatment_process.clicked.connect(self.Create_collection_dict)
        
        
                

    @QtCore.Slot()        
    def Create_collection_dict(self):
        for x,y,z in [(self.Col.currentText(),self.Col_name.text(),self.collection_1_scheme_model._data),
                        (self.Col_2.currentText(),self.Col_name_2.text(),self.collection_2_scheme_model._data),
                        (self.Col_3.currentText(),self.Col_name_3.text(),self.collection_3_scheme_model._data),
                        (self.Col_4.currentText(),self.Col_name_4.text(),self.collection_4_scheme_model._data),
                        (self.Col_5.currentText(),self.Col_name_5.text(),self.collection_5_scheme_model._data)]:
            if x == 'SF_Colllection':
                self._Collection_processes[y]={}
                self._Collection_processes[y]['input_type']=[]
                self._Collection_processes[y]['model']=None
      
        self.Define_SWM_1.setCurrentWidget(self.Network)
        self.Network.setEnabled(True)
        print(self._Collection_processes)
        
        
    def helper_DFtoDict(self,DF):
        DF= DF.replace(np.nan,0)
        Collection_scheme={}
        for i in ['RWC','SSO_DryRes','REC_WetRes','MRDO']:
            Collection_scheme[i]={}
            Collection_scheme[i]['Contribution']=DF[i][0]
            Collection_scheme[i]['separate_col']={}
            for j in [1,2,3,4,5,6]:
                Collection_scheme[i]['separate_col'][DF['Index'][j]]=DF[i][j]
        return(Collection_scheme)
                
            
            
            
    
                    
                    
                
        

            
    @QtCore.Slot()        
    def create_col_scheme(self,table,col):
        def helper_3():
            if col.currentIndex()!=0:
                table.setEnabled(True)
            else:
                table.setEnabled(False)
        return(helper_3)
    



        


    @QtCore.Slot()
    def Create_Distance_Table(self):
        self.Distance_table.setEnabled(1)
        columns = ['Index'] + [x for x in self._Treatment_processes.keys()] + [x for x in self._Collection_processes.keys()]
        Distance = pd.DataFrame(columns=columns)
        Distance['Index'] = [x for x in self._Treatment_processes.keys()] + [x for x in self._Collection_processes.keys()]        
        self.Dis_data = Table_modeifed_distanceTable(Distance)
        self.Distance_table.setModel(self.Dis_data)
        self.Distance_table.resizeColumnsToContents()

        
        
    @QtCore.Slot()
    def write_project_func(self):
        self.P_Name=self.Project_Name.text()
        self.progressBar_write_project.setValue(5)
        Distance_Data=self.Dis_data._data.set_index('Index')
        self.distance = Distance(Data=Distance_Data)
        
        
        if len(self._Collection_processes)>0:
            for x,y,m,z,k in [(self.Col.currentText(),self.Col_name.text(),self.Col_def_input.isChecked(),self.Col_input_path.text(),self.collection_1_scheme_model._data),
                            (self.Col_2.currentText(),self.Col_name_2.text(),self.Col_def_input_2.isChecked(),self.Col_input_path_2.text(),self.collection_2_scheme_model._data),
                            (self.Col_3.currentText(),self.Col_name_3.text(),self.Col_def_input_3.isChecked(),self.Col_input_path_3.text(),self.collection_3_scheme_model._data),
                            (self.Col_4.currentText(),self.Col_name_4.text(),self.Col_def_input_4.isChecked(),self.Col_input_path_4.text(),self.collection_4_scheme_model._data),
                            (self.Col_5.currentText(),self.Col_name_5.text(),self.Col_def_input_5.isChecked(),self.Col_input_path_5.text(),self.collection_5_scheme_model._data)]:
                if x == 'SF_Colllection':
                    if m:
                        self._Collection_processes[y]['model'] = SF_Col.SF_Col(y,self.helper_DFtoDict(k),self._Treatment_processes,Distance=self.distance)
                    else:
                        self._Collection_processes[y]['model'] = SF_Col.SF_Col(y,self.helper_DFtoDict(k),self._Treatment_processes,Distance=self.distance)
            
            print(self._Collection_processes)
        
        
        self.demo = project(self.P_Name,self._Treatment_processes,self.distance,self._Collection_processes)
        self.demo.init_project('SWOLF_AccountMode_LCI DATA.csv')
        self.demo.write_project()
        self.progressBar_write_project.setValue(30)
        self.demo.group_exchanges()
        self.progressBar_write_project.setValue(100)
        
        
        


    @QtCore.Slot()
    def load_params_func(self):
        param_data=pd.DataFrame(self.demo.parameters_list)
        self.param_data = Table_from_pandas_editable(param_data)
        self.Param_table.setModel(self.param_data)
        self.Param_table.resizeColumnsToContents()





        

    @QtCore.Slot()
    def update_network_parameters(self):
        new_param = deepcopy(self.demo.parameters_list)
        i=0
        for x in new_param:
            x['amount'] = self.param_data._data['amount'][i]
            i+=1
        print("\n\n New parameters are : \n",new_param,"\n\n")
        self.demo.update_parameters(new_param)
        self.PySWOLF.setCurrentWidget(self.Create_Scenario)
        self.Create_Scenario.setEnabled(True)
        self.LCA_tab.setEnabled(True)
        self.LCA_tab_init()




    @QtCore.Slot()
    def Create_scenario_func(self):
        self._column_name_def_scenario = ['process','name','amount']
        self.Process.addItems(['...']+[x for x in self.demo.Treatment_processes.keys()])
        self.act_included = pd.DataFrame(columns=self._column_name_def_scenario)
        self.j=0
        self.Process.currentIndexChanged.connect(self.load_Waste_fraction)
        self.Add_act_to_scen.clicked.connect(self.add_act_to_scenario)
        self.Clear_act.clicked.connect(self.delect_act_included)
        self.Create_scenario.clicked.connect(self.create_new_scenario)
            
    
    @QtCore.Slot(int)
    def load_Waste_fraction(self,i):
        if i ==0:
            return(None)
        else:
            process=[x for x in self.demo.Treatment_processes.keys()][i-1]
        self.process_waste=pd.DataFrame(columns=self._column_name_def_scenario)
        self.process_waste['name'] = MSW_Fractions
        self.process_waste['process'] = process
        self.process_WF = Table_from_pandas_editable(self.process_waste)
        self.act_in_process_table.setModel(self.process_WF)
        self.act_in_process_table.resizeColumnsToContents()
     
    @QtCore.Slot()
    def add_act_to_scenario(self):
        for i in range(len(self.process_WF._data['name'])):
            if self.process_WF._data['amount'][i] != 0 and not np.isnan(self.process_WF._data['amount'][i]):
                self.act_included.loc[self.j]=self.process_WF._data.iloc[i]
                self.j+=1
        self.Included_act_table.setEnabled(1)
        self.Inc_act_table = Table_from_pandas(self.act_included)
        self.Included_act_table.setModel(self.Inc_act_table)
        self.Included_act_table.resizeColumnsToContents()
        
            
    @QtCore.Slot()
    def delect_act_included(self):
        self.act_included = pd.DataFrame(columns=self._column_name_def_scenario)
        self.j=0
        self.Inc_act_table = Table_from_pandas(self.act_included)
        self.Included_act_table.setModel(self.Inc_act_table)
        self.Included_act_table.resizeColumnsToContents()
        self.Included_act_table.setDisabled(1)

    
    @QtCore.Slot()
    def create_new_scenario(self):
        scenario = {}
        for i in range(len(self.Inc_act_table._data['process'])):
            if self.Inc_act_table._data['process'][i] not in scenario.keys():
                scenario[self.Inc_act_table._data['process'][i]]={}
                scenario[self.Inc_act_table._data['process'][i]][self.Inc_act_table._data['name'][i]]= float(self.Inc_act_table._data['amount'][i])
            else:
                scenario[self.Inc_act_table._data['process'][i]][self.Inc_act_table._data['name'][i]]= float(self.Inc_act_table._data['amount'][i])
        print('\n \n \n new scenario \n',scenario,'\n\n\n')
        self.demo.process_start_scenario(scenario,self.Name_new_scenario.text())


    def LCA_tab_init(self):
        projects.set_current(self.demo.project_name)
        self.DB_name_list = [x for x in databases]
        self.DB_name_list.sort()
        self.LCA_DataBase.setMaxVisibleItems(1000)
        self.LCA_DataBase.addItems(['...']+self.DB_name_list)
        self.LCA_DataBase.currentIndexChanged.connect(self.load_db)
        list_methods = [str(x) for x in methods]
        list_methods.sort()
        self.LCA_method.addItems(['...']+list_methods)
        self.LCA_Filter_impacts.clicked.connect(self.LCA_Filter)
        self.LCA_Load_method.clicked.connect(self.LCA_Load_method_func)
        self.LCA_bottom.clicked.connect(self.LCA_bottom_func)
        
    

    @QtCore.Slot(int)
    def load_db(self,i):
        if i ==0:
            return(None)
        else:
            db=Database(self.DB_name_list[i-1])
        #acts = [x.as_dict()['name'] for x in db]
        acts = [str(x.key[1]) for x in db]
        acts.sort()
        self.LCA_activity.clear()
        self.LCA_activity.addItems(acts)
        
    @QtCore.Slot()
    def LCA_Filter(self):
        self.LCA_method.clear()
        list_methods= [str(x) for x in methods if self.Filter_impact_keyword.text() in str(x)]
        list_methods.sort()
        self.LCA_method.addItems(['...']+list_methods)
        

    @QtCore.Slot()
    def LCA_Load_method_func(self):
        self.lca_method = Method(ast.literal_eval(self.LCA_method.currentText()))
        self.LCA_Impact_unit.setText(self.lca_method.metadata['unit'])
        self.LCA_Num_cfs.setText(str(self.lca_method.metadata['num_cfs']))
        CFS_data = pd.DataFrame(self.lca_method.load(),columns=['Key','Factor'])
        CFS_data.insert(loc=1, column='Name', value=[get_activity(x) for x in CFS_data['Key']])
        self.CFS_table = Table_from_pandas(CFS_data)
        self.LCA_CFs_table.setModel(self.CFS_table)
        self.LCA_CFs_table.resizeColumnsToContents()


    @QtCore.Slot()
    def LCA_bottom_func(self):
        Demand = {(self.LCA_DataBase.currentText(),self.LCA_activity.currentText()):ast.literal_eval(self.LCA_Func_unit.text())}
        self.LCA_lca=LCA(Demand,self.lca_method.name)
        self.LCA_lca.lci()
        self.LCA_lca.lcia()
        self.LCA_score.setText(str(self.LCA_lca.score))
        self.LCA_Impact_unit_2.setText(self.lca_method.metadata['unit'])
        self.LCA_Top_activity.clicked.connect(self.LCA_top_act_func)
        self.LCA_Top_emssions.clicked.connect(self.LCA_top_emission_func)
        
        
    @QtCore.Slot()
    def LCA_top_act_func(self):
        top_act_data=self.LCA_lca.top_activities()
        Activity=[]
        for x in top_act_data:
            Activity.append(x[2].key)
        top_act_DF = pd.DataFrame(columns=['Activity','Flow','Contribution'])
        top_act_DF['Activity']=Activity
        top_act_DF['Flow']=[x[1] for x in top_act_data]
        top_act_DF['Contribution']=[x[0] for x in top_act_data]
        
        self.top_act_table = Table_from_pandas(top_act_DF)
        self.LCA_top_contribution.setModel(self.top_act_table)
        self.LCA_top_contribution.resizeColumnsToContents()
        
        
        
    @QtCore.Slot()
    def LCA_top_emission_func(self):
        top_emission_data=self.LCA_lca.top_emissions()
        #Activity=[]
        #for x in top_act_data:
            #Activity.append(x[2].key)
        top_emission_DF = pd.DataFrame(columns=['Emission','Flow','Contribution'])
        top_emission_DF['Emission']=[x[2] for x in top_emission_data]
        top_emission_DF['Flow']=[x[1] for x in top_emission_data]
        top_emission_DF['Contribution']=[x[0] for x in top_emission_data]
        
        self.top_emission_table = Table_from_pandas(top_emission_DF)
        self.LCA_top_contribution.setModel(self.top_emission_table)
        self.LCA_top_contribution.resizeColumnsToContents()
    
    




    def load_project_tab(self):
        self.Br_Project_btm.clicked.connect(self.select_file(self.Project_address,"Pickle (*.pickle)"))
        self.Load_Project_btm.clicked.connect(self.load_project_info)
    
    
    @QtCore.Slot()
    def load_project_info(self):
        self.demo = pickle.load(open(self.Project_address.text(),"rb"))
        self.load_P_name.setText(self.demo.project_name) 
        self.P_Name = self.demo.project_name
        projects.set_current(self.demo.project_name)
        
        data = pd.DataFrame(columns=['Name','Type of input','model']) 
        Name = []
        Type_of_Input = []
        Model=[]
        for i in self.demo.Treatment_processes.keys():
            Name.append(i)
            Type_of_Input.append(self.demo.Treatment_processes[i]['input_type'])
            Model.append(self.demo.Treatment_processes[i]['model'])
        data['Name'] = Name
        data['Type of input'] = Type_of_Input
        data['model'] = Model
        
        data_table = Table_from_pandas(data)
        self.load_treatment_info.setModel(data_table)
        self.load_treatment_info.resizeColumnsToContents()
        
        param_data=pd.DataFrame(self.demo.parameters_list)
        self.load_param_data = Table_from_pandas_editable(param_data)
        self.load_Param_table.setModel(self.load_param_data)
        self.load_Param_table.resizeColumnsToContents()
        self.load_update_param.clicked.connect(self.load_update_network_parameters)
        
        self.Create_Scenario.setEnabled(True)
        self.LCA_tab.setEnabled(True)
        self.LCA_tab_init()
                
                
    @QtCore.Slot()
    def load_update_network_parameters(self):
        new_param = deepcopy(self.demo.parameters_list)
        i=0
        for x in new_param:
            x['amount'] = self.load_param_data._data['amount'][i]
            i+=1
        print("\n\n New parameters are : \n",new_param,"\n\n")
        self.demo.update_parameters(new_param)
        
            
        
        
        
        
        
        
    @QtCore.Slot()
    def save(self):
        file = open(self.P_Name+'.pickle', 'wb')
        pickle.dump(self.demo, file)
        
   

           
# =============================================================================
#         self.db_activities=pd.DataFrame(columns=['name','unit','amount'])
#         name=[]
#         unit=[]
#         for x in db:
#             xdict = x.as_dict()
#             name.append(xdict['name'])
#             unit.append(xdict['unit'])
#         self.db_activities['name']=name
#         self.db_activities['unit']=unit
#         self.db_act = Table_from_pandas_editable(self.db_activities)
#         self.act_in_db_table.setModel(self.db_act)
#         self.act_in_db_table.resizeColumnsToContents()        
# =============================================================================
        
            
            
            
    
       # self.demo.project_name
        #self.demo.parameters_list
        
        qt_app.demo.Distance.Distance
        qt_app.demo.processes
        
        
        
        
         

# =============================================================================
#     @QtCore.Slot()
#     def select_process(self,name):
#         self.__Treatment_processes
#         def sel_proces(index):
#             print(index)
#             print(process)
#             print(self.moj)
#             
#             if index == 0:
#                 process = False
#             else:
#                 #process = self._Plist[index]
#                 process = 'dfhdh'
#             print(process)
#         return(sel_proces)
# =============================================================================
    
    

    
    @QtCore.Slot()
    def mojtaba(self,x):
        print(x)
    
    #@QtCore.Slot()
    #def mojtaba1(self):


        


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app  = MyQtApp()
    qt_app.show()
    app.exec_()

