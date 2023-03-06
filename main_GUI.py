from classes.GUI.GUI import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from classes.representation.generator import Generator
from classes.representation.controller import Controller
if __name__ == "__main__":
    generator = Generator()
    controller = Controller(generator)
    window = QApplication(sys.argv)
    app = MainWindow()
    app.show()
    sys.exit(window.exec())
