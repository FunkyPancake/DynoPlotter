import logging
import os.path

from PySide6 import QtGui
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog

from src.custom_plot import CustomPlot
from src.labels_window import LabelsWindow
from src.parser import LogParser
from src.signal_processor import SignalProcessor
from src.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.labels = {}
        self.ow = None
        self.sc = None
        self.is_opened = False
        self.logger = logger
        self.parser = LogParser(logger)
        self.sc = CustomPlot()
        self.load_settings()
        self.signal_processor = SignalProcessor(logger, self.parser, self.labels)

        self.m_ui = Ui_MainWindow()
        self.m_ui.setupUi(self)
        icon_paht = os.path.abspath('static/img/favicon.ico')
        self.setWindowIcon(QtGui.QIcon(icon_paht))

        menubar = self.menuBar()

        self.open_action = QAction("&Open", self)
        self.open_action.triggered.connect(self.open_handler)
        menubar.addAction(self.open_action)

        self.save_action = QAction("&Save", self)
        self.save_action.triggered.connect(self.save_handler)
        menubar.addAction(self.save_action)

        self.select_action = QAction("&Select", self)
        self.select_action.triggered.connect(self.on_select_clicked)
        menubar.addAction(self.select_action)

        self.select_action.setEnabled(False)
        self.save_action.setEnabled(False)

    def closeEvent(self, event):
        if self.ow is not None:
            self.ow.close()
        self.save_settings()
        self.close()

    def on_select_clicked(self):
        self.ow = LabelsWindow(self.parser, self.on_item_changed, self.labels)
        self.ow.show()
        self.logger.debug('Select items button clicked.')

    def on_item_changed(self, item: QStandardItem):
        name = item.text()
        if item.checkState() == Qt.Checked:
            x, y = self.signal_processor.process_signal(name)
            self.sc.add_plot(name, x, y)
        else:
            self.sc.delete_plot(name)
        self.logger.debug(item.text())

    def open_handler(self):
        self.logger.debug('Open file button clicked.')

        filename, selected_filter = QFileDialog.getOpenFileName(self)
        if not (filename is None or filename == ""):
            try:
                self.parser.parse(filename)
            except ValueError as e:
                self.logger.error(e)
                return
            self.select_action.setEnabled(True)
            self.save_action.setEnabled(True)

            self.logger.debug(f'{filename} opened successfully.')
            rpm, torque, power = self.signal_processor.process_base()
            self.sc.add_base_plots(rpm, torque, power)
            self.sc.ax1.set_xticks(self.signal_processor.get_rpm_time_ticks(), minor=True)
            self.sc.ax1.xaxis.grid(True, which='minor', linestyle='--', color='g')
            self.setCentralWidget(self.sc)

    def save_handler(self):
        filename = '../plot.png'
        filename, selected_filter = QFileDialog.getSaveFileName(self, 'Save', filename, filter='PNG Files (*.png)')
        if filename != "":
            self.sc.fig.savefig(filename)
            self.logger.debug(f'Save plot to {filename}.')
        else:
            self.logger.debug('Saving of the file aborted.')

    def load_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        self.labels['time'] = settings.value('time', 'time')
        self.labels['torque'] = settings.value('torque', 'STAT_MOTORMOMENT_AKTUELL_WERT')
        self.labels['rpm'] = settings.value('rpm', 'STAT_MOTORDREHZAHL_WERT')
        self.labels['filter'] = settings.value('filter', '0.65')
        self.logger.setLevel(settings.value('LogLevel', 'INFO'))

    def save_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        settings.setValue('time', self.labels['time'])
        settings.setValue('torque', self.labels['torque'])
        settings.setValue('rpm', self.labels['rpm'])
        settings.setValue('filter', self.labels['filter'])
