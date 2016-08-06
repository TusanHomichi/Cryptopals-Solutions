from matasano import *

plain = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal".encode('ascii')
print(bytes2hex(rep_xor(plain,"ICE".encode('ascii'))))