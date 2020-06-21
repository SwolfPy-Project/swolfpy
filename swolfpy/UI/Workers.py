# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:54:15 2020

@author: msmsa
"""
from PySide2 import QtCore
from time import time

class Worker_WriteProject(QtCore.QThread):
    """
    This class instantiates a new QThread that creates the projects.\n
    We need QThread because we don't want the GUI to be freezed while writing the project.
    """    
    UpdatePBr_WriteProject = QtCore.Signal(int)
    report_time = QtCore.Signal(int)
        
    def __init__(self, parent,project):
        super().__init__(parent)
        self.project= project

    def run(self):
        Time_start = time()
        # set the signal in the Porject class
        self.project.init_project(signal=self.UpdatePBr_WriteProject)
        self.project.write_project(signal=self.UpdatePBr_WriteProject)
        self.project.group_exchanges(signal=self.UpdatePBr_WriteProject)
        Time_finish = time()
        self.report_time.emit(round(Time_finish - Time_start))
        

class Worker_UpdateParam(QtCore.QThread):
    """
    This class instantiates a new QThread that update the project parameters.\n
    """    
    UpdatePBr_UpdateParam = QtCore.Signal(int)
    report_time = QtCore.Signal(int)
        
    def __init__(self, parent,project,param):
        super().__init__(parent)
        self.project= project
        self.param = param

    def run(self):
        Time_start = time()
        self.project.update_parameters(self.param,signal=self.UpdatePBr_UpdateParam)
        Time_finish = time()
        self.report_time.emit(round(Time_finish - Time_start))        
            
            
        
    