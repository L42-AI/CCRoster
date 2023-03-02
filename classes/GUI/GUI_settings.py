from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QComboBox, QSlider,
                               QLabel, QPushButton, QHBoxLayout,
                               QSizePolicy)
import sys

class Settings(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        settings_label = QLabel("Settings")

        settings_layout = QHBoxLayout()
        settings_layout.addWidget(settings_label)
        settings_layout.setAlignment(Qt.AlignHCenter)
        settings_layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(settings_layout)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = Settings()
    app.show()
    sys.exit(window.exec())