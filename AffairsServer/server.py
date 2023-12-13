import asyncio
import json
from mysql.connector import connect
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random.random import getrandbits 

from NocturneServer import NocturneServer

class ServerProtocol(asyncio.Protocol):

    def __init__(self, ip, port):
        self.__connection = connect(
        user='affairs', password='affairs', host='localhost', 
        port="2023", db='AffairsBase', charset='utf8')
        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor(buffered=True)
        self.ip = ip
        self.port = port
        self.nocturne = NocturneServer("n.txt")
        self.connection = False

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):

        if data[0:2] == b'\x10\xAA':
            x, n = self.nocturne.getDataToEst()
            s = long_to_bytes(n) + long_to_bytes(x)
            msg = self.nocturne.signMessage(s) + s
            self.transport.write(b'\x10\xBB' + msg)

        elif data[0:2] == b'\x10\xCC': # TODO: try/except
            nonceLength = bytes_to_long(data[2:4])
            nonce = self.nocturne.makeKey(bytes_to_long(data[4 + nonceLength:]))
            self.nocturne.setDecipher(data[4:4 + nonceLength])
            nonceLength = long_to_bytes(len(nonce), 2)
            s = nonceLength + nonce + self.nocturne.cipherString("Connection is established")
            s = self.nocturne.signMessage(s) + s
            self.transport.write(b'\x10\xDD' + s)

        elif data[0:2] == b'\x10\xEE':
            if self.nocturne.decipherToString(data[2:]) == "Connection is established":
                print(True)
                self.connection = True
            else:
                self.transport.close()   

        elif data[0:2] == b'\x20\xAA': # registration
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            sqlQuery = f'SELECT userId FROM Users WHERE login="{data["login"]}";'
            self.__cursor.execute(sqlQuery)

            if self.__cursor.rowcount:                
                self.transport.write(b'\x20\xBB\x00')
                return

            salt = getrandbits(128) # how many bytes is the question
            shaPass = self.nocturne.shaPassBytes(
                data["password"].encode() + long_to_bytes(salt))
            shaPass = self.nocturne.shaPass(
                shaPass + data["password"].encode() + long_to_bytes(salt))

            self.__cursor.execute(
                f'''
                INSERT INTO Users 
                (login, passwordHash, salt) 
                VALUES 
                ("{data["login"]}", "{shaPass}", "{salt}");''')
            self.transport.write(b'\x20\xBB\x11')
            
                
        elif data[0:2] == b'\x30\xAA': # login
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            sqlQuery = f'''
            SELECT userId, passwordHash, salt 
            FROM Users
            WHERE 
            login="{data["login"]}";'''
            self.__cursor.execute(sqlQuery)
            if not self.__cursor.rowcount:
                self.transport.write(b'\x30\xBB' + b'\x00')
                return
 
            cursorList = self.__cursor.fetchall()[0]
            self.id = cursorList[0]
            
            shaPass = self.nocturne.shaPassBytes(
                data["password"].encode() + long_to_bytes(int(cursorList[2])))
            shaPass = self.nocturne.shaPass(
                shaPass + data["password"].encode() + long_to_bytes(int(cursorList[2])))

            if not cursorList[1] == shaPass:
                self.transport.write(b'\x30\xBB' + b'\x00')
                return
            
            self.transport.write(
                b'\x30\xBB' + b'\x11' + self.nocturne.cipherString(str(self.id)))
            idToServerInstance[self.id] = self

        elif data[0:2] == b'\x50\xAA': # update dockWidget
            self.__cursor.execute(f'SELECT DISTINCT idFrom, login FROM Messages INNER JOIN Users ON Messages.idFrom = Users.userId WHERE idTo ="{self.id}";')
            l1 = self.__cursor.fetchall()
            self.__cursor.execute(f'SELECT DISTINCT idTo, login FROM Messages INNER JOIN Users ON Messages.idTo = Users.userId WHERE idFrom ="{self.id}";')
            l2 = self.__cursor.fetchall()
            l1 = dict.fromkeys(l1+l2).keys()
            listToSend = []
            for tup in l1:
                listToSend.append({"id": tup[0], "name": tup[1]})
            msg = b'\x50\xBB' + self.nocturne.cipherString(json.dumps(listToSend))
            self.transport.write(msg)

        elif data[0:2] == b'\x51\xCC':
            pass

        elif data[0:2] == b'\x60\xAA': # get messages
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            #  sendTime >= ( {data["sendTime"]} - INTERVAL 3 DAY ) TODO in 0.0.2
            self.__cursor.execute(f'''SELECT Messages.messageId, idFrom, sendTime, message, isRead 
                                      FROM Messages 
                                      INNER JOIN MessageText 
                                      ON Messages.messageId = MessageText.messageId
                                      WHERE idFrom = {self.id} AND idTo = {data["id"]} OR idFrom = {data["id"]} AND idTo = {self.id};
                                      ''')
            l = self.__cursor.fetchall()
            listToSend = []
            for row in l:
                listToSend.append({
                    "messageId": row[0],
                    "isSelf": 1 if row[1] == self.id else 0,
                    "sendTime": row[2],
                    "message": row[3],
                    "isRead": row[4]
                })
            msg = b'\x60\xBB' + self.nocturne.cipherString(json.dumps(listToSend, default=str))
            self.transport.write(msg)
            
        elif data[0:2] == b'\x61\xAA': # get unread(!) messages from id
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            self.__cursor.execute(f'''SELECT Messages.messageId, idFrom, sendTime, message, isRead 
                                      FROM Messages 
                                      INNER JOIN MessageText 
                                      ON Messages.messageId = MessageText.messageId 
                                      WHERE 
                                      idFrom = {data["id"]} AND idTo = {self.id} 
                                      AND 
                                      isRead = 0;
                                      ''')
            l = self.__cursor.fetchall()
            if not len(l): # temporary
                return
            listToSend = []
            for row in l:
                listToSend.append({
                    "messageId": row[0],
                    "isSelf": 0,
                    "sendTime": row[2],
                    "message": row[3],
                    "isRead": row[4]
                })
            msg = b'\x61\xBB' + self.nocturne.cipherString(json.dumps(listToSend, default=str))
            self.transport.write(msg)

        elif data[0:2] == b'\x62\xAA': # mark as readed
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            print(data)
            for elem in data: # TODO executemany
                self.__cursor.execute(f'''UPDATE Messages 
                                          SET isRead=1 
                                          WHERE messageId = {elem["messageId"]};''')
                self.__connection.commit() # TODO send notif that is readed

        elif data[0:2] == b'\x70\xAA': # send message
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            self.__cursor.execute(f'INSERT INTO Messages (idFrom, idTo, sendTime, isRead) VALUES \
                                  ({self.id}, {data["idTo"]}, NOW(), 0)')
            self.__cursor.execute(f'INSERT INTO MessageText (messageId, message) VALUES \
                                  (LAST_INSERT_ID(), "{data["message"]}")')
            self.__connection.commit()

            # temporary decision (?)

            self.__cursor.execute(f'''SELECT Messages.messageId, sendTime 
                                      FROM Messages 
                                      WHERE Messages.messageId = LAST_INSERT_ID();
                                      ''')
            row = self.__cursor.fetchall()[0]
            listToSend = [
                {
                    "messageId": row[0],
                    "isSelf": 1,
                    "sendTime": row[1],
                    "message": data["message"],
                    "isRead": 0
                }
            ]
            msg = b'\x61\xBB' + self.nocturne.cipherString(json.dumps(listToSend, default=str))
            self.transport.write(msg)

            if int(data["idTo"]) in idToServerInstance:
                asyncio.create_task(idToServerInstance[int(data["idTo"])].
                                    notifyUser(self.id))
        
        elif data[0:2] == b'\x71\xAA':
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            self.__cursor.execute(f'SELECT login from Users where userId = {data["id"]};')
            row = self.__cursor.fetchall()[0]
            msg = {
                "id": data["id"],
                "name": row[0]
            }
            msg = b'\x71\xBB' + self.nocturne.cipherString(json.dumps(msg, default=str))
            self.transport.write(msg)

        elif data[0:2] == b'\x80\xAA':
            data = json.loads(self.nocturne.decipherToString(data[2:]))
            self.__cursor.execute(f'SELECT userId from Users where login = "{data["login"]}";')
            row = self.__cursor.fetchall()
            if not len(row):
                return
            row = row[0]
            msg = {
                "id": row[0], 
                "name": data["login"]
            }
            msg = b'\x80\xBB' + self.nocturne.cipherString(json.dumps(msg, default=str))
            self.transport.write(msg)

        elif data[0:2] == b'\x40\xAA': # echo (test thing)
            if not self.connection:
                raise RuntimeError
            income = self.nocturne.decipherToString(data[2:])
            jsonMessage = {
                "echo": income
            }
            msg = b'\x40\xBB' + self.nocturne.cipherString(json.dumps(jsonMessage))
            self.transport.write(msg)

        elif (data[0:3] == b'\xEE\xEE\xEE\r\n'):
            print('Close the client socket')
            self.transport.close()

    def connection_lost(self, exc: Exception | None):
        if self.id in idToServerInstance:
            del idToServerInstance[self.id]
        print(f'Server closed session for {self.transport.get_extra_info("peername")}')
        return super().connection_lost(exc)
    
    async def notifyUser(self, idFrom: int): # TODO
        jsonMessage = {
                "idFrom": idFrom
            }
        msg = b'\x70\xBB' + self.nocturne.cipherString(json.dumps(jsonMessage, default=str))
        self.transport.write(msg)

async def main():
    print(f'Server application is up and running')

    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ServerProtocol('127.0.0.1', 8888),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


idToServerInstance = {}

asyncio.run(main())
