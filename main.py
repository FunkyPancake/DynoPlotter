import logging
import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
        stream=sys.stdout)
    logger.setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    app.exec()
