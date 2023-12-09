from PyQt6.QtCore import Qt, QSize, pyqtSlot, QRect, QPropertyAnimation
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QFont, QPainter, QColor

from PyToggles.MDS__PushButton import MDS__PushButton
from PyToggles.Lable import Label
from PyToggles.MDS__LineEdit import MDS__LineEdit

class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        logo = QLabel('Affairs', self)
        logo.setFont(QFont('Academy Engraved LET', 150))

        versionLogo = QLabel('verison: 0.0.1 Alpha', self)
        versionLogo.setFont(QFont('Baskerville', 16))

        self.__loginButton = MDS__PushButton('Войти', 
                                             width=175,
                                             height=75,
                                             radius=20,
                                             bgColor="#025167",
                                             hoverColor="#39AECF",
                                             parent=self)
        self.__registerButton = MDS__PushButton('Зарегистрироваться', 
                                                width=175,
                                                height=75,
                                                radius=20,
                                                bgColor="#025167",
                                                hoverColor="#39AECF",
                                                parent=self)
        
        layout = QGridLayout(self)
        layout.addWidget(QWidget(self), 0, 0)
        layout.addWidget(logo, 0, 1, Qt.AlignmentFlag.AlignCenter)

        layout.setRowMinimumHeight(0, 300)
        layout.setRowMinimumHeight(1, 150)
        layout.setRowMinimumHeight(2, 150)

        layout.addWidget(self.__registerButton, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__loginButton, 2, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(versionLogo, 3, 2,
                          Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        
    @property
    def registerButton(self):
        return self.__registerButton
    @property
    def loginButton(self):
        return self.__loginButton
    
    def paintEvent(self, a0) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        grad = QColor(41, 42, 47)
        
        p.setBrush(grad)
        p.drawRect(rect)

        p.end();

class Register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__protocol = parent.protocol

        logo = QLabel('Регистрация', self)
        logo.setFont(QFont('Academy Engraved LET', 100))

        self.__registerEdit = MDS__LineEdit(focusColor=QColor(50, 50, 58))
        self.__passEdit = MDS__LineEdit(mode="password",
                                        focusColor=QColor(50, 50, 58))

        self.__backButton = MDS__PushButton('Назад', 
                                             width=175,
                                             height=75,
                                             radius=20,
                                             bgColor="#025167",
                                             hoverColor="#39AECF",
                                             parent=self)
        self.__sendButton = MDS__PushButton('Зарегистрироваться', 
                                             width=175,
                                             height=75,
                                             radius=20,
                                             bgColor="#025167",
                                             hoverColor="#39AECF",
                                             parent=self)
        self.__sendButton.clicked.connect(self.register)
        
        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 300)
        layout.setColumnMinimumWidth(2, 300)
        layout.setRowMinimumHeight(0, 100)
        layout.setRowMinimumHeight(5, 300)
        layout.addWidget(logo, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__registerEdit, 2, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__passEdit, 3, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__backButton, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__sendButton, 4, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    @pyqtSlot()
    def register(self):
        if (len(self.__registerEdit.text()) == 0 or len(self.__passEdit.text()) == 0):
            return
        self.__protocol.register(self.__registerEdit.text(), self.__passEdit.text())

    @property
    def backButton(self):
        return self.__backButton
    
    def paintEvent(self, a0) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        
        grad = QColor(41, 42, 47)
        p.setBrush(grad)
        p.drawRect(rect)

        p.end();
    
class Login(QWidget):
    def __init__(self, 
                 fromReg,
                 parent=None):
        super().__init__(parent)

        self.__protocol = parent.protocol

        logo = QLabel('Вход', self)
        logo.setFont(QFont('Academy Engraved LET', 100))

        self.__loginEdit = MDS__LineEdit(focusColor=QColor(50, 50, 58))
        self.__passEdit = MDS__LineEdit(mode="password",
                                        focusColor=QColor(50, 50, 58))

        self.__backButton = MDS__PushButton('Назад', 
                                             width=175,
                                             height=75,
                                             radius=20,
                                             bgColor="#025167",
                                             hoverColor="#39AECF",
                                             parent=self)
        self.__sendButton = MDS__PushButton('Войти',
                                             width=175,
                                             height=75,
                                             radius=20,
                                             bgColor="#025167",
                                             hoverColor="#39AECF",
                                             parent=self)
        self.__sendButton.clicked.connect(self.login)
        
        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 300)
        layout.setColumnMinimumWidth(2, 300)
        layout.setRowMinimumHeight(0, 100)
        layout.setRowMinimumHeight(5, 300)
        layout.addWidget(logo, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__loginEdit, 2, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__passEdit, 3, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__backButton, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__sendButton, 4, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        if fromReg:
            regMessage = QLabel('Вы успешно зарегистрировались!', self)
            regMessage.setFont(QFont('Baskerville', 32))
            layout.addWidget(regMessage, 5, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    @pyqtSlot()
    def login(self):
        if (len(self.__loginEdit.text()) == 0 or len(self.__passEdit.text()) == 0):
            return
        self.__protocol.login(self.__loginEdit.text(), self.__passEdit.text())
    
    @property
    def backButton(self):
        return self.__backButton
    
    def paintEvent(self, a0) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)
        rect = QRect(0, 0, self.width(), self.height())

        grad = QColor(41, 42, 47)
        p.setBrush(grad)
        p.drawRect(rect)

        p.end();
