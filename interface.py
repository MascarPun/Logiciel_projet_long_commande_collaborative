# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 571))
        self.tabWidget.setObjectName("tabWidget")
        self.positionTab = QtWidgets.QWidget()
        self.positionTab.setObjectName("positionTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.positionTab)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.runPos = QtWidgets.QPushButton(self.positionTab)
        self.runPos.setObjectName("runPos")
        self.gridLayout_2.addWidget(self.runPos, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.positionTab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tabWidget.addTab(self.positionTab, "")
        self.vitesseTab = QtWidgets.QWidget()
        self.vitesseTab.setObjectName("vitesseTab")
        self.tabWidget.addTab(self.vitesseTab, "")
        self.courantTab = QtWidgets.QWidget()
        self.courantTab.setObjectName("courantTab")
        self.tabWidget.addTab(self.courantTab, "")
        self.collaboTab = QtWidgets.QWidget()
        self.collaboTab.setObjectName("collaboTab")
        self.tabWidget.addTab(self.collaboTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        self.menuAffichage = QtWidgets.QMenu(self.menubar)
        self.menuAffichage.setObjectName("menuAffichage")
        self.menuAide = QtWidgets.QMenu(self.menubar)
        self.menuAide.setObjectName("menuAide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        self.menubar.addAction(self.menuAffichage.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.runPos.clicked.connect(self.test)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.runPos.setText(_translate("MainWindow", "run"))
        self.label.setText(_translate("MainWindow", "lancer le programme"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.positionTab), _translate("MainWindow", "position"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vitesseTab), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.courantTab), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.collaboTab), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "fichier"))
        self.menuOption.setTitle(_translate("MainWindow", "option"))
        self.menuAffichage.setTitle(_translate("MainWindow", "affichage"))
        self.menuAide.setTitle(_translate("MainWindow", "aide"))



    def test(self):
        self.runpos.setObjectName("test")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

