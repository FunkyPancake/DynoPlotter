import logging

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QFileDialog

from LogParser import LogParser
from SignalProcessor import SignalProcessor
from ui_mainwindow import Ui_MainWindow


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, ax1 = plt.subplots()
        plt.grid(visible=True, which='both')
        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax1.twinx()
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def add_plot(self, x, y):
        self.plots.append((x, y))


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.sc = None
        self.is_opened = False
        self.logger = logger
        self.log_parser = LogParser(logger)

        self.m_ui = Ui_MainWindow()
        self.m_ui.setupUi(self)
        menubar = self.menuBar()

        self.open_action = QAction("&Open", self)
        self.open_action.triggered.connect(self.open_handler)
        menubar.addAction(self.open_action)

        self.save_action = QAction("&Save", self)
        self.save_action.triggered.connect(self.save_handler)
        menubar.addAction(self.save_action)

        self.select_action = QAction("&Select", self)
        self.select_action.triggered.connect(self.select_handler)
        menubar.addAction(self.select_action)

        self.select_action.setEnabled(False)
        self.save_action.setEnabled(False)

    def select_handler(self):
        pass

    def open_handler(self):
        QFileDialog.getOpenFileName(self)
        self.log_parser.parse('./log.csv')
        self.select_action.setEnabled(True)
        self.save_action.setEnabled(True)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        sp = SignalProcessor(self.logger, self.log_parser)
        x_axis = self.log_parser.get_data('STAT_MOTORDREHZAHL_WERT')
        y_axis = self.log_parser.get_data('STAT_MOTORMOMENT_AKTUELL_WERT')
        self.sc.ax1.plot(x_axis, y_axis, 'g-')
        self.sc.ax2.plot(x_axis, sp.calc_power(), 'r-')
        self.sc.ax1.set_xlabel('RPM')
        self.sc.ax1.set_ylabel('Torque [Nm]', color='g')
        self.sc.ax2.set_ylabel('Power [kW]', color='r')

        self.setCentralWidget(self.sc)

        # self.m_ui.widget = sc

    def save_handler(self):
        print(self.log_parser.headers)
        filename = 'plot.png'
        filename, selected_filter = QFileDialog.getSaveFileName(self, 'Save',filename, filter='PNG Files (*.png)')
        if not filename.endswith('.png'):
            filename = filename + '.png'
        self.sc.fig.savefig(filename)
        # self.m_ui.widget = sc

#
# x = LogParser(logger,'./log.csv')
# x.parse()
