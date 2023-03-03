from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox, QWidgetItem)

from classes.representation.controller import Communicator


class AddEmployee(QWidget):
    def __init__(self, Com, parent=None) -> None:
        super().__init__(parent)

        self.Com: Communicator = Com

        self.employees = {}
        self.employee_names = []
        self.tasktypes = ['Allround']

        self.employee_list = QListWidget()
        self.employee_list.itemDoubleClicked.connect(self.edit_employee)

        self.employee_grid = QGridLayout()
        self.employee_name_input = QLineEdit()
        self.employee_wage_input = QLineEdit()
        self.employee_onboarding_input = QCheckBox()


        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)

        self.edit_employee_button = QPushButton("Edit Employee Slot")
        self.edit_employee_button.clicked.connect(self.edit_selected_employee)
        self.edit_employee_button.setEnabled(False)

        self.delete_employee_button = QPushButton("Delete Employee Slot")
        self.delete_employee_button.clicked.connect(self.delete_selected_employee)
        self.delete_employee_button.setEnabled(False)

        self.employee_wage = QVBoxLayout()
        self.employee_wage.addWidget(QLabel("Hourly Wage:"))
        self.employee_wage.addWidget(self.employee_wage_input)

        self.employee_onboarding = QVBoxLayout()
        self.employee_onboarding.addWidget(QLabel("Onboarding:"))
        self.employee_onboarding.addWidget(self.employee_onboarding_input)

        self.employee_extra_layout = QHBoxLayout()
        self.employee_extra_layout.addLayout(self.employee_wage)
        self.employee_extra_layout.addLayout(self.employee_onboarding)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_employee_button)
        button_layout.addWidget(self.edit_employee_button)
        button_layout.addWidget(self.delete_employee_button)

        self.add_employee_layout = QVBoxLayout()
        self.add_employee_layout.addWidget(QLabel("Employee Name:"))
        self.add_employee_layout.addWidget(self.employee_name_input)
        self.add_employee_layout.addLayout(self.employee_extra_layout)
        self.add_employee_layout.addLayout(button_layout)

        self.add_employee_role_layout = QVBoxLayout()
        for role in self.tasktypes:
            self.add_employee_role_layout.addWidget(QCheckBox(role))

        self.total_employee_layout = QHBoxLayout()
        self.total_employee_layout.addLayout(self.add_employee_layout)
        self.total_employee_layout.addLayout(self.add_employee_role_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.employee_list)
        layout.addLayout(self.employee_grid)
        layout.addLayout(self.total_employee_layout)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)

    def add_employee(self):
        name, wage, onboarding, roles = self.__get_employee_input_options()

        self.employees[name] = {'wage': wage, 'onboarding': onboarding, 'roles': roles}

        self.employee_list.addItem(f'{name, wage, onboarding, roles}')

        self.__clear_input_fields()

    def edit_employee(self, item: object) -> None:

        # Get timeslot
        name, wage, onboarding, roles = self.__get_info(item)

        # Find start and end times
        self.employee_name_input.setText(name)
        self.employee_wage_input.setText(wage)

        if onboarding == True:
            self.employee_onboarding_input.setChecked(True)

        for role in roles:
            for checkbox_num in range(self.add_employee_role_layout.count()):
                checkbox = self.add_employee_role_layout.itemAt(checkbox_num).widget()
                if checkbox.text() == role:
                    checkbox.setChecked(True)

        # Enable buttons
        self.edit_employee_button.setEnabled(True)
        self.delete_employee_button.setEnabled(True)

    def edit_selected_employee(self) -> None:

        item = self.employee_list.currentItem()

        if item is not None:

            index = self.employee_list.row(item)

            old_name, _, _, _ = self.__get_info(item)

            new_name, wage, onboarding, roles = self.__get_employee_input_options()

            del self.employees[old_name]
            self.employees[new_name] = {'wage': wage, 'onboarding': onboarding, 'roles': roles}

            self.employee_list.takeItem(index)
            self.employee_list.addItem(f'{new_name, wage, onboarding, roles}')

            self.__clear_input_fields()


    def delete_selected_employee(self) -> None:
        # Get selected time slot
        item = self.employee_list.currentItem()

        if item is not None:

            index = self.employee_list.row(item)

            old_name, _, _, _ = self.__get_info(item)

            # Remove from list and widget
            del self.employees[old_name]
            self.employee_list.takeItem(index)

            # Disable buttons
            self.edit_employee_button.setEnabled(False)
            self.delete_employee_button.setEnabled(False)

            self.__clear_input_fields()

    def __clear_input_fields(self) -> None:

            self.employee_name_input.clear()
            self.employee_wage_input.clear()

            if self.employee_onboarding_input.isChecked():
                self.employee_onboarding_input.setChecked(False)

            for checkbox_num in range(self.add_employee_role_layout.count()):
                checkbox = self.add_employee_role_layout.itemAt(checkbox_num).widget()
                if checkbox.isChecked():
                    checkbox.setChecked(False)

    def __get_info(self, item: QWidgetItem) -> tuple:

        # Extract text of selected item
        selected_str = item.text()

        # Find timeslot
        info = selected_str.strip("(").strip(")").replace("'", '').replace(" ", '')
        name, wage, onboarding, roles = info.split(',')

        roles = roles[1:-1].split(", ")
        return name, wage, onboarding, roles

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

    def save(self) -> None:
        print(self.employees)