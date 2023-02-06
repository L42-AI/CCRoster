from PySide2.QtWidgets import QApplication, QLabel, QTextEdit

app = QApplication([])

text_edit = QTextEdit()
label = QLabel("Hello World!")
text_edit.textChanged.connect(lambda: label.setText(text_edit.toPlainText()))
text_edit.show()
label.show()
app.exec_()
