from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox, QWidgetItem, QComboBox)

from classes.representation.controller import Controller


class AddEmployee(QWidget):
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con

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

        self.employee_task_layout = QVBoxLayout()
        for task in self.tasktypes:
            self.employee_task_layout.addWidget(QCheckBox(task))

        self.employee_info_layout = QGridLayout()
        self.employee_info_layout.addLayout(self.employee_onboarding,2,0,2,2)
        self.employee_info_layout.addLayout(self.employee_wage_layout,0,0,2,2)
        self.employee_info_layout.addLayout(self.employee_task_layout,0,2,4,2)

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
        first_name, last_name, wage, level, tasks = self.__get_employee_input_options()

        self.Controller.create_employee(first_name, last_name, wage, level, tasks)
        self.employee_list.addItem(f'{first_name, last_name, wage, level, tasks}')

        self.__clear_input_fields()

    def edit_employee(self, item: object) -> None:

        # Get timeslot
        name, wage, level, tasks = self.__get_info(item)

        # Find start and end times
        self.employee_first_name_input.setText(name)
        self.employee_last_name_input.setText(name)
        self.employee_wage_input.setText(wage)

        if level == True:
            self.employee_level_input.setChecked(True)

        for task in tasks:
            for checkbox_num in range(self.employee_task_layout.count()):
                checkbox = self.employee_task_layout.itemAt(checkbox_num).widget()
                if checkbox.text() == task:
                    checkbox.setChecked(True)

        # Enable buttons
        self.edit_employee_button.setEnabled(True)
        self.delete_employee_button.setEnabled(True)

    def edit_selected_employee(self) -> None:

        item = self.employee_list.currentItem()

        if item is not None:

            index = self.employee_list.row(item)

            old_name, _, _, _ = self.__get_info(item)

            new_first_name, new_last_name, wage, level, tasks = self.__get_employee_input_options()

            self.Controller.delete_employee(old_name, old_name)
            self.employee_list.takeItem(index)

            self.Controller.create_employee(new_first_name, new_last_name, wage, level, tasks)
            self.employee_list.addItem(f'{new_first_name, new_last_name, wage, level, tasks}')

            self.__clear_input_fields()


    def delete_selected_employee(self) -> None:
        # Get selected time slot
        item = self.employee_list.currentItem()

        if item is not None:

            index = self.employee_list.row(item)

            old_name, _, _, _ = self.__get_info(item)

            # Remove from list and widget
            self.Controller.delete_employee(old_name, old_name)
            self.employee_list.takeItem(index)

            # Disable buttons
            self.edit_employee_button.setEnabled(False)
            self.delete_employee_button.setEnabled(False)

            self.__clear_input_fields()

    def __clear_input_fields(self) -> None:

            self.employee_first_name_input.clear()
            self.employee_last_name_input.clear()
            self.employee_wage_input.clear()

            if self.employee_level_input.isChecked():
                self.employee_level_input.setChecked(False)

            for checkbox_num in range(self.employee_task_layout.count()):
                task_checkbox = self.employee_task_layout.itemAt(checkbox_num).widget()
                if task_checkbox.isChecked():
                    task_checkbox.setChecked(False)

    def __get_info(self, item: QWidgetItem) -> tuple:

        # Extract text of selected item
        selected_str = item.text()

        # Find timeslot
        info = selected_str.strip("(").strip(")").replace("'", '').replace(" ", '')
        name, wage, level, tasks = info.split(',')

        tasks = tasks[1:-1].split(", ")
        return name, wage, level, tasks

    def __get_employee_input_options(self) -> tuple:
        # Get start and end time inputs
        first_name = self.employee_first_name_input.text()
        last_name = self.employee_last_name_input.text()
        wage = self.employee_wage_input.text()
        level = self.employee_level_input.isChecked()

        tasks = []
        for task_widget_num in range(self.employee_task_layout.count()):
            task_widget = self.employee_task_layout.itemAt(task_widget_num).widget()
            task = task_widget.text()
            if task_widget.isChecked():
                tasks.append(task)

        return first_name, last_name, wage, level, tasks

    def save(self) -> None:
        [print(employee.get_name()) for employee in self.Controller.get_employee_list()]