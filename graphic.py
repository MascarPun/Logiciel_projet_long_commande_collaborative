

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
import numpy
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtGui

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):

    def __init__(self,t,s, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure(t,s)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_initial_figure(self):
        pass

    def actualisation_graph(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self,t,s, *args, **kwargs):
        MyMplCanvas.__init__(self,t,s, *args, **kwargs)
        self.compute_initial_figure(t,s)

    def compute_initial_figure(self,t,s):
        for i in range(len(s)):
            self.axes.plot(t, s[i])

    def actualisation_graph(self,t,s):
        self.axes.cla()
        for i in range(len(s)):
            self.axes.plot(t, s[i])

        self.draw()




class Ui_MainWindow(object):

    def __init__(self, s,t):
        #self.controleur = controleur
        self.s = s
        self.t = t

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

        self.sc = MyStaticMplCanvas(self.t, self.s, width=5, height=4, dpi=100)

        self.gridLayout.addWidget(self.sc, 0, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)





        self.pushButton.clicked.connect(lambda: self.update_bouton(self.sc, self.s, self.t))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox_pos.setText(_translate("MainWindow", "position"))
        self.checkBox_vit.setText(_translate("MainWindow", "vitesse"))
        self.checkBox_cour.setText(_translate("MainWindow", "intensité"))
        self.pushButton.setText(_translate("MainWindow", "plot"))

    def update_bouton(self, graph, s, t):
        if (self.checkBox_pos.isChecked() == True and self.checkBox_vit.isChecked() == True and self.checkBox_cour.isChecked() ==True):
            s = numpy.array([s[0], s[1], s[2]])
            graph.actualisation_graph(t,s)
            self.sc.actualisation_graph(t, s)
        elif (self.checkBox_pos.isChecked()==True and self.checkBox_vit.isChecked()==True and self.checkBox_cour.isChecked()==False):
            s = numpy.array([s[0], s[1]])
            graph.actualisation_graph(t,s)
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==True and self.checkBox_vit.isChecked()==False and self.checkBox_cour.isChecked()==True):
            s = numpy.array([s[0], s[2]])
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==True and self.checkBox_vit.isChecked()==False and self.checkBox_cour.isChecked()==False):
            s = numpy.array([s[0]])
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==False and self.checkBox_vit.isChecked()==True and self.checkBox_cour.isChecked()==True):
            s = numpy.array([s[1], s[2]])
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==False and self.checkBox_vit.isChecked()==True and self.checkBox_cour.isChecked()==False):
            s = numpy.array([s[1]])
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==False and self.checkBox_vit.isChecked()==False and self.checkBox_cour.isChecked()==True):
            s = numpy.array([s[2]])
            self.sc.actualisation_graph(t,s)
        elif (self.checkBox_pos.isChecked()==False and self.checkBox_vit.isChecked()==False and self.checkBox_cour.isChecked()==False):
            s = numpy.array([])
            self.sc.actualisation_graph(t,s)

    def launch(self,t,s):
        if __name__ == "__main__":
            import sys
            app = QtWidgets.QApplication(sys.argv)
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow(s, t)
            ui.setupUi(MainWindow)
            MainWindow.show()
            sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    t = arange(0.0, 3.0, 0.01)
    s = numpy.array([2*sin(2 * pi * t), 3*sin(2 * pi * t + 0.2), 4*sin(2 * pi * t + 0.4)])
    ui = Ui_MainWindow(s,t)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


