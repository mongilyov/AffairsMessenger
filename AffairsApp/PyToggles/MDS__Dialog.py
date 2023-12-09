from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout

class MDS__Dialog(QDialog):

    def __init__(self, titleText: str, parent = None):
        super().__init__(parent)

        label = QLabel(titleText, self)
        self.__message = QLineEdit(self)
        sendButton = QPushButton('Выбрать этого пользователя', self)
        sendButton.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.__message)
        layout.addWidget(sendButton)
        self.setLayout(layout)

    def getData(self):
        return self.__message.text()