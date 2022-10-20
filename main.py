from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from actions.archiver import Request

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

class TrainingModel(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("./gui/main.ui", self)
        self.setWindowTitle("Data Analyzer")
        self.trainButton.clicked.connect(self.request)

        self.x = []
        self.y = []

    def request(self):
        pv = self.processVariable.text()
        ini = self.iniDatetime.dateTime().toPyDateTime()
        end = self.endDatetime.dateTime().toPyDateTime()

        data = Request([pv], ini, end, 1)
        self.x = data.result[pv]["datetimes"]
        self.y = data.result[pv]["values"]

        self.plot()

    def plot(self):
        self.fig = plt.figure(figsize=(8, 6))
        ax = self.fig.add_subplot(211)
        ax.plot(self.x, self.y, '-')
        ax.set_title('Press left mouse button and drag to test')
        self.ax2 = self.fig.add_subplot(212)
        self.line2, = self.ax2.plot(self.x, self.y, '-')

        def onselect(xmin, xmax):
            print("oi")
            indmin, indmax = np.searchsorted(self.x, (xmin, xmax))
            indmax = min(len(self.x) - 1, indmax)

            thisx = self.x[indmin:indmax]
            thisy = self.y[indmin:indmax]
            self.line2.set_data(thisx, thisy)
            self.ax2.set_xlim(thisx[0], thisx[-1])
            self.ax2.set_ylim(thisy.min(), thisy.max())
            self.fig.canvas.draw_idle()
            
            # save
            np.savetxt("text.out", np.c_[thisx, thisy])

        span = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))
        plt.show()


app = QApplication([])
window = TrainingModel()
window.show()
app.exec_()