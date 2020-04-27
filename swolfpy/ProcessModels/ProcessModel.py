# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:31:49 2020

@author: msmsa
"""
from abc import ABC, abstractmethod 
import pandas as pd
from .CommonData import *

class ProcessModel(ABC):
    def __init__(self,CommonDataObjct):
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()
            
        ### Read Material properties
        self.Material_Properties=pd.read_excel(Path(__file__).parent.parent/"Data/Material properties.xlsx",index_col = 'Materials')
        self.Material_Properties.fillna(0,inplace=True)

        self.Index = self.CommonData.Index

    @property
    @abstractmethod
    def Process_Type(self):
        pass

    @abstractmethod
    def calc(self):
        pass
    
    @abstractmethod
    def setup_MC(self,seed=None):
        pass
    
    @abstractmethod
    def MC_calc(self):
        pass
    
    @abstractmethod
    def report(self):
        pass