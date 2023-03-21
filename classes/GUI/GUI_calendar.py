import sys
from PySide6.QtWidgets import QApplication, QWidget, QCalendarWidget, QPushButton, \
							QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QTextCharFormat, QIcon
import datetime

class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.start_date = None
        self.end_date = None

        self.selected_dates = []

        self.highlighter_format = QTextCharFormat()
        
        self.highlighter_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlighter_format.setForeground(self.palette().color(QPalette.HighlightedText))

        # this will pass selected date value as a QDate object
        self.clicked.connect(self.select_range)

        super().dateTextFormat()

    def highlight_range(self, format):
        if self.start_date and self.end_date:
            d1 = min(self.start_date, self.end_date)
            d2 = max(self.start_date, self.end_date)
            while d1 <= d2:
                self.setDateTextFormat(d1, format)
                self.selected_dates.append(d1)
                d1 = d1.addDays(1)
        else:
            [self.setDateTextFormat(date, QTextCharFormat()) for date in self.selected_dates]
            self.selected_dates.clear()


    def select_range(self, date_value):
        # check if a keyboard modifer is pressed
        if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.start_date:
            self.end_date = date_value
            # print(self.start_date, self.end_date)
            self.highlight_range(self.highlighter_format)
        else:
            # required
            self.start_date = date_value	
            self.end_date = None

        self.highlight_range(self.highlighter_format)
    
    def export_date_list(self) -> list[datetime.date]:
            return [datetime.date(qdate.year(), qdate.month(), qdate.day()) for qdate in self.selected_dates]