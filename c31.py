from matasano import *
from time import time,sleep

assert(hmac(b"",b"",sha1) == hex2bytes("fbdb1d1b18aa6c08324b7d64b71fb76370690e1d"))
assert(hmac(b"key",b"The quick brown fox jumps over the lazy dog",sha1) == hex2bytes("de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9"))
print("HMAC implementation OK!")

def insec_comp(a,b):
	for i in range(len(a)):
		if a[i] != b[i]:
			return False
		sleep(0.05)
	return True

key = bytes([randint(97,122) for i in range(16)])
def check(file,mac):
	return insec_comp(hmac(key,file,sha1),mac)
	
def leak(file):
	mac = b'\x00'*sha1.hash_size
	for i in range(sha1.hash_size):
		times = []
		for j in range(256):
			mac = mac[:i] + bytes([j]) + mac[i+1:]
			t1 = time()
			check(file,mac)
			t2 = time()
			times.append((t2-t1,j))
		times = sorted(times, reverse=True)
		mac = mac[:i] + bytes([times[0][1]]) + mac[i+1:]
	return mac