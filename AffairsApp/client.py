import json

from PyQt6.QtCore import QObject
from Crypto.Util.number import long_to_bytes, bytes_to_long

from NocturneClient import NocturneClient

class Client(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__transport = None
        self.nocturne = NocturneClient()

    @property
    def transport(self):
        return self.__transport

    def connection_made(self, transport):
        print(f'Connection established with {transport.get_extra_info("peername")}')
        self.__transport = transport

    def send_message(self, message: bytes):
        self.transport.write(message)

    def data_received(self, data: bytes):

        if data[0:2] == b'\x10\xBB': # server hello
            self.nocturne.setModulus(bytes_to_long(data[2:514])) # n length = 512
            nonce = self.nocturne.makeKey(bytes_to_long(data[514:]))
            nonceLength = long_to_bytes(len(nonce), 2)
            s = b'\x10\xCC' + nonceLength + nonce + long_to_bytes(self.nocturne.getDataToEst())
            self.send_message(s)

        elif data[0:2] == b'\x10\xDD':
            nonceLength = bytes_to_long(data[2:4])
            self.nocturne.setDecipher(data[4:4 + nonceLength])
            if self.nocturne.decipherToString(data[4 + nonceLength:]) == "Connection is established":
                s = b'\x10\xEE' + self.nocturne.cipherString("Connection is established")
                self.send_message(s)

        elif data[0:2] == b'\x20\xBB':
            if data[1:3] == b'\xBB\x11':
                self.mainWindow.registerSignal.emit()
            elif data[1:3] == b'\xBB\x00':
                print(f'Such user exists')

        elif data[0:2] == b'\x30\xBB':
            if data[1:3] == b'\xBB\x11':
                id = self.nocturne.decipherToString(data[3:])
                print(f'User id is: {id}')
                self.mainWindow.loginSignal.emit(id)
            elif data[1:3] == b'\xBB\x00':
                print('Wrong login or password')

        elif data[0:2] == b'\x40\xBB':
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            print(f'Echoed: {data["echo"]}')

        elif data[0:2] == b'\x50\xBB':
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            self.mainWindow.catalogueFill.emit(data)

        elif data[0:2] == b'\x51\xBB':
            self.mainWindow.messagesAdd.emit(
                json.loads(self.nocturne.decipherToString(data[2:])))

        elif data[0:2] == b'\x60\xBB': # get messages
            self.mainWindow.messagesFill.emit(
                json.loads(self.nocturne.decipherToString(data[2:])))
            
        elif data[0:2] == b'\x61\xBB': # get new messages
            self.mainWindow.messagesAdd.emit(
                json.loads(self.nocturne.decipherToString(data[2:])))
        
        elif data[0:2] == b'\x70\xBB': # notification
            self.mainWindow.recieveNotification.emit(
                json.loads(self.nocturne.decipherToString(data[2:]))["idFrom"])
            
        elif data[0:2] == b'\x71\xBB': # add name to new user added via notification
            self.mainWindow.renameNewUser.emit(
                json.loads(self.nocturne.decipherToString(data[2:])))
            
        elif data[0:2] == b'\x80\xBB':
            self.mainWindow.addNewDialog.emit(
                json.loads(self.nocturne.decipherToString(data[2:])))

    def setMainWindow(self, mW):
        self.mainWindow = mW

    def register(self, login: str, password: str):
        jsonMsg = {
            "login": login,
            "password": password
        }
        msg = b'\x20\xAA' + self.nocturne.cipherString(json.dumps(jsonMsg))
        self.transport.write(msg)

    def login(self, login: str, password: str):
        jsonMsg = {
            "login": login,
            "password": password
        }
        msg = b'\x30\xAA' + self.nocturne.cipherString(json.dumps(jsonMsg))
        self.transport.write(msg)

    def echo(self, message: str):
        msg = b'\x40\xAA' + self.nocturne.cipherString(message)
        self.transport.write(msg)

    def getUsersForFill(self):
        self.transport.write(b'\x50\xAA')

    def getMessages(self, id: int):
        msg = {
            "id": id
        }
        self.transport.write(b'\x60\xAA' + self.nocturne.cipherString(json.dumps(msg)))

    def getOnlyUnreadMessages(self, id: int):
        msg = {
            "id": id
        }
        self.transport.write(b'\x61\xAA' + self.nocturne.cipherString(json.dumps(msg)))
    
    def markAsReaded(self, l: list):
        self.transport.write(b'\x62\xAA' + self.nocturne.cipherString(json.dumps(l)))

    def sendMessage(self, idTo: int, message: str):
        msg = {
            "idTo": idTo,
            "message": message
        }
        self.transport.write(b'\x70\xAA' + self.nocturne.cipherString(json.dumps(msg)))

    def newUser(self, username: str):
        msg = {
            "login": username
        }
        self.transport.write(b'\x80\xAA' + self.nocturne.cipherString(json.dumps(msg)))
        
    def getNameForNewUser(self, id: int):
        msg = {
            "id": id
        }
        s = b'\x71\xAA' + self.nocturne.cipherString(json.dumps(msg))
        self.transport.write(s)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)
