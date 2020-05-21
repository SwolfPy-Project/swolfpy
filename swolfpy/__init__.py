# -*- coding: utf-8 -*-
"""
@author: msardar2

Solid Waste Optimization Life-cycle Framework in Python(SwolfPy)
"""


__all__ = [
    'Technosphere',
    'Project',
    'import_methods',
    'Optimization',
    'Monte_Carlo',
    'MyQtApp',
    'swolfpy'
]

__version__ = '0.1.8'


from .Technosphere import Technosphere
from .Project import Project
from .swolfpy_method import import_methods
from .Optimization import Optimization
from .Monte_Carlo import Monte_Carlo
from .UI.PySWOLF_run import MyQtApp
from PySide2 import QtCore, QtGui, QtWidgets

class swolfpy():
    def __init__(self):
        self.app = QtWidgets.QApplication()
        self.qt_app  = MyQtApp()
        self. qt_app.show()
        self.app.exec_()


