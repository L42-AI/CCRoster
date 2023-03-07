from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget,
                               QComboBox, QCheckBox, QSizePolicy, QStackedWidget,
                               QLayout)


from classes.representation.controller import Controller
from classes.representation.employee import Employee
from classes.representation.shift import Shift

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Availability(QWidget):
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con


        self.tasktypes = {'Allround': 1}
        self.timeslots = []
        self.selected_employee: Employee = None
        self.amount_of_weeks = 4


        # Create timeslot_dict
        self.init_timeslot_dict()

        # Create schedule widget
        self.schedule_widget = self.init_schedule_widget()
        self.schedule_layout = self.init_schedule_layout(self.schedule_widget)

        # Create bottom layouts
        self.left_layout = self.init_left_layout()
        self.mid_layout = self.init_mid_layout()
        self.right_layout = self.init_right_layout()

        # Create a widget for the right layout
        work_frequency_widget = QWidget()
        work_frequency_widget.setLayout(self.right_layout)
        work_frequency_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        work_frequency_widget.setMinimumSize(work_frequency_widget.sizeHint())

        # Stack info layouts horizontally
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addLayout(self.left_layout)
        self.bottom_layout.addLayout(self.mid_layout)
        self.bottom_layout.addWidget(work_frequency_widget)

        # Add to total layout
        layout = QVBoxLayout(self)
        layout.addLayout(self.schedule_layout)
        layout.addLayout(self.bottom_layout)

    """ Init """

    def init_timeslot_dict(self) -> dict:
        self.timeslots_dict = {task: [] for task in self.tasktypes.values()}
        shift_list: list[Shift] = self.Controller.get_shift_list()

        for shift in shift_list:

            self.timeslots_dict[shift.task].append(shift)

    def init_left_layout(self) -> QVBoxLayout:
        self.task_combobox = QComboBox()
        self.task_combobox.setFixedWidth(150)
        self.task_combobox.activated.connect(self.update_shift_display)
        self.task_combobox = self.fill_tasktype_combobox(self.task_combobox)

        self.timeslots_layout = QVBoxLayout()
        self.timeslots_layout = self.fill_timeslot_display_layout(self.timeslots_layout)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Shifts"))
        layout.addWidget(self.task_combobox)
        layout.addLayout(self.timeslots_layout)

        return layout

    def fill_tasktype_combobox(self, combobox: QComboBox) -> QComboBox:
        combobox.addItems(self.tasktypes.keys())
        return combobox

    def fill_timeslot_display_layout(self, layout: QVBoxLayout) -> QVBoxLayout:
        existant = set()
        for shift in self.timeslots:
            if tuple((shift.start_time, shift.end_time)) not in existant:
                existant.add(tuple((shift.start_time, shift.end_time)))
                timeslot_label = QLabel(self.display_time(shift.start_time) + ' - ' + self.display_time(shift.end_time))
                layout.addWidget(timeslot_label)
        return layout

    def init_mid_layout(self) -> QVBoxLayout:
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

        self.employee_wage_label = QLabel("Wage: N/A")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self.employee_combo)
        layout.addWidget(self.employee_wage_label)

        return layout

    def init_right_layout(self) -> QGridLayout:
        layout = QGridLayout()

        label = QLabel('Diensten Per Week')
        label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(label, 0, 1, 1, 3)


        for week in range(4):

            label = QLabel(f'Week {week + 1}')

            editor = QLineEdit()
            editor.setFixedWidth(18)
            editor.week = week

            info_button = QPushButton('i')
            info_button.setFixedWidth(25)

            layout.addWidget(label, week + 1, 1)
            layout.addWidget(editor, week + 1, 2)
            layout.addWidget(info_button, week + 1, 3)

        return layout

    def init_schedule_widget(self) -> QStackedWidget:
        schedule_widget = QStackedWidget()
        schedule_widget.setContentsMargins(0,0,0,0)

        for week_num in range(self.amount_of_weeks):
            week_widget = self.init_week_widget(week_num)
            schedule_widget.addWidget(week_widget)

        return schedule_widget

    def init_week_widget(self, week_num: int) -> QWidget:
        week_layout = QHBoxLayout()
        week_layout.setContentsMargins(0,0,0,0)
        week_layout.setSpacing(0)

        for day_num, day in enumerate(DAYS):
            day_widget = self.init_day_widget(week_num, day_num, day)
            week_layout.addWidget(day_widget)

        week_widget = QWidget()
        week_widget.setContentsMargins(0,0,0,0)
        week_widget.setLayout(week_layout)

        return week_widget

    def init_day_widget(self, week_num: int, day_num: int, day: str) -> QWidget:
        day_label = QLabel(day)
        day_label.setAlignment(Qt.AlignHCenter)

        day_layout = QVBoxLayout()
        day_layout.setContentsMargins(0,0,0,0)
        day_layout.addWidget(day_label)

        for timeslot_num, timeslot in enumerate(self.timeslots):
            checkbox = self.init_checkbox(week_num, day_num, timeslot_num, timeslot)
            day_layout.addWidget(checkbox)

        day_widget = QWidget()
        day_widget.setLayout(day_layout)
        day_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        day_widget.setMinimumSize(day_widget.sizeHint())

        return day_widget

    def init_checkbox(self, week_num: int, day_num: int, timeslot_num: int, timeslot: str) -> QCheckBox:
        checkbox = QCheckBox(timeslot)
        checkbox.week = week_num
        checkbox.day = day_num
        checkbox.timeslot = timeslot_num
        checkbox.clicked.connect(self.availability_checkbox_clicked)
        checkbox.setChecked(False)

        return checkbox

    def init_schedule_layout(self, schedule_widget: QStackedWidget) -> QGridLayout:

        self.week_label = QLabel(f'Week: 1')

        forward_button = QPushButton('>')
        forward_button.setFixedHeight(100)
        forward_button.setFixedWidth(20)

        backward_button = QPushButton('<')
        backward_button.setFixedHeight(100)
        backward_button.setFixedWidth(20)

        forward_button.clicked.connect(lambda: self.schedule_scroller(forward=True))
        backward_button.clicked.connect(lambda: self.schedule_scroller(forward=False))

        layout = QGridLayout()
        layout.addWidget(self.week_label, 0, 0, 1, 3, Qt.AlignHCenter)
        layout.addWidget(backward_button, 1, 0, 2, 1)
        layout.addWidget(schedule_widget, 1, 1, 2, 1)
        layout.addWidget(forward_button, 1, 2, 2, 1)

        return layout

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
                    self.Controller.edit_employee_availability(timeslot, add=True)
            else:
                if timeslot in self.selected_employee.availability:
                    self.selected_employee.availability.remove(timeslot)
                    self.Controller.edit_employee_availability(timeslot, add=False)

    def update_shift_display(self):
        selected_task = self.task_combobox.currentText()
        self.init_timeslot_dict()
        self.timeslots = self.set_timeslot_list(selected_task)

        self.clear_layout(self.timeslots_layout)
        self.timeslots_layout = self.fill_timeslot_display_layout(self.timeslots_layout)


    def set_timeslot_list(self, selected_task: str) -> list[Shift]:
        tasknum = self.tasktypes[selected_task]
        return self.timeslots_dict[tasknum]

    def clear_layout(self, layout: QLayout) -> None:
        # Remove and delete all the widgets in the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def clear_schedule_shifts(self, layout: QStackedWidget) -> None:
        pass

    def display_time(self, time: str) -> str:
        return f'{time[:2]}:{time[2:]}'