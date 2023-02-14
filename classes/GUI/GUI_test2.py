import sys
import os
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QScrollArea, QComboBox
from data.assign import employee_list

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.student_object_dict = self.init_student_object_dict()


        # Define the days of the week and timeslots
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.timeslots = ["7:00-12:00", "12:00-18:00"]
        self.selected_employee = None

        # Create the scrollable schedule view with checkboxes
        self.schedule_scroll = QScrollArea()
        self.schedule_scroll.setWidgetResizable(True)
        self.schedule_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.weeks_layout = QHBoxLayout()

        for week_num in range(4):
            week_layout = QHBoxLayout()
            week_layout.setSpacing(10)
            for day in self.days:
                day_label = QLabel(day)
                day_layout = QVBoxLayout()
                day_layout.addWidget(day_label)
                for i, timeslot in enumerate(self.timeslots):
                    checkbox = QCheckBox(timeslot)
                    checkbox.setChecked(False)
                    checkbox.week = week_num
                    checkbox.day = self.days.index(day)
                    checkbox.timeslot = i
                    checkbox.clicked.connect(self.checkbox_clicked)

                    day_layout.addWidget(checkbox)
                week_layout.addLayout(day_layout)
            self.weeks_layout.addLayout(week_layout)
        self.schedule_widget = QWidget()
        self.schedule_widget.setLayout(self.weeks_layout)
        self.schedule_scroll.setWidget(self.schedule_widget)

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
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.schedule_scroll)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(left_widget)
        self.bottom_layout.addWidget(right_widget)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

    def init_student_object_dict(self) -> dict:
        dictionary = {}
        for employee in employee_list:
            dictionary[employee.get_name()] = employee
        return dictionary

    def get_student_object(self, name: str) -> object:
        return self.student_object_dict.get(name)

    def set_employee(self, name):
        self.selected_employee = self.get_student_object(name)
        self.employee_name_label.setText(name)

        if self.selected_employee == None:
            self.employee_wage_label.setText("Wage: N/A")
        else:
            self.employee_wage_label.setText(f"Wage: €{self.selected_employee.get_wage()}")

    def checkbox_clicked(self):
        if self.selected_employee != None:
            checkbox = self.sender()
            week_num = checkbox.week
            day = checkbox.day
            timeslot_num = checkbox.timeslot
            timeslot = [week_num, day, timeslot_num]

            if checkbox.isChecked():
                if timeslot not in self.selected_employee.availability:
                    self.selected_employee.availability.append(timeslot)
            else:
                if timeslot in self.selected_employee.availability:
                    self.selected_employee.availability.remove(timeslot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab1 = ScheduleWidget()
    tab1.show()
    sys.exit(app.exec_())