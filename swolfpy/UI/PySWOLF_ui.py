# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PySWOLF.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import  PyWOLF_Resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(941, 830)
        MainWindow.setMinimumSize(QSize(800, 800))
        icon = QIcon()
        icon.addFile(u":/ICONS/PySWOLF_ICONS/PySWOLF.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionHelp_Guides = QAction(MainWindow)
        self.actionHelp_Guides.setObjectName(u"actionHelp_Guides")
        icon1 = QIcon()
        icon1.addFile(u":/ICONS/PySWOLF_ICONS/Help.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionHelp_Guides.setIcon(icon1)
        self.actionReferences = QAction(MainWindow)
        self.actionReferences.setObjectName(u"actionReferences")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.PySWOLF = QTabWidget(self.centralwidget)
        self.PySWOLF.setObjectName(u"PySWOLF")
        self.PySWOLF.setEnabled(True)
        font = QFont()
        font.setKerning(True)
        self.PySWOLF.setFont(font)
        self.Start = QWidget()
        self.Start.setObjectName(u"Start")
        self.gridLayout_2 = QGridLayout(self.Start)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.textBrowser = QTextBrowser(self.Start)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QSize(0, 0))
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)

        self.verticalLayout_11.addWidget(self.textBrowser)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_11.addItem(self.verticalSpacer_4)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_17)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_8 = QGroupBox(self.Start)
        self.groupBox_8.setObjectName(u"groupBox_8")
        font1 = QFont()
        font1.setBold(True)
        font1.setWeight(75)
        font1.setKerning(True)
        self.groupBox_8.setFont(font1)
        self.gridLayout_72 = QGridLayout(self.groupBox_8)
        self.gridLayout_72.setObjectName(u"gridLayout_72")
        self.label_55 = QLabel(self.groupBox_8)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_72.addWidget(self.label_55, 0, 0, 1, 1)

        self.Start_def_process = QRadioButton(self.groupBox_8)
        self.Start_def_process.setObjectName(u"Start_def_process")
        font2 = QFont()
        font2.setBold(False)
        font2.setWeight(50)
        font2.setKerning(True)
        self.Start_def_process.setFont(font2)

        self.gridLayout_72.addWidget(self.Start_def_process, 1, 0, 1, 1)

        self.Start_new_project = QPushButton(self.groupBox_8)
        self.Start_new_project.setObjectName(u"Start_new_project")
        font3 = QFont()
        font3.setBold(False)
        font3.setUnderline(False)
        font3.setWeight(50)
        font3.setKerning(True)
        self.Start_new_project.setFont(font3)

        self.gridLayout_72.addWidget(self.Start_new_project, 3, 0, 1, 2)

        self.Start_user_process = QRadioButton(self.groupBox_8)
        self.Start_user_process.setObjectName(u"Start_user_process")
        self.Start_user_process.setFont(font2)

        self.gridLayout_72.addWidget(self.Start_user_process, 2, 0, 1, 2)


        self.verticalLayout_10.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.Start)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setFont(font1)
        self.gridLayout_73 = QGridLayout(self.groupBox_9)
        self.gridLayout_73.setObjectName(u"gridLayout_73")
        self.Start_load_project = QPushButton(self.groupBox_9)
        self.Start_load_project.setObjectName(u"Start_load_project")
        self.Start_load_project.setFont(font3)
        icon2 = QIcon()
        icon2.addFile(u":/ICONS/PySWOLF_ICONS/Load.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Start_load_project.setIcon(icon2)

        self.gridLayout_73.addWidget(self.Start_load_project, 0, 0, 1, 1)


        self.verticalLayout_10.addWidget(self.groupBox_9)


        self.horizontalLayout_15.addLayout(self.verticalLayout_10)


        self.verticalLayout_11.addLayout(self.horizontalLayout_15)


        self.gridLayout_2.addLayout(self.verticalLayout_11, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.Start, "")
        self.Import_PM = QWidget()
        self.Import_PM.setObjectName(u"Import_PM")
        self.Import_PM.setEnabled(True)
        self.gridLayout_21 = QGridLayout(self.Import_PM)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.ImportProcessModels = QPushButton(self.Import_PM)
        self.ImportProcessModels.setObjectName(u"ImportProcessModels")
        self.ImportProcessModels.setMinimumSize(QSize(200, 0))
        self.ImportProcessModels.setIcon(icon2)

        self.gridLayout_21.addWidget(self.ImportProcessModels, 1, 1, 1, 1)

        self.init_process_toolbox = QTabWidget(self.Import_PM)
        self.init_process_toolbox.setObjectName(u"init_process_toolbox")
        self.PM_PMTab = QWidget()
        self.PM_PMTab.setObjectName(u"PM_PMTab")
        self.gridLayout_22 = QGridLayout(self.PM_PMTab)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.groupBox_3 = QGroupBox(self.PM_PMTab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_24 = QGridLayout(self.groupBox_3)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.PM = QComboBox(self.groupBox_3)
        self.PM.setObjectName(u"PM")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PM.sizePolicy().hasHeightForWidth())
        self.PM.setSizePolicy(sizePolicy1)
        self.PM.setMinimumSize(QSize(300, 0))
        self.PM.setFont(font2)

        self.gridLayout_24.addWidget(self.PM, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.gridLayout_24.addWidget(self.label_4, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(350, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)

        self.Help_ImportProcess = QPushButton(self.groupBox_3)
        self.Help_ImportProcess.setObjectName(u"Help_ImportProcess")
        self.Help_ImportProcess.setIcon(icon1)
        self.Help_ImportProcess.setIconSize(QSize(24, 24))

        self.gridLayout_24.addWidget(self.Help_ImportProcess, 0, 2, 1, 1)


        self.gridLayout_22.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.PM_PMTab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.IT_Default = QRadioButton(self.groupBox)
        self.IT_Default.setObjectName(u"IT_Default")
        self.IT_Default.setFont(font2)

        self.gridLayout_6.addWidget(self.IT_Default, 0, 1, 1, 1)

        self.IT_UserDefine = QRadioButton(self.groupBox)
        self.IT_UserDefine.setObjectName(u"IT_UserDefine")
        self.IT_UserDefine.setFont(font2)

        self.gridLayout_6.addWidget(self.IT_UserDefine, 0, 2, 1, 1)

        self.IT_BR = QToolButton(self.groupBox)
        self.IT_BR.setObjectName(u"IT_BR")
        self.IT_BR.setFont(font2)

        self.gridLayout_6.addWidget(self.IT_BR, 0, 3, 1, 1)

        self.IT_FName = QLineEdit(self.groupBox)
        self.IT_FName.setObjectName(u"IT_FName")
        self.IT_FName.setFont(font2)

        self.gridLayout_6.addWidget(self.IT_FName, 0, 4, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(400, 330))
        self.gridLayout_23 = QGridLayout(self.groupBox_2)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.frame_rec = QFrame(self.groupBox_2)
        self.frame_rec.setObjectName(u"frame_rec")
        self.frame_rec.setFont(font2)
        self.frame_rec.setFrameShape(QFrame.StyledPanel)
        self.frame_rec.setFrameShadow(QFrame.Raised)

        self.gridLayout_23.addWidget(self.frame_rec, 0, 4, 1, 1)

        self.frame_Prod = QFrame(self.groupBox_2)
        self.frame_Prod.setObjectName(u"frame_Prod")
        self.frame_Prod.setFont(font2)
        self.frame_Prod.setFrameShape(QFrame.StyledPanel)
        self.frame_Prod.setFrameShadow(QFrame.Raised)

        self.gridLayout_23.addWidget(self.frame_Prod, 0, 2, 1, 1)

        self.frame_Col = QFrame(self.groupBox_2)
        self.frame_Col.setObjectName(u"frame_Col")
        self.frame_Col.setFont(font2)
        self.frame_Col.setFrameShape(QFrame.StyledPanel)
        self.frame_Col.setFrameShadow(QFrame.Raised)

        self.gridLayout_23.addWidget(self.frame_Col, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_2, 1, 0, 1, 5)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_6)

        self.Clear_PM_setting = QPushButton(self.groupBox)
        self.Clear_PM_setting.setObjectName(u"Clear_PM_setting")
        self.Clear_PM_setting.setFont(font2)
        icon3 = QIcon()
        icon3.addFile(u":/ICONS/PySWOLF_ICONS/Remove.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Clear_PM_setting.setIcon(icon3)

        self.horizontalLayout_11.addWidget(self.Clear_PM_setting)

        self.Update_PM_setting = QPushButton(self.groupBox)
        self.Update_PM_setting.setObjectName(u"Update_PM_setting")
        self.Update_PM_setting.setFont(font2)
        icon4 = QIcon()
        icon4.addFile(u":/ICONS/PySWOLF_ICONS/Update.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Update_PM_setting.setIcon(icon4)

        self.horizontalLayout_11.addWidget(self.Update_PM_setting)


        self.gridLayout_6.addLayout(self.horizontalLayout_11, 2, 0, 1, 5)


        self.gridLayout_22.addWidget(self.groupBox, 1, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_22.addItem(self.horizontalSpacer_4, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_22.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.init_process_toolbox.addTab(self.PM_PMTab, "")
        self.PM_CMTab = QWidget()
        self.PM_CMTab.setObjectName(u"PM_CMTab")
        self.gridLayout_199 = QGridLayout(self.PM_CMTab)
        self.gridLayout_199.setObjectName(u"gridLayout_199")
        self.frame_7 = QFrame(self.PM_CMTab)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_7)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.groupBox_38 = QGroupBox(self.frame_7)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setFont(font1)
        self.gridLayout_96 = QGridLayout(self.groupBox_38)
        self.gridLayout_96.setObjectName(u"gridLayout_96")
        self.IT_BR_0 = QToolButton(self.groupBox_38)
        self.IT_BR_0.setObjectName(u"IT_BR_0")
        self.IT_BR_0.setFont(font2)

        self.gridLayout_96.addWidget(self.IT_BR_0, 0, 2, 1, 1)

        self.IT_UserDefine_0 = QRadioButton(self.groupBox_38)
        self.IT_UserDefine_0.setObjectName(u"IT_UserDefine_0")
        self.IT_UserDefine_0.setFont(font2)

        self.gridLayout_96.addWidget(self.IT_UserDefine_0, 0, 1, 1, 1)

        self.IT_FName_0 = QLineEdit(self.groupBox_38)
        self.IT_FName_0.setObjectName(u"IT_FName_0")
        self.IT_FName_0.setMinimumSize(QSize(250, 0))
        self.IT_FName_0.setFont(font2)

        self.gridLayout_96.addWidget(self.IT_FName_0, 0, 3, 1, 1)

        self.IT_Default_0 = QRadioButton(self.groupBox_38)
        self.IT_Default_0.setObjectName(u"IT_Default_0")
        self.IT_Default_0.setFont(font2)

        self.gridLayout_96.addWidget(self.IT_Default_0, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.groupBox_38, 0, 0, 1, 1)

        self.horizontalSpacer_35 = QSpacerItem(733, 939, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_35, 0, 1, 3, 1)

        self.groupBox_37 = QGroupBox(self.frame_7)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setFont(font1)
        self.gridLayout_97 = QGridLayout(self.groupBox_37)
        self.gridLayout_97.setObjectName(u"gridLayout_97")
        self.IT_Default_00 = QRadioButton(self.groupBox_37)
        self.IT_Default_00.setObjectName(u"IT_Default_00")
        self.IT_Default_00.setFont(font2)

        self.gridLayout_97.addWidget(self.IT_Default_00, 0, 0, 1, 1)

        self.IT_UserDefine_00 = QRadioButton(self.groupBox_37)
        self.IT_UserDefine_00.setObjectName(u"IT_UserDefine_00")
        self.IT_UserDefine_00.setFont(font2)

        self.gridLayout_97.addWidget(self.IT_UserDefine_00, 0, 1, 1, 1)

        self.IT_BR_00 = QToolButton(self.groupBox_37)
        self.IT_BR_00.setObjectName(u"IT_BR_00")
        self.IT_BR_00.setFont(font2)

        self.gridLayout_97.addWidget(self.IT_BR_00, 0, 2, 1, 1)

        self.IT_FName_00 = QLineEdit(self.groupBox_37)
        self.IT_FName_00.setObjectName(u"IT_FName_00")
        self.IT_FName_00.setFont(font2)

        self.gridLayout_97.addWidget(self.IT_FName_00, 0, 3, 1, 1)


        self.gridLayout_25.addWidget(self.groupBox_37, 1, 0, 1, 1)

        self.verticalSpacer_29 = QSpacerItem(20, 797, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_25.addItem(self.verticalSpacer_29, 2, 0, 1, 1)


        self.gridLayout_199.addWidget(self.frame_7, 0, 0, 1, 1)

        self.init_process_toolbox.addTab(self.PM_CMTab, "")
        self.PM_TCTab = QWidget()
        self.PM_TCTab.setObjectName(u"PM_TCTab")
        self.gridLayout_271 = QGridLayout(self.PM_TCTab)
        self.gridLayout_271.setObjectName(u"gridLayout_271")
        self.frame = QFrame(self.PM_TCTab)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_200 = QGridLayout(self.frame)
        self.gridLayout_200.setObjectName(u"gridLayout_200")
        self.verticalSpacer_62 = QSpacerItem(20, 655, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_200.addItem(self.verticalSpacer_62, 4, 0, 1, 1)

        self.groupBox_33 = QGroupBox(self.frame)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.groupBox_33.setFont(font1)
        self.gridLayout_124 = QGridLayout(self.groupBox_33)
        self.gridLayout_124.setObjectName(u"gridLayout_124")
        self.IT_BR_Tech = QToolButton(self.groupBox_33)
        self.IT_BR_Tech.setObjectName(u"IT_BR_Tech")
        self.IT_BR_Tech.setFont(font2)

        self.gridLayout_124.addWidget(self.IT_BR_Tech, 0, 2, 1, 1)

        self.IT_UserDefine_Tech = QRadioButton(self.groupBox_33)
        self.IT_UserDefine_Tech.setObjectName(u"IT_UserDefine_Tech")
        self.IT_UserDefine_Tech.setFont(font2)

        self.gridLayout_124.addWidget(self.IT_UserDefine_Tech, 0, 1, 1, 1)

        self.IT_Default_Tech = QRadioButton(self.groupBox_33)
        self.IT_Default_Tech.setObjectName(u"IT_Default_Tech")
        self.IT_Default_Tech.setFont(font2)

        self.gridLayout_124.addWidget(self.IT_Default_Tech, 0, 0, 1, 1)

        self.IT_FName_Tech = QLineEdit(self.groupBox_33)
        self.IT_FName_Tech.setObjectName(u"IT_FName_Tech")
        self.IT_FName_Tech.setMinimumSize(QSize(250, 0))
        self.IT_FName_Tech.setFont(font2)

        self.gridLayout_124.addWidget(self.IT_FName_Tech, 0, 3, 1, 1)


        self.gridLayout_200.addWidget(self.groupBox_33, 0, 0, 1, 1)

        self.groupBox_34 = QGroupBox(self.frame)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setFont(font1)
        self.gridLayout_125 = QGridLayout(self.groupBox_34)
        self.gridLayout_125.setObjectName(u"gridLayout_125")
        self.IT_FName_LCI = QLineEdit(self.groupBox_34)
        self.IT_FName_LCI.setObjectName(u"IT_FName_LCI")
        self.IT_FName_LCI.setFont(font2)

        self.gridLayout_125.addWidget(self.IT_FName_LCI, 0, 3, 1, 1)

        self.IT_UserDefine_LCI = QRadioButton(self.groupBox_34)
        self.IT_UserDefine_LCI.setObjectName(u"IT_UserDefine_LCI")
        self.IT_UserDefine_LCI.setFont(font2)

        self.gridLayout_125.addWidget(self.IT_UserDefine_LCI, 0, 1, 1, 1)

        self.IT_BR_LCI = QToolButton(self.groupBox_34)
        self.IT_BR_LCI.setObjectName(u"IT_BR_LCI")
        self.IT_BR_LCI.setFont(font2)

        self.gridLayout_125.addWidget(self.IT_BR_LCI, 0, 2, 1, 1)

        self.IT_Default_LCI = QRadioButton(self.groupBox_34)
        self.IT_Default_LCI.setObjectName(u"IT_Default_LCI")
        self.IT_Default_LCI.setFont(font2)

        self.gridLayout_125.addWidget(self.IT_Default_LCI, 0, 0, 1, 1)


        self.gridLayout_200.addWidget(self.groupBox_34, 1, 0, 1, 1)

        self.groupBox_36 = QGroupBox(self.frame)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setFont(font1)
        self.gridLayout_127 = QGridLayout(self.groupBox_36)
        self.gridLayout_127.setObjectName(u"gridLayout_127")
        self.IT_Default_EcoSpold2 = QRadioButton(self.groupBox_36)
        self.IT_Default_EcoSpold2.setObjectName(u"IT_Default_EcoSpold2")
        self.IT_Default_EcoSpold2.setFont(font2)

        self.gridLayout_127.addWidget(self.IT_Default_EcoSpold2, 0, 0, 1, 1)

        self.IT_BR_EcoSpold2 = QToolButton(self.groupBox_36)
        self.IT_BR_EcoSpold2.setObjectName(u"IT_BR_EcoSpold2")
        self.IT_BR_EcoSpold2.setFont(font2)

        self.gridLayout_127.addWidget(self.IT_BR_EcoSpold2, 0, 2, 1, 1)

        self.IT_UserDefine_EcoSpold2 = QRadioButton(self.groupBox_36)
        self.IT_UserDefine_EcoSpold2.setObjectName(u"IT_UserDefine_EcoSpold2")
        self.IT_UserDefine_EcoSpold2.setFont(font2)

        self.gridLayout_127.addWidget(self.IT_UserDefine_EcoSpold2, 0, 1, 1, 1)

        self.IT_FName_EcoSpold2 = QLineEdit(self.groupBox_36)
        self.IT_FName_EcoSpold2.setObjectName(u"IT_FName_EcoSpold2")
        self.IT_FName_EcoSpold2.setFont(font2)

        self.gridLayout_127.addWidget(self.IT_FName_EcoSpold2, 0, 3, 1, 1)


        self.gridLayout_200.addWidget(self.groupBox_36, 3, 0, 1, 1)

        self.groupBox_35 = QGroupBox(self.frame)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setFont(font1)
        self.gridLayout_126 = QGridLayout(self.groupBox_35)
        self.gridLayout_126.setObjectName(u"gridLayout_126")
        self.IT_BR_LCI_Ref = QToolButton(self.groupBox_35)
        self.IT_BR_LCI_Ref.setObjectName(u"IT_BR_LCI_Ref")
        self.IT_BR_LCI_Ref.setFont(font2)

        self.gridLayout_126.addWidget(self.IT_BR_LCI_Ref, 0, 2, 1, 1)

        self.IT_UserDefine_LCI_Ref = QRadioButton(self.groupBox_35)
        self.IT_UserDefine_LCI_Ref.setObjectName(u"IT_UserDefine_LCI_Ref")
        self.IT_UserDefine_LCI_Ref.setFont(font2)

        self.gridLayout_126.addWidget(self.IT_UserDefine_LCI_Ref, 0, 1, 1, 1)

        self.IT_Default_LCI_Ref = QRadioButton(self.groupBox_35)
        self.IT_Default_LCI_Ref.setObjectName(u"IT_Default_LCI_Ref")
        self.IT_Default_LCI_Ref.setFont(font2)

        self.gridLayout_126.addWidget(self.IT_Default_LCI_Ref, 0, 0, 1, 1)

        self.IT_FName_LCI_Ref = QLineEdit(self.groupBox_35)
        self.IT_FName_LCI_Ref.setObjectName(u"IT_FName_LCI_Ref")
        self.IT_FName_LCI_Ref.setFont(font2)

        self.gridLayout_126.addWidget(self.IT_FName_LCI_Ref, 0, 3, 1, 1)


        self.gridLayout_200.addWidget(self.groupBox_35, 2, 0, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_200.addItem(self.horizontalSpacer_23, 3, 1, 1, 1)


        self.gridLayout_271.addWidget(self.frame, 0, 0, 1, 1)

        self.init_process_toolbox.addTab(self.PM_TCTab, "")

        self.gridLayout_21.addWidget(self.init_process_toolbox, 0, 0, 1, 2)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_9, 1, 0, 1, 1)

        self.PySWOLF.addTab(self.Import_PM, "")
        self.Define_SWM = QWidget()
        self.Define_SWM.setObjectName(u"Define_SWM")
        self.gridLayout_4 = QGridLayout(self.Define_SWM)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.scrollArea_2 = QScrollArea(self.Define_SWM)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 897, 724))
        self.gridLayout_105 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_105.setObjectName(u"gridLayout_105")
        self.frame_2 = QFrame(self.scrollAreaWidgetContents_6)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_98 = QGridLayout(self.frame_2)
        self.gridLayout_98.setObjectName(u"gridLayout_98")
        self.Define_SWM_1 = QToolBox(self.frame_2)
        self.Define_SWM_1.setObjectName(u"Define_SWM_1")
        self.Define_SWM_1.setMinimumSize(QSize(0, 600))
        self.Collection_process = QWidget()
        self.Collection_process.setObjectName(u"Collection_process")
        self.Collection_process.setGeometry(QRect(0, 0, 859, 605))
        self.gridLayout_99 = QGridLayout(self.Collection_process)
        self.gridLayout_99.setObjectName(u"gridLayout_99")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.Add_col = QPushButton(self.Collection_process)
        self.Add_col.setObjectName(u"Add_col")
        icon5 = QIcon()
        icon5.addFile(u":/ICONS/PySWOLF_ICONS/ADD.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Add_col.setIcon(icon5)

        self.horizontalLayout_19.addWidget(self.Add_col)

        self.Help_ColSector = QPushButton(self.Collection_process)
        self.Help_ColSector.setObjectName(u"Help_ColSector")
        self.Help_ColSector.setIcon(icon1)
        self.Help_ColSector.setIconSize(QSize(24, 24))

        self.horizontalLayout_19.addWidget(self.Help_ColSector)

        self.horizontalSpacer_36 = QSpacerItem(528, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_36)


        self.gridLayout_99.addLayout(self.horizontalLayout_19, 0, 0, 1, 1)

        self.Collection = QTabWidget(self.Collection_process)
        self.Collection.setObjectName(u"Collection")

        self.gridLayout_99.addWidget(self.Collection, 1, 0, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer_38 = QSpacerItem(745, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_38)

        self.Create_Collection_process = QPushButton(self.Collection_process)
        self.Create_Collection_process.setObjectName(u"Create_Collection_process")
        icon6 = QIcon()
        icon6.addFile(u":/ICONS/PySWOLF_ICONS/Create.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Create_Collection_process.setIcon(icon6)

        self.horizontalLayout_18.addWidget(self.Create_Collection_process)


        self.gridLayout_99.addLayout(self.horizontalLayout_18, 2, 0, 1, 1)

        self.Define_SWM_1.addItem(self.Collection_process, u"Collection Processes")
        self.Treatment_process = QWidget()
        self.Treatment_process.setObjectName(u"Treatment_process")
        self.Treatment_process.setGeometry(QRect(0, 0, 310, 129))
        self.gridLayout_100 = QGridLayout(self.Treatment_process)
        self.gridLayout_100.setObjectName(u"gridLayout_100")
        self.frame_Process_treatment = QFrame(self.Treatment_process)
        self.frame_Process_treatment.setObjectName(u"frame_Process_treatment")
        self.frame_Process_treatment.setFrameShape(QFrame.StyledPanel)
        self.frame_Process_treatment.setFrameShadow(QFrame.Raised)
        self.gridLayout_101 = QGridLayout(self.frame_Process_treatment)
        self.gridLayout_101.setObjectName(u"gridLayout_101")
        self.label_84 = QLabel(self.frame_Process_treatment)
        self.label_84.setObjectName(u"label_84")

        self.gridLayout_101.addWidget(self.label_84, 0, 4, 1, 1)

        self.label_10 = QLabel(self.frame_Process_treatment)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_101.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_16 = QLabel(self.frame_Process_treatment)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_101.addWidget(self.label_16, 0, 3, 1, 1)

        self.label_17 = QLabel(self.frame_Process_treatment)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_101.addWidget(self.label_17, 0, 5, 1, 1)

        self.label_14 = QLabel(self.frame_Process_treatment)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_101.addWidget(self.label_14, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_Process_treatment)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_101.addWidget(self.label_15, 0, 2, 1, 1)


        self.gridLayout_100.addWidget(self.frame_Process_treatment, 1, 0, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_39)

        self.Treat_process_Clear = QPushButton(self.Treatment_process)
        self.Treat_process_Clear.setObjectName(u"Treat_process_Clear")
        self.Treat_process_Clear.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.Treat_process_Clear)

        self.Create_Treat_prc_dict = QPushButton(self.Treatment_process)
        self.Create_Treat_prc_dict.setObjectName(u"Create_Treat_prc_dict")
        self.Create_Treat_prc_dict.setMinimumSize(QSize(150, 0))
        self.Create_Treat_prc_dict.setIcon(icon6)

        self.horizontalLayout_2.addWidget(self.Create_Treat_prc_dict)


        self.gridLayout_100.addLayout(self.horizontalLayout_2, 3, 0, 1, 3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_100.addItem(self.verticalSpacer_3, 2, 1, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.Add_process = QPushButton(self.Treatment_process)
        self.Add_process.setObjectName(u"Add_process")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Add_process.sizePolicy().hasHeightForWidth())
        self.Add_process.setSizePolicy(sizePolicy2)
        self.Add_process.setIcon(icon5)

        self.horizontalLayout_20.addWidget(self.Add_process)

        self.Help_AddProcess = QPushButton(self.Treatment_process)
        self.Help_AddProcess.setObjectName(u"Help_AddProcess")
        self.Help_AddProcess.setIcon(icon1)
        self.Help_AddProcess.setIconSize(QSize(24, 24))

        self.horizontalLayout_20.addWidget(self.Help_AddProcess)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_40)


        self.gridLayout_100.addLayout(self.horizontalLayout_20, 0, 0, 1, 3)

        self.Define_SWM_1.addItem(self.Treatment_process, u"Treatment Processes")
        self.Network = QWidget()
        self.Network.setObjectName(u"Network")
        self.Network.setGeometry(QRect(0, 0, 820, 508))
        self.gridLayout_26 = QGridLayout(self.Network)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_8 = QLabel(self.Network)
        self.label_8.setObjectName(u"label_8")
        font4 = QFont()
        font4.setBold(True)
        font4.setWeight(75)
        self.label_8.setFont(font4)

        self.horizontalLayout_21.addWidget(self.label_8)

        self.spinBox = QSpinBox(self.Network)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_21.addWidget(self.spinBox)

        self.Create_Distance = QPushButton(self.Network)
        self.Create_Distance.setObjectName(u"Create_Distance")
        self.Create_Distance.setMaximumSize(QSize(200, 16777215))
        self.Create_Distance.setIcon(icon6)

        self.horizontalLayout_21.addWidget(self.Create_Distance)

        self.Help_DistanceTable = QPushButton(self.Network)
        self.Help_DistanceTable.setObjectName(u"Help_DistanceTable")
        self.Help_DistanceTable.setIcon(icon1)
        self.Help_DistanceTable.setIconSize(QSize(24, 24))

        self.horizontalLayout_21.addWidget(self.Help_DistanceTable)

        self.horizontalSpacer_48 = QSpacerItem(663, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_48)


        self.gridLayout_26.addLayout(self.horizontalLayout_21, 0, 0, 1, 1)

        self.splitter_8 = QSplitter(self.Network)
        self.splitter_8.setObjectName(u"splitter_8")
        self.splitter_8.setOrientation(Qt.Vertical)
        self.TransportWidget = QTabWidget(self.splitter_8)
        self.TransportWidget.setObjectName(u"TransportWidget")
        self.TransportWidget.setMinimumSize(QSize(0, 300))
        self.splitter_8.addWidget(self.TransportWidget)
        self.layoutWidget = QWidget(self.splitter_8)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_12 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_42 = QLabel(self.layoutWidget)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(0, 0))
        self.label_42.setFont(font1)

        self.horizontalLayout_26.addWidget(self.label_42)

        self.Project_Name = QLineEdit(self.layoutWidget)
        self.Project_Name.setObjectName(u"Project_Name")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Project_Name.sizePolicy().hasHeightForWidth())
        self.Project_Name.setSizePolicy(sizePolicy3)
        self.Project_Name.setMinimumSize(QSize(100, 0))
        self.Project_Name.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_26.addWidget(self.Project_Name)

        self.write_project = QPushButton(self.layoutWidget)
        self.write_project.setObjectName(u"write_project")
        self.write_project.setMaximumSize(QSize(16777215, 16777215))
        self.write_project.setIcon(icon6)

        self.horizontalLayout_26.addWidget(self.write_project)

        self.progressBar_write_project = QProgressBar(self.layoutWidget)
        self.progressBar_write_project.setObjectName(u"progressBar_write_project")
        self.progressBar_write_project.setMinimumSize(QSize(300, 0))
        self.progressBar_write_project.setValue(0)

        self.horizontalLayout_26.addWidget(self.progressBar_write_project)

        self.Load_params = QPushButton(self.layoutWidget)
        self.Load_params.setObjectName(u"Load_params")
        self.Load_params.setIcon(icon2)

        self.horizontalLayout_26.addWidget(self.Load_params)

        self.Help_Project_Param = QPushButton(self.layoutWidget)
        self.Help_Project_Param.setObjectName(u"Help_Project_Param")
        self.Help_Project_Param.setIcon(icon1)
        self.Help_Project_Param.setIconSize(QSize(24, 24))

        self.horizontalLayout_26.addWidget(self.Help_Project_Param)

        self.horizontalSpacer_49 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_49)


        self.verticalLayout_12.addLayout(self.horizontalLayout_26)

        self.Param_table = QTableView(self.layoutWidget)
        self.Param_table.setObjectName(u"Param_table")
        self.Param_table.setMinimumSize(QSize(800, 0))
        self.Param_table.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_12.addWidget(self.Param_table)

        self.splitter_8.addWidget(self.layoutWidget)

        self.gridLayout_26.addWidget(self.splitter_8, 1, 0, 1, 1)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.update_param = QPushButton(self.Network)
        self.update_param.setObjectName(u"update_param")
        self.update_param.setMaximumSize(QSize(200, 16777215))
        self.update_param.setIcon(icon4)

        self.horizontalLayout_25.addWidget(self.update_param)

        self.progressBar_updateParam = QProgressBar(self.Network)
        self.progressBar_updateParam.setObjectName(u"progressBar_updateParam")
        self.progressBar_updateParam.setValue(0)

        self.horizontalLayout_25.addWidget(self.progressBar_updateParam)

        self.Show_SWM_Network = QPushButton(self.Network)
        self.Show_SWM_Network.setObjectName(u"Show_SWM_Network")
        icon7 = QIcon()
        icon7.addFile(u":/ICONS/PySWOLF_ICONS/show.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Show_SWM_Network.setIcon(icon7)

        self.horizontalLayout_25.addWidget(self.Show_SWM_Network)

        self.Show_SWM_Network_AllFlows = QCheckBox(self.Network)
        self.Show_SWM_Network_AllFlows.setObjectName(u"Show_SWM_Network_AllFlows")

        self.horizontalLayout_25.addWidget(self.Show_SWM_Network_AllFlows)

        self.horizontalSpacer_44 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_44)


        self.gridLayout_26.addLayout(self.horizontalLayout_25, 2, 0, 1, 1)

        self.Define_SWM_1.addItem(self.Network, u"System")

        self.gridLayout_98.addWidget(self.Define_SWM_1, 0, 0, 1, 1)


        self.gridLayout_105.addWidget(self.frame_2, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_6)

        self.gridLayout_4.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.Define_SWM, "")
        self.Load_Project = QWidget()
        self.Load_Project.setObjectName(u"Load_Project")
        self.gridLayout_63 = QGridLayout(self.Load_Project)
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.scrollArea_3 = QScrollArea(self.Load_Project)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName(u"scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, 0, 880, 801))
        self.gridLayout_106 = QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_106.setObjectName(u"gridLayout_106")
        self.frame_40 = QFrame(self.scrollAreaWidgetContents_7)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_40)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Br_Project_btm = QToolButton(self.frame_40)
        self.Br_Project_btm.setObjectName(u"Br_Project_btm")
        sizePolicy1.setHeightForWidth(self.Br_Project_btm.sizePolicy().hasHeightForWidth())
        self.Br_Project_btm.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.Br_Project_btm)

        self.Project_address = QLineEdit(self.frame_40)
        self.Project_address.setObjectName(u"Project_address")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.Project_address.sizePolicy().hasHeightForWidth())
        self.Project_address.setSizePolicy(sizePolicy4)
        self.Project_address.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.Project_address)

        self.Load_Project_btm = QPushButton(self.frame_40)
        self.Load_Project_btm.setObjectName(u"Load_Project_btm")
        self.Load_Project_btm.setIcon(icon2)

        self.horizontalLayout.addWidget(self.Load_Project_btm)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.label_53 = QLabel(self.frame_40)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_3.addWidget(self.label_53, 0, 1, 1, 1)

        self.splitter_2 = QSplitter(self.frame_40)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.groupBox_7 = QGroupBox(self.splitter_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_75 = QGridLayout(self.groupBox_7)
        self.gridLayout_75.setObjectName(u"gridLayout_75")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_54 = QLabel(self.groupBox_7)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_17.addWidget(self.label_54)

        self.load_P_name = QLabel(self.groupBox_7)
        self.load_P_name.setObjectName(u"load_P_name")
        self.load_P_name.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_17.addWidget(self.load_P_name)

        self.horizontalSpacer_20 = QSpacerItem(527, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_20)


        self.gridLayout_75.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)

        self.load_treatment_info = QTableView(self.groupBox_7)
        self.load_treatment_info.setObjectName(u"load_treatment_info")
        self.load_treatment_info.setMinimumSize(QSize(0, 200))

        self.gridLayout_75.addWidget(self.load_treatment_info, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.groupBox_7)
        self.groupBox_10 = QGroupBox(self.splitter_2)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_74 = QGridLayout(self.groupBox_10)
        self.gridLayout_74.setObjectName(u"gridLayout_74")
        self.load_Param_table = QTableView(self.groupBox_10)
        self.load_Param_table.setObjectName(u"load_Param_table")
        self.load_Param_table.setMinimumSize(QSize(0, 400))

        self.gridLayout_74.addWidget(self.load_Param_table, 0, 0, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.Load_params_Load = QPushButton(self.groupBox_10)
        self.Load_params_Load.setObjectName(u"Load_params_Load")
        self.Load_params_Load.setIcon(icon2)

        self.horizontalLayout_16.addWidget(self.Load_params_Load)

        self.load_update_param = QPushButton(self.groupBox_10)
        self.load_update_param.setObjectName(u"load_update_param")
        self.load_update_param.setIcon(icon4)

        self.horizontalLayout_16.addWidget(self.load_update_param)

        self.load_PBar_updateParam = QProgressBar(self.groupBox_10)
        self.load_PBar_updateParam.setObjectName(u"load_PBar_updateParam")
        self.load_PBar_updateParam.setValue(0)

        self.horizontalLayout_16.addWidget(self.load_PBar_updateParam)

        self.Show_SWM_Network_Load = QPushButton(self.groupBox_10)
        self.Show_SWM_Network_Load.setObjectName(u"Show_SWM_Network_Load")
        self.Show_SWM_Network_Load.setIcon(icon7)

        self.horizontalLayout_16.addWidget(self.Show_SWM_Network_Load)

        self.Show_SWM_Network_Load_AllFlows = QCheckBox(self.groupBox_10)
        self.Show_SWM_Network_Load_AllFlows.setObjectName(u"Show_SWM_Network_Load_AllFlows")

        self.horizontalLayout_16.addWidget(self.Show_SWM_Network_Load_AllFlows)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_19)


        self.gridLayout_74.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.groupBox_10)

        self.gridLayout_3.addWidget(self.splitter_2, 1, 0, 1, 3)


        self.gridLayout_106.addWidget(self.frame_40, 0, 0, 1, 1)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_7)

        self.gridLayout_63.addWidget(self.scrollArea_3, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.Load_Project, "")
        self.Create_Scenario = QWidget()
        self.Create_Scenario.setObjectName(u"Create_Scenario")
        self.gridLayout_107 = QGridLayout(self.Create_Scenario)
        self.gridLayout_107.setObjectName(u"gridLayout_107")
        self.scrollArea_4 = QScrollArea(self.Create_Scenario)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setMinimumSize(QSize(700, 0))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setObjectName(u"scrollAreaWidgetContents_8")
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, 0, 880, 726))
        self.gridLayout_52 = QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.frame_39 = QFrame(self.scrollAreaWidgetContents_8)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_39)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.Start_new_sen = QPushButton(self.frame_39)
        self.Start_new_sen.setObjectName(u"Start_new_sen")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.Start_new_sen.sizePolicy().hasHeightForWidth())
        self.Start_new_sen.setSizePolicy(sizePolicy5)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.Start_new_sen)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Help_CreateScenario = QPushButton(self.frame_39)
        self.Help_CreateScenario.setObjectName(u"Help_CreateScenario")
        self.Help_CreateScenario.setIcon(icon1)
        self.Help_CreateScenario.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.Help_CreateScenario)

        self.horizontalSpacer_32 = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_32)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_38 = QLabel(self.frame_39)
        self.label_38.setObjectName(u"label_38")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_38)

        self.Name_new_scenario = QLineEdit(self.frame_39)
        self.Name_new_scenario.setObjectName(u"Name_new_scenario")
        sizePolicy4.setHeightForWidth(self.Name_new_scenario.sizePolicy().hasHeightForWidth())
        self.Name_new_scenario.setSizePolicy(sizePolicy4)
        self.Name_new_scenario.setMinimumSize(QSize(200, 0))
        self.Name_new_scenario.setMaxLength(32768)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.Name_new_scenario)

        self.label_37 = QLabel(self.frame_39)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(0, 0))

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_37)

        self.Process = QComboBox(self.frame_39)
        self.Process.setObjectName(u"Process")
        sizePolicy1.setHeightForWidth(self.Process.sizePolicy().hasHeightForWidth())
        self.Process.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.Process)


        self.gridLayout_16.addLayout(self.formLayout, 0, 0, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(735, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_16, 0, 1, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.Add_act_to_scen = QPushButton(self.frame_39)
        self.Add_act_to_scen.setObjectName(u"Add_act_to_scen")
        self.Add_act_to_scen.setIcon(icon5)

        self.verticalLayout_7.addWidget(self.Add_act_to_scen)

        self.label_39 = QLabel(self.frame_39)
        self.label_39.setObjectName(u"label_39")

        self.verticalLayout_7.addWidget(self.label_39)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_12)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.Included_act_table = QTableView(self.frame_39)
        self.Included_act_table.setObjectName(u"Included_act_table")
        self.Included_act_table.setMinimumSize(QSize(500, 200))

        self.verticalLayout_8.addWidget(self.Included_act_table)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_31 = QSpacerItem(206, 18, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_31)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Clear_act = QPushButton(self.frame_39)
        self.Clear_act.setObjectName(u"Clear_act")
        self.Clear_act.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.Clear_act)

        self.Create_scenario = QPushButton(self.frame_39)
        self.Create_scenario.setObjectName(u"Create_scenario")
        self.Create_scenario.setMinimumSize(QSize(100, 0))
        self.Create_scenario.setIcon(icon6)

        self.horizontalLayout_3.addWidget(self.Create_scenario)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)


        self.gridLayout_16.addLayout(self.verticalLayout_8, 2, 0, 1, 2)

        self.act_in_process_table = QTableView(self.frame_39)
        self.act_in_process_table.setObjectName(u"act_in_process_table")
        self.act_in_process_table.setMinimumSize(QSize(0, 300))

        self.gridLayout_16.addWidget(self.act_in_process_table, 1, 0, 1, 2)


        self.gridLayout_52.addWidget(self.frame_39, 0, 0, 1, 1)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_8)

        self.gridLayout_107.addWidget(self.scrollArea_4, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.Create_Scenario, "")
        self.LCA_tab = QWidget()
        self.LCA_tab.setObjectName(u"LCA_tab")
        self.gridLayout_70 = QGridLayout(self.LCA_tab)
        self.gridLayout_70.setObjectName(u"gridLayout_70")
        self.LCA_subTab = QTabWidget(self.LCA_tab)
        self.LCA_subTab.setObjectName(u"LCA_subTab")
        self.LCA_setup_tab = QWidget()
        self.LCA_setup_tab.setObjectName(u"LCA_setup_tab")
        self.gridLayout_17 = QGridLayout(self.LCA_setup_tab)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.frame_44 = QFrame(self.LCA_setup_tab)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_44)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizontalSpacer_37 = QSpacerItem(554, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_37, 2, 0, 1, 1)

        self.groupBox_25 = QGroupBox(self.frame_44)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.gridLayout_20 = QGridLayout(self.groupBox_25)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.Filter_impact_keyword = QLineEdit(self.groupBox_25)
        self.Filter_impact_keyword.setObjectName(u"Filter_impact_keyword")
        sizePolicy4.setHeightForWidth(self.Filter_impact_keyword.sizePolicy().hasHeightForWidth())
        self.Filter_impact_keyword.setSizePolicy(sizePolicy4)

        self.gridLayout_20.addWidget(self.Filter_impact_keyword, 0, 1, 1, 1)

        self.LCA_Filter_impacts = QPushButton(self.groupBox_25)
        self.LCA_Filter_impacts.setObjectName(u"LCA_Filter_impacts")
        icon8 = QIcon()
        icon8.addFile(u":/ICONS/PySWOLF_ICONS/Filter.png", QSize(), QIcon.Normal, QIcon.Off)
        self.LCA_Filter_impacts.setIcon(icon8)

        self.gridLayout_20.addWidget(self.LCA_Filter_impacts, 0, 2, 1, 1)

        self.horizontalSpacer_34 = QSpacerItem(334, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_34, 0, 3, 1, 2)

        self.LCA_method = QComboBox(self.groupBox_25)
        self.LCA_method.setObjectName(u"LCA_method")
        sizePolicy1.setHeightForWidth(self.LCA_method.sizePolicy().hasHeightForWidth())
        self.LCA_method.setSizePolicy(sizePolicy1)
        self.LCA_method.setMinimumSize(QSize(350, 0))

        self.gridLayout_20.addWidget(self.LCA_method, 1, 1, 1, 2)

        self.LCA_View_method = QPushButton(self.groupBox_25)
        self.LCA_View_method.setObjectName(u"LCA_View_method")
        self.LCA_View_method.setIcon(icon7)

        self.gridLayout_20.addWidget(self.LCA_View_method, 1, 3, 1, 1)

        self.LCA_AddImpact = QPushButton(self.groupBox_25)
        self.LCA_AddImpact.setObjectName(u"LCA_AddImpact")
        self.LCA_AddImpact.setIcon(icon5)

        self.gridLayout_20.addWidget(self.LCA_AddImpact, 1, 4, 1, 1)

        self.label_7 = QLabel(self.groupBox_25)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_20.addWidget(self.label_7, 2, 0, 1, 1)

        self.LCA_Impact_table = QTableView(self.groupBox_25)
        self.LCA_Impact_table.setObjectName(u"LCA_Impact_table")

        self.gridLayout_20.addWidget(self.LCA_Impact_table, 2, 1, 1, 4)

        self.label_52 = QLabel(self.groupBox_25)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_20.addWidget(self.label_52, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_25, 1, 0, 1, 2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.LCA_ClearSetup = QPushButton(self.frame_44)
        self.LCA_ClearSetup.setObjectName(u"LCA_ClearSetup")
        self.LCA_ClearSetup.setIcon(icon3)

        self.horizontalLayout_7.addWidget(self.LCA_ClearSetup)

        self.LCA_CreateLCA = QPushButton(self.frame_44)
        self.LCA_CreateLCA.setObjectName(u"LCA_CreateLCA")
        self.LCA_CreateLCA.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_7.addWidget(self.LCA_CreateLCA)


        self.gridLayout_19.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(92, 306, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_14, 1, 2, 1, 1)

        self.groupBox_24 = QGroupBox(self.frame_44)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.gridLayout_18 = QGridLayout(self.groupBox_24)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.LCA_DataBase = QComboBox(self.groupBox_24)
        self.LCA_DataBase.setObjectName(u"LCA_DataBase")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.LCA_DataBase.sizePolicy().hasHeightForWidth())
        self.LCA_DataBase.setSizePolicy(sizePolicy6)

        self.gridLayout_18.addWidget(self.LCA_DataBase, 0, 1, 1, 3)

        self.label_12 = QLabel(self.groupBox_24)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_18.addWidget(self.label_12, 3, 0, 1, 1)

        self.label_49 = QLabel(self.groupBox_24)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_18.addWidget(self.label_49, 1, 0, 1, 1)

        self.LCA_AddAct = QPushButton(self.groupBox_24)
        self.LCA_AddAct.setObjectName(u"LCA_AddAct")
        self.LCA_AddAct.setIcon(icon5)

        self.gridLayout_18.addWidget(self.LCA_AddAct, 2, 3, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(308, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_15, 2, 4, 1, 1)

        self.LCA_ActTable = QTableView(self.groupBox_24)
        self.LCA_ActTable.setObjectName(u"LCA_ActTable")
        self.LCA_ActTable.setMinimumSize(QSize(400, 0))

        self.gridLayout_18.addWidget(self.LCA_ActTable, 3, 1, 1, 4)

        self.LCA_activity = QComboBox(self.groupBox_24)
        self.LCA_activity.setObjectName(u"LCA_activity")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.LCA_activity.sizePolicy().hasHeightForWidth())
        self.LCA_activity.setSizePolicy(sizePolicy7)
        self.LCA_activity.setMinimumSize(QSize(400, 0))

        self.gridLayout_18.addWidget(self.LCA_activity, 1, 1, 1, 3)

        self.label_51 = QLabel(self.groupBox_24)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_18.addWidget(self.label_51, 0, 0, 1, 1)

        self.label_48 = QLabel(self.groupBox_24)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_18.addWidget(self.label_48, 2, 0, 1, 1)

        self.LCA_FU_unit = QLabel(self.groupBox_24)
        self.LCA_FU_unit.setObjectName(u"LCA_FU_unit")
        self.LCA_FU_unit.setFont(font1)

        self.gridLayout_18.addWidget(self.LCA_FU_unit, 2, 1, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_24, 0, 0, 1, 2)


        self.gridLayout_17.addWidget(self.frame_44, 0, 0, 1, 1)

        self.LCA_subTab.addTab(self.LCA_setup_tab, "")
        self.LCA_Results_tab = QWidget()
        self.LCA_Results_tab.setObjectName(u"LCA_Results_tab")
        self.gridLayout_66 = QGridLayout(self.LCA_Results_tab)
        self.gridLayout_66.setObjectName(u"gridLayout_66")
        self.frame_4 = QFrame(self.LCA_Results_tab)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.splitter_4 = QSplitter(self.frame_4)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Vertical)
        self.LCA_Results_Table = QTableView(self.splitter_4)
        self.LCA_Results_Table.setObjectName(u"LCA_Results_Table")
        self.splitter_4.addWidget(self.LCA_Results_Table)
        self.layoutWidget1 = QWidget(self.splitter_4)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_13 = QLabel(self.layoutWidget1)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.horizontalLayout_24.addWidget(self.label_13)

        self.LCA_Results_ImpactFig = QComboBox(self.layoutWidget1)
        self.LCA_Results_ImpactFig.setObjectName(u"LCA_Results_ImpactFig")
        self.LCA_Results_ImpactFig.setMinimumSize(QSize(450, 0))

        self.horizontalLayout_24.addWidget(self.LCA_Results_ImpactFig)

        self.horizontalSpacer_21 = QSpacerItem(37, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_21)


        self.verticalLayout_5.addLayout(self.horizontalLayout_24)

        self.LCA_Results_fig = QWidget(self.layoutWidget1)
        self.LCA_Results_fig.setObjectName(u"LCA_Results_fig")
        self.LCA_Results_fig.setMinimumSize(QSize(0, 360))

        self.verticalLayout_5.addWidget(self.LCA_Results_fig)

        self.splitter_4.addWidget(self.layoutWidget1)

        self.verticalLayout_9.addWidget(self.splitter_4)


        self.gridLayout_66.addWidget(self.frame_4, 0, 0, 1, 1)

        self.LCA_subTab.addTab(self.LCA_Results_tab, "")
        self.LCA_Contribution_tab = QWidget()
        self.LCA_Contribution_tab.setObjectName(u"LCA_Contribution_tab")
        self.gridLayout_64 = QGridLayout(self.LCA_Contribution_tab)
        self.gridLayout_64.setObjectName(u"gridLayout_64")
        self.groupBox_26 = QGroupBox(self.LCA_Contribution_tab)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.gridLayout_68 = QGridLayout(self.groupBox_26)
        self.gridLayout_68.setObjectName(u"gridLayout_68")
        self.groupBox_23 = QGroupBox(self.groupBox_26)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.gridLayout_60 = QGridLayout(self.groupBox_23)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_60 = QLabel(self.groupBox_23)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setMinimumSize(QSize(100, 0))

        self.verticalLayout.addWidget(self.label_60)

        self.label_61 = QLabel(self.groupBox_23)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setMinimumSize(QSize(100, 0))

        self.verticalLayout.addWidget(self.label_61)

        self.label_11 = QLabel(self.groupBox_23)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout.addWidget(self.label_11)


        self.gridLayout_60.addLayout(self.verticalLayout, 0, 0, 2, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.LCA_Contr_FU = QComboBox(self.groupBox_23)
        self.LCA_Contr_FU.setObjectName(u"LCA_Contr_FU")
        sizePolicy6.setHeightForWidth(self.LCA_Contr_FU.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_FU.setSizePolicy(sizePolicy6)

        self.verticalLayout_2.addWidget(self.LCA_Contr_FU)

        self.LCA_Contr_Method = QComboBox(self.groupBox_23)
        self.LCA_Contr_Method.setObjectName(u"LCA_Contr_Method")
        sizePolicy6.setHeightForWidth(self.LCA_Contr_Method.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_Method.setSizePolicy(sizePolicy6)

        self.verticalLayout_2.addWidget(self.LCA_Contr_Method)


        self.gridLayout_60.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.LCA_Contr_CutOffType = QComboBox(self.groupBox_23)
        self.LCA_Contr_CutOffType.setObjectName(u"LCA_Contr_CutOffType")

        self.horizontalLayout_22.addWidget(self.LCA_Contr_CutOffType)

        self.LCA_Contr_CutOff = QDoubleSpinBox(self.groupBox_23)
        self.LCA_Contr_CutOff.setObjectName(u"LCA_Contr_CutOff")
        sizePolicy5.setHeightForWidth(self.LCA_Contr_CutOff.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_CutOff.setSizePolicy(sizePolicy5)
        self.LCA_Contr_CutOff.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_22.addWidget(self.LCA_Contr_CutOff)

        self.LCA_Contr__Top_act = QRadioButton(self.groupBox_23)
        self.LCA_Contr__Top_act.setObjectName(u"LCA_Contr__Top_act")
        sizePolicy5.setHeightForWidth(self.LCA_Contr__Top_act.sizePolicy().hasHeightForWidth())
        self.LCA_Contr__Top_act.setSizePolicy(sizePolicy5)

        self.horizontalLayout_22.addWidget(self.LCA_Contr__Top_act)

        self.LCA_Contr_Top_emis = QRadioButton(self.groupBox_23)
        self.LCA_Contr_Top_emis.setObjectName(u"LCA_Contr_Top_emis")
        sizePolicy5.setHeightForWidth(self.LCA_Contr_Top_emis.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_Top_emis.setSizePolicy(sizePolicy5)

        self.horizontalLayout_22.addWidget(self.LCA_Contr_Top_emis)

        self.LCA_Contr_updat = QPushButton(self.groupBox_23)
        self.LCA_Contr_updat.setObjectName(u"LCA_Contr_updat")
        sizePolicy5.setHeightForWidth(self.LCA_Contr_updat.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_updat.setSizePolicy(sizePolicy5)
        self.LCA_Contr_updat.setIcon(icon4)

        self.horizontalLayout_22.addWidget(self.LCA_Contr_updat)


        self.gridLayout_60.addLayout(self.horizontalLayout_22, 1, 1, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(252, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_60.addItem(self.horizontalSpacer_22, 1, 2, 1, 1)


        self.gridLayout_68.addWidget(self.groupBox_23, 0, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.groupBox_26)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_84 = QGridLayout(self.groupBox_6)
        self.gridLayout_84.setObjectName(u"gridLayout_84")
        self.scrollArea_7 = QScrollArea(self.groupBox_6)
        self.scrollArea_7.setObjectName(u"scrollArea_7")
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 404, 846))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_59 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_23.addWidget(self.label_59)

        self.LCA_Contr_score = QLineEdit(self.scrollAreaWidgetContents_2)
        self.LCA_Contr_score.setObjectName(u"LCA_Contr_score")
        sizePolicy7.setHeightForWidth(self.LCA_Contr_score.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_score.setSizePolicy(sizePolicy7)

        self.horizontalLayout_23.addWidget(self.LCA_Contr_score)

        self.LCA_Contr_unit = QLineEdit(self.scrollAreaWidgetContents_2)
        self.LCA_Contr_unit.setObjectName(u"LCA_Contr_unit")
        sizePolicy7.setHeightForWidth(self.LCA_Contr_unit.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_unit.setSizePolicy(sizePolicy7)

        self.horizontalLayout_23.addWidget(self.LCA_Contr_unit)

        self.horizontalSpacer_29 = QSpacerItem(726, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_29)


        self.verticalLayout_4.addLayout(self.horizontalLayout_23)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 800))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_131 = QGridLayout(self.frame_3)
        self.gridLayout_131.setObjectName(u"gridLayout_131")
        self.splitter_3 = QSplitter(self.frame_3)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.LCA_contribution_Table = QTableView(self.splitter_3)
        self.LCA_contribution_Table.setObjectName(u"LCA_contribution_Table")
        self.LCA_contribution_Table.setMinimumSize(QSize(0, 200))
        self.splitter_3.addWidget(self.LCA_contribution_Table)
        self.LCA_Contr_fig = QWidget(self.splitter_3)
        self.LCA_Contr_fig.setObjectName(u"LCA_Contr_fig")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.LCA_Contr_fig.sizePolicy().hasHeightForWidth())
        self.LCA_Contr_fig.setSizePolicy(sizePolicy8)
        self.LCA_Contr_fig.setMinimumSize(QSize(0, 200))
        self.splitter_3.addWidget(self.LCA_Contr_fig)

        self.gridLayout_131.addWidget(self.splitter_3, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_84.addWidget(self.scrollArea_7, 0, 0, 1, 1)


        self.gridLayout_68.addWidget(self.groupBox_6, 1, 0, 1, 1)


        self.gridLayout_64.addWidget(self.groupBox_26, 0, 0, 1, 1)

        self.LCA_subTab.addTab(self.LCA_Contribution_tab, "")
        self.LCA_LCI_tab = QWidget()
        self.LCA_LCI_tab.setObjectName(u"LCA_LCI_tab")
        self.gridLayout_82 = QGridLayout(self.LCA_LCI_tab)
        self.gridLayout_82.setObjectName(u"gridLayout_82")
        self.frame_5 = QFrame(self.LCA_LCI_tab)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_86 = QGridLayout(self.frame_5)
        self.gridLayout_86.setObjectName(u"gridLayout_86")
        self.groupBox_28 = QGroupBox(self.frame_5)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.gridLayout_85 = QGridLayout(self.groupBox_28)
        self.gridLayout_85.setObjectName(u"gridLayout_85")
        self.LCA_LCI_Table = QTableView(self.groupBox_28)
        self.LCA_LCI_Table.setObjectName(u"LCA_LCI_Table")
        self.LCA_LCI_Table.setMinimumSize(QSize(0, 0))

        self.gridLayout_85.addWidget(self.LCA_LCI_Table, 0, 0, 1, 2)


        self.gridLayout_86.addWidget(self.groupBox_28, 1, 0, 1, 1)

        self.groupBox_27 = QGroupBox(self.frame_5)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.gridLayout_69 = QGridLayout(self.groupBox_27)
        self.gridLayout_69.setObjectName(u"gridLayout_69")
        self.LCA_LCI_updat = QPushButton(self.groupBox_27)
        self.LCA_LCI_updat.setObjectName(u"LCA_LCI_updat")
        sizePolicy1.setHeightForWidth(self.LCA_LCI_updat.sizePolicy().hasHeightForWidth())
        self.LCA_LCI_updat.setSizePolicy(sizePolicy1)
        self.LCA_LCI_updat.setIcon(icon4)

        self.gridLayout_69.addWidget(self.LCA_LCI_updat, 1, 2, 1, 1)

        self.LCA_LCI_FU = QComboBox(self.groupBox_27)
        self.LCA_LCI_FU.setObjectName(u"LCA_LCI_FU")
        sizePolicy1.setHeightForWidth(self.LCA_LCI_FU.sizePolicy().hasHeightForWidth())
        self.LCA_LCI_FU.setSizePolicy(sizePolicy1)
        self.LCA_LCI_FU.setMinimumSize(QSize(250, 0))

        self.gridLayout_69.addWidget(self.LCA_LCI_FU, 1, 1, 1, 1)

        self.label_80 = QLabel(self.groupBox_27)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setMinimumSize(QSize(100, 0))

        self.gridLayout_69.addWidget(self.label_80, 1, 0, 1, 1)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_69.addItem(self.horizontalSpacer_33, 1, 3, 1, 1)


        self.gridLayout_86.addWidget(self.groupBox_27, 0, 0, 1, 1)


        self.gridLayout_82.addWidget(self.frame_5, 0, 0, 1, 1)

        self.LCA_subTab.addTab(self.LCA_LCI_tab, "")

        self.gridLayout_70.addWidget(self.LCA_subTab, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.LCA_tab, "")
        self.MC_tab = QWidget()
        self.MC_tab.setObjectName(u"MC_tab")
        self.gridLayout_88 = QGridLayout(self.MC_tab)
        self.gridLayout_88.setObjectName(u"gridLayout_88")
        self.scrollArea_6 = QScrollArea(self.MC_tab)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 902, 736))
        self.gridLayout_30 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.splitter_6 = QSplitter(self.scrollAreaWidgetContents)
        self.splitter_6.setObjectName(u"splitter_6")
        self.splitter_6.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_6)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget2 = QWidget(self.splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.groupBox_11 = QGroupBox(self.layoutWidget2)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.groupBox_11)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_65 = QLabel(self.groupBox_11)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setFont(font2)

        self.gridLayout_5.addWidget(self.label_65, 0, 0, 1, 1)

        self.MC_FU_DB = QComboBox(self.groupBox_11)
        self.MC_FU_DB.setObjectName(u"MC_FU_DB")
        sizePolicy1.setHeightForWidth(self.MC_FU_DB.sizePolicy().hasHeightForWidth())
        self.MC_FU_DB.setSizePolicy(sizePolicy1)
        self.MC_FU_DB.setFont(font2)

        self.gridLayout_5.addWidget(self.MC_FU_DB, 0, 1, 1, 3)

        self.label_64 = QLabel(self.groupBox_11)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFont(font2)

        self.gridLayout_5.addWidget(self.label_64, 1, 0, 1, 1)

        self.MC_FU_act = QComboBox(self.groupBox_11)
        self.MC_FU_act.setObjectName(u"MC_FU_act")
        sizePolicy1.setHeightForWidth(self.MC_FU_act.sizePolicy().hasHeightForWidth())
        self.MC_FU_act.setSizePolicy(sizePolicy1)
        self.MC_FU_act.setMinimumSize(QSize(250, 0))
        self.MC_FU_act.setFont(font2)

        self.gridLayout_5.addWidget(self.MC_FU_act, 1, 1, 1, 3)

        self.label_63 = QLabel(self.groupBox_11)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font2)

        self.gridLayout_5.addWidget(self.label_63, 2, 0, 1, 1)

        self.MC_FU_unit = QLabel(self.groupBox_11)
        self.MC_FU_unit.setObjectName(u"MC_FU_unit")

        self.gridLayout_5.addWidget(self.MC_FU_unit, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 2, 3, 1, 1)


        self.verticalLayout_6.addWidget(self.groupBox_11)

        self.groupBox_12 = QGroupBox(self.layoutWidget2)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setFont(font1)
        self.gridLayout_91 = QGridLayout(self.groupBox_12)
        self.gridLayout_91.setObjectName(u"gridLayout_91")
        self.label_66 = QLabel(self.groupBox_12)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setFont(font2)

        self.gridLayout_91.addWidget(self.label_66, 0, 0, 1, 1)

        self.MC_Filter_keyword = QLineEdit(self.groupBox_12)
        self.MC_Filter_keyword.setObjectName(u"MC_Filter_keyword")
        sizePolicy4.setHeightForWidth(self.MC_Filter_keyword.sizePolicy().hasHeightForWidth())
        self.MC_Filter_keyword.setSizePolicy(sizePolicy4)
        self.MC_Filter_keyword.setFont(font2)

        self.gridLayout_91.addWidget(self.MC_Filter_keyword, 0, 1, 1, 1)

        self.MC_Filter_method = QPushButton(self.groupBox_12)
        self.MC_Filter_method.setObjectName(u"MC_Filter_method")
        sizePolicy5.setHeightForWidth(self.MC_Filter_method.sizePolicy().hasHeightForWidth())
        self.MC_Filter_method.setSizePolicy(sizePolicy5)
        self.MC_Filter_method.setFont(font2)
        self.MC_Filter_method.setIcon(icon8)

        self.gridLayout_91.addWidget(self.MC_Filter_method, 0, 2, 1, 1)

        self.MC_method = QComboBox(self.groupBox_12)
        self.MC_method.setObjectName(u"MC_method")
        sizePolicy1.setHeightForWidth(self.MC_method.sizePolicy().hasHeightForWidth())
        self.MC_method.setSizePolicy(sizePolicy1)
        self.MC_method.setMinimumSize(QSize(250, 0))
        self.MC_method.setFont(font2)

        self.gridLayout_91.addWidget(self.MC_method, 1, 0, 1, 2)

        self.MC_add_method = QPushButton(self.groupBox_12)
        self.MC_add_method.setObjectName(u"MC_add_method")
        sizePolicy5.setHeightForWidth(self.MC_add_method.sizePolicy().hasHeightForWidth())
        self.MC_add_method.setSizePolicy(sizePolicy5)
        self.MC_add_method.setFont(font2)
        self.MC_add_method.setIcon(icon5)

        self.gridLayout_91.addWidget(self.MC_add_method, 1, 2, 1, 1)

        self.MC_method_table = QTableView(self.groupBox_12)
        self.MC_method_table.setObjectName(u"MC_method_table")
        self.MC_method_table.setFont(font2)

        self.gridLayout_91.addWidget(self.MC_method_table, 2, 0, 1, 3)


        self.verticalLayout_6.addWidget(self.groupBox_12)

        self.splitter.addWidget(self.layoutWidget2)
        self.groupBox_29 = QGroupBox(self.splitter)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(210, 0))
        self.groupBox_29.setFont(font1)
        self.gridLayout_87 = QGridLayout(self.groupBox_29)
        self.gridLayout_87.setObjectName(u"gridLayout_87")
        self.MC_setting = QToolBox(self.groupBox_29)
        self.MC_setting.setObjectName(u"MC_setting")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.MC_setting.setPalette(palette)
        self.MC_setting.setFont(font2)
        self.Normal = QWidget()
        self.Normal.setObjectName(u"Normal")
        self.Normal.setGeometry(QRect(0, 0, 334, 190))
        self.gridLayout_71 = QGridLayout(self.Normal)
        self.gridLayout_71.setObjectName(u"gridLayout_71")
        self.label_68 = QLabel(self.Normal)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setFont(font2)

        self.gridLayout_71.addWidget(self.label_68, 0, 0, 1, 1)

        self.MC_N_runs = QSpinBox(self.Normal)
        self.MC_N_runs.setObjectName(u"MC_N_runs")
        sizePolicy5.setHeightForWidth(self.MC_N_runs.sizePolicy().hasHeightForWidth())
        self.MC_N_runs.setSizePolicy(sizePolicy5)
        self.MC_N_runs.setFont(font2)

        self.gridLayout_71.addWidget(self.MC_N_runs, 0, 1, 1, 1)

        self.label_69 = QLabel(self.Normal)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFont(font2)

        self.gridLayout_71.addWidget(self.label_69, 1, 0, 1, 1)

        self.MC_included_models = QScrollArea(self.Normal)
        self.MC_included_models.setObjectName(u"MC_included_models")
        self.MC_included_models.setMinimumSize(QSize(200, 0))
        self.MC_included_models.setFont(font2)
        self.MC_included_models.setWidgetResizable(True)
        self.scrollAreaWidgetContents_10 = QWidget()
        self.scrollAreaWidgetContents_10.setObjectName(u"scrollAreaWidgetContents_10")
        self.scrollAreaWidgetContents_10.setGeometry(QRect(0, 0, 314, 125))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.MC_included_models.setWidget(self.scrollAreaWidgetContents_10)

        self.gridLayout_71.addWidget(self.MC_included_models, 2, 0, 1, 3)

        self.MC_setting.addItem(self.Normal, u"Monte Carlo Setup")
        self.Advanced = QWidget()
        self.Advanced.setObjectName(u"Advanced")
        self.Advanced.setGeometry(QRect(0, 0, 180, 70))
        self.gridLayout_89 = QGridLayout(self.Advanced)
        self.gridLayout_89.setObjectName(u"gridLayout_89")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_67 = QLabel(self.Advanced)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font2)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_67)

        self.MC_N_Thread = QSpinBox(self.Advanced)
        self.MC_N_Thread.setObjectName(u"MC_N_Thread")
        sizePolicy1.setHeightForWidth(self.MC_N_Thread.sizePolicy().hasHeightForWidth())
        self.MC_N_Thread.setSizePolicy(sizePolicy1)
        self.MC_N_Thread.setFont(font2)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.MC_N_Thread)

        self.label_83 = QLabel(self.Advanced)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setFont(font2)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_83)

        self.MC_seed = QLineEdit(self.Advanced)
        self.MC_seed.setObjectName(u"MC_seed")
        sizePolicy1.setHeightForWidth(self.MC_seed.sizePolicy().hasHeightForWidth())
        self.MC_seed.setSizePolicy(sizePolicy1)
        self.MC_seed.setFont(font2)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.MC_seed)


        self.gridLayout_89.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(101, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_89.addItem(self.horizontalSpacer_18, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 255, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_89.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.MC_setting.addItem(self.Advanced, u"Advanced")

        self.gridLayout_87.addWidget(self.MC_setting, 0, 0, 1, 1)

        self.splitter.addWidget(self.groupBox_29)
        self.splitter_6.addWidget(self.splitter)
        self.groupBox_13 = QGroupBox(self.splitter_6)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setFont(font1)
        self.gridLayout_65 = QGridLayout(self.groupBox_13)
        self.gridLayout_65.setObjectName(u"gridLayout_65")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_5 = QLabel(self.groupBox_13)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.horizontalLayout_14.addWidget(self.label_5)

        self.MC_Model = QComboBox(self.groupBox_13)
        self.MC_Model.setObjectName(u"MC_Model")
        sizePolicy1.setHeightForWidth(self.MC_Model.sizePolicy().hasHeightForWidth())
        self.MC_Model.setSizePolicy(sizePolicy1)
        self.MC_Model.setMinimumSize(QSize(200, 0))
        self.MC_Model.setFont(font2)

        self.horizontalLayout_14.addWidget(self.MC_Model)

        self.MC_uncertain_filter = QCheckBox(self.groupBox_13)
        self.MC_uncertain_filter.setObjectName(u"MC_uncertain_filter")
        sizePolicy5.setHeightForWidth(self.MC_uncertain_filter.sizePolicy().hasHeightForWidth())
        self.MC_uncertain_filter.setSizePolicy(sizePolicy5)
        self.MC_uncertain_filter.setFont(font2)

        self.horizontalLayout_14.addWidget(self.MC_uncertain_filter)

        self.Help_UncertaintyDist = QPushButton(self.groupBox_13)
        self.Help_UncertaintyDist.setObjectName(u"Help_UncertaintyDist")
        self.Help_UncertaintyDist.setFont(font2)
        self.Help_UncertaintyDist.setIcon(icon1)
        self.Help_UncertaintyDist.setIconSize(QSize(24, 24))

        self.horizontalLayout_14.addWidget(self.Help_UncertaintyDist)

        self.horizontalSpacer_47 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_47)

        self.MC_unceratin_clear = QPushButton(self.groupBox_13)
        self.MC_unceratin_clear.setObjectName(u"MC_unceratin_clear")
        sizePolicy5.setHeightForWidth(self.MC_unceratin_clear.sizePolicy().hasHeightForWidth())
        self.MC_unceratin_clear.setSizePolicy(sizePolicy5)
        self.MC_unceratin_clear.setFont(font2)
        self.MC_unceratin_clear.setIcon(icon3)

        self.horizontalLayout_14.addWidget(self.MC_unceratin_clear)

        self.MC_uncertain_update = QPushButton(self.groupBox_13)
        self.MC_uncertain_update.setObjectName(u"MC_uncertain_update")
        sizePolicy5.setHeightForWidth(self.MC_uncertain_update.sizePolicy().hasHeightForWidth())
        self.MC_uncertain_update.setSizePolicy(sizePolicy5)
        self.MC_uncertain_update.setFont(font2)
        self.MC_uncertain_update.setIcon(icon4)

        self.horizontalLayout_14.addWidget(self.MC_uncertain_update)


        self.gridLayout_65.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)

        self.MC_Uncertain_table = QTableView(self.groupBox_13)
        self.MC_Uncertain_table.setObjectName(u"MC_Uncertain_table")
        self.MC_Uncertain_table.setMinimumSize(QSize(0, 300))
        self.MC_Uncertain_table.setFont(font2)

        self.gridLayout_65.addWidget(self.MC_Uncertain_table, 1, 0, 1, 1)

        self.splitter_6.addWidget(self.groupBox_13)

        self.gridLayout_30.addWidget(self.splitter_6, 0, 0, 1, 1)

        self.groupBox_14 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setFont(font1)
        self.gridLayout_94 = QGridLayout(self.groupBox_14)
        self.gridLayout_94.setObjectName(u"gridLayout_94")
        self.MC_run = QPushButton(self.groupBox_14)
        self.MC_run.setObjectName(u"MC_run")
        self.MC_run.setFont(font2)
        icon9 = QIcon()
        icon9.addFile(u":/ICONS/PySWOLF_ICONS/run.png", QSize(), QIcon.Normal, QIcon.Off)
        self.MC_run.setIcon(icon9)

        self.gridLayout_94.addWidget(self.MC_run, 0, 0, 1, 1)

        self.MC_show = QPushButton(self.groupBox_14)
        self.MC_show.setObjectName(u"MC_show")
        self.MC_show.setFont(font2)
        self.MC_show.setIcon(icon7)

        self.gridLayout_94.addWidget(self.MC_show, 0, 3, 1, 1)

        self.MC_PBr = QProgressBar(self.groupBox_14)
        self.MC_PBr.setObjectName(u"MC_PBr")
        self.MC_PBr.setMaximumSize(QSize(300, 16777215))
        self.MC_PBr.setValue(0)
        self.MC_PBr.setTextVisible(False)

        self.gridLayout_94.addWidget(self.MC_PBr, 0, 1, 1, 1)

        self.MC_save = QPushButton(self.groupBox_14)
        self.MC_save.setObjectName(u"MC_save")
        self.MC_save.setFont(font2)
        icon10 = QIcon()
        icon10.addFile(u":/ICONS/PySWOLF_ICONS/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.MC_save.setIcon(icon10)

        self.gridLayout_94.addWidget(self.MC_save, 0, 4, 1, 1)

        self.horizontalSpacer_46 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_94.addItem(self.horizontalSpacer_46, 0, 2, 1, 1)


        self.gridLayout_30.addWidget(self.groupBox_14, 1, 0, 1, 1)

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_88.addWidget(self.scrollArea_6, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.MC_tab, "")
        self.Opt_tab = QWidget()
        self.Opt_tab.setObjectName(u"Opt_tab")
        self.gridLayout_15 = QGridLayout(self.Opt_tab)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.scrollArea_5 = QScrollArea(self.Opt_tab)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setMinimumSize(QSize(0, 0))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.Base, brush)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.scrollArea_5.setPalette(palette1)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_9 = QWidget()
        self.scrollAreaWidgetContents_9.setObjectName(u"scrollAreaWidgetContents_9")
        self.scrollAreaWidgetContents_9.setGeometry(QRect(0, 0, 1032, 1051))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.Base, brush)
        brush1 = QBrush(QColor(240, 240, 240, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.scrollAreaWidgetContents_9.setPalette(palette2)
        self.gridLayout_13 = QGridLayout(self.scrollAreaWidgetContents_9)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.splitter_7 = QSplitter(self.scrollAreaWidgetContents_9)
        self.splitter_7.setObjectName(u"splitter_7")
        self.splitter_7.setOrientation(Qt.Horizontal)
        self.groupBox_15 = QGroupBox(self.splitter_7)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setFont(font1)
        self.gridLayout_7 = QGridLayout(self.groupBox_15)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_71 = QLabel(self.groupBox_15)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setFont(font2)

        self.gridLayout_7.addWidget(self.label_71, 0, 0, 1, 1)

        self.label_72 = QLabel(self.groupBox_15)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setFont(font2)

        self.gridLayout_7.addWidget(self.label_72, 1, 0, 1, 1)

        self.Opt_FU_act = QComboBox(self.groupBox_15)
        self.Opt_FU_act.setObjectName(u"Opt_FU_act")
        sizePolicy2.setHeightForWidth(self.Opt_FU_act.sizePolicy().hasHeightForWidth())
        self.Opt_FU_act.setSizePolicy(sizePolicy2)
        self.Opt_FU_act.setMinimumSize(QSize(100, 0))
        self.Opt_FU_act.setFont(font2)

        self.gridLayout_7.addWidget(self.Opt_FU_act, 1, 1, 1, 3)

        self.label_73 = QLabel(self.groupBox_15)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setFont(font2)

        self.gridLayout_7.addWidget(self.label_73, 2, 0, 1, 1)

        self.Opt_FU_unit = QLabel(self.groupBox_15)
        self.Opt_FU_unit.setObjectName(u"Opt_FU_unit")

        self.gridLayout_7.addWidget(self.Opt_FU_unit, 2, 2, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_10, 2, 3, 1, 1)

        self.Opt_FU_DB = QComboBox(self.groupBox_15)
        self.Opt_FU_DB.setObjectName(u"Opt_FU_DB")
        sizePolicy2.setHeightForWidth(self.Opt_FU_DB.sizePolicy().hasHeightForWidth())
        self.Opt_FU_DB.setSizePolicy(sizePolicy2)
        self.Opt_FU_DB.setFont(font2)

        self.gridLayout_7.addWidget(self.Opt_FU_DB, 0, 1, 1, 3)

        self.splitter_7.addWidget(self.groupBox_15)
        self.groupBox_16 = QGroupBox(self.splitter_7)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setFont(font1)
        self.gridLayout_95 = QGridLayout(self.groupBox_16)
        self.gridLayout_95.setObjectName(u"gridLayout_95")
        self.label_74 = QLabel(self.groupBox_16)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setFont(font2)

        self.gridLayout_95.addWidget(self.label_74, 0, 0, 1, 1)

        self.Opt_method = QComboBox(self.groupBox_16)
        self.Opt_method.setObjectName(u"Opt_method")
        sizePolicy2.setHeightForWidth(self.Opt_method.sizePolicy().hasHeightForWidth())
        self.Opt_method.setSizePolicy(sizePolicy2)
        self.Opt_method.setMinimumSize(QSize(100, 0))
        self.Opt_method.setFont(font2)

        self.gridLayout_95.addWidget(self.Opt_method, 1, 0, 1, 3)

        self.Opt_Filter_keyword = QLineEdit(self.groupBox_16)
        self.Opt_Filter_keyword.setObjectName(u"Opt_Filter_keyword")
        sizePolicy4.setHeightForWidth(self.Opt_Filter_keyword.sizePolicy().hasHeightForWidth())
        self.Opt_Filter_keyword.setSizePolicy(sizePolicy4)
        self.Opt_Filter_keyword.setFont(font2)

        self.gridLayout_95.addWidget(self.Opt_Filter_keyword, 0, 1, 1, 1)

        self.Opt_Filter_method = QPushButton(self.groupBox_16)
        self.Opt_Filter_method.setObjectName(u"Opt_Filter_method")
        sizePolicy2.setHeightForWidth(self.Opt_Filter_method.sizePolicy().hasHeightForWidth())
        self.Opt_Filter_method.setSizePolicy(sizePolicy2)
        self.Opt_Filter_method.setFont(font2)
        self.Opt_Filter_method.setIcon(icon8)

        self.gridLayout_95.addWidget(self.Opt_Filter_method, 0, 2, 1, 1)

        self.splitter_7.addWidget(self.groupBox_16)

        self.gridLayout_13.addWidget(self.splitter_7, 0, 0, 1, 1)

        self.groupBox_20 = QGroupBox(self.scrollAreaWidgetContents_9)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setFont(font1)
        self.gridLayout_14 = QGridLayout(self.groupBox_20)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.groupBox_18 = QGroupBox(self.groupBox_20)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setFont(font1)
        self.gridLayout_8 = QGridLayout(self.groupBox_18)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.Opt_Const2_val = QLineEdit(self.groupBox_18)
        self.Opt_Const2_val.setObjectName(u"Opt_Const2_val")
        sizePolicy1.setHeightForWidth(self.Opt_Const2_val.sizePolicy().hasHeightForWidth())
        self.Opt_Const2_val.setSizePolicy(sizePolicy1)
        self.Opt_Const2_val.setMaximumSize(QSize(16777215, 16777215))
        self.Opt_Const2_val.setFont(font2)

        self.gridLayout_8.addWidget(self.Opt_Const2_val, 0, 7, 1, 1)

        self.Opt_Const2_Inequality = QComboBox(self.groupBox_18)
        self.Opt_Const2_Inequality.setObjectName(u"Opt_Const2_Inequality")
        sizePolicy1.setHeightForWidth(self.Opt_Const2_Inequality.sizePolicy().hasHeightForWidth())
        self.Opt_Const2_Inequality.setSizePolicy(sizePolicy1)
        self.Opt_Const2_Inequality.setMinimumSize(QSize(100, 0))
        self.Opt_Const2_Inequality.setFont(font2)

        self.gridLayout_8.addWidget(self.Opt_Const2_Inequality, 0, 5, 1, 1)

        self.horizontalSpacer_27 = QSpacerItem(193, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_27, 0, 10, 1, 1)

        self.label_79 = QLabel(self.groupBox_18)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setFont(font2)

        self.gridLayout_8.addWidget(self.label_79, 0, 2, 1, 1)

        self.label_77 = QLabel(self.groupBox_18)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setFont(font2)

        self.gridLayout_8.addWidget(self.label_77, 0, 0, 1, 1)

        self.Opt_add_Const2 = QPushButton(self.groupBox_18)
        self.Opt_add_Const2.setObjectName(u"Opt_add_Const2")
        sizePolicy5.setHeightForWidth(self.Opt_add_Const2.sizePolicy().hasHeightForWidth())
        self.Opt_add_Const2.setSizePolicy(sizePolicy5)
        self.Opt_add_Const2.setFont(font2)
        self.Opt_add_Const2.setIcon(icon5)

        self.gridLayout_8.addWidget(self.Opt_add_Const2, 0, 9, 1, 1)

        self.label_78 = QLabel(self.groupBox_18)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setFont(font2)

        self.gridLayout_8.addWidget(self.label_78, 0, 6, 1, 1)

        self.label_87 = QLabel(self.groupBox_18)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setFont(font2)

        self.gridLayout_8.addWidget(self.label_87, 0, 4, 1, 1)

        self.Opt_Const2_process = QComboBox(self.groupBox_18)
        self.Opt_Const2_process.setObjectName(u"Opt_Const2_process")
        sizePolicy1.setHeightForWidth(self.Opt_Const2_process.sizePolicy().hasHeightForWidth())
        self.Opt_Const2_process.setSizePolicy(sizePolicy1)
        self.Opt_Const2_process.setMinimumSize(QSize(150, 0))
        self.Opt_Const2_process.setFont(font2)

        self.gridLayout_8.addWidget(self.Opt_Const2_process, 0, 1, 1, 1)

        self.Opt_Const2_flow = QComboBox(self.groupBox_18)
        self.Opt_Const2_flow.setObjectName(u"Opt_Const2_flow")
        sizePolicy1.setHeightForWidth(self.Opt_Const2_flow.sizePolicy().hasHeightForWidth())
        self.Opt_Const2_flow.setSizePolicy(sizePolicy1)
        self.Opt_Const2_flow.setMinimumSize(QSize(300, 0))
        self.Opt_Const2_flow.setFont(font2)

        self.gridLayout_8.addWidget(self.Opt_Const2_flow, 0, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox_18)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.gridLayout_8.addWidget(self.label_2, 0, 8, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_18, 1, 0, 1, 1)

        self.groupBox_19 = QGroupBox(self.groupBox_20)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setFont(font1)
        self.gridLayout_10 = QGridLayout(self.groupBox_19)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_88 = QLabel(self.groupBox_19)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setFont(font2)

        self.gridLayout_10.addWidget(self.label_88, 0, 2, 1, 1)

        self.Opt_add_Const3 = QPushButton(self.groupBox_19)
        self.Opt_add_Const3.setObjectName(u"Opt_add_Const3")
        sizePolicy5.setHeightForWidth(self.Opt_add_Const3.sizePolicy().hasHeightForWidth())
        self.Opt_add_Const3.setSizePolicy(sizePolicy5)
        self.Opt_add_Const3.setFont(font2)
        self.Opt_add_Const3.setIcon(icon5)

        self.gridLayout_10.addWidget(self.Opt_add_Const3, 0, 7, 1, 1)

        self.label_81 = QLabel(self.groupBox_19)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setFont(font2)

        self.gridLayout_10.addWidget(self.label_81, 0, 0, 1, 1)

        self.Opt_Const3_Inequality = QComboBox(self.groupBox_19)
        self.Opt_Const3_Inequality.setObjectName(u"Opt_Const3_Inequality")
        sizePolicy1.setHeightForWidth(self.Opt_Const3_Inequality.sizePolicy().hasHeightForWidth())
        self.Opt_Const3_Inequality.setSizePolicy(sizePolicy1)
        self.Opt_Const3_Inequality.setMinimumSize(QSize(0, 0))
        self.Opt_Const3_Inequality.setFont(font2)

        self.gridLayout_10.addWidget(self.Opt_Const3_Inequality, 0, 3, 1, 1)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_28, 0, 8, 1, 1)

        self.Opt_Const3_flow = QComboBox(self.groupBox_19)
        self.Opt_Const3_flow.setObjectName(u"Opt_Const3_flow")
        sizePolicy1.setHeightForWidth(self.Opt_Const3_flow.sizePolicy().hasHeightForWidth())
        self.Opt_Const3_flow.setSizePolicy(sizePolicy1)
        self.Opt_Const3_flow.setMinimumSize(QSize(350, 0))
        self.Opt_Const3_flow.setFont(font2)

        self.gridLayout_10.addWidget(self.Opt_Const3_flow, 0, 1, 1, 1)

        self.label_82 = QLabel(self.groupBox_19)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setFont(font2)

        self.gridLayout_10.addWidget(self.label_82, 0, 4, 1, 1)

        self.Opt_Const3_val = QLineEdit(self.groupBox_19)
        self.Opt_Const3_val.setObjectName(u"Opt_Const3_val")
        sizePolicy1.setHeightForWidth(self.Opt_Const3_val.sizePolicy().hasHeightForWidth())
        self.Opt_Const3_val.setSizePolicy(sizePolicy1)
        self.Opt_Const3_val.setMinimumSize(QSize(0, 0))
        self.Opt_Const3_val.setFont(font2)

        self.gridLayout_10.addWidget(self.Opt_Const3_val, 0, 5, 1, 1)

        self.label_3 = QLabel(self.groupBox_19)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.gridLayout_10.addWidget(self.label_3, 0, 6, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_19, 2, 0, 1, 1)

        self.groupBox_17 = QGroupBox(self.groupBox_20)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setFont(font1)
        self.gridLayout_12 = QGridLayout(self.groupBox_17)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.Opt_Const1_val = QLineEdit(self.groupBox_17)
        self.Opt_Const1_val.setObjectName(u"Opt_Const1_val")
        sizePolicy1.setHeightForWidth(self.Opt_Const1_val.sizePolicy().hasHeightForWidth())
        self.Opt_Const1_val.setSizePolicy(sizePolicy1)
        self.Opt_Const1_val.setFont(font2)

        self.gridLayout_12.addWidget(self.Opt_Const1_val, 0, 5, 1, 1)

        self.label_76 = QLabel(self.groupBox_17)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setFont(font2)

        self.gridLayout_12.addWidget(self.label_76, 0, 4, 1, 1)

        self.Opt_add_Const1 = QPushButton(self.groupBox_17)
        self.Opt_add_Const1.setObjectName(u"Opt_add_Const1")
        sizePolicy5.setHeightForWidth(self.Opt_add_Const1.sizePolicy().hasHeightForWidth())
        self.Opt_add_Const1.setSizePolicy(sizePolicy5)
        self.Opt_add_Const1.setFont(font2)
        self.Opt_add_Const1.setIcon(icon5)

        self.gridLayout_12.addWidget(self.Opt_add_Const1, 0, 7, 1, 1)

        self.Opt_Const1_Inequality = QComboBox(self.groupBox_17)
        self.Opt_Const1_Inequality.setObjectName(u"Opt_Const1_Inequality")
        sizePolicy1.setHeightForWidth(self.Opt_Const1_Inequality.sizePolicy().hasHeightForWidth())
        self.Opt_Const1_Inequality.setSizePolicy(sizePolicy1)

        self.gridLayout_12.addWidget(self.Opt_Const1_Inequality, 0, 3, 1, 1)

        self.label_75 = QLabel(self.groupBox_17)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setFont(font2)

        self.gridLayout_12.addWidget(self.label_75, 0, 0, 1, 1)

        self.label_86 = QLabel(self.groupBox_17)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setFont(font2)

        self.gridLayout_12.addWidget(self.label_86, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_3, 0, 8, 1, 1)

        self.Opt_Const1_process = QComboBox(self.groupBox_17)
        self.Opt_Const1_process.setObjectName(u"Opt_Const1_process")
        sizePolicy1.setHeightForWidth(self.Opt_Const1_process.sizePolicy().hasHeightForWidth())
        self.Opt_Const1_process.setSizePolicy(sizePolicy1)
        self.Opt_Const1_process.setMinimumSize(QSize(150, 0))
        self.Opt_Const1_process.setFont(font2)

        self.gridLayout_12.addWidget(self.Opt_Const1_process, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_17)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)

        self.gridLayout_12.addWidget(self.label, 0, 6, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_17, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_20, 1, 0, 1, 1)

        self.splitter_5 = QSplitter(self.scrollAreaWidgetContents_9)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setMinimumSize(QSize(0, 700))
        self.splitter_5.setOrientation(Qt.Vertical)
        self.groupBox_22 = QGroupBox(self.splitter_5)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setFont(font1)
        self.gridLayout_11 = QGridLayout(self.groupBox_22)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.Opt_Const_table = QTableView(self.groupBox_22)
        self.Opt_Const_table.setObjectName(u"Opt_Const_table")
        sizePolicy.setHeightForWidth(self.Opt_Const_table.sizePolicy().hasHeightForWidth())
        self.Opt_Const_table.setSizePolicy(sizePolicy)
        self.Opt_Const_table.setMinimumSize(QSize(0, 100))
        self.Opt_Const_table.setFont(font2)

        self.gridLayout_11.addWidget(self.Opt_Const_table, 0, 0, 1, 1)

        self.splitter_5.addWidget(self.groupBox_22)
        self.groupBox_21 = QGroupBox(self.splitter_5)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setMinimumSize(QSize(500, 0))
        self.groupBox_21.setFont(font1)
        self.gridLayout_9 = QGridLayout(self.groupBox_21)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.Opt_CalObjFunc = QPushButton(self.groupBox_21)
        self.Opt_CalObjFunc.setObjectName(u"Opt_CalObjFunc")

        self.horizontalLayout_13.addWidget(self.Opt_CalObjFunc)

        self.Opt_CalObjFunc_Res = QLineEdit(self.groupBox_21)
        self.Opt_CalObjFunc_Res.setObjectName(u"Opt_CalObjFunc_Res")
        sizePolicy7.setHeightForWidth(self.Opt_CalObjFunc_Res.sizePolicy().hasHeightForWidth())
        self.Opt_CalObjFunc_Res.setSizePolicy(sizePolicy7)

        self.horizontalLayout_13.addWidget(self.Opt_CalObjFunc_Res)

        self.horizontalSpacer_13 = QSpacerItem(377, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_13)

        self.Opt_ClearConstr = QPushButton(self.groupBox_21)
        self.Opt_ClearConstr.setObjectName(u"Opt_ClearConstr")
        self.Opt_ClearConstr.setIcon(icon3)

        self.horizontalLayout_13.addWidget(self.Opt_ClearConstr)

        self.Opt_update_param = QPushButton(self.groupBox_21)
        self.Opt_update_param.setObjectName(u"Opt_update_param")
        self.Opt_update_param.setFont(font2)
        self.Opt_update_param.setIcon(icon4)

        self.horizontalLayout_13.addWidget(self.Opt_update_param)


        self.gridLayout_9.addLayout(self.horizontalLayout_13, 2, 0, 1, 1)

        self.Opt_Param_table = QTableView(self.groupBox_21)
        self.Opt_Param_table.setObjectName(u"Opt_Param_table")
        self.Opt_Param_table.setMinimumSize(QSize(0, 150))
        self.Opt_Param_table.setFont(font2)

        self.gridLayout_9.addWidget(self.Opt_Param_table, 1, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.Opt_optimize = QPushButton(self.groupBox_21)
        self.Opt_optimize.setObjectName(u"Opt_optimize")
        sizePolicy5.setHeightForWidth(self.Opt_optimize.sizePolicy().hasHeightForWidth())
        self.Opt_optimize.setSizePolicy(sizePolicy5)
        self.Opt_optimize.setFont(font2)

        self.horizontalLayout_12.addWidget(self.Opt_optimize)

        self.Opt_PBr = QProgressBar(self.groupBox_21)
        self.Opt_PBr.setObjectName(u"Opt_PBr")
        self.Opt_PBr.setEnabled(True)
        self.Opt_PBr.setMaximumSize(QSize(300, 16777215))
        self.Opt_PBr.setMaximum(100)
        self.Opt_PBr.setValue(0)
        self.Opt_PBr.setTextVisible(False)

        self.horizontalLayout_12.addWidget(self.Opt_PBr)

        self.label_9 = QLabel(self.groupBox_21)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)

        self.horizontalLayout_12.addWidget(self.label_9)

        self.Opt_score = QLineEdit(self.groupBox_21)
        self.Opt_score.setObjectName(u"Opt_score")
        sizePolicy5.setHeightForWidth(self.Opt_score.sizePolicy().hasHeightForWidth())
        self.Opt_score.setSizePolicy(sizePolicy5)
        self.Opt_score.setFont(font2)

        self.horizontalLayout_12.addWidget(self.Opt_score)

        self.Opt_unit = QLineEdit(self.groupBox_21)
        self.Opt_unit.setObjectName(u"Opt_unit")
        sizePolicy5.setHeightForWidth(self.Opt_unit.sizePolicy().hasHeightForWidth())
        self.Opt_unit.setSizePolicy(sizePolicy5)
        self.Opt_unit.setFont(font2)

        self.horizontalLayout_12.addWidget(self.Opt_unit)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_11)

        self.adv_opt_btm = QPushButton(self.groupBox_21)
        self.adv_opt_btm.setObjectName(u"adv_opt_btm")
        self.adv_opt_btm.setFont(font2)
        self.adv_opt_btm.setIcon(icon6)

        self.horizontalLayout_12.addWidget(self.adv_opt_btm)


        self.gridLayout_9.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)

        self.splitter_5.addWidget(self.groupBox_21)

        self.gridLayout_13.addWidget(self.splitter_5, 2, 0, 1, 1)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_9)

        self.gridLayout_15.addWidget(self.scrollArea_5, 0, 0, 1, 1)

        self.PySWOLF.addTab(self.Opt_tab, "")

        self.gridLayout.addWidget(self.PySWOLF, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 941, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuReferences = QMenu(self.menubar)
        self.menuReferences.setObjectName(u"menuReferences")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuReferences.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp_Guides)
        self.menuReferences.addAction(self.actionReferences)

        self.retranslateUi(MainWindow)

        self.PySWOLF.setCurrentIndex(1)
        self.init_process_toolbox.setCurrentIndex(0)
        self.Define_SWM_1.setCurrentIndex(0)
        self.Collection.setCurrentIndex(-1)
        self.TransportWidget.setCurrentIndex(-1)
        self.LCA_subTab.setCurrentIndex(0)
        self.MC_setting.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"swolfpy", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionHelp_Guides.setText(QCoreApplication.translate("MainWindow", u"Help Guides", None))
        self.actionReferences.setText(QCoreApplication.translate("MainWindow", u"References", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:20pt; font-weight:600; color:#aa0000;\">Solid Waste Optimization Life-cycle Framework in Python</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:16pt; color:#aa0000;\">Developed at North Carolina State University</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/I"
                        "CONS/PySWOLF_ICONS/PySWOLF.ico\" /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; color:#aa0000;\">Related Links:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-in"
                        "dent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:600;\">Install: </span><a href=\"https://pypi.org/project/swolfpy/\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;\">https://pypi.org/project/swolfpy/</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:600;\">Document: </span><a href=\"https://go.ncsu.edu/swolfpy_docs\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;\">https://go.ncsu.edu/swolfpy_docs</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:600;\">Source Code: </span><a href=\"https://go.ncsu.edu/swolfpy_source_code\"><span style=\" font"
                        "-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;\">https://go.ncsu.edu/swolfpy_source_code</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:600;\">Report bugs: </span><a href=\"https://go.ncsu.edu/swolfpy_issues\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;\">https://go.ncsu.edu/swolfpy_issues</span></a></p></body></html>", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Strat New Project", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Options:", None))
        self.Start_def_process.setText(QCoreApplication.translate("MainWindow", u"Default Process Models", None))
        self.Start_new_project.setText(QCoreApplication.translate("MainWindow", u"Start New Project", None))
        self.Start_user_process.setText(QCoreApplication.translate("MainWindow", u"User Defined Process Models", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Load Project", None))
        self.Start_load_project.setText(QCoreApplication.translate("MainWindow", u"Load Project", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Start), QCoreApplication.translate("MainWindow", u"Start", None))
        self.ImportProcessModels.setText(QCoreApplication.translate("MainWindow", u"Import Process Models", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Process Model", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Process Model:", None))
        self.Help_ImportProcess.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Process Model Setting", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.IT_Default.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.IT_UserDefine.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_BR.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_FName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Input Flow Type:", None))
        self.Clear_PM_setting.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Update_PM_setting.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.init_process_toolbox.setTabText(self.init_process_toolbox.indexOf(self.PM_PMTab), QCoreApplication.translate("MainWindow", u"Process Models", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.IT_BR_0.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_UserDefine_0.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_FName_0.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.IT_Default_0.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("MainWindow", u"Input Data:", None))
        self.IT_Default_00.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.IT_UserDefine_00.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_BR_00.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_FName_00.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.init_process_toolbox.setTabText(self.init_process_toolbox.indexOf(self.PM_CMTab), QCoreApplication.translate("MainWindow", u"Common Data", None))
        self.groupBox_33.setTitle(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.IT_BR_Tech.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_UserDefine_Tech.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_Default_Tech.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.IT_FName_Tech.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"SwolfPy Technosphere LCI:", None))
        self.IT_FName_LCI.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.IT_UserDefine_LCI.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_BR_LCI.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_Default_LCI.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.groupBox_36.setTitle(QCoreApplication.translate("MainWindow", u"Technosphere EcoSpold2:", None))
        self.IT_Default_EcoSpold2.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.IT_BR_EcoSpold2.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_UserDefine_EcoSpold2.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_FName_EcoSpold2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("MainWindow", u"Technosphere Reference:", None))
        self.IT_BR_LCI_Ref.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.IT_UserDefine_LCI_Ref.setText(QCoreApplication.translate("MainWindow", u"User Defined", None))
        self.IT_Default_LCI_Ref.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.IT_FName_LCI_Ref.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the user defined model", None))
        self.init_process_toolbox.setTabText(self.init_process_toolbox.indexOf(self.PM_TCTab), QCoreApplication.translate("MainWindow", u"Technosphere", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Import_PM), QCoreApplication.translate("MainWindow", u"Import Process Models", None))
        self.Add_col.setText(QCoreApplication.translate("MainWindow", u"Add Sector", None))
        self.Help_ColSector.setText("")
        self.Create_Collection_process.setText(QCoreApplication.translate("MainWindow", u"Create Collection processes", None))
        self.Define_SWM_1.setItemText(self.Define_SWM_1.indexOf(self.Collection_process), QCoreApplication.translate("MainWindow", u"Collection Processes", None))
        self.label_84.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Input Type", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Address to input file", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.Treat_process_Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Create_Treat_prc_dict.setText(QCoreApplication.translate("MainWindow", u"Create Treatment Processes", None))
        self.Add_process.setText(QCoreApplication.translate("MainWindow", u"Add Process", None))
        self.Help_AddProcess.setText("")
        self.Define_SWM_1.setItemText(self.Define_SWM_1.indexOf(self.Treatment_process), QCoreApplication.translate("MainWindow", u"Treatment Processes", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Transportation modes:", None))
        self.Create_Distance.setText(QCoreApplication.translate("MainWindow", u"Create Distance Table", None))
        self.Help_DistanceTable.setText("")
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Project Name:", None))
        self.Project_Name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the name of project", None))
        self.write_project.setText(QCoreApplication.translate("MainWindow", u"Create System", None))
        self.Load_params.setText(QCoreApplication.translate("MainWindow", u"Load Parameters", None))
        self.Help_Project_Param.setText("")
        self.update_param.setText(QCoreApplication.translate("MainWindow", u"Update Parameters", None))
        self.Show_SWM_Network.setText(QCoreApplication.translate("MainWindow", u"Show Network", None))
        self.Show_SWM_Network_AllFlows.setText(QCoreApplication.translate("MainWindow", u"Include zero flows", None))
        self.Define_SWM_1.setItemText(self.Define_SWM_1.indexOf(self.Network), QCoreApplication.translate("MainWindow", u"System", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Define_SWM), QCoreApplication.translate("MainWindow", u"Define SWM System", None))
        self.Br_Project_btm.setText(QCoreApplication.translate("MainWindow", u"Browse Project", None))
        self.Load_Project_btm.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_53.setText("")
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Project Info", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Project Name:", None))
        self.load_P_name.setText(QCoreApplication.translate("MainWindow", u"............", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.Load_params_Load.setText(QCoreApplication.translate("MainWindow", u"Load Parameters", None))
        self.load_update_param.setText(QCoreApplication.translate("MainWindow", u"Update Parameters", None))
        self.Show_SWM_Network_Load.setText(QCoreApplication.translate("MainWindow", u"Show Network", None))
        self.Show_SWM_Network_Load_AllFlows.setText(QCoreApplication.translate("MainWindow", u"Include zero flows", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Load_Project), QCoreApplication.translate("MainWindow", u"Load Project", None))
        self.Start_new_sen.setText(QCoreApplication.translate("MainWindow", u"Start New Scenario", None))
        self.Help_CreateScenario.setText("")
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Name of scenario", None))
        self.Name_new_scenario.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the name of scenario", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Data Base:", None))
        self.Add_act_to_scen.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Included activities:", None))
        self.Clear_act.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Create_scenario.setText(QCoreApplication.translate("MainWindow", u"Create Scenario", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Create_Scenario), QCoreApplication.translate("MainWindow", u"Create Scenario", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Impact Assessment Categories", None))
        self.Filter_impact_keyword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter by search", None))
        self.LCA_Filter_impacts.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.LCA_View_method.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.LCA_AddImpact.setText(QCoreApplication.translate("MainWindow", u"Add method to LCA", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Impacts:", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"LCIA method:", None))
        self.LCA_ClearSetup.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.LCA_CreateLCA.setText(QCoreApplication.translate("MainWindow", u"LCA", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Functional Unit", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Activities:", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Activity:", None))
        self.LCA_AddAct.setText(QCoreApplication.translate("MainWindow", u"Add activity to LCA", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Database:", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Unit:", None))
        self.LCA_FU_unit.setText("")
        self.LCA_subTab.setTabText(self.LCA_subTab.indexOf(self.LCA_setup_tab), QCoreApplication.translate("MainWindow", u"Setup LCA", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Environmmental Impact: ", None))
        self.LCA_subTab.setTabText(self.LCA_subTab.indexOf(self.LCA_Results_tab), QCoreApplication.translate("MainWindow", u"LCA Results", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"Contribution analysis", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Functional Unit:", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Environmental Impact:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CutOff:", None))
        self.LCA_Contr__Top_act.setText(QCoreApplication.translate("MainWindow", u"Top Activities", None))
        self.LCA_Contr_Top_emis.setText(QCoreApplication.translate("MainWindow", u"Top Emissions", None))
        self.LCA_Contr_updat.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Contribution Results", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Impact:", None))
        self.LCA_subTab.setTabText(self.LCA_subTab.indexOf(self.LCA_Contribution_tab), QCoreApplication.translate("MainWindow", u"Contribution Analysis", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Life Cycle Inventory", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.LCA_LCI_updat.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Functional Unit:", None))
        self.LCA_subTab.setTabText(self.LCA_subTab.indexOf(self.LCA_LCI_tab), QCoreApplication.translate("MainWindow", u"Life Cycle Inventory", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.LCA_tab), QCoreApplication.translate("MainWindow", u"LCA", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Functional Unit", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"Database:", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"Activity:", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Unit:", None))
        self.MC_FU_unit.setText("")
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Impact Categories", None))
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"LCIA method:", None))
        self.MC_Filter_keyword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter by search", None))
        self.MC_Filter_method.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.MC_add_method.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Monte Carlo setting", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"Nnmber of runs:", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Models included:", None))
        self.MC_setting.setItemText(self.MC_setting.indexOf(self.Normal), QCoreApplication.translate("MainWindow", u"Monte Carlo Setup", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Number of threads:", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Seed:", None))
        self.MC_setting.setItemText(self.MC_setting.indexOf(self.Advanced), QCoreApplication.translate("MainWindow", u"Advanced", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Uncertainty Browser", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.MC_uncertain_filter.setText(QCoreApplication.translate("MainWindow", u"Only show input variables with defined uncertainty", None))
        self.Help_UncertaintyDist.setText(QCoreApplication.translate("MainWindow", u"Uncertainty Distributions Help", None))
        self.MC_unceratin_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.MC_uncertain_update.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.MC_run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.MC_show.setText(QCoreApplication.translate("MainWindow", u"Show Results", None))
        self.MC_save.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.MC_tab), QCoreApplication.translate("MainWindow", u"Monte Carlo simulation", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Functional Unit", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Database:", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"Activity:", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Unit:", None))
        self.Opt_FU_unit.setText("")
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Environmental Impact", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"LCIA method:", None))
        self.Opt_Filter_keyword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter by search", None))
        self.Opt_Filter_method.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Constraints", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Constraint on Waste to Process", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Waste Fraction:", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"Process:", None))
        self.Opt_add_Const2.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"Limit:", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"Inequality:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Unit: Mg", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Constraints on Emissions", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"Inequality:", None))
        self.Opt_add_Const3.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"Emission:", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Limit:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Unit: kg", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Constraint on Total Mass to Process", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"Limit:", None))
        self.Opt_add_Const1.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"Process:", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"Inequality:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Unit: Mg", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Table of Constraints", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Results", None))
        self.Opt_CalObjFunc.setText(QCoreApplication.translate("MainWindow", u"Objective Function", None))
        self.Opt_ClearConstr.setText(QCoreApplication.translate("MainWindow", u"Clear Constraints", None))
        self.Opt_update_param.setText(QCoreApplication.translate("MainWindow", u"Update project parameters", None))
        self.Opt_optimize.setText(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Results:", None))
        self.adv_opt_btm.setText(QCoreApplication.translate("MainWindow", u"Optimization setting", None))
        self.PySWOLF.setTabText(self.PySWOLF.indexOf(self.Opt_tab), QCoreApplication.translate("MainWindow", u"Optimization", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuReferences.setTitle(QCoreApplication.translate("MainWindow", u"References", None))
    # retranslateUi

