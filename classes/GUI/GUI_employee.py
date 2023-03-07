from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox, QListWidgetItem, QComboBox)

from classes.representation.controller import Controller


class AddEmployee(QWidget):
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con

        self.tasktypes = {'Allround': 1}
        self.levels = {'Stagair': 0, 'Manager': 1, 'Lead':2}

        self.employee_list = QListWidget()
        self.employee_list.itemDoubleClicked.connect(self.edit_employee)
        self.init_employees_display()

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
        [self.employee_level_input.addItem(level) for level in self.levels.keys()]

        self.employee_level_layout = QVBoxLayout()
        self.employee_level_layout.addWidget(QLabel("Level:"))
        self.employee_level_layout.addWidget(self.employee_level_input)

        self.employee_task_layout = QVBoxLayout()
        for task in self.tasktypes.keys():
            self.employee_task_layout.addWidget(QCheckBox(task))

        self.employee_info_layout = QGridLayout()
        self.employee_info_layout.addLayout(self.employee_level_layout,2,0,2,2)
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

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)

    def init_employees_display(self):
        employees = self.Controller.employees_input()
        self.employee_list.addItems(employees)

    def add_employee(self):
        fields = self.__get_input_fields()
        self.Controller.create_employee(*fields)
        self.employee_list.addItem(str(fields))
        self.__clear_input_fields()

    def edit_employee(self, item: QListWidgetItem) -> None:
        fields = self.__get_list_item_info(item)
        self.employee_first_name_input.setText(fields[0])
        self.employee_last_name_input.setText(fields[1])
        self.employee_wage_input.setText(fields[2])
        self.employee_level_input.setCurrentText(fields[3])
        for task in fields[4]:
            checkboxes = [c for c in self.employee_task_layout.children()[1:] if c.text() == task]
            if checkboxes:
                checkboxes[0].setChecked(True)
        self.edit_employee_button.setEnabled(True)
        self.delete_employee_button.setEnabled(True)

    def edit_selected_employee(self) -> None:
        item = self.employee_list.currentItem()
        if item is not None:
            index = self.employee_list.row(item)
            old_fields = self.__get_list_item_info(item)
            new_fields = self.__get_input_fields()
            self.Controller.delete_employee(*old_fields[:2])
            self.employee_list.takeItem(index)
            self.Controller.create_employee(*new_fields)
            self.employee_list.addItem(str(new_fields))
            self.__clear_input_fields()

    def delete_selected_employee(self) -> None:
        item = self.employee_list.currentItem()
        if item is not None:
            index = self.employee_list.row(item)
            fields = self.__get_list_item_info(item)
            self.Controller.delete_employee(*fields[:2])
            self.employee_list.takeItem(index)
            self.edit_employee_button.setEnabled(False)
            self.delete_employee_button.setEnabled(False)
            self.__clear_input_fields()

    def __clear_input_fields(self) -> None:
        """ Clear all input fields """
        self.employee_first_name_input.clear()
        self.employee_last_name_input.clear()
        self.employee_wage_input.clear()

        for checkbox_num in range(self.employee_task_layout.count()):
            task_checkbox: QCheckBox = self.employee_task_layout.itemAt(checkbox_num).widget()
            if task_checkbox.isChecked():
                task_checkbox.setChecked(False)

    def __get_list_item_info(self, item: QListWidgetItem) -> tuple:
        """ Retrieve the info of the selected list item """
        # Extract text of selected item
        selected_str = item.text()

        # Find timeslot
        info = selected_str[1:-1].replace("'", '').replace(" ", '')
        first_name, last_name, wage, level, tasks = info.split(',')
        tasks = tasks[1:-1].split(", ")

        return first_name, last_name, wage, level, tasks

    def __get_input_fields(self) -> tuple:
        """ Get input fields """
        # Get start and end time inputs
        first_name = self.employee_first_name_input.text()
        last_name = self.employee_last_name_input.text()
        wage = self.employee_wage_input.text()
        level = self.levels[self.employee_level_input.currentText()]

        tasks = []
        for task_widget_num in range(self.employee_task_layout.count()):
            task_widget: QCheckBox = self.employee_task_layout.itemAt(task_widget_num).widget()
            task = task_widget.text()
            if task_widget.isChecked():
                tasks.append(self.tasktypes[task])

        return first_name, last_name, wage, level, tasks

    def save(self) -> None:
        [print(employee.name) for employee in self.Controller.get_employee_list()]