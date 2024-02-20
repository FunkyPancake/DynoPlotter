import logging

from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QWidget, QListView, QCheckBox, QVBoxLayout
from PySide6.QtCore import Qt
from matplotlib.widgets import Cursor

from CustomPlot import CustomPlot
from LogParser import LogParser
from SignalProcessor import SignalProcessor
from ui_mainwindow import Ui_MainWindow


class OtherWindow(QWidget):
    def __init__(self, parser, item_changed_event):
        super(OtherWindow, self).__init__()

        layout = QVBoxLayout(self)
        list_view = QListView()
        self.model = QStandardItemModel()
        for name in parser.headers:
            item = QStandardItem(name)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)
        list_view.setModel(self.model)
        layout.addWidget(list_view)
        self.model.itemChanged.connect(item_changed_event)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    X_NAME = 'STAT_MOTORDREHZAHL_WERT'

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.ow = None
        self.sc = None
        self.is_opened = False
        self.logger = logger
        self.log_parser = LogParser(logger)
        self.sc = CustomPlot()

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
        self.select_action.triggered.connect(self.on_select_clicked)
        menubar.addAction(self.select_action)

        self.select_action.setEnabled(False)
        self.save_action.setEnabled(False)

    def closeEvent(self, event):
        if self.ow is not None:
            self.ow.close()
        self.close()

    def on_select_clicked(self):
        self.ow = OtherWindow(self.log_parser, self.on_item_changed)
        self.ow.show()
        self.logger.debug('Select items button clicked.')

    def on_item_changed(self, item: QStandardItem):
        name = item.text()
        if item.checkState() == Qt.Checked:
            x_axis = self.log_parser.get_data(self.X_NAME)
            y_axis = self.log_parser.get_data(name)
            self.sc.add_plot(name, x_axis, y_axis)
        else:
            self.sc.delete_plot(name)
        self.logger.debug(item.text())

    def open_handler(self):
        self.logger.debug('Open file button clicked.')

        filename, selected_filter = QFileDialog.getOpenFileName(self)
        if filename is not None:
            try:
                self.log_parser.parse(filename)
            except ValueError as e:
                self.logger.error(e)
                return
            self.select_action.setEnabled(True)
            self.save_action.setEnabled(True)

            self.logger.debug(f'{filename} opened successfully.')

            sp = SignalProcessor(self.logger, self.log_parser)
            x_axis = self.log_parser.get_data(self.X_NAME)
            y_axis = self.log_parser.get_data('STAT_MOTORMOMENT_AKTUELL_WERT')
            self.sc.add_base_plots(x_axis, y_axis,  sp.calc_power())

            self.setCentralWidget(self.sc)

    def save_handler(self):
        filename = 'plot.png'
        filename, selected_filter = QFileDialog.getSaveFileName(self, 'Save', filename, filter='PNG Files (*.png)')
        if filename != "":
            self.sc.fig.savefig(filename)
            self.logger.debug(f'Save plot to {filename}.')
        else:
            self.logger.debug('Saving of the file aborted.')
