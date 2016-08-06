from matasano import *

try:
	print(pkcs7_unpad(b"ICE ICE BABY\x04\x04\x04\x04"))
except:
	print("Bad padding")
	
try:
	print(pkcs7_unpad(b"ICE ICE BABY\x05\x05\x05\x05"))
except:
	print("Bad padding")
	
try:
	print(pkcs7_unpad(b"ICE ICE BABY\x01\x02\x03\x04"))
except:
	print("Bad padding")