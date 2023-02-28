from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QPushButton, QWidget, QListWidget, QDialog, QComboBox,
                               QScrollArea, QCheckBox, QWidgetItem, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
import sys

from GUI_utility import SetNullMargin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)

        self.pages = ['People', 'Schedule', 'Settings', 'Team']

        self.container = QFrame()
        self.container.setObjectName('container')

        self.container_layout = QHBoxLayout()

        self.sidebar = QVBoxLayout()
        self.sidebar = SetNullMargin(self.sidebar)
        self.sidebar.setObjectName('sidebar')
        for i, page in enumerate(self.pages):
            self.page_button = QPushButton()
            self.page_button.setObjectName(page)
            self.page_button.setStyleSheet("#People { background-color: #000 }")
            self.sidebar.addWidget(self.page_button)

        self.container_layout.addLayout(self.sidebar)

        self.container.setLayout(self.container_layout)
        self.setCentralWidget(self.container)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
