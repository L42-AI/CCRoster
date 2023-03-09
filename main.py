from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QCheckBox, QListWidgetItem)
import re
import sys
# from classes.representation.controller import Controller
# from classes.representation.generator import Generator
# from classes.GUI.GUI_shiftsheet import ShiftSheetViewer
from classes.GUI.GUI_shiftsheet import ShiftSheet

if __name__ == "__main__":
    # generator = Generator()
    # controller = Controller(1)
    app = QApplication(sys.argv)
    window = ShiftSheet()
    window.show()
    # app = ShiftSheetViewer(controller)
    # app.show()
    sys.exit(app.exec())