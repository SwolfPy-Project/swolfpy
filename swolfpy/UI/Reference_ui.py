# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Reference.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import PyWOLF_Resource_rc

class Ui_References(object):
    def setupUi(self, References):
        if not References.objectName():
            References.setObjectName(u"References")
        References.resize(781, 847)
        icon = QIcon()
        icon.addFile(u":/ICONS/PySWOLF_ICONS/PySWOLF.ico", QSize(), QIcon.Normal, QIcon.Off)
        References.setWindowIcon(icon)
        self.gridLayout = QGridLayout(References)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(References)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.kwrd = QLineEdit(self.groupBox)
        self.kwrd.setObjectName(u"kwrd")

        self.horizontalLayout.addWidget(self.kwrd)

        self.Filter = QPushButton(self.groupBox)
        self.Filter.setObjectName(u"Filter")
        icon1 = QIcon()
        icon1.addFile(u":/ICONS/PySWOLF_ICONS/Filter.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Filter.setIcon(icon1)

        self.horizontalLayout.addWidget(self.Filter)

        self.Export = QPushButton(self.groupBox)
        self.Export.setObjectName(u"Export")
        icon2 = QIcon()
        icon2.addFile(u":/ICONS/PySWOLF_ICONS/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Export.setIcon(icon2)

        self.horizontalLayout.addWidget(self.Export)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.TableRef = QTableView(self.groupBox)
        self.TableRef.setObjectName(u"TableRef")

        self.gridLayout_2.addWidget(self.TableRef, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(References)

        QMetaObject.connectSlotsByName(References)
    # setupUi

    def retranslateUi(self, References):
        References.setWindowTitle(QCoreApplication.translate("References", u"SwolfPy References ", None))
        self.groupBox.setTitle(QCoreApplication.translate("References", u"References", None))
        self.kwrd.setInputMask("")
        self.kwrd.setPlaceholderText(QCoreApplication.translate("References", u"Filter", None))
        self.Filter.setText(QCoreApplication.translate("References", u"Filter", None))
        self.Export.setText(QCoreApplication.translate("References", u"Export", None))
    # retranslateUi

