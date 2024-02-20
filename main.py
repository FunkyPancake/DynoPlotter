import logging
import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='app.log', encoding='utf-8')
    formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s)",
                                  datefmt="%d/%b/%Y %H:%M:%S", )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    app.exec()
