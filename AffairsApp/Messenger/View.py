from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor

from PyToggles.MDS__Catalogue import MDS__Catalogue
from PyToggles.MDS__PushButton import MDS__PushButton
from PyToggles.MDS__MessageDisplay import MDS__MessageDisplay
from PyToggles.MDS__TextEdit import MDS__TextEdit
from PyToggles.MDS__Dialog import MDS__Dialog

from .Model import Model

class View(QWidget):
    getMessages = pyqtSignal(int)
    sendMessageViaTextEdit = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.setObjectName("View")

        self.sendMessageViaTextEdit.connect(self.sendMessage)

        self.__messageList = MDS__MessageDisplay(self)
        self.__messageList.setObjectName("messageList")

        self.__catalogue = MDS__Catalogue(self)
        self.__catalogue.setMaximumWidth(200)
        self.__catalogue.setObjectName("catalogue")
        
        self.__messageDisplayModel = Model(parent.protocol, self.__catalogue, self.__messageList)

        self.newMessageButton = MDS__PushButton('Новый диалог',
                                                 width=200,
                                                 height=50,
                                                 radius=0,
                                                 bgColor="#025167",
                                                 hoverColor="#39AECF",
                                                 parent=self)
        
        self.newMessageButton.clicked.connect(self.newMessageToUser)
        layout = QGridLayout(self)
        layout.setRowMinimumHeight(2, 100)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.__messageList, 0, 0, 2, 1)
        layout.addWidget(self.newMessageButton, 0, 1)
        layout.addWidget(self.__catalogue, 1, 1, 2, 1)
        self.__messageEdit = MDS__TextEdit(self)
        self.__messageEdit.setFixedWidth(300)
        self.__messageEdit.setMaximumHeight(100)

        self.__messageEdit.setObjectName("messageEdit");
        
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.__messageEdit, alignment=Qt.AlignmentFlag.AlignCenter)
        sendButton = MDS__PushButton('Отправить', 100, 20,
                                     bgColor="#025167",
                                     hoverColor="#39AECF",
                                     parent=self)
        sendButton.clicked.connect(self.sendMessage)
        bottomLayout.addWidget(sendButton, 
                               alignment=
                               Qt.AlignmentFlag.AlignHCenter 
                               | 
                               Qt.AlignmentFlag.AlignBottom)

        layout.addLayout(bottomLayout, 2, 0, Qt.AlignmentFlag.AlignHCenter)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
    
    @property
    def messageDisplayModel(self):
        return self.__messageDisplayModel

    @pyqtSlot()
    def newMessageToUser(self):
        dialog = MDS__Dialog('Введите имя пользователя', self)
        if not dialog.exec():
            self.__messageDisplayModel.dealWithNewUser(dialog.getData())

    @pyqtSlot()
    def sendMessage(self):
        text = self.__messageEdit.toPlainText()
        if len(text):
            self.__messageDisplayModel.dealWithMessage(text)
            self.__messageEdit.clear()
