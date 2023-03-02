from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget,
                               QComboBox, QCheckBox, QSizePolicy, QStackedWidget)

from PySide6.QtCore import Qt

from data.assign import employee_list

class Availability(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.tasktypes = ['Allround']
        self.timeslots = ["7:00-12:00", "12:00-18:00"]
        self.selected_employee = None
        self.amount_of_weeks = 4

        # Make coversion dict from name to object
        self.employee_object_dict = self.init_employee_object_dict()

        self.init_schedule_widget()

        # Create the left widget with an overview of all possible timeslots
        self.timeslots_label = QLabel("Shifts")

        self.role_combobox = QComboBox()
        for role in self.tasktypes:
            self.role_combobox.addItem(role)

        self.timeslots_layout = QVBoxLayout()
        for timeslot in self.timeslots:
            timeslot_label = QLabel(timeslot)
            self.timeslots_layout.addWidget(timeslot_label)


        self.left_widget_layout = QVBoxLayout()
        self.left_widget_layout.addWidget(self.timeslots_label)
        self.left_widget_layout.addWidget(self.role_combobox)
        self.left_widget_layout.addLayout(self.timeslots_layout)

        # Create the right widget with employee information

        self.employee_combo = QComboBox()
        self.employee_combo.currentIndexChanged.connect(self.set_employee)

        name_lengths = []

        self.employee_combo.addItem('Geen Werknemer')
        name_lengths.append(len('Geen Werknemer'))
        for employee in employee_list:
            name = employee.get_name()
            self.employee_combo.addItem(name)
            name_lengths.append(len(name))

        width = max(name_lengths) * 10
        self.employee_combo.setFixedWidth(width)

        self.employee_wage_label = QLabel("Wage: N/A")

        work_frequency_layout = QGridLayout()

        work_frequency_label = QLabel('Diensten Per Week')
        work_frequency_label.setAlignment(Qt.AlignHCenter)
        work_frequency_layout.addWidget(work_frequency_label, 0, 1, 1, 3)


        for week in range(4):

            label = QLabel(f'Week {week + 1}')

            editor = QLineEdit()
            editor.setFixedWidth(18)
            editor.week = week

            info_button = QPushButton('i')
            info_button.setFixedWidth(25)

            work_frequency_layout.addWidget(label, week + 1, 1)
            work_frequency_layout.addWidget(editor, week + 1, 2)
            work_frequency_layout.addWidget(info_button, week + 1, 3)

        work_frequency_widget = QWidget()
        work_frequency_widget.setLayout(work_frequency_layout)
        work_frequency_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        work_frequency_widget.setMinimumSize(work_frequency_widget.sizeHint())

        employee_info_layout = QVBoxLayout()
        employee_info_layout.setAlignment(Qt.AlignHCenter)
        employee_info_layout.setAlignment(Qt.AlignVCenter)
        employee_info_layout.addWidget(self.employee_combo)
        employee_info_layout.addWidget(self.employee_wage_label)

        # Add the schedule view and two widgets to the main layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addLayout(self.left_widget_layout)
        self.bottom_layout.addLayout(employee_info_layout)
        self.bottom_layout.addWidget(work_frequency_widget)

        self.tab3_layout = QVBoxLayout(self)
        self.tab3_layout.addLayout(self.schedule_viewer)
        self.tab3_layout.addLayout(self.bottom_layout)

    """ Init """

    def init_employee_object_dict(self) -> dict:
        dictionary = {}
        for employee in employee_list:
            dictionary[employee.get_name()] = employee
        return dictionary

    def init_schedule_widget(self) -> None:

        self.schedule_widget = QStackedWidget()

        # For each week:
        for week_num in range(self.amount_of_weeks):

            # Make a layout for the week
            week_layout = QHBoxLayout()
            week_layout.setSpacing(0)
            week_layout.setContentsMargins(0,0,0,0)

            # For each day:
            for day_num, day in enumerate(self.days):

                # Create a label and a layout for each day
                day_label = QLabel(day)
                day_label.setAlignment(Qt.AlignHCenter)
                day_layout = QVBoxLayout()
                day_layout.setSpacing(0)
                day_layout.setContentsMargins(0,0,0,0)
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

                day_widget = QWidget()
                day_widget.setLayout(day_layout)
                day_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                day_widget.setMinimumSize(day_widget.sizeHint())

                # Add each day to the week layout
                week_layout.addWidget(day_widget)


            week_label = QLabel(f'Week: {week_num + 1}')

            week_layout_with_label = QVBoxLayout()
            week_layout_with_label.addWidget(week_label)
            week_layout_with_label.addLayout(week_layout)


            # Add each week to the schedule
            week_widget = QWidget()
            week_widget.setLayout(week_layout_with_label)

            self.schedule_widget.addWidget(week_widget)

        forward_button = QPushButton('>')
        forward_button.setFixedHeight(100)
        forward_button.setFixedWidth(20)

        backward_button = QPushButton('<')
        backward_button.setFixedHeight(100)
        backward_button.setFixedWidth(20)

        forward_button.clicked.connect(lambda: self.schedule_scroller(forward=True))
        backward_button.clicked.connect(lambda: self.schedule_scroller(forward=False))

        self.schedule_viewer = QHBoxLayout()
        self.schedule_viewer.addWidget(backward_button)
        self.schedule_viewer.addWidget(self.schedule_widget)
        self.schedule_viewer.addWidget(forward_button)

    """ Get """

    def get_employee_object(self, name: str) -> object:
        return self.employee_object_dict.get(name)

    """ Methods """

    def schedule_scroller(self, forward: bool) -> None:
        if forward:
            index = (self.schedule_widget.currentIndex() + 1) % self.schedule_widget.count()
        else:
            index = (self.schedule_widget.currentIndex() - 1) % self.schedule_widget.count()

        self.schedule_widget.setCurrentIndex(index)

    def update_schedule_availability(self):
        """ Update the availability checkboxes based on the availability of the employee instance """

        # For each week
        for week_num in range(self.schedule_widget.count()):

            # Find the child layout containing all the days
            week_widget = self.schedule_widget.widget(week_num)
            widget_layout = week_widget.layout()

            for child in range(widget_layout.count()):

                child = widget_layout.itemAt(child)

                # Skip if child is not layout containing days
                if not isinstance(child, QHBoxLayout):
                    continue

            # For each day
            for day_num in range(child.count()):

                # Find the child layout containing all the days
                second_child = child.itemAt(day_num).widget()
                second_child_layout = second_child.layout()


                # For each shift
                for shift_num in range(second_child_layout.count()):

                    # Find the child widgets
                    third_child = second_child_layout.itemAt(shift_num).widget()

                    # Exclude the labels
                    if isinstance(third_child, QLabel):
                        continue

                    # Set checkbox to true if employee is available
                    if [third_child.week, third_child.day, third_child.timeslot] in self.selected_employee.availability:
                        third_child.setChecked(True)
                    else:
                        third_child.setChecked(False)

    def set_employee(self):

        combobox = self.sender()

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
            else:
                if timeslot in self.selected_employee.availability:
                    self.selected_employee.availability.remove(timeslot)
