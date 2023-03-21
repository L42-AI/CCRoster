from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QGridLayout, QScrollArea, QDialog, QTimeEdit, QDateEdit,
                               QDateTimeEdit, QCalendarWidget)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPen, QPainter, QPalette, QBrush
from datetime import datetime, time, date

from classes.GUI.GUI_calendar import Calendar

import re
import sys
# from classes.representation.controller import Controller
# from classes.representation.generator import Generator


# class ShiftSheetViewer(QWidget):
#     update_signal = Signal()
#     def __init__(self, Con, parent=None) -> None:
#         super().__init__(parent)

#         self.Controller: Controller = Con

#         # Set mutable object
#         self.tasktypes = {'Allround':1, 'Begels':2, 'Koffie':3, 'Kassa':4}
#         self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         self.amount_of_weeks = 4

#         """ Create Widgets """

#         self.initUI()

#     def initUI(self):

#         Sheet = ShiftSheet()

#         layout = QGridLayout(self)
#         layout.addWidget(Sheet, 1,1,1,1)

class ShiftSheet(QScrollArea):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)

        # Create container widget for shift grid
        self.shift_grid_container = QWidget()
        self.shift_grid = self.create_shift_grid()
        self.shift_grid_container.setLayout(self.shift_grid)

        self.shift_grid_container.paintEvent = self.paintEvent

        # Add the container widget to the scroll area
        self.setWidget(self.shift_grid_container)

        for shift_widget in shift_list:
            self.place_shift(shift_widget)

        # Set the background color and draw lines
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)

    """ Init """

    def place_shift(self, Shift):
        for cell_num in range(self.shift_grid.count()):
            widget = self.shift_grid.itemAt(cell_num).widget()
            if not isinstance(widget, ClickableWidget):
                continue
            if widget.time == Shift.start.time():
                index = self.shift_grid.indexOf(widget)
                row, col, _, colspan = self.shift_grid.getItemPosition(index)
                shift_duration_minutes = (Shift.end - Shift.start).total_seconds() / 60
                rowspan = int(shift_duration_minutes / 15)
                print(row, col, rowspan, colspan)
                self.shift_grid.addWidget(Shift, row , col, rowspan, colspan)
                break

    def create_shift_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)

        # Add labels to the grid
        for col in range(5):
            for row in range(96):
                widget = ClickableWidget()
                widget.position = (row + 1) * (col + 1)
                hour = row // 4
                minute = (row % 4) * 15
                widget.time = time(hour, minute)
                widget.clicked.connect(self.add_shift_widget)
                grid.addWidget(widget, row, col)

        return grid



    def add_shift_widget(self):
        # Create blue widget
        grid_slot = self.sender()
        gridslot_hour = grid_slot.time.hour
        gridslot_minute = grid_slot.time.minute
        Shift = ShiftWidget(datetime(2023,2,2,gridslot_hour,gridslot_minute), datetime(2023,2,2,gridslot_hour + 2,gridslot_minute), self)
        index = self.shift_grid.indexOf(grid_slot)
        row, col, _, colspan = self.shift_grid.getItemPosition(index)
        shift_duration_minutes = (Shift.end - Shift.start).total_seconds() / 60
        rowspan = int(shift_duration_minutes / 15)
        self.shift_grid.addWidget(Shift, row, col, rowspan, colspan)


    def paintEvent(self, event) -> None:
        grid = self.shift_grid

        with QPainter(self.shift_grid_container) as painter:

            self.dot_gray_lines(painter, grid)

            self.draw_black_lines(painter, grid)

    def draw_black_lines(self, painter: QPainter, grid: QGridLayout) -> None:
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        width = grid.cellRect(0, 0).width()
        height = grid.cellRect(0, 0).height()

        for row in range(grid.rowCount()):
            for col in range(grid.columnCount()):
                x = grid.cellRect(row, col).x()
                y = grid.cellRect(row, col).y()

                painter.drawLine(x, y, x, y + height)

                if col == grid.columnCount() - 1:
                    painter.drawLine(x + width, y, x + width, y + height)

    def dot_gray_lines(self, painter: QPainter, grid: QGridLayout)-> None:
        width = grid.cellRect(0, 0).width()
        height = grid.cellRect(0, 0).height()

        for row in range(grid.rowCount()):
            for col in range(grid.columnCount()):

                x = grid.cellRect(row, col).x()
                y = grid.cellRect(row, col).y()

                if row == 0 or row % 12 == 0:
                    painter.setPen(QPen(Qt.gray, 3, Qt.DotLine))
                elif row % 4 == 0:
                    painter.setPen(QPen(Qt.gray, 2, Qt.DotLine))
                else:
                    painter.setPen(QPen(Qt.gray, 1, Qt.DotLine))

                painter.drawLine(x, y, x + width, y)

                if row == grid.rowCount() - 1:
                    painter.setPen(QPen(Qt.gray, 3, Qt.DotLine))
                    painter.drawLine(x, y + height, x + width, y + height)

class ShiftWidget(QWidget):
    clicked = Signal()

    def __init__(self, start, end, parent=None) -> None:
        super().__init__(parent)
        self.setContentsMargins(0,0,0,0)

        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")

        self.start = start
        self.end = end

        display_start = self.start.time().strftime("%H:%M")
        display_end = self.end.time().strftime("%H:%M")

        self.shift_time_display = QLabel(f'{display_start} - {display_end}')
        self.shift_time_display.setAlignment(Qt.AlignHCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.shift_time_display)

    def mousePressEvent(self, event):
        self.show_info("Allround")
        super().mousePressEvent(event)

    def show_info(self, role):
        self.dialog = QDialog()
        layout = QVBoxLayout()

        display_start = self.start.time().strftime("%H:%M")
        display_end = self.end.time().strftime("%H:%M")

        time_label = QLabel(f"Time: {display_start} - {display_end}")
        role_label = QLabel(f"Role: {role}")

        time_edit = QTimeEdit()
        date_edit = QDateEdit()
        self.datetime_edit = Calendar()

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        save_button = QPushButton("save")
        save_button.clicked.connect(self.save)

        layout.addWidget(time_label)
        layout.addWidget(time_edit)
        layout.addWidget(date_edit)
        layout.addWidget(role_label)
        layout.addWidget(delete_button)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def delete(self) -> None:
        self.dialog.deleteLater()
        self.deleteLater()


class ClickableWidget(QWidget):
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

shift_list = []
shift_list.append(ShiftWidget(start=datetime(2023,2,2,7,00), end=datetime(2023,2,2,12,00)))
shift_list.append(ShiftWidget(start=datetime(2023,2,2,13,00), end=datetime(2023,2,2,14,00)))
shift_list.append(ShiftWidget(start=datetime(2023,2,2,14,00), end=datetime(2023,2,2,18,00)))
shift_list.append(ShiftWidget(start=datetime(2023,2,2,19,00), end=datetime(2023,2,2,20,00)))
shift_list.append(ShiftWidget(start=datetime(2023,2,2,21,00), end=datetime(2023,2,2,23,00)))
