import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QVBoxLayout, QHBoxLayout,
                               QStackedWidget, QWidget)

from classes.GUI.GUI_navigation import NavigationOptions

from classes.GUI.GUI_welcome import Welcome
from classes.GUI.GUI_shifts import Shifts
from classes.GUI.GUI_employee import AddEmployee
from classes.GUI.GUI_availability import Availability
from classes.GUI.GUI_team import EmployeeMatch
from classes.GUI.GUI_weight import Weight
from classes.GUI.GUI_settings import Settings

from classes.representation.controller import Controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consilium")
        self.setGeometry(100, 100, 875, 625)

        self.Com = Controller(1)

        self.shifts_button = NavigationOptions()
        self.shifts_button.clicked.connect(self.change_page)
        self.shifts_button.index = 1

        self.employee_button = NavigationOptions()
        self.employee_button.clicked.connect(self.change_page)
        self.employee_button.index = 2

        self.availability_button = NavigationOptions()
        self.availability_button.clicked.connect(self.change_page)
        self.availability_button.index = 3

        self.team_button = NavigationOptions()
        self.team_button.clicked.connect(self.change_page)
        self.team_button.index = 4

        self.weight_button = NavigationOptions()
        self.weight_button.clicked.connect(self.change_page)
        self.weight_button.index = 5

        self.settings_button = NavigationOptions()
        self.settings_button.clicked.connect(self.change_page)
        self.settings_button.index = 6


        self.navigation_bar = QVBoxLayout()
        self.navigation_bar.setSpacing(0)
        self.navigation_bar.setContentsMargins(0,0,0,0)

        self.navigation_bar.addWidget(self.shifts_button)
        self.navigation_bar.addWidget(self.employee_button)
        self.navigation_bar.addWidget(self.availability_button)
        self.navigation_bar.addWidget(self.team_button)
        self.navigation_bar.addWidget(self.weight_button)
        self.navigation_bar.addWidget(self.settings_button)

        self.welcome_widget = Welcome()
        self.shift_widget = Shifts(self.Com)
        self.employee_widget = AddEmployee(self.Com)
        self.availability_widget = Availability(self.Com)
        self.relation_widget = EmployeeMatch(self.Com)
        self.weight_widget = Weight()
        self.settings_widget = Settings()

        self.pages = QStackedWidget()
        self.pages.addWidget(self.welcome_widget)
        self.pages.addWidget(self.shift_widget)
        self.pages.addWidget(self.employee_widget)
        self.pages.addWidget(self.availability_widget)
        self.pages.addWidget(self.relation_widget)
        self.pages.addWidget(self.weight_widget)
        self.pages.addWidget(self.settings_widget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        layout.addLayout(self.navigation_bar)
        layout.addWidget(self.pages)

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

    def change_page(self) -> None:
        index = self.sender().index
        self.pages.setCurrentWidget(self.pages.widget(index))

        self.__communicate_server()

    def __communicate_server(self):
        """
        Function to upload all queries that are put in the queue and download all new info
        """
        pass
    def aboutToQuit(self):
        Controller.close = True

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = MainWindow()
    app.show()
    sys.exit(window.exec())
