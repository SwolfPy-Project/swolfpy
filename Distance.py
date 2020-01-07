# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:50:00 2020

@author: msardar2
"""
import pandas as pd
class Distance():
    def __init__(self,path):
        self.data = pd.read_csv(path,index_col='Index')
        self.Distance = {}
        for i in self.data.columns:
            for j in self.data.columns:
                if (j,i) not in self.Distance.keys():
                    if not pd.isna(self.data[i][j]):
                        self.Distance[(i,j)] = self.data[i][j]
                        self.Distance[(j,i)] = self.data[i][j]
                        if not pd.isna(self.data[j][i]) and self.data[j][i]!=self.data[i][j]:
                            raise Exception(f'Distance from {i} to {j} is not equal to distance from {j} to {i}')
                            
