from PySide6.QtWidgets import QRadioButton, QSizePolicy, QLabel, QVBoxLayout
from PySide6.QtGui import QColor, QPalette, QPainter, QIcon
from PySide6.QtCore import Qt

class NavigationOptions(QRadioButton):
    def __init__(self) -> None:
        super().__init__()

        self.setStyleSheet(
            """
            QRadioButton {
                border: none;
                margin: 0px;
                padding: 0px;
                background-color: rgb(50, 50, 50);
            }
            QRadioButton:hover {
                background-color: rgb(100, 100, 100);
            }
            QRadioButton:checked {
                background-color: rgb(150, 150, 150);
            }
            """
        )

        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(policy)

        # Create the label widget for the icon
        self.icon_label = QLabel()
        self.icon_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Load the icon from the given path
        icon = QIcon()

        # Set the icon to the label
        self.icon_label.setPixmap(icon.pixmap(40, 40))

        # Set the icon to the button
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.icon_label)

        # Set the minimum size for the radio button
        self.setMinimumSize(100, 100)

        self.setAutoExclusive(True)

        # Remove the focus rectangle
        self.setFocusPolicy(Qt.NoFocus)

        # Set the base and hover colors
        self.base_color = QColor(80, 80, 80)
        self.hover_color = QColor(120, 120, 120)
        self.setCheckedColor()

    def setCheckedColor(self):
        if self.isChecked():
            color = self.hover_color
        else:
            color = self.base_color

        palette = self.palette()
        palette.setColor(QPalette.Base, color)
        self.setPalette(palette)

    def enterEvent(self, event):
        self.setCheckedColor()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCheckedColor()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setCheckedColor()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCheckedColor()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isChecked():
            color = self.hover_color
        else:
            color = self.base_color

        painter.fillRect(self.rect(), color)

