import logging
import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    app.exec()
