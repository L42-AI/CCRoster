import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLabel, QLineEdit, QCheckBox, QPushButton, QWidget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Scheduling")
        self.setGeometry(100, 100, 800, 600)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Tab 1: Create Time Slots
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Create Time Slots")
        self.tab1_layout = QVBoxLayout(self.tab1)
        
        self.timeslots = []
        for i in range(7):
            for j in range(4):
                for k in range(6):
                    self.timeslots.append((i, j, k))
        
        self.labels = []
        for i, slot in enumerate(self.timeslots):
            day, week, time = slot
            label = QLabel(f"Week {week + 1}, Day {day + 1}, Time {time + 1}")
            self.labels.append(label)
            self.tab1_layout.addWidget(label)
        
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
    
    def add_employee():
        pass

if __name__ == "__main__":
    window = QApplication()
    app = MainWindow()
    app.show()
    sys.exit(window.exec_())
