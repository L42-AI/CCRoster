from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QWidget, QListWidget, QComboBox,
                               QGridLayout, QScrollArea, QDialog)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPen, QPainter, QPalette, QBrush
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

        # Set the background color and draw lines
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)

    """ Init """

    def create_shift_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(0)

        # Add labels to the grid
        for row in range(5):
            for col in range(96):
                label = ClickableLabel(f"")
                label.position = (row + 1) * (col + 1)
                label.setAlignment(Qt.AlignCenter)
                label.clicked.connect(self.add_blue_widget_to_cell)
                grid.addWidget(label, row, col)

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

                painter.drawLine(x, y, x + width, y)

                if row == grid.rowCount() - 1:
                    painter.drawLine(x, y + height, x + width, y + height)

    def dot_gray_lines(self, painter: QPainter, grid: QGridLayout)-> None:
        width = grid.cellRect(0, 0).width()
        height = grid.cellRect(0, 0).height()

        for row in range(grid.rowCount()):
            for col in range(grid.columnCount()):

                x = grid.cellRect(row, col).x()
                y = grid.cellRect(row, col).y()

                if col == 0 or col % 12 == 0:
                    painter.setPen(QPen(Qt.gray, 3, Qt.DotLine))
                elif col % 4 == 0:
                    painter.setPen(QPen(Qt.gray, 2, Qt.DotLine))
                else:
                    painter.setPen(QPen(Qt.gray, 1, Qt.DotLine))

                painter.drawLine(x, y, x , y + height)

                if col == grid.columnCount() - 1:
                    painter.setPen(QPen(Qt.gray, 3, Qt.DotLine))
                    painter.drawLine(x + width, y, x + width, y + height)


    def add_blue_widget_to_cell(self):
        # Create blue widget
        label = self.sender()
        blue_widget = OptionWidget(self)
        print(blue_widget.pos())
        blue_widget.setStyleSheet("background-color: magenta;")
        index = self.shift_grid.indexOf(label)
        row, col, rowspan, colspan = self.shift_grid.getItemPosition(index)
        self.shift_grid.addWidget(blue_widget, row, col, rowspan, colspan)

        # Make the blue widget draggable horizontally
        blue_widget.setMouseTracking(True)
        blue_widget.mousePressEvent = self.start_drag
        # blue_widget.mouseMoveEvent = self.do_drag
        # blue_widget.mouseReleaseEvent = self.end_drag

    def start_drag(self, event):
        # print(self)
        print('EVENT POSITION')
        print(event.pos())
        self.dragged_widget = self.sender()
        print(self.dragged_widget)
        self.dragged_widget.mouse_pos = event.pos()
        print(event)
        self.dragged_widget.start_colspan = self.shift_grid.columnSpan(self.shift_grid.indexOf(self.dragged_widget))[1]

    def do_drag(self, event):
        if not hasattr(self, 'dragged_widget'):
            return

        widget = self.dragged_widget
        delta = event.pos() - widget.mouse_pos

        # Calculate the new geometry of the widget after drag
        new_geometry = widget.geometry()
        new_geometry.setLeft(new_geometry.left() + delta.x())
        new_geometry.setRight(new_geometry.right() + delta.x())

        # Find the columns that the widget is intersecting with
        cell_width = self.shift_grid.cellRect(0, 0).width()
        col_start = max(0, (new_geometry.left() // cell_width) - widget.start_col)
        col_end = max(0, (new_geometry.right() // cell_width) - widget.start_col)

        # Update the column span of the widget to span the intersecting columns
        new_colspan = widget.start_colspan + col_end - col_start
        self.shift_grid.addWidget(widget, self.shift_grid.row(widget), widget.start_col, 1, new_colspan)

        # Update the geometry of the widget and its mouse position
        new_geometry.setLeft(widget.start_col * cell_width)
        new_geometry.setRight((widget.start_col + new_colspan) * cell_width)
        widget.setGeometry(new_geometry)
        widget.mouse_pos = event.pos()

    def end_drag(self, event):
        pass

class OptionWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.setStyleSheet("background-color: lightblue;")
        self.setContentsMargins(0,0,0,0)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(QLabel(''))

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def show_info(self, time, role):
        dialog = QDialog()
        layout = QVBoxLayout()

        time_label = QLabel(f"Time: {time}")
        role_label = QLabel(f"Role: {role}")

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.deleteLater)

        layout.addWidget(time_label)
        layout.addWidget(role_label)
        layout.addWidget(delete_button)

        dialog.setLayout(layout)
        dialog.exec()

class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)