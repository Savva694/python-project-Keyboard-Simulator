import sys

from PyQt5.QtWidgets import QApplication

from src.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
