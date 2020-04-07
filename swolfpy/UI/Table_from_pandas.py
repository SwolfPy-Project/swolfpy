# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:40:11 2020

@author: msardar2
"""
from PySide2 import QtWidgets, QtGui, QtCore
import numpy as np
import io
import csv

def f_n(x):
    """
    format number function
    If the input is string, it returns string but if the input in number, it will return it in sceintific format.
    """
    if (isinstance(x,float) or isinstance(x,int)) and len(str(x))>6:
        return("{:.4e}".format(x))
    else:
        return(str(x))


#%% Table: View Pandas Data Frame
class Table_from_pandas(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return f_n(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return str(self._data.columns[col])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[col]
    
    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        """sort table by given column number column"""
        if order == QtCore.Qt.AscendingOrder:
            self._data = self._data.sort_values(self._data.columns[col],ascending=True)
        elif order == QtCore.Qt.DescendingOrder:
            self._data = self._data.sort_values(self._data.columns[col],ascending=False)
        """
        If the structure of the underlying data changes, the model can emit layoutChanged() to
        indicate to any attached views that they should redisplay any items shown, taking the
        new structure into account.
        """
        self.layoutChanged.emit()


#%% Table: View and edit Pandas Data Frame
class Table_from_pandas_editable(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return f_n(self._data.iloc[index.row(), index.column()])
            
            elif role == QtCore.Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
                     
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[col]
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        """sort table by given column number column"""
        if order == QtCore.Qt.AscendingOrder:
            self._data = self._data.sort_values(self._data.columns[col],ascending=True)
        elif order == QtCore.Qt.DescendingOrder:
            self._data = self._data.sort_values(self._data.columns[col],ascending=False)
        """
        If the structure of the underlying data changes, the model can emit layoutChanged() to
        indicate to any attached views that they should redisplay any items shown, taking the
        new structure into account.
        """
        self.layoutChanged.emit()

#%% Table: Distance Table
class Table_modeifed_distanceTable(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return f_n(self._data.iloc[index.row(), index.column()])

            if role==QtCore.Qt.BackgroundColorRole and index.row() >= index.column():
                return QtGui.QBrush(QtCore.Qt.gray)
            
            if role == QtCore.Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
                     
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[col]
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.row() >= index.column():
             return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable           
        
#%% Table: Collection scheme table
class Table_modeifed_collection_schm(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return f_n(self._data.iloc[index.row(), index.column()])
            
            # gray color for fix cells
            elif role==QtCore.Qt.BackgroundColorRole and index.column()==0:
                return QtGui.QBrush(QtCore.Qt.white)
            elif role==QtCore.Qt.BackgroundColorRole and self._data.iloc[0, index.column()]==0 and index.row()>=1:
                return QtGui.QBrush(QtCore.Qt.gray)
            
            elif role==QtCore.Qt.BackgroundColorRole and self._data.iloc[0, index.column()]>0 and index.row() in [1,2,3,4]:
                return QtGui.QBrush(QtCore.Qt.cyan)
            
            elif role==QtCore.Qt.BackgroundColorRole and self._data.iloc[0, index.column()]>0 and index.row() in [5,6]:
                return QtGui.QBrush(QtCore.Qt.darkGreen)
            
            elif role==QtCore.Qt.BackgroundColorRole and index.row() ==0 and index.column() !=0:
                return QtGui.QBrush(QtCore.Qt.darkMagenta)
            
            
            elif role == QtCore.Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
                     
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data.index[col]
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.row()==0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable  
        elif index.column()>=1:
            if self._data.iloc[0, index.column()]>0:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
            else:
                return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    