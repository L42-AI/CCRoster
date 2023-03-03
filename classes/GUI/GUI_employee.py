from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox, QWidgetItem, QComboBox)

from classes.representation.controller import Controller


class AddEmployee(QWidget):
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con

        self.employees = {}
        self.employee_names = []
        self.tasktypes = ['Allround']
        self.levels = ['Stagair', 'Manager', 'Lead']

        self.employee_list = QListWidget()
        self.employee_list.itemDoubleClicked.connect(self.edit_employee)

        self.employee_first_name_input = QLineEdit()
        self.employee_last_name_input = QLineEdit()

        self.employee_name_layout = QVBoxLayout()
        self.employee_name_layout.addWidget(QLabel("First Name:"))
        self.employee_name_layout.addWidget(self.employee_first_name_input)
        self.employee_name_layout.addWidget(QLabel("Last Name:"))
        self.employee_name_layout.addWidget(self.employee_last_name_input)


        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)

        self.edit_employee_button = QPushButton("Edit Employee Slot")
        self.edit_employee_button.clicked.connect(self.edit_selected_employee)
        self.edit_employee_button.setEnabled(False)

        self.delete_employee_button = QPushButton("Delete Employee Slot")
        self.delete_employee_button.clicked.connect(self.delete_selected_employee)
        self.delete_employee_button.setEnabled(False)


        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_employee_button)
        button_layout.addWidget(self.edit_employee_button)
        button_layout.addWidget(self.delete_employee_button)


        self.employee_wage_input = QLineEdit()
        self.employee_wage_input.setFixedWidth(50)

        self.employee_wage_layout = QHBoxLayout()
        self.employee_wage_layout.addWidget(QLabel("Hourly Wage:"))
        self.employee_wage_layout.addWidget(self.employee_wage_input)

        self.employee_level_input = QComboBox()
        [self.employee_level_input.addItem(level) for level in self.levels]

        self.employee_onboarding = QVBoxLayout()
        self.employee_onboarding.addWidget(QLabel("Level:"))
        self.employee_onboarding.addWidget(self.employee_level_input)

        self.employee_role_layout = QVBoxLayout()
        for role in self.tasktypes:
            self.employee_role_layout.addWidget(QCheckBox(role))

        self.employee_info_layout = QGridLayout()
        self.employee_info_layout.addLayout(self.employee_onboarding,2,0,2,2)
        self.employee_info_layout.addLayout(self.employee_wage_layout,0,0,2,2)
        self.employee_info_layout.addLayout(self.employee_role_layout,0,2,4,2)


        self.employee_layout = QHBoxLayout()
        self.employee_layout.addLayout(self.employee_name_layout)
        self.employee_layout.addLayout(self.employee_info_layout)

        self.add_employee_layout = QVBoxLayout()
        self.add_employee_layout.addLayout(self.employee_layout)
        self.add_employee_layout.addLayout(button_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.employee_list)
        layout.addLayout(self.add_employee_layout)
        layout.addLayout(self.employee_layout)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)

    def add_employee(self):
        name, wage, onboarding, roles = self.__get_employee_input_options()

        self.Controller.create_employee(name, name, wage, onboarding, roles)
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
            for checkbox_num in range(self.employee_role_layout.count()):
                checkbox = self.employee_role_layout.itemAt(checkbox_num).widget()
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

            self.Controller.delete_employee(old_name, old_name)
            del self.employees[old_name]
            self.employee_list.takeItem(index)

            self.Controller.create_employee(new_name, new_name, wage, onboarding, roles)
            self.employees[new_name] = {'wage': wage, 'onboarding': onboarding, 'roles': roles}
            self.employee_list.addItem(f'{new_name, wage, onboarding, roles}')

            self.__clear_input_fields()


    def delete_selected_employee(self) -> None:
        # Get selected time slot
        item = self.employee_list.currentItem()

        if item is not None:

            index = self.employee_list.row(item)

            old_name, _, _, _ = self.__get_info(item)

            # Remove from list and widget
            self.Controller.delete_employee(old_name, old_name)
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

            for checkbox_num in range(self.employee_role_layout.count()):
                checkbox = self.employee_role_layout.itemAt(checkbox_num).widget()
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
        for role_widget_num in range(self.employee_role_layout.count()):
            role_widget = self.employee_role_layout.itemAt(role_widget_num).widget()
            role = role_widget.text()
            if role_widget.isChecked():
                roles.append(role)

        return name, wage, onboarding, roles

    def save(self) -> None:
        print(self.employees)