from classes.GUI.GUI import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from classes.representation.generator import Generator

if __name__ == "__main__":
    # Generator()
    window = QApplication(sys.argv)
    app = MainWindow()
    app.show()
    sys.exit(window.exec())
