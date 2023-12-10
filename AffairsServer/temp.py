import json


b = b'abcdefg'
msg = {
    "message": b
}
s = json.dumps(msg, default=str).encode()
print(s)
d = json.loads(s.decode())
print(d["message"])