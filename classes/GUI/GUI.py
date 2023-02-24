import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget, QDialog, QComboBox,
                               QScrollArea, QCheckBox, QWidgetItem)

import re

from data.assign import employee_list



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Scheduling")
        self.setGeometry(100, 100, 875, 625)

        # Define the days of the week and timeslots
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.timeslots = ["7:00-12:00", "12:00-18:00"]
        self.amount_of_weeks = 4
        self.task_types = ['Allround']
        self.selected_employee = None

        # List for tab 1
        self.time_slots = {}

        # Make coversion dict from name to object
        self.student_object_dict = self.init_student_object_dict()

        # Define dictionary to keep track of checkboxes in tab 3 for each timeslot
        self.timeslot_checkboxes = {}

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: Add timeslots
        self.init_tab_1()

        # Tab 2: Add Employees
        self.init_tab_2()

        # Tab 3: Assign Employee Availability
        self.init_tab_3()


    """ Init """

    def init_tab_1(self):
        self.tab1 = QDialog()
        self.tabs.addTab(self.tab1, "Dienst Uren")

        self.time_slot_list = QListWidget()
        self.time_slot_list.itemDoubleClicked.connect(self.edit_time_slot)

        self.start_time_label = QLabel("Start Time:")
        self.start_time_edit = QLineEdit()

        self.end_time_label = QLabel("End Time:")
        self.end_time_edit = QLineEdit()

        self.add_time_slot_button = QPushButton("Add Time Slot")
        self.add_time_slot_button.clicked.connect(self.add_time_slot)

        self.edit_time_slot_button = QPushButton("Edit Time Slot")
        self.edit_time_slot_button.clicked.connect(self.edit_selected_time_slot)
        self.edit_time_slot_button.setEnabled(False)

        self.delete_time_slot_button = QPushButton("Delete Time Slot")
        self.delete_time_slot_button.clicked.connect(self.delete_selected_time_slot)
        self.delete_time_slot_button.setEnabled(False)

        # Create the weekday checkboxes
        self.days_layout = QHBoxLayout()
        for day in self.days:
                label = QLabel(day[:2])
                box = QCheckBox()
                box.day = day

                day_layout = QVBoxLayout()
                day_layout.addWidget(label)
                day_layout.addWidget(box)

                self.days_layout.addLayout(day_layout)

        # Create the week selector
        self.weeks_select_layout = QHBoxLayout()

        all_weeks_layout = QVBoxLayout()

        all_weeks_label = QLabel('Uniform')

        self.all_weeks_checkbox = QCheckBox()
        self.all_weeks_checkbox.setChecked(True)
        self.all_weeks_checkbox.clicked.connect(self.all_weeks_checkbox_clicked)

        all_weeks_layout.addWidget(all_weeks_label)
        all_weeks_layout.addWidget(self.all_weeks_checkbox)

        self.weeks_select_layout.addLayout(all_weeks_layout)


        self.task_type_box = QComboBox()
        for task_type in self.task_types:
            self.task_type_box.addItem(task_type)

        """ Layout """

        # Create the time widgets layout
        times_layout = QVBoxLayout()
        times_layout.addWidget(self.start_time_label)
        times_layout.addWidget(self.start_time_edit)
        times_layout.addWidget(self.end_time_label)
        times_layout.addWidget(self.end_time_edit)

        # Add the day layouts
        self.moment_layout = QVBoxLayout()
        self.moment_layout.addLayout(self.days_layout)
        self.moment_layout.addLayout(self.weeks_select_layout)

        # Create the time set layout
        timeset_layout = QHBoxLayout()
        timeset_layout.addLayout(times_layout)
        timeset_layout.addLayout(self.moment_layout)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_time_slot_button)
        button_layout.addWidget(self.edit_time_slot_button)
        button_layout.addWidget(self.delete_time_slot_button)

        # Create the main layout
        layout = QVBoxLayout(self.tab1)
        layout.addWidget(self.task_type_box)
        layout.addWidget(self.time_slot_list)
        layout.addLayout(timeset_layout)
        layout.addLayout(button_layout)

    def init_tab_2(self):
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Werknemers")
        self.tab2_layout = QVBoxLayout(self.tab2)

        self.employee_list = QListWidget()
        self.tab2_layout.addWidget(self.employee_list)

        self.employee_grid = QGridLayout()
        self.tab2_layout.addLayout(self.employee_grid)

        self.employee_names = []

        self.add_employee_layout = QVBoxLayout()
        self.employee_extra_layout = QHBoxLayout()
        self.employee_wage = QVBoxLayout()
        self.employee_onboarding = QVBoxLayout()

        self.employee_name_input = QLineEdit()
        self.employee_wage_input = QLineEdit()
        self.employee_onboarding_input = QCheckBox()
        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)

        self.employee_wage.addWidget(QLabel("Hourly Wage:"))
        self.employee_wage.addWidget(self.employee_wage_input)

        self.employee_onboarding.addWidget(QLabel("Onboarding:"))
        self.employee_onboarding.addWidget(self.employee_onboarding_input)

        self.employee_extra_layout.addLayout(self.employee_wage)
        self.employee_extra_layout.addLayout(self.employee_onboarding)


        self.add_employee_layout.addWidget(QLabel("Employee Name:"))
        self.add_employee_layout.addWidget(self.employee_name_input)
        self.add_employee_layout.addLayout(self.employee_extra_layout)
        self.add_employee_layout.addWidget(self.add_employee_button)
        self.tab2_layout.addLayout(self.add_employee_layout)

    def init_tab_3(self):

        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "Beschikbaarheid")

        self.init_schedule_widget()

        # Create the left widget with an overview of all possible timeslots
        self.timeslots_label = QLabel("Shifts")
        self.timeslots_layout = QVBoxLayout()
        for timeslot in self.timeslots:
            timeslot_label = QLabel(timeslot)
            self.timeslots_layout.addWidget(timeslot_label)
        self.left_widget_layout = QVBoxLayout()
        self.left_widget_layout.addWidget(self.timeslots_label)
        self.left_widget_layout.addLayout(self.timeslots_layout)
        left_widget = QWidget()
        left_widget.setLayout(self.left_widget_layout)

        # Create the right widget with employee information
        self.employee_label = QLabel("Employee:")
        self.employee_name_label = QLabel("No employee selected")
        self.employee_wage_label = QLabel("Wage: N/A")
        self.employee_combo = QComboBox()
        self.employee_combo.addItem('Geen Werknemer')


        for employee in employee_list:
            self.employee_combo.addItem(employee.get_name())

        self.employee_combo.currentIndexChanged.connect(lambda: self.set_employee(self.employee_combo.currentText()))
        self.right_widget_layout = QVBoxLayout()
        self.right_widget_layout.addWidget(self.employee_label)
        self.right_widget_layout.addWidget(self.employee_combo)
        self.right_widget_layout.addWidget(self.employee_name_label)
        self.right_widget_layout.addWidget(self.employee_wage_label)
        right_widget = QWidget()
        right_widget.setLayout(self.right_widget_layout)

        # Add the schedule view and two widgets to the main layout
        self.tab3_layout = QVBoxLayout(self.tab3)
        self.tab3_layout.addWidget(self.schedule_scroll)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(left_widget)
        self.bottom_layout.addWidget(right_widget)
        self.tab3_layout.addLayout(self.bottom_layout)


    def init_student_object_dict(self) -> dict:
        dictionary = {}
        for employee in employee_list:
            dictionary[employee.get_name()] = employee
        return dictionary

    def init_schedule_widget(self) -> None:
        # Create the scrollable schedule view with checkboxes
        self.schedule_scroll = QScrollArea()
        self.schedule_scroll.setWidgetResizable(True)
        # self.schedule_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.weeks_layout = self.init_schedule_av()

        self.schedule_widget = QWidget()
        self.schedule_widget.setLayout(self.weeks_layout)
        self.schedule_scroll.setWidget(self.schedule_widget)

    def init_schedule_av(self) -> object:
        """ Create content of schedule widget """

        # Create layout
        weeks_layout = QVBoxLayout()

        # For each week:
        for week_num in range(4):

            # Make a layout for the week
            week_layout = QHBoxLayout()
            week_layout.setSpacing(10)

            # For each day:
            for day_num, day in enumerate(self.days):

                # Create a label and a layout for each day
                day_label = QLabel(day)
                day_layout = QVBoxLayout()
                day_layout.addWidget(day_label)

                # For each timeslot
                for timeslot_num, timeslot in enumerate(self.timeslots):

                    # Make checkbox
                    checkbox = QCheckBox(timeslot)
                    checkbox.week = week_num
                    checkbox.day = day_num
                    checkbox.timeslot = timeslot_num
                    checkbox.clicked.connect(self.availability_checkbox_clicked)
                    checkbox.setChecked(False)

                    # Add to day layout
                    day_layout.addWidget(checkbox)

                # Add each day to the week layout
                week_layout.addLayout(day_layout)

            # Add each week to the schedule
            weeks_layout.addLayout(week_layout)

            # Add a seperating label in between the weeks
            if week_num < 3:
                weeks_layout.addWidget(QLabel('==============================================================================================='))

        return weeks_layout

    """ Get """

    def get_student_object(self, name: str) -> object:
        return self.student_object_dict.get(name)

    """ Methods """

    def update_schedule_availability(self):
        """ Update the availability checkboxes based on the availability of the employee instance """

        # For each week
        for week_num in range(self.weeks_layout.count()):

            # Find the child layout containing all the days
            child_layout = self.weeks_layout.itemAt(week_num)

            # Skip if child is not layout containing days
            if isinstance(child_layout, QWidgetItem):
                continue

            # For each day
            for day_num in range(child_layout.count()):

                # Find the child layout containing all the days
                second_child_layout = child_layout.itemAt(day_num)

                # For each shift
                for shift_num in range(second_child_layout.count()):

                    # Find the child widgets
                    child = second_child_layout.itemAt(shift_num).widget()

                    # Exclude the labels
                    if isinstance(child, QLabel):
                        continue

                    # Set checkbox to true if employee is available
                    if [child.week, child.day, child.timeslot] in self.selected_employee.availability:
                        child.setChecked(True)
                    else:
                        child.setChecked(False)

    def set_employee(self, name: str):

        # Get student object
        self.selected_employee = self.get_student_object(name)

        # Set the name
        self.employee_name_label.setText(name)

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
            else:
                if timeslot in self.selected_employee.availability:
                    self.selected_employee.availability.remove(timeslot)

    def all_weeks_checkbox_clicked(self):
        checkbox = self.sender()

        children_layouts = []

        if checkbox.isChecked():

            for week_num in range(1, self.weeks_select_layout.count()):
                child_layout = self.weeks_select_layout.itemAt(week_num).layout()
                children_layouts.append(child_layout)

            for child_layout in children_layouts:
                # Remove all the widgets from the QVBoxLayout and delete them
                while child_layout.count() > 0:
                    widget = child_layout.takeAt(0).widget()
                    widget.setParent(None)
                    widget.deleteLater()

                # Remove the QVBoxLayout itself and delete it
                self.weeks_select_layout.removeItem(child_layout)
                child_layout.deleteLater()

            self.weeks_select_layout.update()
        else:
            self.__add_week_selection(self.weeks_select_layout)
            self.weeks_select_layout.update()

    """ Buttons """

    def add_time_slot(self):

        timeslot, days, week, task_type, info_string = self.__get_timeslot_input_options()

        if self.__check_correct_time(timeslot) is False:
            return

        # Add to list and display widget
        self.time_slots[timeslot] = {'day': days, 'week': week, 'type': task_type}
        self.time_slot_list.addItem(info_string)

        # Add new checkboxes to dict
        for day in self.days:
            checkbox = QCheckBox()
            self.timeslot_checkboxes.setdefault(day, {})[timeslot] = checkbox

        # Reset the text inputs
        self.start_time_edit.clear()
        self.end_time_edit.clear()

    def edit_time_slot(self, item: object):

        # Get timeslot
        timeslot = self.__get_timeslot(item)

        # Find start and end times
        start_time, end_time = timeslot.split(' - ')

        # Set text
        self.start_time_edit.setText(start_time)
        self.end_time_edit.setText(end_time)

        # Enable buttons
        self.edit_time_slot_button.setEnabled(True)
        self.delete_time_slot_button.setEnabled(True)

    def edit_selected_time_slot(self):

        item = self.time_slot_list.currentItem()

        if item is not None:

            index = self.time_slot_list.row(item)

            old_timeslot = self.__get_timeslot(item)

            new_timeslot, days, week, task_type, info_string = self.__get_timeslot_input_options()

            if self.__check_correct_time(new_timeslot) is False:
                return

            del self.time_slots[old_timeslot]
            self.time_slots[new_timeslot] = {'day': days, 'week': week, 'type': task_type}

            self.time_slot_list.takeItem(index)
            self.time_slot_list.addItem(info_string)

            self.start_time_edit.clear()
            self.end_time_edit.clear()

    def delete_selected_time_slot(self):
        # Get selected time slot
        item = self.time_slot_list.currentItem()

        if item is not None:

            timeslot = self.__get_timeslot(item)

            # Remove from list and widget
            del self.time_slots[timeslot]
            self.time_slot_list.takeItem(self.time_slot_list.currentRow())

            # Disable buttons
            self.edit_time_slot_button.setEnabled(False)
            self.delete_time_slot_button.setEnabled(False)

            # Remove from dict
            for day in self.days:
                checkbox = self.timeslot_checkboxes[day].pop(item)
                del checkbox

            # Reset text to nothing
            self.start_time_edit.clear()
            self.end_time_edit.clear()


    def add_employee():
        pass



    def __check_correct_time(timeslot: str) -> bool:
        start_time, end_time = timeslot.split(' - ')

        if not all(re.match("^(?!2[4-9])(([01][0-9])|(2[0-3]))(?!6)[0-5][0-9]$", time) for time in [start_time, end_time]):
            return False
        else:
            return True

    def __add_week_selection(self, widget_layout: object):
        for week_num in range(1, self.amount_of_weeks + 1):
            layout = QVBoxLayout()
            label = QLabel(f'Week {week_num}')
            box = QCheckBox()
            box.week = week_num
            layout.addWidget(label)
            layout.addWidget(box)
            widget_layout.addLayout(layout)

    def __get_timeslot_input_options(self) -> tuple:
        # Get start and end time inputs
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()

        # Create new time slot
        time_slot = f"{start_time} - {end_time}"

        days = []
        for layout_num in range(self.days_layout.count()):
            day_layout = self.days_layout.itemAt(layout_num)

            for widget_num in range(day_layout.count()):
                child_widget = day_layout.itemAt(widget_num).widget()

                if isinstance(child_widget, QLabel):
                    day = child_widget.text()

                else:
                    if child_widget.isChecked():
                        days.append(day)


        weeks = []
        if self.all_weeks_checkbox.isChecked():
            weeks = 'All'
        else:
            for week_num in range(1, self.weeks_select_layout.count()):
                week_layout = self.weeks_select_layout.itemAt(week_num)

                for widget_num in range(1, week_layout.count()):
                    box = week_layout.itemAt(widget_num).widget()

                    if box.isChecked():
                        weeks.append(week_num)

        task_type = self.task_type_box.currentText()

        info_string = f"TIME: {time_slot}, DAYS: {days}, WEEK: {weeks}, TYPE: {task_type}"

        return time_slot, days, weeks, task_type, info_string

    def __get_timeslot(self, item: object) -> str:
        # Extract text of selected item
        selected_str = item.text()

        # Find timeslot
        timeslot = selected_str.split('TIME: ')[1].split(', DAYS')[0]

        return timeslot



if __name__ == "__main__":
    window = QApplication()
    app = MainWindow()
    app.show()
    sys.exit(window.exec_())
