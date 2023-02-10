import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QFormLayout, QLabel, QPushButton, QTextEdit

class EmployeeForm(QDialog):
    def __init__(self, parent=None):
        super(EmployeeForm, self).__init__(parent)
        
        self.employee_names = []
        self.employee_availabilities = []
        
        self.setWindowTitle("Employee Availability")
        
        self.employee_name_input = QLineEdit()
        self.employee_availability_start = QLineEdit()
        self.employee_availability_finish = QLineEdit()
        
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Employee Name:"), self.employee_name_input)
        form_layout.addRow(QLabel("Availability:"), self.employee_availability_start, QLabel("-"), self.employee_availability_finish)
        
        add_button = QPushButton("Add Employee")
        add_button.clicked.connect(self.add_employee)
        
        form_layout.addRow(add_button)
        
        self.employee_overview = QTextEdit()
        self.employee_overview.setReadOnly(True)
        form_layout.addRow(self.employee_overview)
        
        self.setLayout(form_layout)
        
    def add_employee(self):
        employee_name = self.employee_name_input.text()
        employee_availability_start = self.employee_availability_start.text()
        employee_availability_finish = self.employee_availability_finish.text()
        
        self.employee_names.append(employee_name)
        self.employee_availabilities.append((employee_availability_start, employee_availability_finish))
        
        self.employee_name_input.clear()
        self.employee_availability_start.clear()
        self.employee_availability_start.clear()
        
        self.update_employee_overview()
        
    def update_employee_overview(self):
        overview = ""
        for i in range(len(self.employee_names)):
            overview += f"{self.employee_names[i]} - {self.employee_availabilities[i]}\n"
        self.employee_overview.setText(overview)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EmployeeForm()
    form.show()
    sys.exit(app.exec_())
