from matasano import *
from os import urandom
from base64 import b64decode

key = urandom(16)
unknown = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
prefix = urandom(urandom(1)[0]%32+16)

def oracle(b):
	return aes_ecb_enc(pkcs7_pad(prefix+b+unknown,16), key)
	
def detect_block_size():
	len1 = len(oracle(bytes([])))
	i=1
	len2 = len(oracle(b'a'*i))
	while len1 == len2:
		i += 1
		len2 = len(oracle(b'a'*i))
	return len2-len1
	
def verify_ecb(block_size):
	s = oracle(bytes([96]*(3*block_size-1)))
	for i in range(block_size,len(s),block_size):
		if s[i-block_size:i] == s[i:i+block_size]:
			return True
	return False
	
def detect_prefix_len(block_size):
	pad = b'a'*(3*block_size-1)
	s = oracle(pad)
	for i in range(0,len(s)-block_size,block_size):
		if s[i:i+block_size] == s[i+block_size:i+2*block_size]:
			pad_block = s[i:i+block_size]
			pad_len = i	#Currently number of blocks
			break
	pad = b'a'*block_size
	s = oracle(pad)
	while s[pad_len:pad_len+block_size] != pad_block:
		pad += b"a"
		s = oracle(pad)
	pad_len = pad_len + block_size - len(pad)
	return pad_len
	
def detect_len(block_size):
	len1 = len(oracle(bytes([])))
	i=1
	len2 = len(oracle(b'a'*i))
	while len1 == len2:
		i += 1
		len2 = len(oracle(b'a'*i))
	return len1-i
	
def decrypt():
	block_size = detect_block_size()
	print("Block size: %d" % block_size)
	print("ECB: %s" % verify_ecb(block_size))
	str_len = detect_len(block_size)
	pref_len = detect_prefix_len(block_size)
	str_len -= pref_len
	pref_block = pref_len - pref_len%block_size + block_size
	print("Plaintext length: %d" % str_len)
	known = bytes([])
	for i in range(str_len):
		pad_len = pref_block - pref_len + block_size-1-(i%block_size)
		s = oracle(b'a'*pad_len)
		block = s[pref_block+i-(i%block_size):pref_block+i-(i%block_size)+block_size]
		if i >= block_size:
			plaintext = b'a'*(pref_block-pref_len) + known[-block_size+1:]
		else:
			plaintext = b'a'*pad_len + known
		for j in range(256):
			new_block = oracle(plaintext+bytes([j]))[pref_block:pref_block+block_size]
			if block == new_block:
				known += bytes([j])
				break
	return known

known = decrypt()
print("Correct decryption: %s" % (unknown == known))
print()
print(known.decode('ascii'))
