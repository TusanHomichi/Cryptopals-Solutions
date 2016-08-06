from matasano import *
from os import urandom
from base64 import b64decode

key = urandom(16)
unknown = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

def oracle(b):
	return aes_ecb_enc(pkcs7_pad(b+unknown,16), key)
	
def detect_block_size():
	len1 = len(oracle(bytes([])))
	i=1
	len2 = len(oracle(bytes([97]*i)))
	while len1 == len2:
		i += 1
		len2 = len(oracle(bytes([97]*i)))
	return len2-len1
	
def verify_ecb(block_size):
	s = oracle(bytes([96]*(3*block_size-1)))
	for i in range(block_size,len(s),block_size):
		if s[i-block_size:i] == s[i:i+block_size]:
			return True
	return False
	
def detect_len(block_size):
	len1 = len(oracle(bytes([])))
	i=1
	len2 = len(oracle(bytes([97]*i)))
	while len1 == len2:
		i += 1
		len2 = len(oracle(bytes([97]*i)))
	return len1-i
	
def decrypt():
	block_size = detect_block_size()
	print("Block size: %d" % block_size)
	print("ECB: %s" % verify_ecb(block_size))
	str_len = detect_len(block_size)
	print("Plaintext length: %d" % str_len)
	known = bytes([])
	for i in range(str_len):
		pad_len = block_size-1-(i%block_size)
		s = oracle(bytes([97]*pad_len))
		block = s[i-(i%block_size):i-(i%block_size)+block_size]
		if i >= block_size:
			plaintext = known[-block_size+1:]
		else:
			plaintext = bytes([97]*pad_len) + known
		for j in range(256):
			new_block = oracle(plaintext+bytes([j]))[:block_size]
			if block == new_block:
				known += bytes([j])
				break
	return known

known = decrypt()
print("Correct decryption: %s" % (unknown == known))
print()
print(known.decode('ascii'))
