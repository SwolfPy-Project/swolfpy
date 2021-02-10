# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import PyWOLF_Resource_rc

class Ui_MC_Results(object):
    def setupUi(self, MC_Results):
        if not MC_Results.objectName():
            MC_Results.setObjectName(u"MC_Results")
        MC_Results.resize(1180, 1068)
        icon = QIcon()
        icon.addFile(u":/ICONS/PySWOLF_ICONS/PySWOLF.ico", QSize(), QIcon.Normal, QIcon.Off)
        MC_Results.setWindowIcon(icon)
        self.gridLayout = QGridLayout(MC_Results)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(MC_Results)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(400, 0))
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.MC_Data = QWidget()
        self.MC_Data.setObjectName(u"MC_Data")
        self.gridLayout_2 = QGridLayout(self.MC_Data)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.MC_Res_Table = QTableView(self.MC_Data)
        self.MC_Res_Table.setObjectName(u"MC_Res_Table")

        self.gridLayout_2.addWidget(self.MC_Res_Table, 0, 0, 1, 1)

        self.tabWidget.addTab(self.MC_Data, "")
        self.MC_Plot = QWidget()
        self.MC_Plot.setObjectName(u"MC_Plot")
        self.gridLayout_5 = QGridLayout(self.MC_Plot)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.scrollArea = QScrollArea(self.MC_Plot)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1136, 1004))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.splitter = QSplitter(self.scrollAreaWidgetContents)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 900))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.splitter_2 = QSplitter(self.frame)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.groupBox = QGroupBox(self.splitter_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 3, 1, 1)

        self.hexbin = QRadioButton(self.groupBox)
        self.hexbin.setObjectName(u"hexbin")

        self.gridLayout_3.addWidget(self.hexbin, 1, 5, 1, 1)

        self.y_axis = QComboBox(self.groupBox)
        self.y_axis.setObjectName(u"y_axis")
        self.y_axis.setMinimumSize(QSize(400, 0))

        self.gridLayout_3.addWidget(self.y_axis, 1, 1, 1, 1)

        self.scatter = QRadioButton(self.groupBox)
        self.scatter.setObjectName(u"scatter")

        self.gridLayout_3.addWidget(self.scatter, 1, 4, 1, 1)

        self.x_axis = QComboBox(self.groupBox)
        self.x_axis.setObjectName(u"x_axis")

        self.gridLayout_3.addWidget(self.x_axis, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.Update_plot = QPushButton(self.groupBox)
        self.Update_plot.setObjectName(u"Update_plot")
        icon1 = QIcon()
        icon1.addFile(u":/ICONS/PySWOLF_ICONS/Update.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Update_plot.setIcon(icon1)

        self.gridLayout_3.addWidget(self.Update_plot, 1, 6, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 7, 1, 1)

        self.plot = QWidget(self.groupBox)
        self.plot.setObjectName(u"plot")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setMinimumSize(QSize(0, 100))

        self.gridLayout_3.addWidget(self.plot, 2, 0, 1, 8)

        self.splitter_2.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 1, 0, 2, 1)

        self.plot_dist = QWidget(self.groupBox_2)
        self.plot_dist.setObjectName(u"plot_dist")
        sizePolicy.setHeightForWidth(self.plot_dist.sizePolicy().hasHeightForWidth())
        self.plot_dist.setSizePolicy(sizePolicy)
        self.plot_dist.setMinimumSize(QSize(0, 100))

        self.gridLayout_4.addWidget(self.plot_dist, 3, 0, 1, 6)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)

        self.param = QComboBox(self.groupBox_2)
        self.param.setObjectName(u"param")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.param.sizePolicy().hasHeightForWidth())
        self.param.setSizePolicy(sizePolicy1)
        self.param.setMinimumSize(QSize(400, 0))

        self.gridLayout_4.addWidget(self.param, 0, 1, 1, 3)

        self.hist = QRadioButton(self.groupBox_2)
        self.hist.setObjectName(u"hist")

        self.gridLayout_4.addWidget(self.hist, 2, 1, 1, 1)

        self.box = QRadioButton(self.groupBox_2)
        self.box.setObjectName(u"box")

        self.gridLayout_4.addWidget(self.box, 2, 2, 1, 1)

        self.density = QRadioButton(self.groupBox_2)
        self.density.setObjectName(u"density")

        self.gridLayout_4.addWidget(self.density, 2, 3, 1, 1)

        self.Update_dist_fig = QPushButton(self.groupBox_2)
        self.Update_dist_fig.setObjectName(u"Update_dist_fig")
        self.Update_dist_fig.setIcon(icon1)

        self.gridLayout_4.addWidget(self.Update_dist_fig, 2, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 2, 5, 1, 1)

        self.splitter_2.addWidget(self.groupBox_2)

        self.gridLayout_7.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.splitter.addWidget(self.frame)

        self.gridLayout_6.addWidget(self.splitter, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_5.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget.addTab(self.MC_Plot, "")
        self.MC_Corr = QWidget()
        self.MC_Corr.setObjectName(u"MC_Corr")
        self.gridLayout_9 = QGridLayout(self.MC_Corr)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox_3 = QGroupBox(self.MC_Corr)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_8 = QGridLayout(self.groupBox_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_8.addWidget(self.label_6, 0, 0, 1, 1)

        self.Corr_Impact = QComboBox(self.groupBox_3)
        self.Corr_Impact.setObjectName(u"Corr_Impact")
        self.Corr_Impact.setMinimumSize(QSize(400, 0))

        self.gridLayout_8.addWidget(self.Corr_Impact, 0, 1, 1, 1)

        self.Update_Corr_fig = QPushButton(self.groupBox_3)
        self.Update_Corr_fig.setObjectName(u"Update_Corr_fig")
        self.Update_Corr_fig.setIcon(icon1)

        self.gridLayout_8.addWidget(self.Update_Corr_fig, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(589, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.Corr_plot = QWidget(self.groupBox_3)
        self.Corr_plot.setObjectName(u"Corr_plot")

        self.gridLayout_8.addWidget(self.Corr_plot, 1, 0, 1, 4)


        self.gridLayout_9.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.MC_Corr, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(MC_Results)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MC_Results)
    # setupUi

    def retranslateUi(self, MC_Results):
        MC_Results.setWindowTitle(QCoreApplication.translate("MC_Results", u"Monte Carlo Results", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MC_Data), QCoreApplication.translate("MC_Results", u"Data", None))
        self.groupBox.setTitle(QCoreApplication.translate("MC_Results", u"Plot", None))
        self.label_3.setText(QCoreApplication.translate("MC_Results", u"Plot type", None))
        self.hexbin.setText(QCoreApplication.translate("MC_Results", u"hexbin", None))
        self.scatter.setText(QCoreApplication.translate("MC_Results", u"scatter", None))
        self.label.setText(QCoreApplication.translate("MC_Results", u"X axis", None))
        self.Update_plot.setText(QCoreApplication.translate("MC_Results", u"Update", None))
        self.label_2.setText(QCoreApplication.translate("MC_Results", u"Y axis", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MC_Results", u"Distribution", None))
        self.label_4.setText(QCoreApplication.translate("MC_Results", u"Plot type", None))
        self.label_5.setText(QCoreApplication.translate("MC_Results", u"Parameter", None))
        self.hist.setText(QCoreApplication.translate("MC_Results", u"hist", None))
        self.box.setText(QCoreApplication.translate("MC_Results", u"box", None))
        self.density.setText(QCoreApplication.translate("MC_Results", u"density", None))
        self.Update_dist_fig.setText(QCoreApplication.translate("MC_Results", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MC_Plot), QCoreApplication.translate("MC_Results", u"Plot", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MC_Results", u"Correlation plot", None))
        self.label_6.setText(QCoreApplication.translate("MC_Results", u"Impact", None))
        self.Update_Corr_fig.setText(QCoreApplication.translate("MC_Results", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MC_Corr), QCoreApplication.translate("MC_Results", u"Correlation", None))
    # retranslateUi

