from classes.GUI.GUI import MainWindow
from PySide2.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    window = QApplication()
    app = MainWindow()
    app.show()
    sys.exit(window.exec_())