from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QGridLayout, QScrollArea, QDialog)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPen, QPainter, QPalette, QBrush
from datetime import datetime, time
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
            if widget.time == Shift.start.time():
                index = self.shift_grid.indexOf(widget)
                row, col, _, colspan = self.shift_grid.getItemPosition(index)
                print(row, col, _, colspan)
                shift_duration_minutes = (Shift.end - Shift.start).total_seconds() / 60
                rowspan = int(shift_duration_minutes / 15) + 1
                self.shift_grid.addWidget(Shift, row , col, rowspan, colspan)

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


    def add_shift_widget(self):
        # Create blue widget
        label = self.sender()
        Shift = ShiftWidget(self)
        index = self.shift_grid.indexOf(label)
        row, col, _, colspan = self.shift_grid.getItemPosition(index)
        shift_duration_minutes = (Shift.end - Shift.start).total_seconds() / 60
        rowspan = int(shift_duration_minutes / 15)
        self.shift_grid.addWidget(Shift, row + 1, col, rowspan, colspan)

class ShiftWidget(QWidget):
    clicked = Signal()

    def __init__(self, start, end, parent=None) -> None:
        super().__init__(parent)
        self.setContentsMargins(0,0,0,0)

        self.setStyleSheet("background-color: lightblue;")

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

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        layout.addWidget(time_label)
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
