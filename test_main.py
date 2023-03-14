from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    window = QApplication(sys.argv)
    from classes.GUI.GUI_shiftsheet import ShiftSheet
    app = ShiftSheet()
    app.show()
    sys.exit(window.exec())
