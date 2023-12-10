from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random.random import getrandbits
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

class NocturneServer:

    def __init__(self, filename: str):
        self.__a = getrandbits(1024)
        with open(filename, "r") as file:
            s = file.read();
            s = s.strip();
            s = s.lower();
            s = s.replace(" ", "")
            s = s.replace("\n", "");
            self.__n = int(s, 16)
        self.signature = pkcs1_15.new(
            RSA.import_key(
            open("privatekey.pem").read()))
    
    def getDataToEst(self):
        x = pow(2, self.__a, self.__n)
        return x, self.__n
  
    def makeKey(self, y: int) -> bytes:
        keyMask = pow(y, self.__a, self.__n)
        h = SHA256.new()
        h.update(keyMask.to_bytes(keyMask.bit_length()))
        self.__digest = h.digest()
        self.__cipher = AES.new(self.__digest, AES.MODE_EAX)
        return self.__cipher.nonce
 
    def setDecipher(self, fNonce: bytes) -> None:
        self.__decipher = AES.new(self.__digest, AES.MODE_EAX, fNonce)

    def cipherString(self, message: str):
        return self.__cipher.encrypt(message.encode()) # TODO: encrypt_and_digest?
  
    def cipherBytes(self, message: bytes):
        return self.__cipher.encrypt(message)
 
    def decipherToString(self, message: bytes) -> str:
        return self.__decipher.decrypt(message).decode()

    def decipherToBytes(self, message: bytes) -> bytes:
        return self.__decipher.decrypt(message)
   
    def shaPass(self, password: bytes) -> str:
        h = SHA256.new(password)
        return h.hexdigest()
    
    def shaPassBytes(self, password: bytes) -> bytes:
        h = SHA256.new(password)
        return h.digest()
  
    def signMessage(self, msg: bytes):
        hasher = SHA256.new(msg)
        return self.signature.sign(hasher)
    