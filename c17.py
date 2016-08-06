from matasano import *

strs = [b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=", b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=", b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==", b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==", b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl", b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==", b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==", b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=", b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=", b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

key = randbytes(16)

def gen(i=-1):
	if i not in range(10):
		i = randint(0,9)
	s = strs[i]
	iv = randbytes(16)
	return aes_cbc_enc(pkcs7_pad(s,16),key,iv),iv
	
def check(c,iv):
	p = aes_cbc_dec(c,key,iv)
	try:
		p = pkcs7_unpad(p)
		return True
	except:
		return False
		
def decrypt_block(c,iv):
	known = bytes([])
	i = 15
	j = 0
	while i >= 0:
		while j < 256:
			new_iv = iv[:i] + bytes([j^(16-i)]) + xor(known,bytes([16-i]*len(known)))
			if check(c,new_iv):
				known = bytes([j]) + known
				i -= 1
				j = 0
				break
			j += 1
		if j == 256:
			i += 1
			j = known[0] + 1
			known = known[1:]
	return xor(known,iv)
		
def decrypt(c,iv):
	plain = decrypt_block(c[:16], iv)
	for i in range(16,len(c),16):
		plain += decrypt_block(c[i:i+16],c[i-16:i])
	return plain
	
for i in range(10):
	c,iv = gen(i)
	print(decrypt(c,iv))