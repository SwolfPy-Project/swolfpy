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
        """Create Distance object.            

        :param path: Path to the *csv* file
        :type path: str, optional
        :param Data: Padans Dataframe for the distances between the process models. Dataframe should use the name of processes as both column and row index.
        :type Data: class: `pandas.DataFrame` , optional

        :Example:
        
        >>> from swolfpy.Distance import Distance
        >>> import pandas as pd
        >>> Processes = ['LF','WTE','AD']
        >>> Data = pd.DataFrame([[None,20,30],[None,None,10],[None,None,None]],index=Processes,columns=Processes)
        >>> Data
               LF   WTE    AD
        LF   None  20.0  30.0
        WTE  None   NaN  10.0
        AD   None   NaN   NaN
        >>> distance = Distance(Data=Data)
        >>> distance.Distance[('LF','WTE')]
        20.0
        
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