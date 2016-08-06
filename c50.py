from matasano import *

key = b"YELLOW SUBMARINE"
iv = b"\x00"*16

orig = b"alert('MZA who was that?');\n"
new = b"alert('Ayo, the Wu is back!');//"
#Find padding block
pad = xor(cbc_mac(new,key,iv),aes_ecb_dec(iv,key))
inject = new+b"\x10"*16+pad+orig

print("Original MAC: %s" % bytes2hex(cbc_mac(orig,key,iv)))
print("New MAC: %s" % bytes2hex(cbc_mac(inject,key,iv)))