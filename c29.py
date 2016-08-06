from matasano import *
import struct

key = bytes([randint(97,122) for i in range(16)])
message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
mac = keyed_mac(message,key,sha1())

#Extend message
l = 8*len(key)+8*len(message)
new_message = message
new_message += b'\x80'
while (len(key)+len(new_message))%64 != 56:
	new_message += b'\x00'
new_message += struct.pack(">Q",l)
l = len(key) + len(new_message)
new_message += b';admin=true'

#Extend mac
a,b,c,d,e = struct.unpack(">LLLLL",mac)
m = sha1(a,b,c,d,e)
m.update(b';admin=true',l)
new_mac = m.digest()

#Verify new mac
assert(keyed_mac(new_message,key,sha1()) == new_mac)
print("Extended OK!")
