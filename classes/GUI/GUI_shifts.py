from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QCheckBox, QListWidgetItem, QLayout)
import re
from classes.representation.controller import Controller

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Shifts(QWidget):
    def __init__(self, Con, parent=None) -> None:
        super().__init__(parent)

        self.Controller: Controller = Con

        # Set mutable object
        self.amount_of_weeks = 4

        """ Call in init for now """
        self.update_task_types()

        self.init_UI()

    """ Init """

    def init_UI(self) -> None:

        """ Timeslot Widget """

        self.time_slot_list = QListWidget()
        self.time_slot_list.itemDoubleClicked.connect(self.edit_time_slot)

        """ Time input widgets """

        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()

        times_layout = QVBoxLayout()
        times_layout.addWidget(QLabel("Start Time:"))
        times_layout.addWidget(self.start_time_edit)
        times_layout.addWidget(QLabel("End Time:"))
        times_layout.addWidget(self.end_time_edit)

        """ Interact buttons """

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

        """ Day checkboxes """

        self.days_layout = QHBoxLayout()
        for day in DAYS:
            label = QLabel(day[:2])
            box = QCheckBox()
            box.day = day

            day_layout = QVBoxLayout()
            day_layout.addWidget(label)
            day_layout.addWidget(box)

            self.days_layout.addLayout(day_layout)

        """ Week checkboxes """

        self.weeks_layout = QHBoxLayout()

        all_weeks_label = QLabel('Uniform')

        self.all_weeks_checkbox = QCheckBox()
        self.all_weeks_checkbox.setChecked(True)
        self.all_weeks_checkbox.clicked.connect(self.all_weeks_checkbox_clicked)

        all_weeks_layout = QVBoxLayout()
        all_weeks_layout.addWidget(all_weeks_label)
        all_weeks_layout.addWidget(self.all_weeks_checkbox)

        # Create the week selector
        self.weeks_layout.addLayout(all_weeks_layout)

        """ Tasks """

        self.task_box = QComboBox()
        self.update_task_box()

        self.update_shifts_display()

        """ Layout """

        # Add the day layouts
        self.moment_layout = QVBoxLayout()
        self.moment_layout.addLayout(self.days_layout)
        self.moment_layout.addLayout(self.weeks_layout)

        # Create the time set layout
        timeset_layout = QHBoxLayout()
        timeset_layout.addLayout(times_layout)
        timeset_layout.addLayout(self.moment_layout)


        # Create the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.task_box)
        layout.addWidget(self.time_slot_list)
        layout.addLayout(timeset_layout)
        layout.addLayout(button_layout)

    def update_shifts_display(self) -> None:
        shifts = self.Controller.shifts_input()
        for shift in shifts:
            if shift[1] == self.Tasks[self.task_box.currentText()].value:
                self.time_slot_list.addItem(str(shift[0]))

    def update_task_box(self) -> None:
        for task in self.Tasks:
            self.task_box.addItem(task.name)

    def update_task_types(self) -> None:
        """ FOR FUTURE CONNECTION WITH SETTINGS PAGE """
        self.Tasks = self.Controller.get_Tasks_enum()

    """ Methods """

    def add_time_slot(self) -> None:

        timeslot, days, week, task_type, info_string = self.__get_timeslot_input_options()

        if self.__check_correct_time(timeslot) is False:
            return

        # Add to list and display widget
        self.__export_shift_to_connector(timeslot, days, week, task_type)
        self.time_slot_list.addItem(info_string)

        # Reset the text inputs
        self.start_time_edit.clear()
        self.end_time_edit.clear()

        self.Controller.update_shift_dict()

    def edit_time_slot(self, item: QListWidgetItem) -> None:

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

    def edit_selected_time_slot(self) -> None:

        item = self.time_slot_list.currentItem()

        if item is not None:

            index = self.time_slot_list.row(item)

            old_timeslot = self.__get_timeslot(item)

            new_timeslot, days, week, task_type, info_string = self.__get_timeslot_input_options()

            if self.__check_correct_time(new_timeslot) is False:
                return

            self.Controller.delete_shift(old_timeslot)
            self.time_slot_list.takeItem(index)

            self.__export_shift_to_connector(new_timeslot, days, week, task_type)
            self.time_slot_list.addItem(info_string)

            self.start_time_edit.clear()
            self.end_time_edit.clear()

            self.Controller.update_shift_dict()

    def delete_selected_time_slot(self) -> None:
        # Get selected time slot
        item = self.time_slot_list.currentItem()

        if item is not None:

            timeslot = self.__get_timeslot(item)

            # Remove from list and widget
            self.Controller.delete_shift(timeslot)
            self.time_slot_list.takeItem(self.time_slot_list.currentRow())

            # Disable buttons
            self.edit_time_slot_button.setEnabled(False)
            self.delete_time_slot_button.setEnabled(False)

            # Reset text to nothing
            self.start_time_edit.clear()
            self.end_time_edit.clear()

            self.Controller.update_shift_dict()

    def all_weeks_checkbox_clicked(self) -> None:
        checkbox = self.sender()

        children_layouts = []

        if checkbox.isChecked():

            for week_num in range(1, self.weeks_layout.count()):
                child_layout = self.weeks_layout.itemAt(week_num).layout()
                children_layouts.append(child_layout)

            for child_layout in children_layouts:
                # Remove all the widgets from the QVBoxLayout and delete them
                while child_layout.count() > 0:
                    widget = child_layout.takeAt(0).widget()
                    widget.setParent(None)
                    widget.deleteLater()

                # Remove the QVBoxLayout itself and delete it
                self.weeks_layout.removeItem(child_layout)
                child_layout.deleteLater()

            self.weeks_layout.update()
        else:
            self.__add_week_selection(self.weeks_layout)
            self.weeks_layout.update()

    """ Helpers """

    def __check_correct_time(self, timeslot: str) -> bool:
        start_time, end_time = timeslot.split(' - ')

        if not all(re.match("^(?!2[4-9])(([01][0-9])|(2[0-3]))(?!6)[0-5][0-9]$", time) for time in [start_time, end_time]):
            return False
        else:
            return True

    def __get_timeslot(self, item: object) -> str:

        # Extract text of selected item
        selected_str = item.text()

        # Find timeslot
        timeslot = selected_str.split('TIME: ')[1].split(', DAYS')[0]

        return timeslot

    def __add_week_selection(self, widget_layout: QHBoxLayout) -> None:
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
            day_layout: QVBoxLayout = self.days_layout.itemAt(layout_num)

            for widget_num in range(day_layout.count()):
                child_widget = day_layout.itemAt(widget_num).widget()

                if isinstance(child_widget, QLabel):
                    day = child_widget.text()
                else:
                    if child_widget.isChecked():

                        days.append(layout_num)


        weeks = []
        if self.all_weeks_checkbox.isChecked():
            weeks = [0,1,2,3]
        else:
            for week_num in range(1, self.weeks_layout.count()):
                week_layout: QLayout = self.weeks_layout.itemAt(week_num)

                for widget_num in range(1, week_layout.count()):
                    box: QCheckBox = week_layout.itemAt(widget_num).widget()

                    if box.isChecked():
                        weeks.append(week_num)

        task_type = self.task_box.currentIndex() + 1 # default is 1 ipv 0
        # task_type = self.task_box.currentText() oude versie luka, miss wil je dit weer terugzetten
        info_string = f"TIME: {time_slot}, DAYS: {days}, WEEK: {weeks}, TYPE: {task_type}"

        return time_slot, days, weeks, task_type, info_string

    def __export_shift_to_connector(self, timeslot, days: list[int], weeks: list[int], task) -> None:
        '''
        creates a shift in the controller class with the input from the GUI
        '''
        for week in weeks:
            for day in days:
                self.Controller.create_shift(time=timeslot, day=day, week=week, task=task)