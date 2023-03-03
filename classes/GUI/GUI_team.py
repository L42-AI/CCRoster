from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QComboBox, QSlider,
                               QLabel, QPushButton, QHBoxLayout,
                               QSizePolicy)
import sys
from classes.representation.communicator import Communicator
from data.assign import employee_list

class EmployeeMatch(QWidget):
    def __init__(self, Com, parent=None) -> None:
        super().__init__(parent)

        self.Com: Communicator = Com

        self.employee_1_combobox = QComboBox()
        self.employee_2_combobox = QComboBox()

        for employee in sorted([employee.name for employee in employee_list]):
            self.employee_1_combobox.addItem(employee)
            self.employee_2_combobox.addItem(employee)

        self.score_slider = QSlider()
        self.score_slider.setOrientation(Qt.Horizontal)
        self.score_slider.setRange(-10, 10)
        self.score_slider.valueChanged.connect(self.on_slider_value_changed)

        self.score_label = QLabel("0")

        self.create_relation_button = QPushButton("Add Relation")
        self.create_relation_button.clicked.connect(self.create_relation)

        # Employee selector layout
        employee_layout = QHBoxLayout()
        employee_layout.addWidget(self.employee_1_combobox)
        employee_layout.addWidget(self.employee_2_combobox)

        # Score layout
        score_layout = QHBoxLayout()
        score_layout.addWidget(self.score_slider)
        score_layout.addWidget(self.score_label)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_relation_button)

        # Create the top layout
        self.top_section_layout = QVBoxLayout()

        top_section_widget = QWidget()
        top_section_widget.setLayout(self.top_section_layout)
        top_section_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_section_widget.setMinimumSize(top_section_widget.sizeHint())

        # Create the bottom layout
        bottom_section_layout = QVBoxLayout()
        bottom_section_layout.addLayout(employee_layout)
        bottom_section_layout.addLayout(score_layout)
        bottom_section_layout.addLayout(button_layout)

        bottom_section_widget = QWidget()
        bottom_section_widget.setLayout(bottom_section_layout)
        bottom_section_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bottom_section_widget.setMinimumSize(bottom_section_widget.sizeHint())

        # Put into complete layout
        layout = QVBoxLayout()
        layout.addWidget(top_section_widget)
        layout.addWidget(bottom_section_widget)

        # Set Layout
        self.setLayout(layout)

    def on_slider_value_changed(self, value):

        self.score_label.setText(f"{value}")

        color = self.__get_color(value)

        self.score_label.setStyleSheet(f"color: {color}")

    def create_relation(self):
        employee_1, employee_2, slider_value = self.__get_widget_state()

        color = self.__get_color(slider_value)

        employee_1_widget = QLabel(employee_1)
        employee_1_widget.setStyleSheet(f"color: {color}")

        intermezo_label = QLabel('<--->')
        intermezo_label.setStyleSheet(f"color: {color}")

        employee_2_widget = QLabel(employee_2)
        employee_2_widget.setStyleSheet(f"color: {color}")

        score_label = QLabel(f'{slider_value}')
        score_label.setStyleSheet(f"color: {color}")

        delete_button = QPushButton('D')
        delete_button.clicked.connect(self.delete_relation)
        delete_button.setFixedWidth(25)

        relation_layout = QHBoxLayout()
        relation_layout.addWidget(QLabel(f'{self.top_section_layout.count() + 1}.'))
        relation_layout.addWidget(employee_1_widget)
        relation_layout.addWidget(intermezo_label)
        relation_layout.addWidget(employee_2_widget)
        relation_layout.addWidget(score_label)
        relation_layout.addWidget(delete_button)

        self.top_section_layout.addLayout(relation_layout)

        self.__clear_widget_state()

    def delete_relation(self):
        for relation_num in range(self.top_section_layout.count()):

            relation_layout = self.top_section_layout.itemAt(relation_num)

            if relation_layout == None:
                continue

            if self.sender() == relation_layout.itemAt(5).widget():
                self.__delete_layout_content(relation_layout)
                self.top_section_layout.removeItem(relation_layout)

        self.__reset_relation_labels()

    def __reset_relation_labels(self) -> None:
        for relation_num in range(self.top_section_layout.count()):

            relation_layout = self.top_section_layout.itemAt(relation_num)

            if relation_layout == None:
                continue

            label = relation_layout.itemAt(0).widget()
            label.setText(f'{relation_num + 1}.')

    def __delete_layout_content(self, layout: QHBoxLayout) -> None:
        # While child widgets
        while layout.count() > 0:

            # Find widget and delete
            widget = layout.takeAt(0).widget()
            widget.deleteLater()

        # Delete layout
        layout.deleteLater()

    def __get_color(self, value: int) -> tuple:

        if value < 0:
            color = 'red'
        elif value == 0:
            color = 'black'
        else:
            color = 'green'

        return color

    def __get_widget_state(self) -> tuple:
        employee_1 = self.employee_1_combobox.currentText()
        employee_2 = self.employee_2_combobox.currentText()
        slider_value = self.score_slider.value()

        return employee_1, employee_2, slider_value

    def __clear_widget_state(self) -> None:
        self.employee_1_combobox.setCurrentText('None')
        self.employee_2_combobox.setCurrentText('None')
        self.score_slider.setValue(0)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = EmployeeMatch()
    app.show()
    sys.exit(window.exec())