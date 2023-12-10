from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random.random import getrandbits
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

class NocturneClient:
    
    def __init__(self):
        self.__b = getrandbits(1024)
        self.signature = pkcs1_15.new(
            RSA.import_key(
            open("publicAffairsKey.pem").read()))
    
    def setModulus(self, n):
        self.__n = n
  
    def getDataToEst(self) -> int:
        y = pow(2, self.__b, self.__n)
        return y
 
    def makeKey(self, x):
        keyMask = pow(x, self.__b, self.__n)
        h = SHA256.new()
        h.update(keyMask.to_bytes(keyMask.bit_length()))
        self.__digest = h.digest()
        self.__cipher = AES.new(self.__digest, AES.MODE_EAX)
        return self.__cipher.nonce

    def setDecipher(self, fNonce):
        self.__decipher = AES.new(self.__digest, AES.MODE_EAX, fNonce)
   
    def cipherString(self, message: str):
        return self.__cipher.encrypt(message.encode())
  
    def cipherBytes(self, message: bytes):
        return self.__cipher.encrypt(message)
    
    def decipherToString(self, message: bytes) -> str:
        return self.__decipher.decrypt(message).decode()
   
    def decipherToBytes(self, message: bytes) -> bytes:
        return self.__decipher.decrypt(message)

    def verifySignature(self, message: bytes, signature: bytes) -> bool:
        hasher = SHA256.new()
        hasher.update(message)
        try:
            self.signature.verify(hasher, signature)
            return True
        except:
            return False
