from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout

class Dialog(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.__message = QTextEdit(self)
        sendButton = QPushButton('Отправить', self)
        sendButton.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.__message)
        layout.addWidget(sendButton)
        self.setLayout(layout)

    def getData(self):
        return self.__message.toPlainText()