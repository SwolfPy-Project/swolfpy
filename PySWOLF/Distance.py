# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:50:00 2020

@author: msardar2
"""
import pandas as pd
class Distance():
    """Python class for importing the distances between the process models

    The Distance class import the distances from path to *csv* file or *pandas.DataFrame* and report it with ``self.Distance[(i,j)]`` which shows the distance from process i to process j.

    """
    def __init__(self,path=None,Data=None):
        """Create Distance class.

        Args:
            * *path* (str,optional): Path to the *csv* file.
            * *Data* (pd.DataFrame, optional): Padans Dataframe for the distances between the process models. Dataframe should use the name of processes as both column and row index.

        Returns:
            A new Distance object.

        """
        if path:
            self.data = pd.read_csv(path,index_col='Index')
        elif isinstance(Data,pd.DataFrame) :
            self.data = Data
        self.Distance = {}
        for i in self.data.columns:
            for j in self.data.columns:
                if (j,i) not in self.Distance.keys():
                    if not pd.isna(self.data[i][j]) and self.data[i][j]!='':
                        self.Distance[(i,j)] = self.data[i][j]
                        self.Distance[(j,i)] = self.data[i][j]
                        if not pd.isna(self.data[j][i]) and self.data[j][i]!='' and self.data[j][i]!=self.data[i][j]:
                            raise Exception(f'Distance from {i} to {j} is not equal to distance from {j} to {i}')
                            
