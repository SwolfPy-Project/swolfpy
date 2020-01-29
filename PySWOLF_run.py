# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:44:09 2020

@author: msardar2
"""
from PySide2 import QtCore, QtGui, QtWidgets
from Table_from_pandas import *
import os
import PySWOLF_1
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






class MyQtApp(PySWOLF_1.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp,self).__init__()
        self.setupUi(self)
        
        self.PySWOLF.setCurrentWidget(self.Basic)
        
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/ICONS/PySWOLF_ICONS/PySWOLF.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
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
        self.Distance_table.setDisabled(True)
        
        ### Start tab
        #Radio bottoms
        self.Start_def_process.setChecked(True)
        self.Start_user_process.clicked.connect(lambda: self.Start_def_process.setChecked(not(self.Start_user_process.isChecked())))
        self.Start_def_process.clicked.connect(lambda: self.Start_user_process.setChecked(not(self.Start_def_process.isChecked())))
        
        #bottoms connection
        self.Start_new_project.clicked.connect(self.Start_new_project_func)
        self.Start_load_project.clicked.connect(self.Start_load_project_func)
        
        #import process models
        self.Importing_processes()
        
        
        
        
        #Create treatment dict
        self._Plist = ['...','LF','WTE','Composting','AD']
        self.P_index = 1
        # Add process and create dict
        self.Add_process.clicked.connect(self.add_process_func(self.frame_Process_treatment,self.gridLayout_59))
        self.Treat_process_next.clicked.connect(self.Treat_process_next_func)


        
        
        
        
    
        
        
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
        
      
    
        
# =============================================================================
# =============================================================================
    ### First Page
# =============================================================================
# =============================================================================
    @QtCore.Slot()  #Change tab: go to the process models or Define SWM system based on the user input
    def Start_new_project_func(self):
        self._Collection_processes = {}
        self._Treatment_processes = {}
        if self.Start_def_process.isChecked():
            self.Import_Process_models_func()
            self.PySWOLF.setCurrentWidget(self.Define_SWM)
            self.Define_SWM.setEnabled(True)
            
        else:
            self.PySWOLF.setCurrentWidget(self.Basic)
            self.Basic.setEnabled(True)
                           
    @QtCore.Slot()  #Change tab and import process models
    def Start_load_project_func(self):
        self.PySWOLF.setCurrentWidget(self.Load_Project)
        self.Load_Project.setEnabled(True)      
        
        
# =============================================================================
# =============================================================================
    ### Import processes
# =============================================================================
# =============================================================================           
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

    @QtCore.Slot()  #Change tab and import process models
    def Import_Process_models_func(self): 
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

        #Does include collection
        self.isCollection = QtWidgets.QMessageBox()
        self.isCollection.setIcon(self.isCollection.Icon.Question)
        self.isCollection.setWindowTitle('PySWOLF')
        self.isCollection.setWindowIcon(self.icon)
        self.isCollection.setText('System Boundary')
        self.isCollection.setInformativeText('Is the model include collection process?')
        Yes=self.isCollection.addButton(self.isCollection.Yes)
        No=self.isCollection.addButton(self.isCollection.No)
        self.isCollection.exec()
        if self.isCollection.clickedButton()==Yes:
            self.PySWOLF.setCurrentWidget(self.Define_SWM)
            self.Define_SWM.setEnabled(True)
            self.Define_SWM_1.setCurrentWidget(self.Collection_process)
            self.Collection.setCurrentWidget(self.Col1_tab)
            self.Collection_process.setEnabled(True)
            self.init_collection()
        elif self.isCollection.clickedButton()==No:
            self.PySWOLF.setCurrentWidget(self.Define_SWM)
            self.Define_SWM.setEnabled(True)
            self.Define_SWM_1.setCurrentWidget(self.Treatment_process)
            self.Collection_process.setDisabled(True)
            self.Treatment_process.setEnabled(True)
    
    # add the checked QCheckBoxes to the list
    def helper_1(self,x,List_of_input_type):
        if x.isChecked():
            List_of_input_type.append(x.text())




# =============================================================================
# =============================================================================
    ### Treatment Processes
# =============================================================================
# =============================================================================    
    def add_process_func(self,frame,gridLayout):
        def add_process_helper():
            Process_Label = QtWidgets.QLabel(frame)
            Process_Label.setObjectName("Process_Label_"+str(self.P_index))
            Process_Label.setText("Process "+str(self.P_index))
            gridLayout.addWidget(Process_Label, self.P_index, 0, 1, 1)

            
            Process = QtWidgets.QComboBox(frame)
            Process.setObjectName("Process_"+str(self.P_index))
            gridLayout.addWidget(Process, self.P_index, 1, 1, 1)
            Process.addItems(self._Plist)
            
       
            Process_Name = QtWidgets.QLineEdit(frame)
            Process_Name.setObjectName("Process_Name_"+str(self.P_index))
            gridLayout.addWidget(Process_Name, self.P_index, 2, 1, 1)
            Process_Name.setPlaceholderText('Enter the name of process')
            

            #Create name for process models
            Process.currentTextChanged.connect(self.set_process_name(Process_Name,self.P_index))
            
            
            
            Type_input = QtWidgets.QCheckBox(frame)
            Type_input.setObjectName("P_"+str(self.P_index)+"_Type_input")
            gridLayout.addWidget(Type_input, self.P_index, 3, 1, 1)
            Type_input.setText('Default')
            #set defualt input
            Type_input.setChecked(True)
            
            
            Br_input = QtWidgets.QToolButton(frame)
            Br_input.setObjectName("P_"+str(self.P_index)+"_Br_input")
            gridLayout.addWidget(Br_input, self.P_index, 4, 1, 1)
            Br_input.setText('Browse')
            
            #Uncheck the defualt input
            Br_input.clicked.connect(lambda: Type_input.setChecked(False))
            
            
            
            Process_path = QtWidgets.QLineEdit(frame)
            Process_path.setObjectName("P_"+str(self.P_index)+"_Process_path")
            gridLayout.addWidget(Process_path, self.P_index, 5, 1, 1)
            Process_path.setPlaceholderText('Enter the file address')
            
            #Browse input and import the address to linedit
            Br_input.clicked.connect(self.select_file(Process_path,"CSV (*.csv)"))
            
            #Number of processes
            self.P_index +=1
            
            #Create Treatment Dictionary
            self.Create_Treat_prc_dict.clicked.connect(self.Create_Treatment_process_dict(Process,Process_Name,Process_path,Type_input,Process_Label))
            
            #Clear
            self.Treat_process_Clear.clicked.connect(self.Treat_process_Clear_func(Process,Process_Name,Process_path,Type_input,Process_Label))
        return(add_process_helper)
    
    @QtCore.Slot()    
    def set_process_name(self,name_place,index):
        def set_name_helper(name):
            if name !='...':
                full_name ='P'+str(index)+"_"+name
            else:
                full_name = ''
            name_place.setText(full_name)
        return(set_name_helper)
        
    @QtCore.Slot()
    def Create_Treatment_process_dict(self,Process,Process_Name,Process_path,Type_input,Process_Label):
        def Create_Treatment_process_dict_helper():
            #Success font
            font1 = QtGui.QFont()
            font1.setBold(True)
            font1.setStrikeOut(False)
            #Error font
            font2 = QtGui.QFont()
            font2.setStrikeOut(True)
            font2.setBold(False)
            
            if Process.currentText()== 'LF':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = LF.LF(input_data_path=Process_path.text())
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = LF.LF()
                self._Treatment_processes[Process_Name.text()]['input_type']=self.LF_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
    
            elif Process.currentText() == 'WTE':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = WTE.WTE(input_data_path=Process_path.text())
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = WTE.WTE()
                self._Treatment_processes[Process_Name.text()]['input_type']=self.WTE_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
    
            elif Process.currentText() == 'AD':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = AD.AD(input_data_path=Process_path.text())
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = AD.AD()
                self._Treatment_processes[Process_Name.text()]['input_type']=self.AD_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
    
            elif Process.currentText() == 'Composting':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = COMP.Comp(input_data_path=Process_path.text())
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = COMP.Comp()
                self._Treatment_processes[Process_Name.text()]['input_type']=self.COMP_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
            
            else:
                Process_Label.setFont(font2)
                
            
            
            
        return(Create_Treatment_process_dict_helper)
          
    @QtCore.Slot()
    def Treat_process_next_func(self):        
        print(self._Treatment_processes)
        self.Define_SWM_1.setCurrentWidget(self.Network)
        self.Network.setEnabled(True)


    @QtCore.Slot()
    def Treat_process_Clear_func(self,Process,Process_Name,Process_path,Type_input,Process_Label):
        def Treat_process_Clear_func_helper():
            Process.setCurrentIndex(0)
            Process_Name.setText("")
            Process_path.setText("")
            Type_input.setChecked(True)
            #Normal font
            font = QtGui.QFont()
            font.setBold(False)
            font.setStrikeOut(False)
            Process_Label.setFont(font)
            if len(self._Treatment_processes)> 0:
                self._Treatment_processes = {}
        return(Treat_process_Clear_func_helper)
            
            
        
            
# =============================================================================
# =============================================================================
    ### General Functions
# =============================================================================
# =============================================================================
    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def select_file(self, LineEdit,Filter):
        self.fileDialog = QtWidgets.QFileDialog()
        def edit_line():
            wdr_path = str(os.getcwd()).replace('\\','/')
            file_name = str(self.fileDialog.getOpenFileName(filter=Filter)[0]).split('/')[-1]
            LineEdit.setText(file_name)
        return(edit_line)
        
    @QtCore.Slot()
    def save(self):
        file = open(self.P_Name+'.pickle', 'wb')
        pickle.dump(self.demo, file)


# =============================================================================
# =============================================================================
    ### Collection
# =============================================================================
# =============================================================================
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
        
        self.Create_Collection_process.clicked.connect(self.Create_collection_dict)
        
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
      
        self.Define_SWM_1.setCurrentWidget(self.Treatment_process)
        self.Treatment_process.setEnabled(True)
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
    


# =============================================================================
# =============================================================================
    ### Write project
# =============================================================================
# =============================================================================
    @QtCore.Slot()
    def Create_Distance_Table(self):
        self.Distance_table.setEnabled(1)
        columns =  [x for x in self._Treatment_processes.keys()] + [x for x in self._Collection_processes.keys()]
        Distance = pd.DataFrame(columns=columns,index=columns)        
        self.Dis_data = Table_modeifed_distanceTable(Distance)
        self.Distance_table.setModel(self.Dis_data)
        self.Distance_table.resizeColumnsToContents()


        
    @QtCore.Slot()
    def write_project_func(self):
        self.P_Name=self.Project_Name.text()
        self.progressBar_write_project.setValue(5)
        self.distance = Distance(Data=self.Dis_data._data)
        
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
        
        #Notift the user that the project has created successfully
        self.project_is_written = QtWidgets.QMessageBox()
        self.project_is_written.setIcon(self.project_is_written.Icon.Information)
        self.project_is_written.setWindowTitle('PySWOLF')
        self.project_is_written.setWindowIcon(self.icon)
        self.project_is_written.setText('Project')
        self.project_is_written.setInformativeText('Project has created successfully')
        Ok=self.project_is_written.addButton(self.project_is_written.Ok)
        self.project_is_written.exec()
        

    @QtCore.Slot()
    def load_params_func(self):
        param_data=pd.DataFrame(self.demo.parameters_list)
        param_data['Unit'] = 'fraction'
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
        self.MC_tab_init()


# =============================================================================
# =============================================================================
    ### Create Scenario
# =============================================================================
# =============================================================================
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

# =============================================================================
# =============================================================================
    ### LCA
# =============================================================================
# =============================================================================
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
        if self.LCA_Top_activity.isChecked():
            self.LCA_top_act_func()
        self.LCA_Top_emssions.clicked.connect(self.LCA_top_emission_func)
        if self.LCA_Top_emssions.isChecked():
            self.LCA_top_emission_func()
        
    @QtCore.Slot()
    def LCA_top_act_func(self):
        top_act_data=self.LCA_lca.top_activities()
        Activity=[]
        Flow_unit=[]
        for x in top_act_data:
            Activity.append(x[2].key)
            Flow_unit.append(x[2].as_dict()['unit'])
        top_act_DF = pd.DataFrame(columns=['Activity','Flow','Flow Unit','Contribution','Unit'])
        top_act_DF['Activity']=Activity
        top_act_DF['Flow']=[x[1] for x in top_act_data]
        top_act_DF['Flow Unit']=Flow_unit
        top_act_DF['Contribution']=[x[0] for x in top_act_data]
        top_act_DF['Unit']=self.lca_method.metadata['unit']
        self.top_act_table = Table_from_pandas(top_act_DF)
        self.LCA_top_contribution.setModel(self.top_act_table)
        self.LCA_top_contribution.resizeColumnsToContents()
        
    @QtCore.Slot()
    def LCA_top_emission_func(self):
        top_emission_data=self.LCA_lca.top_emissions()
        Emission=[]
        Compartment=[]
        Flow_unit=[]
        for x in top_emission_data:
            Emission.append(x[2].as_dict()['name'])
            Compartment.append(x[2].as_dict()['categories'])
            Flow_unit.append(x[2].as_dict()['unit'])
            
        top_emission_DF = pd.DataFrame(columns=['Emission','Compartment','Flow','Flow Unit','Contribution','Unit'])
        top_emission_DF['Emission']=Emission
        top_emission_DF['Compartment']=Compartment
        top_emission_DF['Flow']=[x[1] for x in top_emission_data]
        top_emission_DF['Flow Unit']=Flow_unit
        top_emission_DF['Contribution']=[x[0] for x in top_emission_data]
        top_emission_DF['Unit']=self.lca_method.metadata['unit']
        
        self.top_emission_table = Table_from_pandas(top_emission_DF)
        self.LCA_top_contribution.setModel(self.top_emission_table)
        self.LCA_top_contribution.resizeColumnsToContents()
    

# =============================================================================
# =============================================================================
    ### Load Project
# =============================================================================
# =============================================================================
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
        param_data['Unit'] = 'fraction'
        self.load_param_data = Table_from_pandas_editable(param_data)
        self.load_Param_table.setModel(self.load_param_data)
        self.load_Param_table.resizeColumnsToContents()
        self.load_update_param.clicked.connect(self.load_update_network_parameters)
        
        self.Create_Scenario.setEnabled(True)
        self.LCA_tab.setEnabled(True)
        self.LCA_tab_init()
        self.MC_tab_init()
        
        
                
    @QtCore.Slot()
    def load_update_network_parameters(self):
        new_param = deepcopy(self.demo.parameters_list)
        i=0
        for x in new_param:
            x['amount'] = self.load_param_data._data['amount'][i]
            i+=1
        print("\n\n New parameters are : \n",new_param,"\n\n")
        self.demo.update_parameters(new_param)
        
            
# =============================================================================
# =============================================================================
    ### Monte-Carlo Simulation
# =============================================================================
# =============================================================================       
    @QtCore.Slot()
    def MC_tab_init(self):
        self.MC_tab.setEnabled(True)
        projects.set_current(self.demo.project_name)
        self.DB_name_list = [x for x in databases]
        self.DB_name_list.sort()
        self.MC_FU_DB.addItems(['...']+self.DB_name_list)
        self.MC_FU_DB.currentIndexChanged.connect(self.MC_load_db_func)
        
        list_methods = [str(x) for x in methods]
        list_methods.sort()
        self.MC_method.setMaxVisibleItems(1000)
        self.MC_method.addItems(['...']+list_methods)
        
        self.MC_Filter_method.clicked.connect(self.MC_Filter_func)
        self.MC_add_method.clicked.connect(self.MC_add_method_func)
        
        self.method_DF = pd.DataFrame(columns=['LCIA method','Unit'])
        self.method_DF_index=0
        
        #SpinBox for number of cpu threads
        self.MC_N_Thread.setMaximum(mp.cpu_count())
        self.MC_N_Thread.setMinimum(1)
        self.MC_N_Thread.stepBy(mp.cpu_count()-2)
        
        #SpinBox for number of runs
        self.MC_N_runs.setMaximum(100000)
        self.MC_N_runs.setMinimum(0)
        self.MC_N_runs.stepBy(100)
        



        self.MC_run.clicked.connect(self.MC_run_func)
        
        
        #List of models include collection, treatment and Common Data
        keys = ['...']+[x for x in self.demo.Treatment_processes.keys()]+[x for x in self.demo.Collection_processes.keys()]
        self.MC_Model.addItems(keys)
        self.MC_Model_load.clicked.connect(self.MC_load_uncertain_func)
        self.MC_uncertain_filter.clicked.connect(self.MC_load_uncertain_func)
    
    
        CheckBoxes = ['CommonData','Parameters']+[x for x in self.demo.Treatment_processes.keys()]+[x for x in self.demo.Collection_processes.keys()]
        self.include_model_dict = dict(zip(CheckBoxes,[False for i in range(len(CheckBoxes))]))
        for x in self.include_model_dict:
            self.create_check_box(x,self.MC_included_models,self.verticalLayout_3)
        

    def create_check_box (self,Name,Frame,Layout):
        checkBox = QtWidgets.QCheckBox(Frame,Layout) 
        checkBox.setObjectName(Name)
        checkBox.setText(Name)
        Layout.addWidget(checkBox)
        checkBox.clicked.connect(self.update_include_act(Name))

    @QtCore.Slot()
    def update_include_act(self,Model):
        def update_include_act_helper():
            self.include_model_dict[Model]= not self.include_model_dict[Model]
        return(update_include_act_helper)
    
    
    @QtCore.Slot(int)
    def MC_load_db_func(self,i):
        if i ==0:
            return(None)
        else:
            db=Database(self.DB_name_list[i-1])
        acts = [str(x.key[1]) for x in db]
        acts.sort()
        self.MC_FU_act.clear()
        self.MC_FU_act.addItems(acts)
        
    @QtCore.Slot()
    def MC_Filter_func(self):
        self.MC_method.clear()
        list_methods= [str(x) for x in methods if self.MC_Filter_keyword.text() in str(x)]
        list_methods.sort()
        self.MC_method.addItems(['...']+list_methods)
    
    @QtCore.Slot()
    def MC_add_method_func(self):
        method = Method(ast.literal_eval(self.MC_method.currentText()))
        self.method_DF.loc[self.method_DF_index]=[method.name,method.metadata['unit']]
        self.method_DF_index+=1
        self.MC_method_table_model = Table_from_pandas(self.method_DF)
        self.MC_method_table.setModel(self.MC_method_table_model)
        self.MC_method_table.resizeColumnsToContents()        
         
    @QtCore.Slot()
    def MC_load_uncertain_func(self):
        if self.MC_Model.currentText() in self.demo.Treatment_processes.keys():
            self.uncertain_data = deepcopy(self.demo.Treatment_processes[self.MC_Model.currentText()]['model'].InputData.Data)
        
        elif self.MC_Model.currentText() in self.demo.Collection_processes.keys():
            self.uncertain_data = deepcopy(self.demo.Collection_processes[self.MC_Model.currentText()]['model'].InputData.Data)
        
        
        if self.MC_uncertain_filter.isChecked():
            MC_Uncertain_model = Table_from_pandas_editable(self.uncertain_data[:][self.uncertain_data['uncertainty_type']>1])
        else:
            MC_Uncertain_model = Table_from_pandas_editable(self.uncertain_data)
        self.MC_Uncertain_table.setModel(MC_Uncertain_model)
        self.MC_Uncertain_table.resizeColumnsToContents()            
            
    @QtCore.Slot()
    def MC_run_func(self):
        projects.set_current(self.demo.project_name)
        project = self.demo.project_name
        FU = {(self.MC_FU_DB.currentText(),self.MC_FU_act.currentText()):ast.literal_eval(self.MC_FU_amount.text())}
        method = self.MC_method_table_model._data['LCIA method'].values.tolist()
        process_models = list()
        process_model_names = list()
        
        Treatment_processes = deepcopy(self.demo.Treatment_processes)
        Collection_processe = deepcopy(self.demo.Collection_processes)
        
        for x in self.include_model_dict:
            if self.include_model_dict[x]:
                if x in Treatment_processes.keys():
                    process_models.append(Treatment_processes[x]['model'])
                    process_model_names.append(x)
                
                if x in Collection_processe.keys():
                    process_models.append(Collection_processe[x]['model'])
                    process_model_names.append(x)
            
        
        print("""
              
#########    Setup Monte Carlo Simulatio    ############
  
    Functional Unit = {FU}
  
    Methods = {method}
  
    Number of threads = {Nthread}
  
    Number of runs = {nruns}
  
### Moldes included
    
  Names: {process_model_names}
  
  Models: {process_models}
  
#################################             
              """.format(FU=FU,method=method,Nthread=int(self.MC_N_Thread.text()),nruns=int(self.MC_N_runs.text()),
                          process_model_names=process_model_names,process_models=process_models))
        
        
        Monte_carlo = ParallelData(FU, method, project,process_models=process_models,process_model_names=process_model_names,seed = 1)

        Monte_carlo.run(int(self.MC_N_Thread.text()),int(self.MC_N_runs.text()))
        self.resultssss = Monte_carlo.result_to_DF()
        print(self.resultssss)
        








# =============================================================================
#     Index(['Category', 'Dictonary_Name', 'Parameter', 'Name', 'amount', 'unit',
#        'uncertainty_type', 'loc', 'scale', 'shape', 'minimum', 'maximum',
#        'Reference', 'Comment'],
#       dtype='object')    
# =============================================================================
        

        
   

           
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

