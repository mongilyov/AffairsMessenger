from PyQt6.QtWidgets import QMenuBar 

class MainMenu(QMenuBar):
    def __init__(self, parent = None):
        super().__init__(parent)

        sendMenu = self.addMenu('Send')
        helpMenu = self.addMenu('Help')  
        
        self.__about = helpMenu.addAction('О программе...')
        self.__aboutQt = helpMenu.addAction('О библиотеке Qt...')
        self.__sendEchoedMessage = sendMenu.addAction('Отправить echo-запрос')

    @property
    def about(self):
        return self.__about
    
    @property
    def aboutQt(self):
        return self.__aboutQt
    
    @property
    def sendEchoedMessage(self):
        return self.__sendEchoedMessage;