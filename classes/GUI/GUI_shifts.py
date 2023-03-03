from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QCheckBox)
import re
from classes.representation.controller import Communicator

class Shifts(QWidget):
    def __init__(self, Com, parent=None) -> None:
        super().__init__(parent)

        self.Com: Communicator = Com

        # Set mutable object
        self.timeslots = {}
        self.tasktypes = ['Allround', 'Begels', 'Koffie', 'Kassa']
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.amount_of_weeks = 4

        """ Create Widgets """

        self.time_slot_list = QListWidget()
        self.time_slot_list.itemDoubleClicked.connect(self.edit_time_slot)

        self.start_time_label = QLabel("Start Time:")
        self.start_time_edit = QLineEdit()

        self.end_time_label = QLabel("End Time:")
        self.end_time_edit = QLineEdit()

        self.init_timeslot_buttons()

        # Create the weekday checkboxes
        self.days_layout = QHBoxLayout()
        self.init_day_checkboxes()

        self.weeks_layout = QHBoxLayout()
        self.init_week_checkboxes()

        self.role_box = QComboBox()
        self.fill_role_box()

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
        self.moment_layout.addLayout(self.weeks_layout)

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
        layout = QVBoxLayout(self)
        layout.addWidget(self.role_box)
        layout.addWidget(self.time_slot_list)
        layout.addLayout(timeset_layout)
        layout.addLayout(button_layout)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)

    """ Init """

    def init_timeslot_buttons(self) -> None:
        self.add_time_slot_button = QPushButton("Add Time Slot")
        self.add_time_slot_button.clicked.connect(self.add_time_slot)

        self.edit_time_slot_button = QPushButton("Edit Time Slot")
        self.edit_time_slot_button.clicked.connect(self.edit_selected_time_slot)
        self.edit_time_slot_button.setEnabled(False)

        self.delete_time_slot_button = QPushButton("Delete Time Slot")
        self.delete_time_slot_button.clicked.connect(self.delete_selected_time_slot)
        self.delete_time_slot_button.setEnabled(False)

    def init_day_checkboxes(self) -> None:
        for day in self.days:
            label = QLabel(day[:2])
            box = QCheckBox()
            box.day = day

            day_layout = QVBoxLayout()
            day_layout.addWidget(label)
            day_layout.addWidget(box)

            self.days_layout.addLayout(day_layout)

    def init_week_checkboxes(self) -> None:

        all_weeks_label = QLabel('Uniform')

        self.all_weeks_checkbox = QCheckBox()
        self.all_weeks_checkbox.setChecked(True)
        self.all_weeks_checkbox.clicked.connect(self.all_weeks_checkbox_clicked)

        all_weeks_layout = QVBoxLayout()
        all_weeks_layout.addWidget(all_weeks_label)
        all_weeks_layout.addWidget(self.all_weeks_checkbox)

        # Create the week selector
        self.weeks_layout.addLayout(all_weeks_layout)

    def fill_role_box(self) -> None:
        for task_type in self.tasktypes:
            self.role_box.addItem(task_type)

    """ Methods """

    def add_time_slot(self) -> None:

        timeslot, days, week, task_type, info_string = self.__get_timeslot_input_options()

        if self.__check_correct_time(timeslot) is False:
            return

        # Add to list and display widget
        self.__export_shift_to_communicator(timeslot, days, week, task_type)
        self.timeslots[timeslot] = {'day': days, 'week': week, 'type': task_type}
        self.time_slot_list.addItem(info_string)

        # Reset the text inputs
        self.start_time_edit.clear()
        self.end_time_edit.clear()

    def edit_time_slot(self, item: object) -> None:

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

            self.Com.delete_shift(old_timeslot)
            del self.timeslots[old_timeslot]
            self.time_slot_list.takeItem(index)

            self.__export_shift_to_communicator(new_timeslot, days, week, task_type)
            self.timeslots[new_timeslot] = {'day': days, 'week': week, 'type': task_type}
            self.time_slot_list.addItem(info_string)

            self.start_time_edit.clear()
            self.end_time_edit.clear()

    def delete_selected_time_slot(self) -> None:
        # Get selected time slot
        item = self.time_slot_list.currentItem()

        if item is not None:

            timeslot = self.__get_timeslot(item)

            # Remove from list and widget
            self.Com.delete_shift(timeslot)
            del self.timeslots[timeslot]
            self.time_slot_list.takeItem(self.time_slot_list.currentRow())

            # Disable buttons
            self.edit_time_slot_button.setEnabled(False)
            self.delete_time_slot_button.setEnabled(False)

            # Reset text to nothing
            self.start_time_edit.clear()
            self.end_time_edit.clear()

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

    def save(self) -> None:

        print(self.timeslots)

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
            weeks = ['All']
        else:
            for week_num in range(1, self.weeks_layout.count()):
                week_layout = self.weeks_layout.itemAt(week_num)

                for widget_num in range(1, week_layout.count()):
                    box = week_layout.itemAt(widget_num).widget()

                    if box.isChecked():
                        weeks.append(week_num)

        task_type = self.role_box.currentText()

        info_string = f"TIME: {time_slot}, DAYS: {days}, WEEK: {weeks}, TYPE: {task_type}"

        return time_slot, days, weeks, task_type, info_string

    def __export_shift_to_communicator(self, timeslot, days, weeks, role) -> None:
        for week in weeks:
            for day in days:
                self.Com.create_shift(time=timeslot, day=day, week=week, role=role)