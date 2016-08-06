from matasano import *

def xor(a,b):
	return bytes([a[i] ^ b[i] for i in range(min(len(a),len(b)))])
	
a = hex2bytes("1c0111001f010100061a024b53535009181c")
b = hex2bytes("686974207468652062756c6c277320657965")
print(bytes2hex(xor(a,b)))