from matasano import *
from base64 import b64decode

print(aes_ctr(b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="),b"YELLOW SUBMARINE",b'\x00'*8))