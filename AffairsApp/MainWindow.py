from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFontDatabase

from Authorization import Menu, Login, Register
from MainMenu import MainMenu
from Dialog import Dialog

import Messenger

class MainWindow(QMainWindow):

    loginSignal = pyqtSignal(str)
    registerSignal = pyqtSignal()
    catalogueFill = pyqtSignal(list)
    messagesFill = pyqtSignal(list)
    messagesAdd = pyqtSignal(list)
    recieveNotification = pyqtSignal(int)
    addNewDialog = pyqtSignal(dict)
    renameNewUser = pyqtSignal(dict)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)

        self.registerSignal.connect(self.showLogin)
        self.loginSignal.connect(self.showMessengerView)
        self.catalogueFill.connect(self.catalogueWidgetFill)
        self.messagesFill.connect(self.messagesWidgetFill)
        self.messagesAdd.connect(self.messagesWidgetAdd)
        self.recieveNotification.connect(self.notificationHandler)
        self.addNewDialog.connect(self.addNewDialogInCatalogue)
        self.renameNewUser.connect(self.nameUserInCatalogue)

        self.__menu = Menu(self)

        self.setCentralWidget(self.__menu)

        mainMenu = MainMenu(parent=self)
        self.setMenuBar(mainMenu)

        mainMenu.aboutQt.triggered.connect(self.aboutQt)
        mainMenu.about.triggered.connect(self.about)
        mainMenu.sendEchoedMessage.triggered.connect(self.sendEchoed)

        self.__menu.loginButton.clicked.connect(self.showLogin)
        self.__menu.registerButton.clicked.connect(self.showRegister)

    def setProtocol(self, protocol):
        protocol.setMainWindow(self)
        self.__protocol = protocol
        self.__protocol.send_message(b'\x10\xAA')

    @pyqtSlot()
    def about(self):
        title = 'Мессенджер Affairs'
        text = ('Мессенджер Affairs - безопасная программа\n' +
                'для мгновенного обмена сообщений')
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def aboutQt(self):
        QMessageBox.aboutQt(self, 'Affairs Messanger')

    @pyqtSlot()
    def sendEchoed(self):
        dialog = Dialog(self)
        if not dialog.exec():
            self.__protocol.echo(dialog.getData())

    @property
    def id(self):
        return self.__id

    @pyqtSlot()
    def showLogin(self):
        temp = self.centralWidget()
        self.__login = Login(isinstance(temp, Register), self)
        
        self.__login.backButton.clicked.connect(self.backButton)
        self.setCentralWidget(self.__login)
        if temp is not None:
            temp.deleteLater()

    @pyqtSlot()
    def showRegister(self):
        temp = self.centralWidget()
        self.__register = Register(self)

        self.__register.backButton.clicked.connect(self.backButton)
        self.setCentralWidget(self.__register)
        if temp is not None:
            temp.deleteLater()

    @pyqtSlot()
    def backButton(self):
        temp = self.centralWidget()
        self.__menu = Menu(self)
        self.__menu.loginButton.clicked.connect(self.showLogin)
        self.__menu.registerButton.clicked.connect(self.showRegister)
        self.setCentralWidget(self.__menu)
        if temp is not None:
            temp.deleteLater()

    @pyqtSlot(str)
    def showMessengerView(self, id):
        self.__id = id
        temp = self.centralWidget()
        self.__view = Messenger.View(self)
        self.setCentralWidget(self.__view)
        if temp is not None:
            temp.deleteLater()

    @property
    def protocol(self):
        return self.__protocol

    @pyqtSlot(list)
    def catalogueWidgetFill(self, l: list):
        self.__view.messageDisplayModel.fillCatalogue(l)

    @pyqtSlot(list)
    def messagesWidgetFill(self, l: list):
        self.__view.messageDisplayModel.fillMessagesDisplay(l)

    @pyqtSlot(list)
    def messagesWidgetAdd(self, l: list):
        self.__view.messageDisplayModel.addNewMessagesToUser(l)

    @pyqtSlot(int)
    def notificationHandler(self, idFrom: int):
        self.__view.messageDisplayModel.dealWithNotification(idFrom)

    @pyqtSlot(dict)
    def addNewDialogInCatalogue(self, msg: dict):
        self.__view.messageDisplayModel.addNewToCatalogue(msg)

    @pyqtSlot(dict)
    def nameUserInCatalogue(self, msg: dict):
        self.__view.messageDisplayModel.nameUserInCatalogue(msg)
