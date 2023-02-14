from classes.GUI.GUI_test2 import ScheduleWidget
from PySide2.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab1 = ScheduleWidget()
    tab1.show()
    sys.exit(app.exec_())