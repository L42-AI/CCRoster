from PySide2.QtWidgets import QApplication, QLabel, QTextEdit, QMainWindow, QPushButton

import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Scheduly")

text_edit = QTextEdit()
label = QLabel("Hello World!")
text_edit.textChanged.connect(lambda: label.setText(text_edit.toPlainText()))

button = QPushButton()
button.setText("Your mom")

text_edit.show()
label.show()
# window.show()
app.exec_()
