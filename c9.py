from matasano import *

print(pkcs7_pad("YELLOW SUBMARINE".encode('ascii'),20).decode('ascii'))