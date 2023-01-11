# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transcriberTool_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QComboBox, QCommandLinkButton, QHBoxLayout,
                               QLabel, QLayout, QLineEdit,
                               QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
                               QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(714, 464)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 10, 679, 433))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.wavLineEdit = QLineEdit(self.widget)
        self.wavLineEdit.setObjectName(u"wavLineEdit")

        self.horizontalLayout.addWidget(self.wavLineEdit)

        self.wavBrowser = QPushButton(self.widget)
        self.wavBrowser.setObjectName(u"wavBrowser")

        self.horizontalLayout.addWidget(self.wavBrowser)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.modelComboBox = QComboBox(self.widget)
        self.modelComboBox.setObjectName(u"modelComboBox")

        self.verticalLayout_3.addWidget(self.modelComboBox)

        self.downloadLinkButton = QCommandLinkButton(self.widget)
        self.downloadLinkButton.setObjectName(u"downloadLinkButton")

        self.verticalLayout_3.addWidget(self.downloadLinkButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.transcriberButton = QPushButton(self.widget)
        self.transcriberButton.setObjectName(u"transcriberButton")

        self.verticalLayout_3.addWidget(self.transcriberButton)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.outputBrowser = QTextBrowser(self.widget)
        self.outputBrowser.setObjectName(u"outputBrowser")

        self.verticalLayout_3.addWidget(self.outputBrowser)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Wav path:", None))
        self.wavBrowser.setText(QCoreApplication.translate("MainWindow", u"Browser...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        # if QT_CONFIG(tooltip)
        self.downloadLinkButton.setToolTip(QCoreApplication.translate("MainWindow",
                                                                      u"You can download the corresponding model you need\uff0cthen put them in the specified path",
                                                                      None))
        # endif // QT_CONFIG(tooltip)
        self.downloadLinkButton.setText(QCoreApplication.translate("MainWindow", u"Download More Model...", None))
        self.transcriberButton.setText(QCoreApplication.translate("MainWindow", u"Transcriber", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Output:", None))
    # retranslateUi
