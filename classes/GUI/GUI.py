import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget, QDialog, QComboBox,
                               QScrollArea, QCheckBox, QWidgetItem)

from data.assign import employee_list

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Scheduling")
        self.setGeometry(100, 100, 875, 625)

        # Define the days of the week and timeslots
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.timeslots = ["7:00-12:00", "12:00-18:00"]
        self.selected_employee = None

        # List for tab 1
        self.time_slots = []

        # Make coversion dict from name to object
        self.student_object_dict = self.init_student_object_dict()

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

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_time_slot_button)
        button_layout.addWidget(self.edit_time_slot_button)
        button_layout.addWidget(self.delete_time_slot_button)

        layout = QVBoxLayout(self.tab1)
        layout.addWidget(self.time_slot_list)
        layout.addWidget(self.start_time_label)
        layout.addWidget(self.start_time_edit)
        layout.addWidget(self.end_time_label)
        layout.addWidget(self.end_time_edit)
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
                    checkbox.clicked.connect(self.checkbox_clicked)
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

    def set_employee(self, name):

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

    def checkbox_clicked(self):

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


    def add_time_slot(self):
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()
        self.time_slots.append((start_time, end_time))
        self.time_slot_list.addItem(f"{start_time} - {end_time}")
        self.start_time_edit.clear()
        self.end_time_edit.clear()

    def edit_time_slot(self, item):
        index = self.time_slot_list.row(item)
        start_time, end_time = self.time_slots[index]
        self.start_time_edit.setText(start_time)
        self.end_time_edit.setText(end_time)
        self.edit_time_slot_button.setEnabled(True)
        self.delete_time_slot_button.setEnabled(True)

    def edit_selected_time_slot(self):
        selected_item = self.time_slot_list.currentItem()
        if selected_item is not None:
            index = self.time_slot_list.row(selected_item)

            new_start_time = self.start_time_edit.text()
            new_end_time = self.end_time_edit.text()

            self.time_slots[index] = new_start_time, new_end_time
            self.time_slot_list.takeItem(index)
            self.time_slot_list.addItem(f"{new_start_time} - {new_end_time}")

    def delete_selected_time_slot(self):
        selected_item = self.time_slot_list.currentItem()
        if selected_item is not None:

            # Find index
            index = self.time_slot_list.row(selected_item)

            # Remove from list
            del self.time_slots[index]

            # Remove item from list box
            self.time_slot_list.takeItem(index)

            # Disable buttons
            self.edit_time_slot_button.setEnabled(False)
            self.delete_time_slot_button.setEnabled(False)

            # Reset text to nothing
            self.start_time_edit.setText('')
            self.end_time_edit.setText('')


    def add_employee():
        pass

if __name__ == "__main__":
    window = QApplication()
    app = MainWindow()
    app.show()
    sys.exit(window.exec_())
