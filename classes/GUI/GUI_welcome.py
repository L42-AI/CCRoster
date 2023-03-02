from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QComboBox, QSlider,
                               QLabel, QPushButton, QHBoxLayout,
                               QSizePolicy)
import sys

class Welcome(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        welcome_label = QLabel("Welcome")

        welcome_layout = QHBoxLayout()
        welcome_layout.addWidget(welcome_label)
        welcome_layout.setAlignment(Qt.AlignHCenter)
        welcome_layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(welcome_layout)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = Welcome()
    app.show()
    sys.exit(window.exec())