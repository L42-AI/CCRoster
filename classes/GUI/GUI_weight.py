from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QComboBox, QSlider,
                               QLabel, QPushButton, QHBoxLayout,
                               QSizePolicy)
import sys

class Weight(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        weight_label = QLabel("Weight")

        weight_layout = QHBoxLayout()
        weight_layout.setAlignment(Qt.AlignHCenter)
        weight_layout.setAlignment(Qt.AlignVCenter)
        weight_layout.addWidget(weight_label)
        self.setLayout(weight_layout)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = Weight()
    app.show()
    sys.exit(window.exec())