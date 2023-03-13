from classes.GUI.GUI import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = MainWindow()
    app.show()
    sys.exit(window.exec())
