import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget, QDialog)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Scheduling")
        self.setGeometry(100, 100, 800, 600)

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QDialog()
        self.tabs.addTab(self.tab1, "Dienst Uren")

        self.time_slots = []

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

        layout = QVBoxLayout()
        layout.addWidget(self.time_slot_list)
        layout.addWidget(self.start_time_label)
        layout.addWidget(self.start_time_edit)
        layout.addWidget(self.end_time_label)
        layout.addWidget(self.end_time_edit)
        layout.addLayout(button_layout)

        self.tab1.setLayout(layout)

        # Tab 2: Assign Employees
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Assign Employees")
        self.tab2_layout = QVBoxLayout(self.tab2)

        self.employee_grid = QGridLayout()
        self.tab2_layout.addLayout(self.employee_grid)

        self.employee_names = []
        self.employee_availability = {}

        self.add_employee_layout = QHBoxLayout()
        self.employee_name_input = QLineEdit()
        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee)
        self.add_employee_layout.addWidget(QLabel("Employee Name:"))
        self.add_employee_layout.addWidget(self.employee_name_input)
        self.add_employee_layout.addWidget(self.add_employee_button)
        self.tab2_layout.addLayout(self.add_employee_layout)

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
