# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:54:15 2020

@author: msmsa
"""
from PySide2 import QtCore
from time import time
from ..Optimization import Optimization

#%% Write project

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
        
#%% Update parameters
class Worker_UpdateParam(QtCore.QThread):
    """
    This class instantiates a new QThread that update the project parameters.\n
    """    
    UpdatePBr_UpdateParam = QtCore.Signal(int)
    report_time = QtCore.Signal(int)
    report_error = QtCore.Signal(str)
        
    def __init__(self, parent, project, param):
        super().__init__(parent)
        self.project= project
        self.param = param

    def run(self):
        Time_start = time()
        try:
            self.project.update_parameters(self.param,signal=self.UpdatePBr_UpdateParam)
        except Exception as e:
            self.report_error.emit(e.__str__())
            return False
        Time_finish = time()
        self.report_time.emit(round(Time_finish - Time_start))      
        return True


#%% Optimize
class Worker_Optimize(QtCore.QThread):
    """
    This class instantiates a new QThread that handle the optimization.\n
    """    
    UpdatePBr_Opt = QtCore.Signal(dict)
    report = QtCore.Signal(dict)
        
    def __init__(self, parent, opt, constraints, collection, is_multi, n_iter, n_proc, iter_mehtod, timeout):
        super().__init__(parent)
        self.opt= opt
        self.constraints = constraints
        self.collection  = collection
        self.is_multi=is_multi
        self.n_iter = n_iter
        self.n_proc = n_proc
        self.iter_mehtod = iter_mehtod
        self.timeout = timeout

    def run(self):
        self.UpdatePBr_Opt.emit({'max':0,'val':0})
        Time_start = time()
        results = Optimization.multi_start_optimization(self.opt, 
                                                        constraints=self.constraints,
                                                        collection=self.collection,
                                                        n_iter=self.n_iter if self.is_multi else 1,
                                                        timeout=self.timeout,
                                                        nproc=self.n_proc,
                                                        initialize_guess=self.iter_mehtod)
        Time_finish = time()
        self.UpdatePBr_Opt.emit({'max':1,'val':1})
        self.report.emit({'time':round(Time_finish - Time_start),'results':results})              
            

#%% Optimize
class Worker_MC(QtCore.QThread):
    """
    This class instantiates a new QThread that handle the MC.\n
    """    
    UpdatePBr_Opt = QtCore.Signal(dict)
    report = QtCore.Signal(dict)
        
    def __init__(self,parent,MC,nproc, n):
        super().__init__(parent)
        self.MC= MC
        self.nproc = nproc
        self.n = n

    def run(self):
        self.UpdatePBr_Opt.emit({'max':0,'val':0})
        Time_start = time()
        self.MC.run(self.nproc,self.n)
        MC_results = self.MC.result_to_DF()
        Time_finish = time()
        self.UpdatePBr_Opt.emit({'max':1,'val':1})
        self.report.emit({'time':round(Time_finish - Time_start),'results':MC_results})     
        
    