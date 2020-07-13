# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:44:09 2020

@author: msardar2
"""
# Import UI
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem, QWebEngineProfile
from .Table_from_pandas import *
from . import MC_ui
from . import adv_opt_ui
from . import PySWOLF_ui

# Import Top level
import os
import io
import csv
import sys
import ast
import pickle
import importlib  #to import moduls with string name

# Import Brightway
from brightway2 import *
from bw2analyzer import ContributionAnalysis

# Import General
import pandas as pd
import numpy as np
from time import time
from copy import deepcopy
from pathlib import Path

# Import matplotlin
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Import swolfpy
from swolfpy_processmodels import Distance
from ..Project import *
from ..Optimization import *
from ..Monte_Carlo import *


from .Workers import * 

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    
    def writelines(self, texts):
        for text in texts:
            self.textWritten.emit(str(text))
    

    

class MyQtApp(PySWOLF_ui.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp,self).__init__()
        self.setupUi(self)
        self.init_app()
        
        #self.cursor = self.Terminal.textCursor()
        #self.cursor.movePosition(QtGui.QTextCursor.Start)
        #Emitting_stream=  EmittingStream()
        #sys.stdout.write = Emitting_stream.write
        #sys.stdout.writelines = Emitting_stream.writelines
        #sys.stderr.write = Emitting_stream.write
        #sys.stderr.writelines = Emitting_stream.writelines
        #Emitting_stream.textWritten.connect(self.onUpdateText)

# =============================================================================
#     def helprrrr(self):
#         self.cursor.movePosition(QtGui.QTextCursor.StartOfLine)
#         self.cursor.select(QtGui.QTextCursor.LineUnderCursor)
#         self.cursor.removeSelectedText()
#         self.cursor.movePosition(QtGui.QTextCursor.End)
# =============================================================================
    

    
    def onUpdateText(self, text):
        self.cursor.insertText(text)
        self.Terminal.setTextCursor(self.cursor)
        self.Terminal.ensureCursorVisible()   
        self.cursor.movePosition(QtGui.QTextCursor.End)
        

# =============================================================================
# PySide2.QtCore.QObject.eventFilter(watched, event)
# Filters events if this object has been installed as an event filter for the watched object.
# In your reimplementation of this function, if you want to filter the event out, i.e. stop it being
# handled further, return true; otherwise return false.
# Notice in the code blow that unhandled events are passed to the base class’s function,
# since the base class might have reimplemented for its own internal purposes
# =============================================================================

    
        
        
         
#%% Init app
# =============================================================================
# =============================================================================
    ### Init app
# =============================================================================
# =============================================================================
    def init_app(self):
        ### Initial main window (set Disable and Enabled)
        self.PySWOLF.setCurrentWidget(self.Basic)
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
        
        
        #Status: Is the tap initiated or not?!
        self.app_init_status = False
        self.ini_load_project_status = False
        self.init_CreateScenario_status = False
        self.LCA_tab_init_status = False
        self.MC_tab_init_status = False
        self.Opt_tab_init_status = False
        self.LCAResults_tab_init_status = False
        self.LCA_Contribution_tab_init_status = False
        self.LCA_LCI_tab_init_status = False
        
        
        
    
        
        #init First paer
        self.init_FirstPage()  
        
        #Icons
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/ICONS/PySWOLF_ICONS/PySWOLF.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        ### Menu
        self.actionSave.triggered.connect(self.save)
        ### Exit
        self.actionExit.triggered.connect(sys.exit)


#%% First Page
# =============================================================================
# =============================================================================
    # First Page
# =============================================================================
# =============================================================================
    def init_FirstPage(self):
        ### Start tab
        #Radio bottoms
        self.Start_def_process.setChecked(True)
        
        #bottoms connection
        self.Start_new_project.clicked.connect(self.Start_new_project_func)
        self.Start_load_project.clicked.connect(self.Start_load_project_func)
        
    
    @QtCore.Slot()  #Change tab: go to the process models or Define SWM system based on the user input
    def Start_new_project_func(self):
        if not self.app_init_status:
            self.app_init_status = True
            #import process models
            self.Importing_processes()
            
            #init treatement processse tab
            self.init_TreatmentProcesses()
            
            #init write project
            self.init_write_project()
            
            self._Collection_processes = {}
            self._Treatment_processes = {}
            
            if self.Start_def_process.isChecked():
                self.Import_Process_models_func()
                self.PySWOLF.setCurrentWidget(self.Define_SWM)
                self.Define_SWM.setEnabled(True)
                
            else:
                self.PySWOLF.setCurrentWidget(self.Basic)
                self.Basic.setEnabled(True)
        else:
            #Notift the user to restart program
            self.msg_popup('swolfpy Mode','Restart the swolfpy to start new project','Warning')
            
                           
    @QtCore.Slot()  #Change tab and import process models
    def Start_load_project_func(self):
        if not self.app_init_status:
            self.app_init_status = True
            #Load project tab
            self.init_load_project_tab()
            self.PySWOLF.setCurrentWidget(self.Load_Project)
            self.Load_Project.setEnabled(True)      
        else:
            #Notift the user to restart program
            self.msg_popup('swolfpy Mode','Restart the swolfpy to load project','Warning')
            

#%% Load Project   
# =============================================================================
# =============================================================================
    ### Load Project
# =============================================================================
# =============================================================================
    def init_load_project_tab(self):
        if not self.ini_load_project_status:
            self.Br_Project_btm.clicked.connect(self.select_file(self.Project_address,"Pickle (*.pickle)"))
            self.Load_Project_btm.clicked.connect(self.load_project_info)
            
            self.load_update_param.clicked.connect(self.load_update_network_parameters)
            self.Show_SWM_Network_Load.clicked.connect(self.show_SWM_Network_func(self.Show_SWM_Network_Load_AllFlows))
            self.Load_params_Load.clicked.connect(self.load_params_func_loadtab)
                    
            self.ini_load_project_status = True
            
            #QTableView
            self.load_treatment_info.installEventFilter(self)
            self.load_treatment_info.setSortingEnabled(True)
            self.load_Param_table.installEventFilter(self)
            self.load_Param_table.setSortingEnabled(True)
            
            self.load_PBar_updateParam.setMinimum(0)
            self.load_PBar_updateParam.setMaximum(100)
            self.load_PBar_updateParam.setValue(0)
            
            self.Show_SWM_Network_Load_AllFlows.setChecked(True)
            
            self.param_status=True
        
    
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
            Model.append(self.demo.Treatment_processes[i]['model'].__class__)
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
        
        self.Create_Scenario.setEnabled(True)
        self.init_CreateScenario()
        self.LCA_tab.setEnabled(True)
        self.LCA_tab_init()
        self.MC_tab_init()
        self.Opt_tab_init()
        
    @QtCore.Slot()
    def load_update_network_parameters(self):
        new_param = deepcopy(self.demo.parameters_list)
        i=0
        for x in new_param:
            x['amount'] = self.load_param_data._data['amount'][i]
            i+=1
        print("\n\n New parameters are : \n",new_param,"\n\n")

        param_updater=Worker_UpdateParam(parent=self.update_param, project=self.demo, param=new_param)
        param_updater.UpdatePBr_UpdateParam.connect(self.load_setPBr_UpdateParam)
        param_updater.report_time.connect(self.load_report_time_UpdateParam)
        param_updater.start()

    @QtCore.Slot(int)
    def load_report_time_UpdateParam(self, time):
        #Notift the user that the project has created successfully
        self.msg_popup('Parameters','Parameters are updated successfully in {} seconds'.format(time),'Information')
        
    @QtCore.Slot(int)
    def load_setPBr_UpdateParam(self, val):
        self.load_PBar_updateParam.setValue(val)

    @QtCore.Slot()
    def load_params_func_loadtab(self):
        param_data=pd.DataFrame(self.demo.parameters_list)
        param_data['Unit'] = 'fraction'
        self.load_Param_table.model()._data = param_data
        self.load_Param_table.model().layoutChanged.emit()
        self.load_Param_table.resizeColumnsToContents()        

#%% Import processes           
# =============================================================================
# =============================================================================
    ### Import processes
# =============================================================================
# =============================================================================           
    def Importing_processes(self):
        self.init_process_toolbox.setCurrentWidget(self.CommonData)
        # CommonData
        self.helper(self.IT_Default_0,self.IT_UserDefine_0,self.IT_BR_0,self.IT_FName_0,"Python (*.py)")
        self.helper(self.IT_Default_00,self.IT_UserDefine_00,self.IT_BR_00,self.IT_FName_00,"CSV (*.csv)")
        
        # Technosphere
        self.helper(self.IT_Default_Tech,self.IT_UserDefine_Tech,self.IT_BR_Tech,self.IT_FName_Tech,"Python (*.py)")
        self.helper(self.IT_Default_LCI,self.IT_UserDefine_LCI,self.IT_BR_LCI,self.IT_FName_LCI,"CSV (*.csv)")
        self.helper(self.IT_Default_LCI_Ref,self.IT_UserDefine_LCI_Ref,self.IT_BR_LCI_Ref,self.IT_FName_LCI_Ref,"CSV (*.csv)")
        self.helper_dir(self.IT_Default_EcoSpold2,self.IT_UserDefine_EcoSpold2,self.IT_BR_EcoSpold2,self.IT_FName_EcoSpold2)
        
        # Landfill
        self.helper(self.IT_Default,self.IT_UserDefine,self.IT_BR,self.IT_FName,"Python (*.py)")
        # Waste_to_Energy (WTE)
        self.helper(self.IT_Default_2,self.IT_UserDefine_2,self.IT_BR_2,self.IT_FName_2,"Python (*.py)")
        # Anaerobic Digestion (AD)
        self.helper(self.IT_Default_3,self.IT_UserDefine_3,self.IT_BR_3,self.IT_FName_3,"Python (*.py)")
        # Aerobic Composting (COMP)
        self.helper(self.IT_Default_4,self.IT_UserDefine_4,self.IT_BR_4,self.IT_FName_4,"Python (*.py)")
        # Single Stream Material Facility (SS_MRF)
        self.helper(self.IT_Default_5,self.IT_UserDefine_5,self.IT_BR_5,self.IT_FName_5,"Python (*.py)")
        # Dual Stream Material Facility (DS_MRF)
        self.helper(self.IT_Default_6,self.IT_UserDefine_6,self.IT_BR_6,self.IT_FName_6,"Python (*.py)")
        # Multi-Stream Material Facility (MS_MRF)
        self.helper(self.IT_Default_7,self.IT_UserDefine_7,self.IT_BR_7,self.IT_FName_7,"Python (*.py)")
        # Reprocessing (REPROC)
        self.helper(self.IT_Default_8,self.IT_UserDefine_8,self.IT_BR_8,self.IT_FName_8,"Python (*.py)")
        
        
        
        # Single Family Collection (SF_Collection)
        self.helper(self.IT_Default_col,self.IT_UserDefine_col,self.IT_BR_col,self.IT_FName_col,"Python (*.py)")
        
        # Multi-Family Collection (MF_Collection)
        self.helper(self.IT_Default_col_2,self.IT_UserDefine_col_2,self.IT_BR_col_2,self.IT_FName_col_2,"Python (*.py)")
        
        # Commercial Collection (COM_Collection)
        self.helper(self.IT_Default_col_3,self.IT_UserDefine_col_3,self.IT_BR_col_3,self.IT_FName_col_3,"Python (*.py)")
        
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
        self.IT_Separated_Organics_3.setChecked(True)
        
        #Defualt Composting input Type
        self.IT_SSO_4.setChecked(True)
        self.IT_SSYW_4.setChecked(True)
        self.IT_SSYWDO_4.setChecked(True)
        self.IT_Separated_Organics_4.setChecked(True)
        
        #Defualt SS_MRF input Type
        self.IT_SSR_5.setChecked(True)
        
        #Defualt DS_MRF input Type
        self.IT_DSR_6.setChecked(True)
        
        #Defualt MS_MRF input Type
        self.IT_REC_7.setChecked(True)
        self.IT_MSR_7.setChecked(True)
        self.IT_MSRDO_7.setChecked(True)
        
        #Defualt REPROC input Type
        self.IT_OCC_8.setChecked(True)
        self.IT_Mixed_Paper_8.setChecked(True)
        self.IT_ONP_8.setChecked(True)
        self.IT_OFF_8.setChecked(True)
        self.IT_Fiber_Other_8.setChecked(True)
        self.IT_PET_8.setChecked(True)
        self.IT_HDPE_Unsorted_8.setChecked(True)
        self.IT_HDPE_P_8.setChecked(True)
        self.IT_HDPE_T_8.setChecked(True)
        self.IT_Polystyrene_8.setChecked(True)
        self.IT_Plastic_Other_8.setChecked(True)
        self.IT_Mixed_Plastic_8.setChecked(True)
        self.IT_Brown_glass_8.setChecked(True)
        self.IT_Clear_glass_8.setChecked(True)
        self.IT_Green_glass_8.setChecked(True)
        self.IT_Mixed_Glass_8.setChecked(True)
        self.IT_PVC_8.setChecked(True)
        self.IT_LDPE_Film_8.setChecked(True)
        self.IT_Polypropylene_8.setChecked(True)
        self.IT_Fe_8.setChecked(True)
        self.IT_Al_8.setChecked(True)
        self.IT_Cu_8.setChecked(True)

        
        #Connect the PushButton [ImportProcessModels]
        self.ImportProcessModels.clicked.connect(self.Import_Process_models_func)
        
    # Check to ethier select Default or User Defined option
    def helper(self,IT_Default,IT_UserDefine,IT_BR,IT_FName,Filter):
        IT_Default.setChecked(True)
        IT_BR.clicked.connect(self.select_file(IT_FName,Filter))
        IT_BR.clicked.connect((lambda : IT_UserDefine.setChecked(True)))
    
    # Check to ethier select Default or User Defined option
    def helper_dir(self,IT_Default,IT_UserDefine,IT_BR,IT_FName):
        IT_Default.setChecked(True)
        IT_BR.clicked.connect(self.select_dir(IT_FName))
        IT_BR.clicked.connect((lambda : IT_UserDefine.setChecked(True)))
    

    @QtCore.Slot()  #Change tab and import process models
    def Import_Process_models_func(self): 
        global LF, WTE, AD, COMP, SF_Col, SS_MRF, CommonData, REPROC, Technosphere

        #Import CommonData
        if self.IT_Default_0.isChecked():
            import swolfpy_inputdata.CommonData as CommonData
        elif self.IT_UserDefine_0.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_0.text()[:-3].split('/')[-1]
            CommonData=importlib.import_module(path)
        CommonData=CommonData
        
        #Import Technosphere
        if self.IT_Default_Tech.isChecked():
            import swolfpy.Technosphere as Technosphere
        elif self.IT_UserDefine_Tech.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_Tech.text()[:-3].split('/')[-1]
            Technosphere=importlib.import_module(path)
        Technosphere=Technosphere
        
        #Import LF
        if self.IT_Default.isChecked():
            import swolfpy_processmodels.LF as LF
        elif self.IT_UserDefine.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName.text()[:-3].split('/')[-1]
            LF=importlib.import_module(path)
        LF=LF
        #Import WTE
        if self.IT_Default_2.isChecked():
            import swolfpy_processmodels.WTE as WTE
        elif self.IT_UserDefine_2.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_2.text()[:-3].split('/')[-1]
            WTE=importlib.import_module(path)
        WTE=WTE
        #Import AD
        if self.IT_Default_3.isChecked():
            import swolfpy_processmodels.AD as AD
        elif self.IT_UserDefine_3.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_3.text()[:-3].split('/')[-1]
            AD=importlib.import_module(path)
        AD=AD   
        #Import COMP
        if self.IT_Default_4.isChecked():
            import swolfpy_processmodels.Comp as COMP
        elif self.IT_UserDefine_4.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_4.text()[:-3].split('/')[-1]
            COMP=importlib.import_module(path)
        COMP=COMP
        #Import SS_MRF
        if self.IT_Default_5.isChecked():
            import swolfpy_processmodels.SS_MRF as SS_MRF
        elif self.IT_UserDefine_5.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_5.text()[:-3].split('/')[-1]
            SS_MRF=importlib.import_module(path)
        SS_MRF=SS_MRF    
        
        #Import DS_MRF later
        #Import MS_MRF later
        
        #Import REPROC
        if self.IT_Default_8.isChecked():
            import swolfpy_processmodels.Reproc as REPROC
        elif self.IT_UserDefine_8.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_8.text()[:-3].split('/')[-1]
            REPROC=importlib.import_module(path)
        REPROC=REPROC    
        
        
        #Import SF_Collection
        if self.IT_Default_col.isChecked():
            import swolfpy_processmodels.SF_Col as SF_Col
        elif self.IT_UserDefine_col.isChecked():
            path = 'swolfpy.ProcessModels.'+self.IT_FName_col.text()[:-3].split('/')[-1]
            SF_Col=importlib.import_module(path)
        SF_Col=SF_Col    
        
        self.LF_input_type = []
        for x in [self.IT_RWC,self.IT_SSO,self.IT_DryRes,self.IT_REC,self.IT_WetRes,self.IT_MRDO,self.IT_SSR,
                  self.IT_DSR,self.IT_MSR,self.IT_MSRDO,self.IT_SSYW,self.IT_SSYWDO,self.IT_Bottom_Ash,self.IT_Fly_Ash,
                  self.IT_Other_Residual,self.IT_Separated_Organics,self.IT_OCC,self.IT_Mixed_Paper,self.IT_ONP,
                  self.IT_OFF,self.IT_Fiber_Other,self.IT_PET,self.IT_HDPE_Unsorted,self.IT_HDPE_P,self.IT_HDPE_T,
                  self.IT_Polystyrene,self.IT_Plastic_Other,self.IT_Mixed_Plastic,self.IT_Brown_glass,self.IT_Clear_glass,
                  self.IT_Green_glass,self.IT_Mixed_Glass,self.IT_PVC,self.IT_LDPE_Film,self.IT_Polypropylene,
                  self.IT_Fe,self.IT_Al,self.IT_Cu]:
            self.helper_1(x,self.LF_input_type)
        
        self.WTE_input_type = []
        for x in [self.IT_RWC_2,self.IT_SSO_2,self.IT_DryRes_2,self.IT_REC_2,self.IT_WetRes_2,self.IT_MRDO_2,self.IT_SSR_2,
                  self.IT_DSR_2,self.IT_MSR_2,self.IT_MSRDO_2,self.IT_SSYW_2,self.IT_SSYWDO_2,self.IT_Bottom_Ash_2,self.IT_Fly_Ash_2,
                  self.IT_Other_Residual_2,self.IT_Separated_Organics_2,self.IT_OCC_2,self.IT_Mixed_Paper_2,self.IT_ONP_2,
                  self.IT_OFF_2,self.IT_Fiber_Other_2,self.IT_PET_2,self.IT_HDPE_Unsorted_2,self.IT_HDPE_P_2,self.IT_HDPE_T_2,
                  self.IT_Polystyrene_2,self.IT_Plastic_Other_2,self.IT_Mixed_Plastic_2,self.IT_Brown_glass_2,self.IT_Clear_glass_2,
                  self.IT_Green_glass_2,self.IT_Mixed_Glass_2,self.IT_PVC_2,self.IT_LDPE_Film_2,self.IT_Polypropylene_2,
                  self.IT_Fe_2,self.IT_Al_2,self.IT_Cu_2]:
            self.helper_1(x,self.WTE_input_type)

        self.AD_input_type = []
        for x in [self.IT_RWC_3,self.IT_SSO_3,self.IT_DryRes_3,self.IT_REC_3,self.IT_WetRes_3,self.IT_MRDO_3,self.IT_SSR_3,
                  self.IT_DSR_3,self.IT_MSR_3,self.IT_MSRDO_3,self.IT_SSYW_3,self.IT_SSYWDO_3,self.IT_Bottom_Ash_3,self.IT_Fly_Ash_3,
                  self.IT_Other_Residual_3,self.IT_Separated_Organics_3,self.IT_OCC_3,self.IT_Mixed_Paper_3,self.IT_ONP_3,
                  self.IT_OFF_3,self.IT_Fiber_Other_3,self.IT_PET_3,self.IT_HDPE_Unsorted_3,self.IT_HDPE_P_3,self.IT_HDPE_T_3,
                  self.IT_Polystyrene_3,self.IT_Plastic_Other_3,self.IT_Mixed_Plastic_3,self.IT_Brown_glass_3,self.IT_Clear_glass_3,
                  self.IT_Green_glass_3,self.IT_Mixed_Glass_3,self.IT_PVC_3,self.IT_LDPE_Film_3,self.IT_Polypropylene_3,
                  self.IT_Fe_3,self.IT_Al_3,self.IT_Cu_3]:
            self.helper_1(x,self.AD_input_type)

        self.COMP_input_type = []
        for x in [self.IT_RWC_4,self.IT_SSO_4,self.IT_DryRes_4,self.IT_REC_4,self.IT_WetRes_4,self.IT_MRDO_4,self.IT_SSR_4,
                  self.IT_DSR_4,self.IT_MSR_4,self.IT_MSRDO_4,self.IT_SSYW_4,self.IT_SSYWDO_4,self.IT_Bottom_Ash_4,self.IT_Fly_Ash_4,
                  self.IT_Other_Residual_4,self.IT_Separated_Organics_4,self.IT_OCC_4,self.IT_Mixed_Paper_4,self.IT_ONP_4,
                  self.IT_OFF_4,self.IT_Fiber_Other_4,self.IT_PET_4,self.IT_HDPE_Unsorted_4,self.IT_HDPE_P_4,self.IT_HDPE_T_4,
                  self.IT_Polystyrene_4,self.IT_Plastic_Other_4,self.IT_Mixed_Plastic_4,self.IT_Brown_glass_4,self.IT_Clear_glass_4,
                  self.IT_Green_glass_4,self.IT_Mixed_Glass_4,self.IT_PVC_4,self.IT_LDPE_Film_4,self.IT_Polypropylene_4,
                  self.IT_Fe_4,self.IT_Al_4,self.IT_Cu_4]:
            self.helper_1(x,self.COMP_input_type)

        self.SS_MRF_input_type = []
        for x in [self.IT_RWC_5,self.IT_SSO_5,self.IT_DryRes_5,self.IT_REC_5,self.IT_WetRes_5,self.IT_MRDO_5,self.IT_SSR_5,
                  self.IT_DSR_5,self.IT_MSR_5,self.IT_MSRDO_5,self.IT_SSYW_5,self.IT_SSYWDO_5,self.IT_Bottom_Ash_5,self.IT_Fly_Ash_5,
                  self.IT_Other_Residual_5,self.IT_Separated_Organics_5,self.IT_OCC_5,self.IT_Mixed_Paper_5,self.IT_ONP_5,
                  self.IT_OFF_5,self.IT_Fiber_Other_5,self.IT_PET_5,self.IT_HDPE_Unsorted_5,self.IT_HDPE_P_5,self.IT_HDPE_T_5,
                  self.IT_Polystyrene_5,self.IT_Plastic_Other_5,self.IT_Mixed_Plastic_5,self.IT_Brown_glass_5,self.IT_Clear_glass_5,
                  self.IT_Green_glass_5,self.IT_Mixed_Glass_5,self.IT_PVC_5,self.IT_LDPE_Film_5,self.IT_Polypropylene_5,
                  self.IT_Fe_5,self.IT_Al_5,self.IT_Cu_5]:
            self.helper_1(x,self.SS_MRF_input_type)

        #DS_MRF Add later
        #MS_MRF Add later

        self.REPROC_input_type = []
        for x in [self.IT_RWC_8,self.IT_SSO_8,self.IT_DryRes_8,self.IT_REC_8,self.IT_WetRes_8,self.IT_MRDO_8,self.IT_SSR_8,
                  self.IT_DSR_8,self.IT_MSR_8,self.IT_MSRDO_8,self.IT_SSYW_8,self.IT_SSYWDO_8,self.IT_Bottom_Ash_8,self.IT_Fly_Ash_8,
                  self.IT_Other_Residual_8,self.IT_Separated_Organics_8,self.IT_OCC_8,self.IT_Mixed_Paper_8,self.IT_ONP_8,
                  self.IT_OFF_8,self.IT_Fiber_Other_8,self.IT_PET_8,self.IT_HDPE_Unsorted_8,self.IT_HDPE_P_8,self.IT_HDPE_T_8,
                  self.IT_Polystyrene_8,self.IT_Plastic_Other_8,self.IT_Mixed_Plastic_8,self.IT_Brown_glass_8,self.IT_Clear_glass_8,
                  self.IT_Green_glass_8,self.IT_Mixed_Glass_8,self.IT_PVC_8,self.IT_LDPE_Film_8,self.IT_Polypropylene_8,
                  self.IT_Fe_8,self.IT_Al_8,self.IT_Cu_8]:
            self.helper_1(x,self.REPROC_input_type)


        #Does include collection
        self.isCollection = QtWidgets.QMessageBox()
        self.isCollection.setIcon(self.isCollection.Icon.Question)
        self.isCollection.setWindowTitle('swolfpy')
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
            #self.Collection.setCurrentWidget(self.Col1_tab)
            self.Collection_process.setEnabled(True)
            #init collection
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


#%% Collection 
# =============================================================================
# =============================================================================
    ### Collection
# =============================================================================
# =============================================================================
    def init_collection(self):
        self.col_index = 1
        self._col_list = ['...','SF_Colllection','MF_Colllection','COM_Colllection']
        self.Add_col.clicked.connect(self.Add_collection)
        self.Create_Collection_process.clicked.connect(self.Create_collection_dict)
    
    
    def Add_collection(self):
        Tab = QtWidgets.QWidget()
        Tab.setObjectName("Collection_process_{}".format(self.col_index))
        #self.gridLayout_12 = QtWidgets.QGridLayout(Tab)
        self.Collection.addTab(Tab,"Sector {}".format(self.col_index))
        self.Collection.setCurrentWidget(Tab)
    
    
        gridLayout = QtWidgets.QGridLayout(Tab)
        gridLayout.setObjectName("main_layout_{}".format(self.col_index))
        
        Tab_gridLayout = QtWidgets.QGridLayout()
        Tab_gridLayout.setObjectName("Tab_gridLayout_{}".format(self.col_index))
        gridLayout.addLayout(Tab_gridLayout, 0, 0, 1, 1)
        
        # Frame1 for browsing the input
        Frame1 = QtWidgets.QFrame(Tab)
        #Frame1.setMinimumSize(QtCore.QSize(0, 0))
        #Frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #Frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        Frame1.setObjectName("Frame1_{}".format(self.col_index))
        F1_layout = QtWidgets.QGridLayout(Frame1)
        F1_layout.setObjectName("F1_layout_{}".format(self.col_index))
        
        
        # For collection scheme table
        Frame2 = QtWidgets.QFrame(Tab)
        #Frame2.setMinimumSize(QtCore.QSize(0, 0))
        #Frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #Frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        Frame2.setObjectName("Frame2_{}".format(self.col_index))
        F2_layout = QtWidgets.QGridLayout(Frame2)
        F2_layout.setObjectName("F2_layout_{}".format(self.col_index))
        
        
        Tab_gridLayout.addWidget(Frame1, 0, 0, 1, 1)
        Tab_gridLayout.addWidget(Frame2, 1, 0, 1, 1)
        
        
        # setup Frame1
        label_1 = QtWidgets.QLabel(Frame1)
        label_1.setObjectName("Lable_1_{}".format(self.col_index))
        F1_layout.addWidget(label_1, 0, 0, 1, 1)
        label_1.setText('Collection')
        
        label_2 = QtWidgets.QLabel(Frame1)
        label_2.setObjectName("Lable_2_{}".format(self.col_index))
        F1_layout.addWidget(label_2, 0, 1, 1, 1)
        label_2.setText('Type')
        
        label_3 = QtWidgets.QLabel(Frame1)
        label_3.setObjectName("Lable_3_{}".format(self.col_index))
        F1_layout.addWidget(label_3, 0, 2, 1, 1)
        label_3.setText('Name')
        
        label_4 = QtWidgets.QLabel(Frame1)
        label_4.setObjectName("Lable_4_{}".format(self.col_index))
        F1_layout.addWidget(label_4, 0, 3, 1, 1)
        label_4.setText('Input Type')
        
        label_5 = QtWidgets.QLabel(Frame1)
        label_5.setObjectName("Lable_5_{}".format(self.col_index))
        F1_layout.addWidget(label_5, 0, 5, 1, 1)
        label_5.setText('Address to Input File')
        
        label_6 = QtWidgets.QLabel(Frame1)
        label_6.setObjectName("Lable_6_{}".format(self.col_index))
        F1_layout.addWidget(label_6, 1, 0, 1, 1)
        label_6.setText('Collection {}'.format(self.col_index))
    
        col = QtWidgets.QComboBox(Frame1)
        col.setObjectName("Col_{}".format(self.col_index))
        F1_layout.addWidget(col, 1, 1, 1, 1)
        col.addItems(self._col_list)
    
        Col_name = QtWidgets.QLineEdit(Frame1)
        Col_name.setObjectName("Col_name_{}".format(self.col_index))
        F1_layout.addWidget(Col_name, 1, 2, 1, 1)
        Col_name.setPlaceholderText('Collection (Sector) Name')
        
        #Create name for collection models
        col.currentTextChanged.connect(self.set_col_name(Col_name,self.col_index))
        
        Col_def_input = QtWidgets.QCheckBox(Frame1)
        Col_def_input.setObjectName("Col_def_input_{}".format(self.col_index))
        F1_layout.addWidget(Col_def_input, 1, 3, 1, 1)
        Col_def_input.setChecked(True)
        Col_def_input.setText('Default')
        
        Col_Br = QtWidgets.QToolButton(Frame1)
        Col_Br.setObjectName("Col_Br_{}".format(self.col_index))
        F1_layout.addWidget(Col_Br, 1, 4, 1, 1)
        Col_Br.setText('Browse')
    
        #Uncheck the defualt input
        Col_Br.clicked.connect(lambda: Col_def_input.setChecked(False))
        
        Col_input_path = QtWidgets.QLineEdit(Frame1)
        Col_input_path.setEnabled(True)
        Col_input_path.setMinimumSize(QtCore.QSize(300, 0))
        Col_input_path.setObjectName("Col_input_path_{}".format(self.col_index))
        F1_layout.addWidget(Col_input_path, 1, 5, 1, 1)
        Col_input_path.setPlaceholderText('Path to the input file')
        
        #Browse input and import the address to linedit
        Col_Br.clicked.connect(self.select_file(Col_input_path,"CSV (*.csv)"))
        
        # setup Frame2
        Sch_Col = QtWidgets.QTableView(Frame2)
        Sch_Col.setObjectName("Sch_Col_{}".format(self.col_index))
        Sch_Col.setMinimumSize(QtCore.QSize(500, 400))
        F2_layout.addWidget(Sch_Col, 0, 0, 1, 1)
        
        #Collection scheme DataFrame
        col_scheme_pd = pd.DataFrame(columns=['RWC','SSO_DryRes','REC_WetRes','MRDO'],
                                     index=['Contribution','SSR','DSR','MSR','MSRDO','SSYW','SSYWDO'])
        #col_scheme_pd.loc['Contribution']=[0,0,0,0]
        col_scheme_pd=col_scheme_pd.fillna(0)
        col_scheme_pd_model = Table_from_pandas_editable(col_scheme_pd)
        Sch_Col.setModel(col_scheme_pd_model)
        Sch_Col.resizeColumnsToContents()
        Sch_Col.installEventFilter(self)

        
        spacerItem_1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        F2_layout.addItem(spacerItem_1, 0, 1, 1, 1)
        spacerItem_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        F2_layout.addItem(spacerItem_2, 1, 0, 1, 1)
        
        self.col_index+=1
        
    @QtCore.Slot()        
    def Create_collection_dict(self):
        for i in np.arange(1,self.col_index):
            x= self.Collection.findChildren(QtWidgets.QComboBox,"Col_{}".format(i))[0].currentText()
            y= self.Collection.findChildren(QtWidgets.QLineEdit,"Col_name_{}".format(i))[0].text()
            z= self.Collection.findChildren(QtWidgets.QTableView,"Sch_Col_{}".format(i))[0].model()._data
        
            if x != '...':
                self._Collection_processes[y]={}
                self._Collection_processes[y]['input_type']=[]
                self._Collection_processes[y]['model']=None
                self._Collection_processes[y]['scheme'] = self.helper_DFtoDict(z)
                
      
        self.Define_SWM_1.setCurrentWidget(self.Treatment_process)
        self.Treatment_process.setEnabled(True)
        print(self._Collection_processes)
    
    @staticmethod
    def helper_DFtoDict(DF):
        DF= DF.fillna(0)
        Collection_scheme={}
        for i in ['RWC','SSO_DryRes','REC_WetRes','MRDO']:
            Collection_scheme[i]={}
            Collection_scheme[i]['Contribution']=DF[i]['Contribution']
            Collection_scheme[i]['separate_col']={}
            for j in ['SSR','DSR','MSR','MSRDO','SSYW','SSYWDO']:
                Collection_scheme[i]['separate_col'][j]=DF[i][j]
        return(Collection_scheme)
                            
    @QtCore.Slot()    
    def set_col_name(self,name_place,index):
        def set_name_helper(name):
            if name !='...':
                full_name ='Col_'+str(index)
            else:
                full_name = ''
            name_place.setText(full_name)
        return(set_name_helper)



#%% Treatment Processes
# =============================================================================
# =============================================================================
    ### Treatment Processes
# =============================================================================
# =============================================================================    
    def init_TreatmentProcesses(self):
        #Create treatment dict
        self._Plist = ['...','LF','WTE','Composting','AD','SS_MRF','REPROC']
        self.P_index = 1
        
        # Add process and create dict
        self.Add_process.clicked.connect(self.add_process_func(self.frame_Process_treatment,self.gridLayout_101))
        
        #Clear
        self.Treat_process_Clear.clicked.connect(self.Treat_process_Clear_func)
        
        #Create Treatment Dictionary
        self.Create_Treat_prc_dict.clicked.connect(self.Create_Treatment_process_dict)
        
        
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
    def Create_Treatment_process_dict(self):
        #Success font
        font1 = QtGui.QFont()
        font1.setBold(True)
        font1.setStrikeOut(False)
        #Error font
        font2 = QtGui.QFont()
        font2.setStrikeOut(True)
        font2.setBold(False)
        
        input_data_path = self.IT_FName_00.text() if self.IT_UserDefine_00.isChecked() else None
        self.CommonData = CommonData(input_data_path=input_data_path)            
            
        for Index in np.arange(1,self.P_index):
            Process = self.frame_Process_treatment.findChildren(QtWidgets.QComboBox,"Process_"+str(Index))[0]
            Process_Name = self.frame_Process_treatment.findChildren(QtWidgets.QLineEdit,"Process_Name_"+str(Index))[0]
            Process_path = self.frame_Process_treatment.findChildren(QtWidgets.QLineEdit,"P_"+str(Index)+"_Process_path")[0]
            Type_input = self.frame_Process_treatment.findChildren(QtWidgets.QCheckBox,"P_"+str(Index)+"_Type_input")[0]
            Process_Label = self.frame_Process_treatment.findChildren(QtWidgets.QLabel,"Process_Label_"+str(Index))[0]
            
            if Process.currentText()== 'LF':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = LF(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = LF(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.LF_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
        
            elif Process.currentText() == 'WTE':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = WTE(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = WTE(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.WTE_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
        
            elif Process.currentText() == 'AD':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = AD(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = AD(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.AD_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
        
            elif Process.currentText() == 'Composting':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = COMP(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = COMP(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.COMP_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))

            elif Process.currentText() == 'SS_MRF':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = SS_MRF(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = SS_MRF(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.SS_MRF_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))

            elif Process.currentText() == 'REPROC':
                self._Treatment_processes[Process_Name.text()]={}
                if Type_input.isChecked():
                    self._Treatment_processes[Process_Name.text()]['model'] = REPROC(CommonDataObjct=self.CommonData)
                else:
                    self._Treatment_processes[Process_Name.text()]['model'] = REPROC(input_data_path=Process_path.text(),CommonDataObjct=self.CommonData)
                self._Treatment_processes[Process_Name.text()]['input_type']=self.REPROC_input_type
                Process_Label.setFont(font1)
                print('Process {} is added to dictionary as {}'.format(Process_Name.text(),Process.currentText()))
            
            else:
                Process_Label.setFont(font2)
                       
        print(self._Treatment_processes)
        self.Define_SWM_1.setCurrentWidget(self.Network)
        self.Network.setEnabled(True)


    @QtCore.Slot()
    def Treat_process_Clear_func(self):
        for x in self.frame_Process_treatment.findChildren(QtWidgets.QComboBox):
            x.deleteLater()
        for x in self.frame_Process_treatment.findChildren(QtWidgets.QLineEdit):
            x.deleteLater()
        for x in self.frame_Process_treatment.findChildren(QtWidgets.QCheckBox):
            x.deleteLater()            
        for x in self.frame_Process_treatment.findChildren(QtWidgets.QToolButton):
            x.deleteLater()            
        for x in self.frame_Process_treatment.findChildren(QtWidgets.QLabel):
            if 'Process_Label_' in str(x.objectName()):
                x.deleteLater() 
        self.P_index = 1
# =============================================================================
#             Process.setCurrentIndex(0)
#             Process_Name.setText("")
#             Process_path.setText("")
#             Type_input.setChecked(True)
#             #Normal font
#             font = QtGui.QFont()
#             font.setBold(False)
#             font.setStrikeOut(False)
#             Process_Label.setFont(font)
# =============================================================================
        if len(self._Treatment_processes)> 0:
            self._Treatment_processes = {}
            
            

#%% Write project
# =============================================================================
# =============================================================================
    ### Write project
# =============================================================================
# =============================================================================
    def init_write_project(self):
        #Import distance data
        self.Create_Distance.clicked.connect(self.Create_Distance_Table)
        
        #Create system and write project
        self.write_project.clicked.connect(self.write_project_func)
        
        #Load parameters
        self.Load_params.clicked.connect(self.load_params_func)
        
        #Show SWM Network
        self.Show_SWM_Network.clicked.connect(self.show_SWM_Network_func(self.Show_SWM_Network_AllFlows))
        
        #Update the parameters
        self.update_param.clicked.connect(self.update_network_parameters)
        
        ### Init progess Bar
        self.progressBar_write_project.setMinimum(0)
        self.progressBar_write_project.setMaximum(100)
        self.progressBar_write_project.setValue(0)
        
        self.progressBar_updateParam.setMinimum(0)
        self.progressBar_updateParam.setMaximum(100)
        self.progressBar_updateParam.setValue(0)
        
        #QTableView
        self.Distance_table.installEventFilter(self)
        self.Param_table.installEventFilter(self)
        self.Param_table.setSortingEnabled(True) 
        
        # Check that the user updates the params
        self.param_status=False
    
        self.Show_SWM_Network_AllFlows.setChecked(True)
        
        
    
    @QtCore.Slot()
    def Create_Distance_Table(self):
        self.Distance_table.setEnabled(1)
        columns =  [x for x in self._Treatment_processes.keys()] + [x for x in self._Collection_processes.keys()]
        Distance = pd.DataFrame(columns=columns,index=columns)
        for i in range(len(columns)):
            j=i
            while j+1 < len(columns):
                Distance[columns[j+1]][columns[i]] = 20
                j+=1
                
        Distance=Distance.fillna('')
        self.Dis_data = Table_modeifed_distanceTable(Distance)
        self.Distance_table.setModel(self.Dis_data)
        self.Distance_table.resizeColumnsToContents()
        
    @QtCore.Slot()
    def write_project_func(self):
        self.P_Name=self.Project_Name.text()
        self.distance = Distance(Data=self.Dis_data._data)
        
        if len(self._Collection_processes)>0:
            for i in np.arange(1,self.col_index):
                x = self.Collection.findChildren(QtWidgets.QComboBox,"Col_{}".format(i))[0].currentText()
                y = self.Collection.findChildren(QtWidgets.QLineEdit,"Col_name_{}".format(i))[0].text()
                m = self.Collection.findChildren(QtWidgets.QLineEdit,"Col_input_path_{}".format(i))[0].text()
                z = self.Collection.findChildren(QtWidgets.QCheckBox,"Col_def_input_{}".format(i))[0].isChecked()
                if x == 'SF_Colllection':
                    if z:
                        self._Collection_processes[y]['model'] = SF_Col(y,self._Collection_processes[y]['scheme'],self._Treatment_processes,Distance=self.distance,CommonDataObjct=self.CommonData)
                    else:
                        self._Collection_processes[y]['model'] = SF_Col(y,self._Collection_processes[y]['scheme'],self._Treatment_processes,Distance=self.distance,CommonDataObjct=self.CommonData,input_data_path=m)
            
            print(self._Collection_processes)

        if self.IT_UserDefine_Tech.isChecked() or self.IT_UserDefine_LCI.isChecked() or self.IT_UserDefine_LCI_Ref.isChecked() or self.IT_UserDefine_EcoSpold2.isChecked():
            LCI_path = self.IT_FName_LCI.text() if self.IT_UserDefine_LCI.isChecked()  else None
            LCI_Reference_path = self.IT_FName_LCI_Ref.text() if self.IT_UserDefine_LCI_Ref.isChecked() else None
            Ecospold2_Path = self.IT_FName_EcoSpold2.text() if self.IT_UserDefine_EcoSpold2.isChecked()  else None
            self.Technosphere = Technosphere.Technosphere(project_name=self.P_Name,LCI_path=LCI_path,LCI_Reference_path=LCI_Reference_path,Ecospold2_Path=Ecospold2_Path)
            self.demo = Project(self.P_Name,self.CommonData,self._Treatment_processes,self.distance,Collection_processes=self._Collection_processes,Technosphere_obj=self.Technosphere)
        else:
            self.demo = Project(self.P_Name,self.CommonData,self._Treatment_processes,self.distance,self._Collection_processes)
          
        project_writer=Worker_WriteProject(parent=self.write_project,project=self.demo)
        project_writer.UpdatePBr_WriteProject.connect(self.setPBr_WriteProject)    
        project_writer.report_time.connect(self.report_time_WP)
        project_writer.start()

    @QtCore.Slot(int)
    def report_time_WP(self, time):
        #Notift the user that the project has created successfully
        self.msg_popup('Project','Project is created successfully in {} seconds'.format(time),'Information')
        
    @QtCore.Slot(int)
    def setPBr_WriteProject(self, val):
        self.progressBar_write_project.setValue(val)

    @QtCore.Slot()
    def load_params_func(self):
        param_data=pd.DataFrame(self.demo.parameters.default_parameters_list())
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
        
        param_updater=Worker_UpdateParam(parent=self.update_param, project=self.demo, param=new_param)
        param_updater.UpdatePBr_UpdateParam.connect(self.setPBr_UpdateParam)
        param_updater.report_time.connect(self.report_time_UpdateParam)
        param_updater.start()
        self.param_status=True

    @QtCore.Slot(int)
    def report_time_UpdateParam(self, time):
        #Notift the user that the project has created successfully
        self.msg_popup('Parameters','Parameters are updated successfully in {} seconds'.format(time),'Information')
        
        #self.PySWOLF.setCurrentWidget(self.Create_Scenario)
        self.Create_Scenario.setEnabled(True)
        self.LCA_tab.setEnabled(True)
        self.LCA_tab_init()
        self.MC_tab_init()
        #init create scenario
        self.init_CreateScenario()
        self.Opt_tab_init()
        
    @QtCore.Slot(int)
    def setPBr_UpdateParam(self, val):
        self.progressBar_updateParam.setValue(val)

    @QtCore.Slot()
    def show_SWM_Network_func(self,all_flow):
        def helper():
            self.demo.parameters.SWM_network(view=True,show_vals=self.param_status,all_flow=all_flow.isChecked())
        return(helper)
# =============================================================================
#         Dialog = QtWidgets.QDialog()
#         Dialog.setWindowIcon(self.icon)
#         Dialog.setWindowTitle('swolfpy: SWM Network')
#         Layout = QtWidgets.QVBoxLayout(Dialog)
#         
#         Label = QtWidgets.QLabel()
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#         Label.setSizePolicy(sizePolicy)
#         image_path =  os.getcwd()+'/SWM_network.png'
#         #QImage object
#         image_profile = QtGui.QImage(image_path) 
#         pixmap = QtGui.QPixmap(image_profile)
#         Label.setPixmap(pixmap)
#         Layout.addWidget(Label)
#         
#         #Show Dialog    
#         Dialog.show()
#         Dialog.exec_()
# =============================================================================
        

#%% Create Scenario
# =============================================================================
# =============================================================================
    ### Create Scenario
# =============================================================================
# =============================================================================
    def init_CreateScenario(self):
        if not self.init_CreateScenario_status:
            #Create new scenario
            self.Start_new_sen.clicked.connect(self.Create_scenario_func)
            self.Process.currentIndexChanged.connect(self.load_Waste_fraction)
            self.Add_act_to_scen.clicked.connect(self.add_act_to_scenario)
            self.Clear_act.clicked.connect(self.delect_act_included)
            self.Create_scenario.clicked.connect(self.create_new_scenario)
            self.init_CreateScenario_status = True
            self.Included_act_table.setDisabled(True)
            self.act_in_process_table.setDisabled(True)
            
            #QTableView
            self.act_in_process_table.installEventFilter(self)
            self.act_in_process_table.setSortingEnabled(True)
            self.Included_act_table.installEventFilter(self)
            self.Included_act_table.setSortingEnabled(True)
            
            
        
    @QtCore.Slot()
    def Create_scenario_func(self):
        self._column_name_def_scenario = ['Process','Name','Amount','Unit']
        self.Process.clear()
        self.Process.addItems(['...']+[x for x in self.demo.Treatment_processes.keys()])
        self.act_included = pd.DataFrame(columns=self._column_name_def_scenario)
        self.delect_act_included()
            
    @QtCore.Slot(int)
    def load_Waste_fraction(self,i):
        if i ==0:
            self.process_waste=pd.DataFrame(columns=self._column_name_def_scenario)
        else:
            process=[x for x in self.demo.Treatment_processes.keys()][i-1]
            self.process_waste=pd.DataFrame(columns=self._column_name_def_scenario)
            db = Database(process)
            flows = []
            units = []
            for x in db:
                act=x.as_dict()
                flows.append(act['code'])
                units.append(act['unit'])
            self.process_waste['Name'] = flows
            self.process_waste['Process'] = process
            self.process_waste['Amount'] = 0
            self.process_waste['Unit'] = units
        self.process_WF = Table_from_pandas_editable(self.process_waste)
        self.act_in_process_table.setEnabled(True)
        self.act_in_process_table.setModel(self.process_WF)
        self.act_in_process_table.resizeColumnsToContents()

        
     
    @QtCore.Slot()
    def add_act_to_scenario(self):
        for i in range(len(self.process_WF._data['Name'])):
            if self.process_WF._data['Amount'].iloc[i] != 0 and not np.isnan(self.process_WF._data['Amount'].iloc[i]):
                self.act_included.loc[self.j]=self.process_WF._data.iloc[i]
                self.j+=1
        self.Included_act_table.setEnabled(True)
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
        self.Name_new_scenario.setText('')

    @QtCore.Slot()
    def create_new_scenario(self):
        print('\n \n \n new scenario \n',self.Inc_act_table._data,'\n\n\n')
        name = self.Name_new_scenario.text()
        mass = 0
        for i in range(len(self.Inc_act_table._data['Unit'])):
            unit = self.Inc_act_table._data['Unit'][i]
            flow = self.Inc_act_table._data['Amount'][i]
            unit_i = unit.split(sep=' ')
            if len(unit_i) > 1:
                mass += float(unit_i[0]) * flow
            if unit_i[0] == 'Mg/year':
                mass += 1 * flow
        
        self.demo.waste_BD.new_activity(code = name, name = name, type = "process", unit = '{} Mg/year'.format(np.round(mass,decimals=2))).save()
        for i in range(len(self.Inc_act_table._data['Process'])):
            self.demo.waste_BD.get(name).new_exchange(input=(self.Inc_act_table._data['Process'][i],self.Inc_act_table._data['Name'][i]),amount=self.Inc_act_table._data['Amount'][i],type="technosphere").save()
        self.demo.waste_BD.get(name).save()   
        
        #Notift the user that the scenario has created successfully
        self.msg_popup('Create Scenario','Scenario {} is created successfully'.format(self.Name_new_scenario.text()),'Information')
        self.delect_act_included()
        
#%% LCA
# =============================================================================
# =============================================================================
    ### LCA setup
# =============================================================================
# =============================================================================
    def LCA_tab_init(self):
        if not self.LCA_tab_init_status:
            self.LCA_tab_init_status = True
            projects.set_current(self.demo.project_name)
            self.LCA_subTab.setCurrentWidget(self.LCA_setup_tab)
            self.LCA_Results_tab.setEnabled(False)
            self.LCA_Contribution_tab.setEnabled(False)
            self.LCA_LCI_tab.setEnabled(False)
            
            # Functional unit
            self.DB_name_list = [x for x in databases if x != 'biosphere3' and x!=self.demo.Technosphere.user_tech_name]
            self.DB_name_list.sort()
            self.LCA_DataBase.setMaxVisibleItems(100)
            self.LCA_DataBase.clear()
            self.LCA_DataBase.addItems(['...']+self.DB_name_list)
            self.LCA_DataBase.currentIndexChanged.connect(self.load_db_func(self.LCA_activity))
            self.LCA_activity.currentTextChanged.connect(self.load_act_unit(self.LCA_DataBase,self.LCA_FU_unit))
            self.LCA_acts_index=0
            self.LCA_List_of_functional_units=[]
            self.LCA_acts_DF = pd.DataFrame(columns=['Key','Name','Amount','Unit'])
            self.LCA_AddAct.clicked.connect(self.LCA_AddAct_Func)
            
            # Impact methods
            list_methods = [str(x) for x in methods]
            list_methods.sort()
            self.LCA_method.clear()
            self.LCA_method.setMaxVisibleItems(1000)
            self.LCA_method.addItems(['...']+list_methods)
            self.LCA_Filter_impacts.clicked.connect(self.Filter_Method_func(self.Filter_impact_keyword,self.LCA_method))
            self.LCA_View_method.clicked.connect(self.LCA_View_method_Func)
            
            self.LCA_impacts_index=0
            self.LCA_List_of_Impacts=[]
            self.LCA_impacts_DF = pd.DataFrame(columns=['Imapct Category','Unit'])
            self.LCA_AddImpact.clicked.connect(self.LCA_AddImpact_Func)
            
            #Clear setup
            self.LCA_ClearSetup.clicked.connect(self.LCA_ClearSetup_Func)
            
            
            #LCA Calculation setup
            self.LCA_CreateLCA.clicked.connect(self.LCA_CreateLCA_Func)
            
            #QTableView
            self.LCA_ActTable.installEventFilter(self)
            self.LCA_ActTable.setSortingEnabled(True)
            self.LCA_Impact_table.installEventFilter(self)
            self.LCA_Impact_table.setSortingEnabled(True)
        
    @QtCore.Slot()
    def LCA_AddAct_Func(self):
        #Updating the pandas DataFrame
        act=get_activity((self.LCA_DataBase.currentText(),self.LCA_activity.currentText()))
        Key = act.key
        Name = act.as_dict()['name']
        Amount = 1
        Unit = act.as_dict()['unit']
        self.LCA_acts_DF.loc[self.LCA_acts_index]=[Key,Name,Amount,Unit]
        self.LCA_acts_index+=1
        
        #Updating the QTableView (self.LCA_ActTable)
        LCA_ActTable_model = Table_from_pandas(self.LCA_acts_DF)
        self.LCA_ActTable.setModel(LCA_ActTable_model)
        self.LCA_ActTable.resizeColumnsToContents()

        #Updating the list of functional units
        self.LCA_List_of_functional_units.append({Key:Amount})
        
        
    @QtCore.Slot()
    def LCA_View_method_Func(self):
        if self.LCA_method.currentText() !='...':
            #Create Dialog
            Dialog = QtWidgets.QDialog()
            Dialog.setObjectName("showMethod_Dialog")
            Dialog.setWindowIcon(self.icon)
            gridLayout = QtWidgets.QGridLayout(Dialog)
            gridLayout.setObjectName("showMethod_gridLayout")
            frame = QtWidgets.QFrame(Dialog)
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName("showMethod_frame")
            gridLayout_2 = QtWidgets.QGridLayout(frame)
            gridLayout_2.setObjectName("showMethod_gridLayout_2")
            
            #Create QtableView
            Method_table = QtWidgets.QTableView(frame)
            Method_table.setObjectName("Show_Method_tableView")
            gridLayout_2.addWidget(Method_table, 0, 0, 1, 1)
            gridLayout.addWidget(frame, 0, 0, 1, 1)
            
            #Create Dataframe for Characterization factors
            lca_method = Method(ast.literal_eval(self.LCA_method.currentText()))
            CFS_data = pd.DataFrame(lca_method.load(),columns=['Key','Factor'])
            CFS_data['Unit'] = lca_method.metadata['unit']
            CFS_data.insert(loc=1, column='Name', value=[get_activity(x) for x in CFS_data['Key']])
            
            #Setup the QTableView                
            Method_table_model = Table_from_pandas(CFS_data)
            Method_table.setModel(Method_table_model)
            Method_table.resizeColumnsToContents()
            Method_table.installEventFilter(self)
            Method_table.setSortingEnabled(True)
            
            #Show Dialog    
            Dialog.show()
            Dialog.exec_()
        

    @QtCore.Slot()
    def LCA_AddImpact_Func(self):
        lca_method = Method(ast.literal_eval(self.LCA_method.currentText()))
        #Updating the pandas DataFrame
        Impact = lca_method.name
        Unit = lca_method.metadata['unit']
        self.LCA_impacts_DF.loc[self.LCA_impacts_index]=[Impact,Unit]
        self.LCA_impacts_index+=1
        
        #Updating the QTableView (self.LCA_Impact_table)
        LCA_Impact_table_model = Table_from_pandas(self.LCA_impacts_DF)
        self.LCA_Impact_table.setModel(LCA_Impact_table_model)
        self.LCA_Impact_table.resizeColumnsToContents()

        #Updating the list of impacts
        self.LCA_List_of_Impacts.append(Impact)
        
    @QtCore.Slot()
    def LCA_CreateLCA_Func(self):
        if len(self.LCA_List_of_functional_units)>0 and len(self.LCA_List_of_Impacts)>0:
            calculation_setups['LCA'] = {'inv':self.LCA_List_of_functional_units, 'ia':self.LCA_List_of_Impacts}
            self.MultiLca = MultiLCA('LCA')
            print(self.MultiLca.results)
            
            #Init results tabs
            self.LCAResults_tab_init()
            self.LCA_Results_ImpactFig.clear()
            self.LCA_Results_ImpactFig.addItems([str(x) for x in self.LCA_List_of_Impacts])
            self.LCA_Contribution_tab_init()
            self.LCA_LCI_tab_init()


    @QtCore.Slot()
    def LCA_ClearSetup_Func(self):
        #Activity
        if self.LCA_acts_index >0:
            self.LCA_acts_index=0
            self.LCA_List_of_functional_units=[]
            self.LCA_acts_DF = pd.DataFrame(columns=['Key','Name','Amount','Unit'])
            self.LCA_ActTable.model()._data = self.LCA_acts_DF
            self.LCA_ActTable.model().layoutChanged.emit()
            self.LCA_ActTable.resizeColumnsToContents()
        
        #Impacts
        if self.LCA_impacts_index >0:
            self.LCA_impacts_index=0
            self.LCA_List_of_Impacts=[]
            self.LCA_impacts_DF = pd.DataFrame(columns=['Imapct Category','Unit'])
            self.LCA_Impact_table.model()._data = self.LCA_impacts_DF
            self.LCA_Impact_table.model().layoutChanged.emit()
            self.LCA_Impact_table.resizeColumnsToContents()

# =============================================================================
# =============================================================================
    ### LCA Results
# =============================================================================
# =============================================================================
    def LCAResults_tab_init(self):
        if not self.LCAResults_tab_init_status:
            self.LCAResults_tab_init_status =True
            self.LCA_Results_tab.setEnabled(True)
            self.LCA_Contribution_tab.setEnabled(True)
            self.LCA_LCI_tab.setEnabled(True)
            self.LCA_subTab.setCurrentWidget(self.LCA_Results_tab)
            
            #Figure initialization
            self.fig_LCA = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            self.canvas_LCA = FigureCanvas(self.fig_LCA)
            toolbar = NavigationToolbar(self.canvas_LCA, self)
            lay = QtWidgets.QVBoxLayout(self.LCA_Results_fig)
            lay.addWidget(toolbar)
            lay.addWidget(self.canvas_LCA)
            self.ax_LCA = self.fig_LCA.add_subplot(111)
            
            #Connect figure input
            self.LCA_Results_ImpactFig.currentIndexChanged.connect(self.LCA_Results_ImpactFig_func)
            
            #QTableView
            self.LCA_Results_Table.installEventFilter(self)
            self.LCA_Results_Table.setSortingEnabled(True)
        
        #updating the results table
        data=self.MultiLca.results
        index=[str(x) for x in list(self.MultiLca.all.keys())]
        columns=[str(x) for x in self.LCA_List_of_Impacts]
        results = pd.DataFrame(data,columns=columns,index=index)
        LCA_Results_Table_model = Table_from_pandas(results)
        self.LCA_Results_Table.setModel(LCA_Results_Table_model)
        self.LCA_Results_Table.resizeColumnsToContents()

        

    @QtCore.Slot(str)
    def LCA_Results_ImpactFig_func(self,impact_index):
        if impact_index >= 0:
            names = [str(x) for x in list(self.MultiLca.all.keys())]
            values =  list((self.MultiLca.results[:,impact_index]))
            self.ax_LCA.clear()
            self.ax_LCA.barh(names,values,height=0.3)
            
            #set lables
            self.ax_LCA.set_title(str(self.LCA_List_of_Impacts[impact_index]), fontsize=20)
            self.ax_LCA.set_xlabel(self.LCA_impacts_DF['Unit'][impact_index], fontsize=18)
            self.ax_LCA.set_ylabel('Scenarios', fontsize=18)
            self.ax_LCA.tick_params(axis='both', which='major', labelsize=18)
            self.ax_LCA.tick_params(axis='both', which='minor', labelsize=16)
            
            #set margins
            self.canvas_LCA.draw()
            self.fig_LCA.set_tight_layout(True)
            
# =============================================================================
# =============================================================================
    ### LCA Contribution analysis
# =============================================================================
# =============================================================================            
    def LCA_Contribution_tab_init(self):
        #Functionl unit
        FU=[]
        for x in self.MultiLca.all.keys():
            FU.append(str(x))
        self.LCA_Contr_FU.clear()
        
        #Impact category
        self.LCA_Contr_FU.addItems(FU)
        self.LCA_Contr_Method.clear()
        self.LCA_Contr_Method.addItems([str(x) for x in self.MultiLca.methods])
        
        if not self.LCA_Contribution_tab_init_status: 
            self.LCA_Contribution_tab_init_status = True
            #CutOff type
            self.LCA_Contr_CutOffType.addItems(['percent','number'])
            self.LCA_Contr_CutOffType.currentTextChanged.connect(self.CutOff_setting)
            self.LCA_Contr_updat.clicked.connect(self.update_contribution)
            self.LCA_Contr__Top_act.setChecked(True)
            self.CutOff_setting('percent')
            self.LCA_Contr__Top_act.clicked.connect(lambda: self.LCA_Contr_Top_emis.setChecked(not(self.LCA_Contr__Top_act.isChecked())))
            self.LCA_Contr_Top_emis.clicked.connect(lambda: self.LCA_Contr__Top_act.setChecked(not(self.LCA_Contr_Top_emis.isChecked())))
            
            #QTableView
            self.LCA_contribution_Table.installEventFilter(self)
            self.LCA_contribution_Table.setSortingEnabled(True)
            
            #Figure initialization
            self.fig_Contr_LCA = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
            self.canvas_Contr_LCA = FigureCanvas(self.fig_Contr_LCA)
            toolbar = NavigationToolbar(self.canvas_Contr_LCA, self)
            lay = QtWidgets.QVBoxLayout(self.LCA_Contr_fig)
            lay.addWidget(toolbar)
            lay.addWidget(self.canvas_Contr_LCA)
            self.ax_Contr_LCA = self.fig_Contr_LCA.add_subplot(111)
            
            
    
    @QtCore.Slot(str)
    def CutOff_setting(self,Type):
        if Type == 'percent':
            self.LCA_Contr_CutOff.setMaximum=1
            self.LCA_Contr_CutOff.setMinimum=0
            self.LCA_Contr_CutOff.setValue(0.05)
            self.LCA_Contr_CutOff.setSingleStep(0.01)
            
        elif Type == 'number':
            self.LCA_Contr_CutOff.setMaximum=100
            self.LCA_Contr_CutOff.setMinimum=1
            self.LCA_Contr_CutOff.setValue(10.00)
            self.LCA_Contr_CutOff.setSingleStep(1)
    
    @QtCore.Slot()
    def update_contribution(self):
        #Create LCA object
        FU = self.MultiLca.func_units[self.LCA_Contr_FU.currentIndex()]
        impact = self.MultiLca.methods[self.LCA_Contr_Method.currentIndex()]
        self.LCA_Contr_lca=LCA(FU,impact) 
        self.LCA_Contr_lca.lci()
        self.LCA_Contr_lca.lcia()
        
        #set impact score and unit
        self.LCA_Contr_score.setText(f_n(self.LCA_Contr_lca.score))
        self.LCA_Contr_unit.setText(Method(impact).metadata['unit'])
        
        #Call contribution analysis functions
        if self.LCA_Contr__Top_act.isChecked():
            self.LCA_top_act_func()
        elif self.LCA_Contr_Top_emis.isChecked():
            self.LCA_top_emission_func()
        
    
    # Contribution analysis , Report the top activities in DF format
    @QtCore.Slot()
    def LCA_top_act_func(self):
        limit_type = self.LCA_Contr_CutOffType.currentText()
        if self.LCA_Contr_CutOffType.currentText()=='number':
            limit = round(float(self.LCA_Contr_CutOff.value()))
        else:
            limit = 35
        
        lca=self.LCA_Contr_lca
        top_act_data= ContributionAnalysis().annotated_top_processes(lca,limit= limit,limit_type ='number')
        
        Activity=[]
        Flow_unit=[]
        if limit_type == 'number':
            for x in top_act_data:
                Activity.append(x[2].key)
                Flow_unit.append(x[2].as_dict()['unit'])
            top_act_DF = pd.DataFrame(columns=['Activity','Flow','Flow Unit','Contribution','Unit'])
            top_act_DF['Activity']=Activity
            top_act_DF['Flow']=[x[1] for x in top_act_data]
            top_act_DF['Flow Unit']=Flow_unit
            top_act_DF['Contribution']=[x[0] for x in top_act_data]
        
        elif limit_type == 'percent':
            flow=[]
            contribution=[]
            for x in top_act_data:
                if abs(x[0]) >=  float(self.LCA_Contr_CutOff.value()) * abs(self.LCA_Contr_lca.score):
                    Activity.append(x[2].key)
                    Flow_unit.append(x[2].as_dict()['unit'])
                    flow.append(x[1])
                    contribution.append(x[0])
            top_act_DF = pd.DataFrame(columns=['Activity','Flow','Flow Unit','Contribution','Unit'])
            top_act_DF['Activity']=Activity
            top_act_DF['Flow']=flow
            top_act_DF['Flow Unit']=Flow_unit
            top_act_DF['Contribution']=contribution
        
        top_act_DF['Unit']=self.LCA_Contr_unit.text()
        LCA_contribution_Table_model = Table_from_pandas(top_act_DF)
        self.LCA_contribution_Table.setModel(LCA_contribution_Table_model)
        self.LCA_contribution_Table.resizeColumnsToContents()

        
        #Creating the DataFrame for top activities
        columns=[]
        for x in top_act_DF['Activity']:
            columns.append(get_activity(x).as_dict()['name'])
        index = [self.LCA_Contr_FU.currentText()]
        data = [[x for x in top_act_DF['Contribution'].values]]
        plot_DF = pd.DataFrame(data,columns=columns,index=index)
        self.LCA_Contr_fig_func(plot_DF)
            
    # Contribution analysis , Report the top emissions in DF format
    @QtCore.Slot()
    def LCA_top_emission_func(self):
        limit_type = self.LCA_Contr_CutOffType.currentText()
        if self.LCA_Contr_CutOffType.currentText()=='number':
            limit = round(float(self.LCA_Contr_CutOff.value()))
        else:
            limit = 35
        
        lca=self.LCA_Contr_lca
        top_emission_data=ContributionAnalysis().annotated_top_emissions(lca,limit= limit,limit_type ='number')
        Emission=[]
        Compartment=[]
        Flow_unit=[]
        if self.LCA_Contr_CutOffType.currentText()=='number':
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
            top_emission_DF['Unit']=self.LCA_Contr_unit.text()
            
        elif self.LCA_Contr_CutOffType.currentText()=='percent':
            flow=[]
            contribution=[]
            for x in top_emission_data:
                if abs(x[0]) >=  float(self.LCA_Contr_CutOff.value()) * abs(self.LCA_Contr_lca.score):
                    Emission.append(x[2].as_dict()['name'])
                    Compartment.append(x[2].as_dict()['categories'])
                    Flow_unit.append(x[2].as_dict()['unit'])
                    flow.append(x[1])
                    contribution.append(x[0])
            top_emission_DF = pd.DataFrame(columns=['Emission','Compartment','Flow','Flow Unit','Contribution','Unit'])
            top_emission_DF['Emission']=Emission
            top_emission_DF['Compartment']=Compartment
            top_emission_DF['Flow']=flow
            top_emission_DF['Flow Unit']=Flow_unit
            top_emission_DF['Contribution']=contribution
            top_emission_DF['Unit']=self.LCA_Contr_unit.text()
            
        LCA_contribution_Table_model = Table_from_pandas(top_emission_DF)
        self.LCA_contribution_Table.setModel(LCA_contribution_Table_model)
        self.LCA_contribution_Table.resizeColumnsToContents()


        #Creating the DataFrame for top emissions
        columns=[]
        legend=[]
        for x,y in top_emission_DF[['Emission','Compartment']].values:
            columns.append(str(x)+' '+str(y))
            legend.append(str(x)+' \n'+str(y))
        index = [self.LCA_Contr_FU.currentText()]
        data = [[x for x in top_emission_DF['Contribution'].values]]
        plot_DF = pd.DataFrame(data,columns=columns,index=index)
        self.LCA_Contr_fig_func(plot_DF,legend)
        

    def LCA_Contr_fig_func(self,DF,legend=None):
        self.ax_Contr_LCA.clear()
        
        #ploting the DataFrame        
        self.ax_Contr_LCA=DF.plot(kind='bar',stacked='True', ax=self.ax_Contr_LCA,width=1)
        
        #set lables
        self.ax_Contr_LCA.set_title('Contribution to '+str(self.LCA_Contr_lca.method), fontsize=18)
        self.ax_Contr_LCA.set_ylabel(self.LCA_Contr_unit.text(), fontsize=18)
        self.ax_Contr_LCA.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_Contr_LCA.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')
        if legend:
            self.ax_Contr_LCA.legend(legend,fontsize=18,bbox_to_anchor=(1, 0, .2, 1),loc=2)
        else:
            self.ax_Contr_LCA.legend(fontsize=18,bbox_to_anchor=(1, 0, .2, 1),loc=2)
        self.ax_Contr_LCA.set_xlim(-0.7,0.7)

        #set margins
        self.canvas_Contr_LCA.draw()
        self.fig_Contr_LCA.set_tight_layout(True)

# =============================================================================
# =============================================================================
    ### LCA LCI
# =============================================================================
# =============================================================================
    def LCA_LCI_tab_init(self):
        if not self.LCA_LCI_tab_init_status:
            self.LCA_LCI_tab_init_status =True
            self.LCA_LCI_updat.clicked.connect(self.LCA_LCI_updat_func)
            
            #TableView
            self.LCA_LCI_Table.installEventFilter(self)
            self.LCA_LCI_Table.setSortingEnabled(True)
        
        #Functionl unit
        FU=[]
        for x in self.MultiLca.all.keys():
            FU.append(str(x))
        self.LCA_LCI_FU.clear()
        self.LCA_LCI_FU.addItems(FU)
    
    #Update the Life Cycle inventory in table
    @QtCore.Slot()
    def LCA_LCI_updat_func(self):
        act= ast.literal_eval(self.LCA_LCI_FU.currentText())
        lca=LCA({act:1})
        lca.lci()
        _,_,bio_rev = lca.reverse_dict()
        Inventory = lca.biosphere_matrix * lca.supply_array
        Inventory_DF = pd.DataFrame(Inventory,columns=['amount'])
        key,name,compartment,unit = [],[],[],[]
        for i in range(len(Inventory_DF)):
            flow = get_activity(bio_rev[i])
            flow = flow.as_dict()
            key.append(flow['code'])
            name.append(flow['name'])
            compartment.append(flow['categories'])
            unit.append(flow['unit'])
        Inventory_DF.insert(0,'key',key)
        Inventory_DF.insert(1,'name',name)
        Inventory_DF.insert(2,'compartment',compartment)
        Inventory_DF.insert(4,'unit',unit)
        
        #setup the TableView for inventory
        LCA_LCI_Table_model = Table_from_pandas(Inventory_DF .sort_values('name'))
        self.LCA_LCI_Table.setModel(LCA_LCI_Table_model)
        self.LCA_LCI_Table.resizeColumnsToContents()

        
        
#%% Monte-Carlo Simulation            
# =============================================================================
# =============================================================================
    ### Monte-Carlo Simulation
# =============================================================================
# =============================================================================       
    @QtCore.Slot()
    def MC_tab_init(self):
        if not self.MC_tab_init_status:
            self.MC_tab_init_status = True
            self.MC_tab.setEnabled(True)
            self.MC_setting.setCurrentWidget(self.Normal)
            projects.set_current(self.demo.project_name)
            self.MC_FU_DB.clear()
            self.MC_FU_DB.addItems(['...']+self.DB_name_list)
            self.MC_FU_DB.currentIndexChanged.connect(self.load_db_func(self.MC_FU_act))
            self.MC_FU_act.currentTextChanged.connect(self.load_act_unit(self.MC_FU_DB,self.MC_FU_unit))
            
            list_methods = [str(x) for x in methods]
            list_methods.sort()
            self.MC_method.setMaxVisibleItems(1000)
            self.MC_method.clear()
            self.MC_method.addItems(['...']+list_methods)
            
            self.MC_Filter_method.clicked.connect(self.Filter_Method_func(self.MC_Filter_keyword,self.MC_method))
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
            keys = ['CommonData']+[x for x in self.demo.Treatment_processes.keys()]
            self.MC_Model.clear()
            self.MC_Model.addItems(keys)
            self.MC_Model.currentTextChanged.connect(self.MC_load_uncertain_func)
            self.MC_load_uncertain_func(self.MC_Model.currentText())
            self.MC_uncertain_filter.clicked.connect(self.MC_uncertain_filter_func)
            self.MC_uncertain_update.clicked.connect(self.MC_uncertain_update_func)
            self.MC_unceratin_clear.clicked.connect(self.MC_uncertain_clear_func)
        
            CheckBoxes = ['CommonData','Parameters']+[x for x in self.demo.Treatment_processes.keys()]
            self.include_model_dict = dict(zip(CheckBoxes,[False for i in range(len(CheckBoxes))]))
            for x in self.MC_included_models.findChildren(QtWidgets.QCheckBox):
                x.deleteLater()
            for x in self.include_model_dict:
                self.create_check_box(x,self.MC_included_models,self.verticalLayout_3)
            
            self.MC_show.clicked.connect(self.show_res_func)
            self.MC_save.clicked.connect(self.MC_save_file())
            
            #TableView
            self.MC_method_table.installEventFilter(self)
            self.MC_method_table.setSortingEnabled(True)
            self.MC_Uncertain_table.installEventFilter(self)
            self.MC_Uncertain_table.setSortingEnabled(True)
        
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
    
    @QtCore.Slot()
    def MC_add_method_func(self):
        method = Method(ast.literal_eval(self.MC_method.currentText()))
        self.method_DF.loc[self.method_DF_index]=[method.name,method.metadata['unit']]
        self.method_DF_index+=1
        self.MC_method_table_model = Table_from_pandas(self.method_DF)
        self.MC_method_table.setModel(self.MC_method_table_model)
        self.MC_method_table.resizeColumnsToContents()
        
    @QtCore.Slot(str)
    def MC_load_uncertain_func(self,process_name):
        if process_name in self.demo.Treatment_processes.keys():
            self.uncertain_data = deepcopy(self.demo.Treatment_processes[process_name]['model'].InputData.Data)
        elif process_name == 'CommonData':
            self.uncertain_data = deepcopy(self.demo.CommonData.Data)
        self.MC_uncertain_filter_func()

    @QtCore.Slot()
    def MC_uncertain_filter_func(self):
        if self.MC_uncertain_filter.isChecked():
            self.MC_Uncertain_table_model = Input_data_table(self.MC_Uncertain_table,self.uncertain_data[:][self.uncertain_data['uncertainty_type']>1])
            #MC_Uncertain_model = Table_from_pandas_editable(self.uncertain_data[:][self.uncertain_data['uncertainty_type']>1])
        else:
            #MC_Uncertain_model = Table_from_pandas_editable(self.uncertain_data)
            self.MC_Uncertain_table_model = Input_data_table(self.MC_Uncertain_table,self.uncertain_data)
        self.MC_Uncertain_table.model().new_index.connect(self.MC_Uncertain_table_model.update_ComboBox)

    @QtCore.Slot()
    def MC_uncertain_update_func(self):
        if self.MC_Model.currentText() in self.demo.Treatment_processes.keys():
            self.demo.Treatment_processes[self.MC_Model.currentText()]['model'].InputData.Update_input(self.MC_Uncertain_table.model()._data)
        elif self.MC_Model.currentText() == 'CommonData':
            self.demo.CommonData.Update_input(self.MC_Uncertain_table.model()._data)
        self.msg_popup('Update input data','Input Data is successfully updated','Information')
        self.MC_load_uncertain_func(self.MC_Model.currentText())

    @QtCore.Slot()
    def MC_uncertain_clear_func(self):
        self.MC_Uncertain_table.model()._data['uncertainty_type'] = 0
        self.MC_Uncertain_table_model.update_ComboBox()
        self.MC_Uncertain_table.model()._data[['loc','scale','shape','minimum','maximum']] = np.nan 
        self.MC_Uncertain_table.model().layoutChanged.emit()
        self.MC_Uncertain_table.resizeColumnsToContents()
        
    @QtCore.Slot()
    def MC_run_func(self):
        projects.set_current(self.demo.project_name)
        project = self.demo.project_name
        self.MC_FU = {(self.MC_FU_DB.currentText(),self.MC_FU_act.currentText()):1}
        method = self.MC_method_table_model._data['LCIA method'].values.tolist()
        process_models = list()
        process_model_names = list()
        
        Treatment_processes = deepcopy(self.demo.Treatment_processes)
        Collection_processe = deepcopy(self.demo.Collection_processes)
        
        CommonData = None
        IsCommonData = 'Not included'
        for x in self.include_model_dict:
            if self.include_model_dict[x]:
                if x in Treatment_processes.keys():
                    process_models.append(Treatment_processes[x]['model'])
                    process_model_names.append(x)
                
                elif x in Collection_processe.keys():
                    process_models.append(Collection_processe[x]['model'])
                    process_model_names.append(x)
                elif x == 'CommonData':
                    CommonData = self.demo.CommonData
                    IsCommonData = 'Included'
        
        # Selecting the seed
        seed = None
        if len(self.MC_seed.text())>0:
            seed = int(self.MC_seed.text())
        
        print("""
              
                #########    Setup Monte Carlo Simulatio    ############
                  
                    Functional Unit = {FU}
                  
                    Methods = {method}
                  
                    Number of threads = {Nthread}
                  
                    Number of runs = {nruns}
                  
                ### Moldes included
                    
                  Names: {process_model_names}
                  
                  Models: {process_models}
                  
                  CommonData: {Yes_No}
                  
                #################################             
              """.format(FU=self.MC_FU,method=method,Nthread=int(self.MC_N_Thread.text()),nruns=int(self.MC_N_runs.text()),
                          process_model_names=process_model_names,process_models=process_models,Yes_No = IsCommonData))
        

        Monte_carlo = Monte_Carlo(self.MC_FU, method, project,process_models=process_models,process_model_names=process_model_names,common_data = CommonData,seed = seed)

        #Monte_carlo.run(int(self.MC_N_Thread.text()),int(self.MC_N_runs.text()))
        
        MC_Simulator = Worker_MC(parent=self.MC_run,
                                 MC=Monte_carlo,
                                 nproc=int(self.MC_N_Thread.text()), 
                                 n=int(self.MC_N_runs.text()))
        MC_Simulator.UpdatePBr_Opt.connect(self.setPBr_MC)
        MC_Simulator.report.connect(self.report_MC_func)
        #MC_Simulator.setPriority(QtCore.QThread.Priority.LowestPriority)
        MC_Simulator.run()
        
         
    @QtCore.Slot(dict)
    def report_MC_func(self, report):
        print("Total time for Monte Carlo simulation: {} seconds".format(report['time']))
        self.msg_popup('Monte Carlo simulation Result','Simulation is done succesfully. \n Total time: {} seconds'.format(report['time']),'Information')
        self.MC_results = report['results']
        self.show_res_func()
        
    @QtCore.Slot(dict)
    def setPBr_MC(self, dict_):
        self.MC_PBr.setMaximum(dict_['max'])
        self.MC_PBr.setValue(dict_['val'])

# =============================================================================
#     @QtCore.Slot()
#     def show_res_func(self):
#         Dialog = QtWidgets.QDialog()
#         Dialog.setObjectName("showRes_Dialog")
#         gridLayout = QtWidgets.QGridLayout(Dialog)
#         gridLayout.setObjectName("showRes_gridLayout")
#         frame = QtWidgets.QFrame(Dialog)
#         frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame.setObjectName("showRes_frame")
#         gridLayout_2 = QtWidgets.QGridLayout(frame)
#         
#         gridLayout_2.setObjectName("showRes_gridLayout_2")
#         MC_res_table = QtWidgets.QTableView(frame)
#         MC_res_table.setObjectName("Show_res_tableView")
#         gridLayout_2.addWidget(MC_res_table, 0, 0, 1, 1)
#         
#         MC_res_table_model = Table_from_pandas(self.MC_results)
#         MC_res_table.setModel(MC_res_table_model)
#         MC_res_table.resizeColumnsToContents()
#         MC_res_table.installEventFilter(self)
#         MC_res_table.setSortingEnabled(True)
#     
#         gridLayout.addWidget(frame, 0, 0, 1, 1)
#         Dialog.show()
#         Dialog.exec_()
# =============================================================================





    @QtCore.Slot()
    def show_res_func(self):
        Dialog = QtWidgets.QDialog()
        self.MC_Widget = MC_ui.Ui_MC_Results()
        self.MC_Widget.setupUi(Dialog)
        self.MC_Widget.tabWidget.setCurrentWidget(self.MC_Widget.MC_Data)
        
        ### Data Tab
        MC_res_table_model = Table_from_pandas(self.MC_results)
        self.MC_Widget.MC_Res_Table.setModel(MC_res_table_model)
        self.MC_Widget.MC_Res_Table.resizeColumnsToContents()
        self.MC_Widget.MC_Res_Table.installEventFilter(self)
        self.MC_Widget.MC_Res_Table.setSortingEnabled(True)
        
        ### Plot tab
        #Figure initialization _ plot
        self.fig_plot_mc = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_plot_mc = FigureCanvas(self.fig_plot_mc)
        toolbar = NavigationToolbar(self.canvas_plot_mc, self)
        lay = QtWidgets.QVBoxLayout(self.MC_Widget.plot)
        lay.addWidget(toolbar)
        lay.addWidget(self.canvas_plot_mc)
        #self.ax_plot_mc = self.fig_plot_mc.add_subplot(111)
        
        #Figure initialization _ plot dist
        self.fig_plot_dist_mc = Figure(figsize=(4, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_plot_dist_mc = FigureCanvas(self.fig_plot_dist_mc)
        toolbar2 = NavigationToolbar(self.canvas_plot_dist_mc, self)
        lay2 = QtWidgets.QVBoxLayout(self.MC_Widget.plot_dist)
        lay2.addWidget(toolbar2)
        lay2.addWidget(self.canvas_plot_dist_mc)
        #self.ax_plot_dist_mc = self.fig_plot_dist_mc.add_subplot(111)
        
        self.MC_Widget.y_axis.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.x_axis.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.scatter.setChecked(True)
        self.MC_Widget.param.addItems([str(x) for x in self.MC_results.columns])
        self.MC_Widget.box.setChecked(True)
        
        
        ### Connect the push bottoms
        self.MC_Widget.Update_plot.clicked.connect(self.mc_plot_func)
        self.MC_Widget.Update_dist_fig.clicked.connect(self.mc_plot_dist_func)
        
        Dialog.show()
        Dialog.exec_()
        
    @QtCore.Slot()
    def mc_plot_func(self):
        self.fig_plot_mc.clear()
        self.ax_plot_mc = self.fig_plot_mc.add_subplot(111)
    
        #ploting the DataFrame        
        self.ax_plot_mc=self.MC_results.plot(kind='scatter' if self.MC_Widget.scatter.isChecked() else 'hexbin',
                                        x=self.MC_results.columns[self.MC_Widget.x_axis.currentIndex()],
                                        y=self.MC_results.columns[self.MC_Widget.y_axis.currentIndex()],
                                        ax=self.ax_plot_mc)
        #set lables
        self.ax_plot_mc.set_title(str(list(self.MC_FU.keys())[0]), fontsize=18)
        self.ax_plot_mc.set_ylabel(self.MC_Widget.y_axis.currentText(), fontsize=18)
        self.ax_plot_mc.set_xlabel(self.MC_Widget.x_axis.currentText(), fontsize=18)
        self.ax_plot_mc.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_mc.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_plot_mc.draw()
        self.fig_plot_mc.set_tight_layout(True)
            
    @QtCore.Slot()    
    def mc_plot_dist_func(self):
        self.fig_plot_dist_mc.clear()
        self.ax_plot_dist_mc = self.fig_plot_dist_mc.add_subplot(111)
        
        if self.MC_Widget.hist.isChecked():
            kind = 'hist'
        elif self.MC_Widget.box.isChecked():
            kind = 'box'
        else:
            kind = 'density'

        #ploting the DataFrame  
        if kind == 'hist':
            self.ax_plot_dist_mc=self.MC_results[self.MC_results.columns[self.MC_Widget.param.currentIndex()]].plot(kind=kind,
                                        ax=self.ax_plot_dist_mc, bins=max(30,len(self.MC_results)/100))
        else:
            self.ax_plot_dist_mc=self.MC_results[self.MC_results.columns[self.MC_Widget.param.currentIndex()]].plot(kind=kind,
                                        ax=self.ax_plot_dist_mc)
            
        

        
        #set lables
        self.ax_plot_dist_mc.set_title(str(list(self.MC_FU.keys())[0]), fontsize=18)
        plt.rcParams["font.size"] = "18"
        self.ax_plot_dist_mc.tick_params(axis='both', which='major', labelsize=18,rotation='auto')
        self.ax_plot_dist_mc.tick_params(axis='both', which='minor', labelsize=16,rotation='auto')

        #set margins
        self.canvas_plot_dist_mc.draw()
        self.fig_plot_dist_mc.set_tight_layout(True)
        
    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def MC_save_file(self):
        fileDialog = QtWidgets.QFileDialog()
        def helper():
            #wdr_path = str(os.getcwd()).replace('\\','/')
            file_name = str(fileDialog.getSaveFileName(filter="CSV (*.csv)")[0])
            self.MC_results.to_csv(file_name)
            
        return(helper)        
        
    
# =============================================================================
#     Index(['Category', 'Dictonary_Name', 'Parameter', 'Name', 'amount', 'unit',
#        'uncertainty_type', 'loc', 'scale', 'shape', 'minimum', 'maximum',
#        'Reference', 'Comment'],
#       dtype='object')    
# =============================================================================
        

#%% Optimization  
# =============================================================================
# =============================================================================
    ### Optimization
# =============================================================================
# =============================================================================    
    @QtCore.Slot()
    def Opt_tab_init(self):
        if not self.Opt_tab_init_status:
            self.Opt_tab_init_status = True
            self.Opt_tab.setEnabled(True)
            
            self.Const_DF = pd.DataFrame(columns=['flow','inequality','limit'])
            self.Const_DF_index=0
            self.constraints={}
            
            #Functional Unit
            projects.set_current(self.demo.project_name)
            self.Opt_FU_DB.clear()
            self.Opt_FU_DB.addItems(['...']+self.DB_name_list)
            self.Opt_FU_DB.currentIndexChanged.connect(self.load_db_func(self.Opt_FU_act))
            self.Opt_FU_act.currentTextChanged.connect(self.load_act_unit(self.Opt_FU_DB,self.Opt_FU_unit))
            
            #Objective Impact
            list_methods = [str(x) for x in methods]
            list_methods.sort()
            self.Opt_method.setMaxVisibleItems(1000)
            self.Opt_method.clear()
            self.Opt_method.addItems(['...']+list_methods)
            self.Opt_Filter_method.clicked.connect(self.Filter_Method_func(self.Opt_Filter_keyword,self.Opt_method))
            
            #Constraint on Total Mass to Process
            self.Opt_Const1_process.clear()
            self.Opt_Const1_process.addItems(['...']+self.DB_name_list)
            self.Opt_Const1_Inequality.clear()
            self.Opt_Const1_Inequality.addItems(['<=','>='])
            self.Opt_add_Const1.clicked.connect(self.Opt_add_const1)
            
            #Constraint on Waste to Process
            self.Opt_Const2_process.clear()
            self.Opt_Const2_process.addItems(['...']+self.DB_name_list)
            self.Opt_Const2_process.currentIndexChanged.connect(self.load_db_func(self.Opt_Const2_flow))
            self.Opt_Const2_Inequality.clear()
            self.Opt_Const2_Inequality.addItems(['<=','>='])
            self.Opt_add_Const2.clicked.connect(self.Opt_add_const2)
            
            #Constraints on Emissions
            bio_db = Database('biosphere3')
            self.bio_dict={}
            for x in bio_db:
                self.bio_dict[str(x)]=x.as_dict()['code']
            self.Opt_Const3_flow.clear()
            self.Opt_Const3_flow.setMaxVisibleItems(5000)
            keys=list(self.bio_dict.keys())
            keys.sort()
            self.Opt_Const3_flow.addItems(['...']+keys)
            self.Opt_add_Const3.clicked.connect(self.Opt_add_const3)
            
            self.Opt_Const3_Inequality.clear()
            self.Opt_Const3_Inequality.addItems(['<=','>='])
            
            self.Opt_optimize.clicked.connect(self.Opt_minimize_func)
            
            self.Opt_update_param.clicked.connect(self.Opt_update_network_parameters)
            
            #QTableView
            self.Opt_Const_table.installEventFilter(self)
            self.Opt_Const_table.setSortingEnabled(True)
            self.Opt_Param_table.installEventFilter(self)
            self.Opt_Param_table.setSortingEnabled(True)
            
            #Remove Constraints
            self.Opt_ClearConstr.clicked.connect(self.Opt_ClearConstr_func)
            
            # connect the signal for download file
            QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)
            
            # Calc objective functions
            self.Opt_CalObjFunc.clicked.connect(self.Opt_CalObjFunc_func)
            
            # advance optimization options
            self.opt_adv_options_status = False
            self.Opt_adv_func()
            self.adv_opt_btm.clicked.connect(self.Opt_adv_func)
     
        
    @QtCore.Slot()
    def Opt_Filter_func(self):
        list_methods= [str(x) for x in methods if self.Opt_Filter_keyword.text() in str(x)]
        list_methods.sort()
        self.Opt_method.clear()
        self.Opt_method.addItems(['...']+list_methods)        
        
        
    @QtCore.Slot()
    def Opt_add_const1(self):
        if self.Opt_Const1_process.currentText() != "...":
            self.Const_DF.loc[self.Const_DF_index]=[self.Opt_Const1_process.currentText(),self.Opt_Const1_Inequality.currentText(),float(self.Opt_Const1_val.text())]
            self.Const_DF_index +=1
            self.Opt_Const_table_update()
            self.constraints[self.Opt_Const1_process.currentText()]= {'limit':float(self.Opt_Const1_val.text()),
                                                                     'KeyType':'Process',
                                                                     'ConstType':self.Opt_Const1_Inequality.currentText()}
        
    @QtCore.Slot()
    def Opt_add_const2(self):
        if self.Opt_Const2_process.currentText() != "...":
            self.Const_DF.loc[self.Const_DF_index]=[(self.Opt_Const2_process.currentText(),self.Opt_Const2_flow.currentText()),self.Opt_Const2_Inequality.currentText(),self.Opt_Const2_val.text()]
            self.Const_DF_index +=1
            self.Opt_Const_table_update()
            self.constraints[(self.Opt_Const2_process.currentText(),self.Opt_Const2_flow.currentText())]= {'limit':float(self.Opt_Const2_val.text()),
                                                                                                                      'KeyType':'WasteToProcess',
                                                                                                                      'ConstType':self.Opt_Const2_Inequality.currentText()}
        
    @QtCore.Slot()
    def Opt_add_const3(self):
        if self.Opt_Const3_flow.currentText() != "...":
            self.Const_DF.loc[self.Const_DF_index]=[self.Opt_Const3_flow.currentText(),self.Opt_Const3_Inequality.currentText(),self.Opt_Const3_val.text()]
            self.Const_DF_index +=1
            self.Opt_Const_table_update()
            self.constraints[self.bio_dict[self.Opt_Const3_flow.currentText()]]= {'limit':float(self.Opt_Const3_val.text()),
                                                                                            'KeyType':'Emission',
                                                                                            'ConstType':self.Opt_Const3_Inequality.currentText()}                                                     
    
    @QtCore.Slot()
    def Opt_Const_table_update(self):
        self.Opt_Const_table_model = Table_from_pandas(self.Const_DF)
        self.Opt_Const_table.setModel(self.Opt_Const_table_model)
        self.Opt_Const_table.resizeColumnsToContents()

    @QtCore.Slot()
    def Opt_adv_func(self):
        # always show
        if self.opt_adv_options_status:
            self.adv_opt.show()
            self.adv_opt.exec_()
        else:
            self.adv_opt = QtWidgets.QDialog()
            self.opt_Widget = adv_opt_ui.Ui_adv_opt()
            self.opt_Widget.setupUi(self.adv_opt)
            
            self.opt_Widget.Opt_incld_flows.setChecked(True)
            
            conf=Optimization.config(self.demo)  
            ### conf Table
            if len(conf.columns) > 0:
                conf_table_model = Table_from_pandas_editable(conf)
                self.opt_Widget.Opt_Conf_table.setModel(conf_table_model)
                self.opt_Widget.Opt_Conf_table.resizeColumnsToContents()
                self.opt_Widget.Opt_Conf_table.installEventFilter(self)
                self.opt_Widget.Opt_Conf_table.setSortingEnabled(True)
            else:
                self.opt_Widget.Opt_Conf_table.setDisabled(True)
            
            self.opt_adv_options_status = True
    
    
    @QtCore.Slot()
    def Opt_minimize_func(self):
        functional_unit = {(self.Opt_FU_DB.currentText(),self.Opt_FU_act.currentText()):1}
        method = [ast.literal_eval( self.Opt_method.currentText())]
        project_name = self.demo.project_name
        Time_start = time()
        
        if self.opt_Widget.Multi_start_opt.isChecked(): 
            max_iter=self.opt_Widget.Opt_trial.value()
        else:
            max_iter = 1
        
        print("""
        Optimization setting:
        
        project_name = {}
        
        functional_unit = {}
        
        method = {}
        
        optimize flows = {}
        
        optimize collection scheme = {}
        
        number of iterations = {}
        
        constraints = {}
        
        """.format(project_name,functional_unit,method,
                    self.opt_Widget.Opt_incld_flows.isChecked(),
                    self.opt_Widget.Opt_incld_col.isChecked(),
                    max_iter,
                    self.constraints))
        
        if len(self.constraints)>0:
            constraints =self.constraints
        else:
            constraints = None
        
        self.opt = Optimization(functional_unit, method, self.demo) 
        if self.opt_Widget.Opt_incld_col.isChecked():
            self.opt.set_config(self.opt_Widget.Opt_Conf_table.model()._data)
        
        optimizer_thread = Worker_Optimize(parent=self.Opt_optimize,
                                           opt=self.opt,
                                           constraints=constraints,
                                           waste_param=self.opt_Widget.Opt_incld_flows.isChecked(),
                                           collection=self.opt_Widget.Opt_incld_col.isChecked(),
                                           is_multi=self.opt_Widget.Multi_start_opt.isChecked(),
                                           max_iter=self.opt_Widget.Opt_trial.value())
        optimizer_thread.UpdatePBr_Opt.connect(self.setPBr_Opt)
        optimizer_thread.report.connect(self.report_opt_func)
        optimizer_thread.start()
# =============================================================================
#         if self.opt_Widget.Multi_start_opt.isChecked():
#             results = self.opt.multi_start_optimization(constraints=constraints,
#                                                         waste_param=self.opt_Widget.Opt_incld_flows.isChecked(), 
#                                                         collection=self.opt_Widget.Opt_incld_col.isChecked(),
#                                                         max_iter=self.opt_Widget.Opt_trial.value())
#         else:
#             results = self.opt.optimize_parameters(constraints=constraints,
#                                                waste_param=self.opt_Widget.Opt_incld_flows.isChecked(), 
#                                                collection=self.opt_Widget.Opt_incld_col.isChecked())
# =============================================================================

    @QtCore.Slot(dict)
    def report_opt_func(self, report):
        print(report['results'])        
        
        print("Total time for optimization: {} seconds".format(report['time']))
        
        if report['results'].success:
            self.msg_popup('Optimization Result',report['results'].message+'\n Total time: {} seconds'.format(report['time']),'Information')
            obj = report['results'].fun*10**self.opt.magnitude
            self.Opt_score.setText(f_n(obj))
            unit =Method(self.opt.method[0]).metadata['unit'] 
            self.Opt_unit.setText(unit)
            
            param_data=pd.DataFrame(self.opt.optimized_x)
            param_data['Unit'] = 'fraction'
            Opt_Param_table_model = Table_from_pandas_editable(param_data)
            self.Opt_Param_table.setModel(Opt_Param_table_model)
            self.Opt_Param_table.resizeColumnsToContents()
            #Draw sankey
            self.Opt_draw_sankey_func()
        else:
            self.msg_popup('Optimization Result',report['results'].message,'Warning')

    @QtCore.Slot(dict)
    def setPBr_Opt(self, dict_):
        self.Opt_PBr.setMaximum(dict_['max'])
        self.Opt_PBr.setValue(dict_['val'])
        

    @QtCore.Slot()
    def Opt_CalObjFunc_func(self):
        x = list(self.Opt_Param_table.model()._data['amount'].values)
        obj=self.opt._objective_function(x)*10**self.opt.magnitude
        self.Opt_CalObjFunc_Res.setText(f_n(obj))
        print(' \n \n \n Constraints \n')
        
        for i,func in enumerate(self.opt.cons):
            if 'Name' in func:
                print('Constraint {} , {} = {}'.format(i,func['Name'],f_n(func['fun'](x))))
            else:
                print('Constraint {} = {}'.format(i,f_n(func['fun'](x))))
        
        self.Opt_draw_sankey_func(params=x)
        
    @QtCore.Slot()
    def Opt_update_network_parameters(self):
        new_param = deepcopy(self.demo.parameters_list)
        i=0
        for x in new_param:
            x['amount'] = self.Opt_Param_table.model()._data['amount'][i]
            i+=1
        print("\n\n New parameters are : \n",new_param,"\n\n")
       
        param_updater=Worker_UpdateParam(parent=self.Opt_update_param, project=self.demo, param=new_param)
        #param_updater.UpdatePBr_UpdateParam.connect(self.setPBr_UpdateParam)
        param_updater.report_time.connect(self.report_time_UpPar)
        param_updater.start()

    @QtCore.Slot(int)
    def report_time_UpPar(self, time):
        #Notift the user that the project has created successfully
        self.msg_popup('Parameters','Parameters are updated successfully in {} seconds'.format(time),'Information')
               
    @QtCore.Slot()
    def Opt_ClearConstr_func(self):
        self.Const_DF = pd.DataFrame(columns=['flow','inequality','limit'])
        self.Const_DF_index=0
        self.Opt_Const_table_update()
        self.constraints={}
        
    def Opt_draw_sankey_func(self,params = None):
        ### plot mass sankey
        if params:
            self.opt.plot_sankey(optimized_flow=True,show=False,fileName=os.getcwd()+'\\Optimized_sankey.html',params=params)
        else:        
            self.opt.plot_sankey(optimized_flow=self.opt_Widget.Opt_incld_flows.isChecked(),
                                 show=False,fileName=os.getcwd()+'\\Optimized_sankey.html')
        self.html_figur = QWebEngineView()
        self.html_figur.setWindowIcon(self.icon)
        self.html_figur.setWindowTitle('swolfpy: Sankey Diagram')
        self.html_figur.setUrl(QtCore.QUrl.fromLocalFile(os.getcwd()+'\\Optimized_sankey.html'))
        self.html_figur.show()
                    
        
#%% General Functions          
# =============================================================================
# =============================================================================
    ### General Functions
# =============================================================================
# =============================================================================
    def eventFilter(self, obj, event):
        if isinstance(obj,QtWidgets.QTableView):
            if event.type() == QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.Copy):
                self.copySelection(obj)
                return True
            elif event.type() == QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.Paste):
                self.pasteSelection(obj)
                return True
            else:
                return False
        else:
            # pass the event on to the parent class
            return super(MyQtApp,self).eventFilter(obj, event)

    # Copy function for QTabelView
    def copySelection(self,obj):
        selection = obj.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtWidgets.QApplication.clipboard().setText(stream.getvalue())
    
    # Paste function for QTabelView
    def pasteSelection(self,obj):
        model = obj.model()
        if hasattr(model,'setData'):
            selection = obj.selectedIndexes()
            if selection:
                buffer = QtWidgets.QApplication.clipboard().text() 
                rows = sorted(index.row() for index in selection)
                columns = sorted(index.column() for index in selection)
                reader = csv.reader(io.StringIO(buffer), delimiter='\t')
                #if the user select only one cell for the location
                if len(rows) == 1 and len(columns) == 1:
                    for i, line in enumerate(reader):
                        for j, cell in enumerate(line):
                            #check that the index is availble in the table
                            if (rows[0]+i) < model.rowCount() and (columns[0]+j) < model.columnCount():     
                                model.setData(model.index(rows[0]+i,columns[0]+j), cell)
                else:
                    arr = [ [ cell for cell in row ] for row in reader]
                    for index in selection:
                        row = index.row() - rows[0]
                        column = index.column() - columns[0]
                        model.setData(model.index(index.row(), index.column()), arr[row][column])
        else:
            print('Warning: The table is not editable!')


    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def select_file(self, LineEdit,Filter):
        fileDialog = QtWidgets.QFileDialog()
        def edit_line():
            #file_name = str(fileDialog.getOpenFileName(filter=Filter)[0]).split('/')[-1]
            file_name = str(fileDialog.getOpenFileName(filter=Filter)[0])
            LineEdit.setText(file_name)
        return(edit_line)

    @QtCore.Slot()  # select file and read the name of it. Import the name to the LineEdit.
    def select_dir(self, LineEdit):
        fileDialog = QtWidgets.QFileDialog()
        def edit_line():
            Directory = str(fileDialog.getExistingDirectory())
            LineEdit.setText(Directory)
        return(edit_line)
        
    @QtCore.Slot()
    def save(self):
        """
        https://stackoverflow.com/questions/15416334/qfiledialog-how-to-set-default-filename-in-save-as-dialog
        """
        cwd = os.getcwd()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", cwd + "/" +self.P_Name , "*.pickle")
        if path:
            file = open(path, 'wb')
            pickle.dump(self.demo, file)
        
    def msg_popup(self,Subject,Information,Type):
        msg = QtWidgets.QMessageBox()
        if Type =='Warning':
            msg.setIcon(msg.Icon.Warning)
        elif Type == 'Information':
            msg.setIcon(msg.Icon.Information)
        msg.setWindowTitle('swolfpy')
        msg.setWindowIcon(self.icon)
        msg.setText(Subject)
        msg.setInformativeText(Information)
        Ok=msg.addButton(msg.Ok)
        msg.exec()


    @QtCore.Slot(int)
    def load_db_func(self,act_ComboBox):
        def load_db_func(i):
            if i ==0:
                act_ComboBox.clear()
            else:
                db=Database(self.DB_name_list[i-1])
                acts = [str(x.key[1]) for x in db]
                acts.sort()
                act_ComboBox.clear()
                act_ComboBox.addItems(acts)  
        return(load_db_func)

    @QtCore.Slot(str)
    def load_act_unit(self,db_ComboBox,Unit_label):
        def load_act_unit(i):
            if len(i) > 0:
                act=get_activity((db_ComboBox.currentText(),i))
                Unit = act.as_dict()['unit']
                Unit_label.setText('{}'.format(Unit))
            else:
                Unit_label.setText('...')
        return(load_act_unit)

    @QtCore.Slot()
    def Filter_Method_func(self,keyWord_lineEdit,Method_ComboBox):
        def Filter_Method_func_helper():
            list_methods= [str(x) for x in methods if keyWord_lineEdit.text() in str(x)]
            list_methods.sort()
            Method_ComboBox.clear()
            Method_ComboBox.addItems(['...']+list_methods)  
        return(Filter_Method_func_helper)


    @QtCore.Slot()
    def on_downloadRequested(self, download):
        """
        https://stackoverflow.com/questions/55963931/how-to-download-csv-file-with-qwebengineview-and-qurl
        """
        old_path = download.url().path()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*.png")
        if path:
            download.setPath(path)
            download.accept()

