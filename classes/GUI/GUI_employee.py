from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget,
                               QCheckBox, QListWidgetItem, QComboBox)

from classes.representation.controller import Controller


class AddEmployee(QWidget):
    update_signal = Signal()
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con

        """ Call in init for now """
        self.update_tasks()

        """ Call in init for now """
        self.update_levels()

        self.init_UI()

    """ Init """

    def init_UI(self) -> None:

        """ Employee Widget """

        self.employee_list = QListWidget()
        self.employee_list.itemDoubleClicked.connect(self.edit_employee)
        self.update_employees_display()

        """ Time input widgets """

        self.employee_first_name_input = QLineEdit()
        self.employee_last_name_input = QLineEdit()

        employee_name_layout = QVBoxLayout()
        employee_name_layout.addWidget(QLabel("First Name:"))
        employee_name_layout.addWidget(self.employee_first_name_input)
        employee_name_layout.addWidget(QLabel("Last Name:"))
        employee_name_layout.addWidget(self.employee_last_name_input)

        """ Interact buttons """

        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)

        self.edit_employee_button = QPushButton("Edit Employee Slot")
        self.edit_employee_button.clicked.connect(self.edit_selected_employee)
        self.edit_employee_button.setEnabled(False)

        self.delete_employee_button = QPushButton("Delete Employee Slot")
        self.delete_employee_button.clicked.connect(self.delete_selected_employee)
        self.delete_employee_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_employee_button)
        button_layout.addWidget(self.edit_employee_button)
        button_layout.addWidget(self.delete_employee_button)

        """ Wage input """

        self.employee_wage_input = QLineEdit()
        self.employee_wage_input.setFixedWidth(50)

        employee_wage_layout = QHBoxLayout()
        employee_wage_layout.addWidget(QLabel("Hourly Wage:"))
        employee_wage_layout.addWidget(self.employee_wage_input)

        """ Level Input """

        self.employee_level_input = QComboBox()
        self.update_level()

        employee_level_layout = QVBoxLayout()
        employee_level_layout.addWidget(QLabel("Level:"))
        employee_level_layout.addWidget(self.employee_level_input)

        """ Task """

        self.employee_task_layout = QVBoxLayout()
        self.update_task_layout()

        employee_info_layout = QGridLayout()
        employee_info_layout.addLayout(employee_level_layout,2,0,2,2)
        employee_info_layout.addLayout(employee_wage_layout,0,0,2,2)
        employee_info_layout.addLayout(self.employee_task_layout,0,2,4,2)

        employee_layout = QHBoxLayout()
        employee_layout.addLayout(employee_name_layout)
        employee_layout.addLayout(employee_info_layout)

        add_employee_layout = QVBoxLayout()
        add_employee_layout.addLayout(employee_layout)
        add_employee_layout.addLayout(button_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.employee_list)
        layout.addLayout(add_employee_layout)

    def update_level(self) -> None:
        [self.employee_level_input.addItem(level.name) for level in self.Levels]

    def update_task_layout(self) -> None:
        [self.employee_task_layout.addWidget(QCheckBox(task.name)) for task in self.Tasks]

    def update_levels(self) -> None:
        """ FOR FUTURE CONNECTION WITH SETTINGS PAGE """
        self.Levels = self.Controller.get_Levels_enum()

    def update_tasks(self) -> None:
        """ FOR FUTURE CONNECTION WITH SETTINGS PAGE """
        self.Tasks = self.Controller.get_Tasks_enum()

    def update_employees_display(self):
        employees = self.Controller.employees_input()
        self.employee_list.addItems(employees)

    def add_employee(self):
        fields = self.__get_input_fields()
        self.Controller.create_employee(*fields)
        self.employee_list.addItem(str(fields))
        self.__clear_input_fields()

        self.update_signal.emit()

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

            self.update_signal.emit()

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

            self.update_signal.emit()

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
        level = self.Levels[self.employee_level_input.currentText()].name

        tasks = []
        for task_widget_num in range(self.employee_task_layout.count()):
            task_widget: QCheckBox = self.employee_task_layout.itemAt(task_widget_num).widget()
            task = task_widget.text()
            if task_widget.isChecked():
                tasks.append(self.Tasks[task].name)

        return first_name, last_name, wage, level, tasks