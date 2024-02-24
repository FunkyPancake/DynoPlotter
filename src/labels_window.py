from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView


class LabelsWindow(QWidget):
    def __init__(self, parser, item_changed_event, labels: dict):
        super(LabelsWindow, self).__init__()
        layout = QVBoxLayout(self)
        list_view = QListView()
        self.model = QStandardItemModel()
        for name in parser.headers:
            if name in labels.values():
                continue
            item = QStandardItem(name)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)
        list_view.setModel(self.model)
        layout.addWidget(list_view)
        self.model.itemChanged.connect(item_changed_event)
        self.setLayout(layout)
