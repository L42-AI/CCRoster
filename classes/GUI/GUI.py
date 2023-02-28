from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget)
import sys

from classes.GUI.GUI_team import EmployeeMatch
from classes.GUI.GUI_shifts import Shifts
from classes.GUI.GUI_employee import AddEmployee
from classes.GUI.GUI_availability import Availability


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Scheduling")
        self.setGeometry(100, 100, 875, 625)

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(Shifts(), "Dienst Uren")

        self.tabs.addTab(AddEmployee(), "Werknemers")

        self.tabs.addTab(Availability(), "Beschikbaarheid")

        self.tabs.addTab(EmployeeMatch(), 'Teamwork')

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = MainWindow()
    app.show()
    sys.exit(window.exec())
