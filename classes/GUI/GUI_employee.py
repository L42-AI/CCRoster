from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox)

class AddEmployee(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.employees = {}
        self.employee_names = []
        self.tasktypes = ['Allround']

        self.employee_list = QListWidget()
        self.employee_grid = QGridLayout()
        self.employee_name_input = QLineEdit()
        self.employee_wage_input = QLineEdit()
        self.employee_onboarding_input = QCheckBox()
        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)

        self.employee_wage = QVBoxLayout()
        self.employee_wage.addWidget(QLabel("Hourly Wage:"))
        self.employee_wage.addWidget(self.employee_wage_input)

        self.employee_onboarding = QVBoxLayout()
        self.employee_onboarding.addWidget(QLabel("Onboarding:"))
        self.employee_onboarding.addWidget(self.employee_onboarding_input)

        self.employee_extra_layout = QHBoxLayout()
        self.employee_extra_layout.addLayout(self.employee_wage)
        self.employee_extra_layout.addLayout(self.employee_onboarding)

        self.add_employee_layout = QVBoxLayout()
        self.add_employee_layout.addWidget(QLabel("Employee Name:"))
        self.add_employee_layout.addWidget(self.employee_name_input)
        self.add_employee_layout.addLayout(self.employee_extra_layout)
        self.add_employee_layout.addWidget(self.add_employee_button)

        self.add_employee_role_layout = QVBoxLayout()
        for role in self.tasktypes:
            self.add_employee_role_layout.addWidget(QCheckBox(role))

        self.total_employee_layout = QHBoxLayout()
        self.total_employee_layout.addLayout(self.add_employee_layout)
        self.total_employee_layout.addLayout(self.add_employee_role_layout)

        self.tab2_layout = QVBoxLayout(self)
        self.tab2_layout.addWidget(self.employee_list)
        self.tab2_layout.addLayout(self.employee_grid)
        self.tab2_layout.addLayout(self.total_employee_layout)

    def add_employee(self):
        name, wage, onboarding, roles = self.__get_employee_input_options()

        self.employees[name] = {'wage': wage, 'onboarding': onboarding, 'roles': roles}

        self.employee_list.addItem(f'{name, wage, onboarding, roles}')

        self.employee_name_input.clear()
        self.employee_wage_input.clear()

    def __get_employee_input_options(self) -> tuple:
        # Get start and end time inputs
        name = self.employee_name_input.text()
        wage = self.employee_wage_input.text()
        onboarding = self.employee_onboarding_input.isChecked()

        roles = []
        for role_widget_num in range(self.add_employee_role_layout.count()):
            role_widget = self.add_employee_role_layout.itemAt(role_widget_num).widget()
            role = role_widget.text()
            if role_widget.isChecked():
                roles.append(role)

        return name, wage, onboarding, roles
