# -*- coding: utf-8 -*-
"""
@author: msardar2

Solid Waste Optimization Life-cycle Framework in Python(SwolfPy)
"""
import sys
import warnings

from PySide2 import QtWidgets

from .Monte_Carlo import Monte_Carlo
from .Optimization import Optimization
from .Project import Project
from .swolfpy_method import import_methods
from .Technosphere import Technosphere
from .UI.PySWOLF_run import MyQtApp

warnings.filterwarnings("ignore", category=RuntimeWarning)


__all__ = [
    "Technosphere",
    "Project",
    "import_methods",
    "Optimization",
    "Monte_Carlo",
    "MyQtApp",
    "swolfpy",
]

__version__ = "1.0.1"


class swolfpy:
    def __init__(self):
        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance()

        self.qt_app = MyQtApp()
        availableGeometry = self.app.desktop().availableGeometry(self.qt_app)
        self.qt_app.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2.85 / 3)
        self.qt_app.show()
        self.app.exec_()
