from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QComboBox, QSlider,
                               QLabel, QPushButton, QHBoxLayout,
                               QSizePolicy)
import sys

from classes.representation.generator import Generator
from classes.representation.controller import Controller

class Generate(QWidget):
    def __init__(self, con: Controller, parent=None) -> None:
        super().__init__(parent)

        self.Controller = con

        generate_label = QLabel("Generate")
        generate_button = QPushButton("Generate")

        generate_button.clicked.connect(self.generate)

        weight_layout = QHBoxLayout()
        weight_layout.setAlignment(Qt.AlignHCenter)
        weight_layout.setAlignment(Qt.AlignVCenter)
        weight_layout.addWidget(generate_label)
        self.setLayout(weight_layout)

    def generate(self):
        self.Generator = Generator(self.Controller)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = Generate()
    app.show()
    sys.exit(window.exec())