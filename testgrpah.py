

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_pos = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_pos.setObjectName("checkBox_pos")
        self.gridLayout.addWidget(self.checkBox_pos, 1, 0, 1, 1)
        self.checkBox_vit = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_vit.setObjectName("checkBox_vit")
        self.gridLayout.addWidget(self.checkBox_vit, 1, 1, 1, 1)
        self.checkBox_cour = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_cour.setObjectName("checkBox_cour")
        self.gridLayout.addWidget(self.checkBox_cour, 1, 2, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox_pos.setText(_translate("MainWindow", "position"))
        self.checkBox_vit.setText(_translate("MainWindow", "vitesse"))
        self.checkBox_cour.setText(_translate("MainWindow", "intensité"))
        self.pushButton.setText(_translate("MainWindow", "plot"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

