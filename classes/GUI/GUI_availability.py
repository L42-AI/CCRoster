from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget,
                               QComboBox, QCheckBox, QSizePolicy, QStackedWidget,
                               QLayout)

import copy
from datetime import date, time, timedelta

from classes.representation.controller import Controller
from classes.representation.employee import Employee
from classes.representation.shift import Shift
from classes.representation.shift import ShiftData

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Availability(QWidget):
    def __init__(self, Con: Controller, parent=None) -> None:
        super().__init__(parent)

        self.Controller = Con

        self.start_date = self.Controller.get_start_date()
        self.end_date = self.Controller.get_end_date()

        self.update_tasks()
        self.update_shift_dict()
        self.update_employee_dict()

        self.selected_employee: Employee = None
        self.amount_of_weeks = int((self.end_date - self.start_date).days / 7)

        """ TEMPORARY """
        self.shifts = self.set_shift_list('Allround')
        self.employees = self.set_employee_list('Allround')

        self.init_UI()

        self.update_schedule_slots()


    """ Init """

    def init_UI(self) -> None:

        """ Schedule widget """
        display_date = copy.copy(self.start_date)
        self.schedule_dict = {}
        self.schedule_widget = QStackedWidget()
        self.schedule_widget.setContentsMargins(0,0,0,0)

        for week_num in range(self.amount_of_weeks):

            week_layout = QHBoxLayout()
            week_layout.setContentsMargins(0,0,0,0)
            week_layout.setSpacing(0)

            for day in DAYS:

                day_num = self.add_zero(display_date.day)
                month_num = self.add_zero(display_date.month)

                day_label = QLabel(f'{day_num} - {month_num} \n {day}')
                day_label.setAlignment(Qt.AlignHCenter)

                day_layout = QVBoxLayout()
                day_layout.setContentsMargins(0,0,0,0)
                day_layout.addWidget(day_label)

                day_widget = QWidget()
                day_widget.setLayout(day_layout)
                day_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                day_widget.setMinimumSize(day_widget.sizeHint())
                self.schedule_dict[display_date] = day_widget

                week_layout.addWidget(day_widget)

                display_date += timedelta(1)

            week_widget = QWidget()
            week_widget.setContentsMargins(0,0,0,0)
            week_widget.setLayout(week_layout)

            self.schedule_widget.addWidget(week_widget)

        """ Schedule layout """

        self.week_label = QLabel(f'Week: 1')

        forward_button = QPushButton('>')
        forward_button.setFixedHeight(100)
        forward_button.setFixedWidth(20)

        backward_button = QPushButton('<')
        backward_button.setFixedHeight(100)
        backward_button.setFixedWidth(20)

        forward_button.clicked.connect(lambda: self.schedule_scroller(forward=True))
        backward_button.clicked.connect(lambda: self.schedule_scroller(forward=False))

        schedule_layout = QGridLayout()
        schedule_layout.addWidget(self.week_label, 0, 0, 1, 3, Qt.AlignHCenter)
        schedule_layout.addWidget(backward_button, 1, 0, 2, 1)
        schedule_layout.addWidget(self.schedule_widget, 1, 1, 2, 1)
        schedule_layout.addWidget(forward_button, 1, 2, 2, 1)

        """ Task combobox """

        self.task_combobox = QComboBox()
        self.task_combobox.setFixedWidth(150)
        self.task_combobox.activated.connect(self.update_shift_display)
        self.update_task_combobox()

        """ Timeslots layout """

        self.shifts_layout = QVBoxLayout()
        self.update_timeslot_display_layout()

        shifts_layout = QVBoxLayout()
        shifts_layout.addWidget(QLabel("Shifts"))
        shifts_layout.addWidget(self.task_combobox)
        shifts_layout.addLayout(self.shifts_layout)

        """ Employee combobox """

        self.employee_combo = QComboBox()
        self.employee_combo.currentIndexChanged.connect(self.set_employee)

        name_lengths = []

        self.employee_combo.addItem('Geen Werknemer')
        name_lengths.append(len('Geen Werknemer'))
        for employee in self.Controller.get_employee_list():
            name = employee.name
            self.employee_combo.addItem(name)
            name_lengths.append(len(name))

        width = max(name_lengths) * 12
        self.employee_combo.setFixedWidth(width)

        """ Employee wage """

        self.employee_wage_label = QLabel("Wage: N/A")

        employee_layout = QVBoxLayout()
        employee_layout.setAlignment(Qt.AlignCenter)
        employee_layout.addWidget(self.employee_combo)
        employee_layout.addWidget(self.employee_wage_label)

        """ Employee work frequency """

        work_frequecy_layout = QGridLayout()

        label = QLabel('Diensten Per Week')
        label.setAlignment(Qt.AlignCenter)
        work_frequecy_layout.addWidget(label, 0, 1, 1, 3)

        for week in range(4):

            label = QLabel(f'Week {week + 1}')

            editor = QLineEdit()
            editor.setFixedWidth(18)
            editor.week = week

            info_button = QPushButton('i')
            info_button.setFixedWidth(25)

            work_frequecy_layout.addWidget(label, week + 1, 1)
            work_frequecy_layout.addWidget(editor, week + 1, 2)
            work_frequecy_layout.addWidget(info_button, week + 1, 3)

        # Create a widget for the right layout
        work_frequency_widget = QWidget()
        work_frequency_widget.setLayout(work_frequecy_layout)
        work_frequency_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        work_frequency_widget.setMinimumSize(work_frequency_widget.sizeHint())

        """ Layout """

        # Stack info layouts horizontally
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(shifts_layout)
        bottom_layout.addLayout(employee_layout)
        bottom_layout.addWidget(work_frequency_widget)

        # Add to total layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(schedule_layout)
        main_layout.addLayout(bottom_layout)

    """ Update """

    def update_schedule_slots(self) -> None:

        # Clear
        for scheduling_date in self.schedule_dict:
            day_layout = self.schedule_dict[scheduling_date]
            self.clear_layout(day_layout, skip=1)

        # Fill
        for shift in self.shifts:
            checkbox = QCheckBox(f'{shift.start} - {shift.end}')
            checkbox.shift = shift
            checkbox.clicked.connect(self.availability_checkbox_clicked)
            checkbox.setChecked(False)

            layout_to_include = self.schedule_dict[shift.date].layout()
            layout_to_include.addWidget(checkbox)


    def update_tasks(self) -> None:
        """ FOR FUTURE CONNECTION WITH SETTINGS PAGE """
        self.tasks = {'Allround': 1, 'Begels': 2, 'Koffie': 3, 'Kassa': 4}

    def update_shift_dict(self) -> None:
        """ Update the dictionary containing all shifts """
        # Set empty dict
        self.shift_dict = {task: [] for task in self.tasks.values()}

        # Get shifts from the controller
        shift_list: list[ShiftData] = self.Controller.get_shift_list()

        # Fill shift dict
        [self.shift_dict[shift.task].append(shift) for shift in shift_list]

    def update_employee_dict(self) -> None:
        """ Update the dictionary containing all shifts """
        # Set empty dict
        self.employee_dict = {task: [] for task in self.tasks.values()}

        # Get employees from the controller
        employee_list: list[Employee] = self.Controller.get_employee_list()

        # Fill employee dict
        """ SLECHT GECODE, CLASSES KRIJGEN REFERENCES IN MUTABLE OBJECTS """
        for employee in employee_list:
            for employee_task in employee.tasks:
                task_code = self.tasks[employee_task]
                self.employee_dict[task_code].append(employee.name)

    def update_shift_display(self):
        """ Update the shifts displayed in the GUI """

        # Update both dicts
        self.update_employee_dict()
        self.update_shift_dict()


        # Find the selected task and make lists of shifts and employees
        selected_task = self.task_combobox.currentText()
        self.shifts = self.set_shift_list(selected_task)
        self.employees = self.set_employee_list(selected_task)

        self.update_timeslot_display_layout()
        self.update_employee_combobox()

    def update_task_combobox(self) -> None:
        self.task_combobox.clear()

        self.task_combobox.addItems(self.tasks.keys())

    def update_employee_combobox(self) -> None:
        self.employee_combo.clear()

        [self.employee_combo.addItem(employee.name) for employee in self.employees]

    def update_timeslot_display_layout(self) -> None:
        self.clear_layout(self.shifts_layout)

        existant = set()
        for shift in self.shifts:
            if tuple((shift.start, shift.end)) not in existant:
                existant.add(tuple((shift.start, shift.end)))
                timeslot_label = QLabel(f'{shift.start} - {shift.end}')
                self.shifts_layout.addWidget(timeslot_label)

    def update_schedule_display(self) -> None:
        """ Method to fill the schedule with appropriate timeslots """
        self.shifts
        self.schedule_widget
        pass

    def set_shift_list(self, selected_task: str) -> list[ShiftData]:
        tasknum = self.tasks[selected_task]
        return self.shift_dict[tasknum]

    def set_employee_list(self, selected_task: str) -> list[Employee]:
        tasknum = self.tasks[selected_task]
        return self.employee_dict[tasknum]

    """ Get """

    def get_employee_object(self, name: str) -> Employee:
        found_employee = [employee for employee in self.Controller.get_employee_list() if employee.name == name]

        if len(found_employee) == 1:
            return found_employee[0]
        elif len(found_employee) < 1:
            return None
        else:
            raise NameError('Two employees with exact same name')

    """ Methods """

    def schedule_scroller(self, forward: bool) -> None:
        if forward:
            index = (self.schedule_widget.currentIndex() + 1) % self.schedule_widget.count()
        else:
            index = (self.schedule_widget.currentIndex() - 1) % self.schedule_widget.count()

        self.schedule_widget.setCurrentIndex(index)

        self.week_label.setText(f'Week: {index + 1}')

    def update_schedule_availability(self):
        """ Update the availability checkboxes based on the availability of the employee instance """

        # For each week
        for week_num in range(self.schedule_widget.count()):

            # Find the child layout containing all the days
            week_widget = self.schedule_widget.widget(week_num)
            week_layout = week_widget.layout()

            # For each day
            for day_num in range(week_layout.count()):

                # Find the child layout containing all the days
                day_widget = week_layout.itemAt(day_num).widget()
                day_layout = day_widget.layout()

                # For each shift
                for shift_num in range(1, day_layout.count()):

                    # Find the child widgets
                    shift_widget = day_layout.itemAt(shift_num).widget()

                    # Set checkbox to true if employee is available
                    if [shift_widget.week, shift_widget.day, shift_widget.timeslot] in self.selected_employee.availability:
                        shift_widget.setChecked(True)
                    else:
                        shift_widget.setChecked(False)

    def set_employee(self):

        combobox: QComboBox = self.sender()

        name = combobox.currentText()
        if name != 'Geen Werknemer':
            # Get student object
            self.selected_employee = self.get_employee_object(name)

            # Only set wage if student is something
            if self.selected_employee != None:
                self.employee_wage_label.setText(f"Wage: €{self.selected_employee.get_wage()}")
            else:
                self.employee_wage_label.setText("Wage: N/A")

            # Update the availability checboxes
            self.update_schedule_availability()

    def availability_checkbox_clicked(self):

        # Only execute if a valid employee is selected
        if self.selected_employee != None:

            # Find sending checkbox
            checkbox = self.sender()

            # Extract info
            week_num = checkbox.week
            day = checkbox.day
            timeslot_num = checkbox.timeslot

            # Create timeslot
            timeslot = [week_num, day, timeslot_num]

            # append or remove timeslot from availability depending on checkbox state state
            if checkbox.isChecked():
                if timeslot not in self.selected_employee.availability:
                    self.selected_employee.availability.append(timeslot)
                    self.Controller.edit_employee_availability(timeslot, add=True)
            else:
                if timeslot in self.selected_employee.availability:
                    self.selected_employee.availability.remove(timeslot)
                    self.Controller.edit_employee_availability(timeslot, add=False)

    def clear_layout(self, layout: QLayout, skip=0) -> None:
        # Remove and delete all the widgets in the layout
        while layout.count() > skip:
            item = layout.takeAt(skip)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_zero(self, digit: int) -> str:
        string = str(digit)
        if len(string) < 2:
            string = '0' + string
        return string