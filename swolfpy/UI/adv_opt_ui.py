# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'adv_opt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import PyWOLF_Resource_rc

class Ui_adv_opt(object):
    def setupUi(self, adv_opt):
        if not adv_opt.objectName():
            adv_opt.setObjectName(u"adv_opt")
        adv_opt.resize(621, 991)
        icon = QIcon()
        icon.addFile(u":/ICONS/PySWOLF_ICONS/PySWOLF.ico", QSize(), QIcon.Normal, QIcon.Off)
        adv_opt.setWindowIcon(icon)
        self.gridLayout_5 = QGridLayout(adv_opt)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_2 = QGroupBox(adv_opt)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.Opt_Conf_table = QTableView(self.groupBox_2)
        self.Opt_Conf_table.setObjectName(u"Opt_Conf_table")

        self.gridLayout_3.addWidget(self.Opt_Conf_table, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox = QGroupBox(adv_opt)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.method = QComboBox(self.groupBox)
        self.method.setObjectName(u"method")

        self.gridLayout.addWidget(self.method, 3, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.nproc = QSpinBox(self.groupBox)
        self.nproc.setObjectName(u"nproc")

        self.gridLayout.addWidget(self.nproc, 2, 1, 1, 1)

        self.Multi_start_opt = QCheckBox(self.groupBox)
        self.Multi_start_opt.setObjectName(u"Multi_start_opt")

        self.gridLayout.addWidget(self.Multi_start_opt, 1, 0, 1, 1)

        self.Opt_trial = QSpinBox(self.groupBox)
        self.Opt_trial.setObjectName(u"Opt_trial")

        self.gridLayout.addWidget(self.Opt_trial, 1, 1, 1, 1)

        self.Opt_incld_col = QCheckBox(self.groupBox)
        self.Opt_incld_col.setObjectName(u"Opt_incld_col")

        self.gridLayout.addWidget(self.Opt_incld_col, 0, 0, 1, 2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.timeout = QSpinBox(self.groupBox)
        self.timeout.setObjectName(u"timeout")

        self.gridLayout.addWidget(self.timeout, 4, 1, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(adv_opt)

        QMetaObject.connectSlotsByName(adv_opt)
    # setupUi

    def retranslateUi(self, adv_opt):
        adv_opt.setWindowTitle(QCoreApplication.translate("adv_opt", u"Optimization setting", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("adv_opt", u"Collection scheme decision variables", None))
        self.groupBox.setTitle(QCoreApplication.translate("adv_opt", u"Options", None))
        self.label_2.setText(QCoreApplication.translate("adv_opt", u"Initial guess", None))
        self.label.setText(QCoreApplication.translate("adv_opt", u"Number of theads", None))
        self.Multi_start_opt.setText(QCoreApplication.translate("adv_opt", u"Multi_start", None))
        self.Opt_incld_col.setText(QCoreApplication.translate("adv_opt", u"Optimize collection scheme", None))
        self.label_3.setText(QCoreApplication.translate("adv_opt", u"Timeout", None))
    # retranslateUi

