# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adv_opt.ui',
# licensing of 'adv_opt.ui' applies.
#
# Created: Thu Jun 11 01:14:02 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_adv_opt(object):
    def setupUi(self, adv_opt):
        adv_opt.setObjectName("adv_opt")
        adv_opt.resize(621, 991)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ICONS/PySWOLF_ICONS/PySWOLF.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        adv_opt.setWindowIcon(icon)
        self.gridLayout_5 = QtWidgets.QGridLayout(adv_opt)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(adv_opt)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Opt_Conf_table = QtWidgets.QTableView(self.groupBox_2)
        self.Opt_Conf_table.setObjectName("Opt_Conf_table")
        self.gridLayout_3.addWidget(self.Opt_Conf_table, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(adv_opt)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.Opt_incld_flows = QtWidgets.QCheckBox(self.groupBox)
        self.Opt_incld_flows.setObjectName("Opt_incld_flows")
        self.gridLayout.addWidget(self.Opt_incld_flows, 0, 0, 1, 2)
        self.Opt_incld_col = QtWidgets.QCheckBox(self.groupBox)
        self.Opt_incld_col.setObjectName("Opt_incld_col")
        self.gridLayout.addWidget(self.Opt_incld_col, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.Multi_start_opt = QtWidgets.QCheckBox(self.groupBox)
        self.Multi_start_opt.setObjectName("Multi_start_opt")
        self.gridLayout.addWidget(self.Multi_start_opt, 2, 0, 1, 1)
        self.Opt_trial = QtWidgets.QSpinBox(self.groupBox)
        self.Opt_trial.setObjectName("Opt_trial")
        self.gridLayout.addWidget(self.Opt_trial, 2, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(adv_opt)
        QtCore.QMetaObject.connectSlotsByName(adv_opt)

    def retranslateUi(self, adv_opt):
        adv_opt.setWindowTitle(QtWidgets.QApplication.translate("adv_opt", "Optimization setting", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("adv_opt", "Collection scheme decision variables", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("adv_opt", "Options", None, -1))
        self.Opt_incld_flows.setText(QtWidgets.QApplication.translate("adv_opt", "Optimize waste fractions", None, -1))
        self.Opt_incld_col.setText(QtWidgets.QApplication.translate("adv_opt", "Optimize collection scheme", None, -1))
        self.Multi_start_opt.setText(QtWidgets.QApplication.translate("adv_opt", "Multi_start", None, -1))

from . import PyWOLF_Resource_rc
